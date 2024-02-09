# stdlib
import base64
from enum import Enum
from typing import Dict, List, Optional, Union

# third party
import pandas as pd
import pyarrow as pa
from pydantic import (
    BaseModel,
    ConfigDict,
    computed_field,
    field_validator,
    model_validator,
)


class TimeGranularity(str, Enum):
    day = "DAY"
    week = "WEEK"
    month = "MONTH"
    quarter = "QUARTER"
    year = "YEAR"


class DatePart(str, Enum):
    DOY = "DOY"
    DOW = "DOW"
    DAY = "DAY"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"


class MetricInput(BaseModel):
    name: str


class GroupByInput(BaseModel):
    name: str
    grain: Optional[TimeGranularity] = None
    datePart: Optional[DatePart] = None

    model_config = ConfigDict(use_enum_values=True)

    @field_validator("grain", mode="before")
    def uppercase_grain(cls, v):
        return v.upper()

    @field_validator("datePart", mode="before")
    def uppercase_date_part(cls, v):
        return v.upper()

    @model_validator(mode="before")
    def check_alternate_field_names(cls, values):
        if "datePart" in values and "date_part" in values:
            raise ValueError("only one of datePart or date_part is allowed")
        if "date_part" in values:
            values["datePart"] = values.pop("date_part")
        return values


class OrderByInput(BaseModel):
    metric: Optional[MetricInput] = None
    groupBy: Optional[GroupByInput] = None
    descending: Optional[bool] = None

    @model_validator(mode="before")
    def check_metric_or_groupBy(cls, values):
        if (values.get("metric") is None) and (values.get("groupBy") is None):
            raise ValueError("either metric or groupBy is required")
        if (values.get("metric") is not None) and (values.get("groupBy") is not None):
            raise ValueError("only one of metric or groupBy is allowed")
        return values

    @model_validator(mode="before")
    def check_alternate_descending(cls, values):
        if "descending" in values and "desc" in values:
            raise ValueError("only one of descending or desc is allowed")
        if "desc" in values:
            values["descending"] = values.pop("desc")
        return values


class WhereInput(BaseModel):
    sql: str


class QueryPage(BaseModel):
    arrowResult: Optional[str]
    error: Optional[str]
    totalPages: Optional[int]
    sql: Optional[str]
    status: str
    queryId: Optional[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @computed_field  # type: ignore[misc]
    @property
    def arrow_table(self) -> pa.Table:
        if self.arrowResult is not None:
            with pa.ipc.open_stream(base64.b64decode(self.arrowResult)) as reader:
                return pa.Table.from_batches(reader, reader.schema)


class QueryResponse(BaseModel):
    result: Optional[Union[pd.DataFrame, pa.Table, List[Dict], List[str]]]
    query_id: Optional[str]
    sql: Optional[str]
    status: str
    error: Optional[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @model_validator(mode="before")
    def check_alternate_query_id(cls, values):
        if "queryId" in values:
            values["query_id"] = values.pop("queryId")
        return values


class QueryResponseConstructor:
    COMMON_ATTRIBUTES = ["queryId", "sql", "status", "error"]

    def __init__(self, query_pages: List[QueryPage], output_format: str):
        self.query_pages = query_pages
        self.output_format = output_format
        valid_tables = [page.arrow_table for page in query_pages if page.arrow_table]
        if valid_tables:
            self.concatenated_arrow_table = pa.concat_tables(valid_tables)
        self._set_common_page_attributes()

    def _is_same_for_each_page(self, attribute: str) -> bool:
        return all(
            getattr(page, attribute) == getattr(self.query_pages[0], attribute)
            for page in self.query_pages
        )

    def _set_common_page_attributes(self):
        common_attributes = {}
        for attribute in self.COMMON_ATTRIBUTES:
            if self._is_same_for_each_page(attribute):
                common_attributes[attribute] = getattr(self.query_pages[0], attribute)
            else:
                values = " ".join(
                    [getattr(page, attribute) for page in self.query_pages]
                )
                common_attributes[attribute] = (
                    f"Multiple values found for {attribute} across multiple pages."
                    f"The following was returned: {values}"
                )
        self.common_page_attributes = common_attributes

    def create(self) -> QueryResponse:
        try:
            result = getattr(self, f"_create_{self.output_format}_response")()
        except AttributeError:
            # No data was returned from the query
            result = None
        return QueryResponse(
            result=result,
            **self.common_page_attributes,
        )

    def _create_pandas_response(self):
        return self.concatenated_arrow_table.to_pandas()

    def _create_arrow_response(self):
        return self.concatenated_arrow_table

    def _create_list_response(self):
        return self.concatenated_arrow_table.to_pylist()

    def _create_raw_response(self):
        return [page.arrowResult for page in self.query_pages]
