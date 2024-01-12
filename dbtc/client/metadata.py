# stdlib
from typing import Any, Dict, List, Union

# third party
import requests

# first party
from dbtc.client.base import _Client


class _MetadataClient(_Client):
    def __init__(self, **kwargs):
        self._use_beta = kwargs.pop("use_beta_endpoint", True)
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.session.headers = self.headers

    _header_property = "service_token"

    @property
    def _path(self):
        if self._use_beta:
            return "/beta/graphql"

        return "/graphql"

    @property
    def _base_url(self):
        return f"https://metadata.{self._host}{self._path}"

    def _find_page_info(self, response_data: Dict):
        for key, value in response_data.items():
            if key == "pageInfo":
                return value

            if isinstance(value, dict):
                result = self._find_page_info(value)
                if result is not None:
                    return result

        return None

    def _find_list_element(self, response_data: Dict):
        for _, value in response_data.items():
            if isinstance(value, list):
                return value

            elif isinstance(value, dict):
                result = self._find_list_element(value)
                if result is not None:
                    return result

        return None

    def _make_request(self, payload: Dict[str, Any], after_cursor: str = None):
        if after_cursor:
            if "variables" not in payload:
                payload["variables"] = {}
            payload["variables"]["after"] = after_cursor

        response = self.session.post(self.full_url(), json=payload)
        return response.json()

    def _get_next_page_cursor(self, response: Dict) -> Union[str, None]:
        page_info = self._find_page_info(response)
        if page_info is None:
            return None

        if page_info.get("hasNextPage", False):
            return page_info["endCursor"]

        return None

    def query(
        self,
        query: str,
        variables: Dict = None,
        max_pages: int = None,
        paginated_request_to_list: bool = True,
    ) -> Union[List[Dict], Dict]:
        """Query the Discovery API

        Args:
            query (str): The GraphQL query to execute.
            variables (Dict, optional): Dictionary containing the variables to include
                in the payload of the request.  Defaults to None.
            max_pages (int, optional): The max number of pages to paginate through when
                Defaults to None.
            paginated_request_to_list (bool, optional): When paginating through a
                request, the elements of the list within each request will be
                combined into a single list of dictionaries. Defaults to True.

        Returns:
            Union[List[Dict], Dict]: _description_
        """
        payload: Dict[str, Any] = {"query": query}
        if variables:
            payload.update({"variables": variables})

        # If we're not paginating, just make the request and return the results
        if "pageInfo" not in query:
            self.console.log("No pageInfo found in query so making a single request.")
            return self._make_request(payload)

        # If we're paginating but the query isn't setup properly for paginating,
        # then make a single request
        if query.count("$after") < 2:
            self.console.log(
                'Query not properly set up with an "$after" variable to paginate '
                "results properly so making a single request."
            )
            return self._make_request(payload)

        cursor = None
        all_results = []
        page = 0

        while True:
            response = self._make_request(payload, cursor)
            cursor = self._get_next_page_cursor(response)
            paginated_results = (
                self._find_list_element(response)
                if paginated_request_to_list
                else response
            )

            all_results.extend(
                paginated_results
            ) if paginated_request_to_list else all_results.append(paginated_results)
            page += 1

            if not cursor:
                self.console.log("No more results to fetch.")
                break

            if max_pages and page >= max_pages:
                self.console.log(f"Reached max page limit of {max_pages}.")
                break

            self.console.log(f"Fetching page {page} for query...")

        return all_results
