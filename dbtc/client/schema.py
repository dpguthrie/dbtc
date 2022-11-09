# third party
import sgqlc.types
import sgqlc.types.datetime

schema = sgqlc.types.Schema()


########################################################################
# Scalars and Enumerations
########################################################################
class AnyScalar(sgqlc.types.Scalar):
    __schema__ = schema


Boolean = sgqlc.types.Boolean

DateTime = sgqlc.types.datetime.DateTime

Float = sgqlc.types.Float


class FreshnessStatus(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('Error', 'Pass', 'Warn')


Int = sgqlc.types.Int


class JSON(sgqlc.types.Scalar):
    __schema__ = schema


class JSONObject(sgqlc.types.Scalar):
    __schema__ = schema


String = sgqlc.types.String


class TimePeriod(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('day', 'hour', 'minute')


########################################################################
# Input Objects
########################################################################

########################################################################
# Output Objects and Interfaces
########################################################################
class CatalogColumn(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        'name',
        'index',
        'type',
        'comment',
        'description',
        'tags',
        'meta',
    )
    name = sgqlc.types.Field(String, graphql_name='name')
    index = sgqlc.types.Field(Int, graphql_name='index')
    type = sgqlc.types.Field(String, graphql_name='type')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    description = sgqlc.types.Field(String, graphql_name='description')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')
    meta = sgqlc.types.Field(JSONObject, graphql_name='meta')


class CatalogStat(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'label', 'description', 'include', 'value')
    id = sgqlc.types.Field(String, graphql_name='id')
    label = sgqlc.types.Field(String, graphql_name='label')
    description = sgqlc.types.Field(String, graphql_name='description')
    include = sgqlc.types.Field(Boolean, graphql_name='include')
    value = sgqlc.types.Field(AnyScalar, graphql_name='value')


class CloudArtifactInterface(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = ('run_id', 'account_id', 'project_id', 'environment_id', 'job_id')
    run_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='runId')
    account_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='accountId')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='projectId')
    environment_id = sgqlc.types.Field(
        sgqlc.types.non_null(Int), graphql_name='environmentId'
    )
    job_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='jobId')


class Criteria(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('warn_after', 'error_after')
    warn_after = sgqlc.types.Field('CriteriaInfo', graphql_name='warnAfter')
    error_after = sgqlc.types.Field('CriteriaInfo', graphql_name='errorAfter')


class CriteriaInfo(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('count', 'period')
    count = sgqlc.types.Field(Int, graphql_name='count')
    period = sgqlc.types.Field(TimePeriod, graphql_name='period')


class MetricFilter(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('field', 'operator', 'value')
    field = sgqlc.types.Field(String, graphql_name='field')
    operator = sgqlc.types.Field(String, graphql_name='operator')
    value = sgqlc.types.Field(String, graphql_name='value')


class NodeInterface(sgqlc.types.Interface):
    __schema__ = schema
    __field_names__ = (
        'resource_type',
        'unique_id',
        'name',
        'description',
        'meta',
        'dbt_version',
        'tags',
    )
    resource_type = sgqlc.types.Field(
        sgqlc.types.non_null(String), graphql_name='resourceType'
    )
    unique_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='uniqueId')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    meta = sgqlc.types.Field(JSONObject, graphql_name='meta')
    dbt_version = sgqlc.types.Field(String, graphql_name='dbtVersion')
    tags = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='tags')


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        'exposures',
        'exposure',
        'macros',
        'macro',
        'metrics',
        'metric',
        'models',
        'model',
        'model_by_environment',
        'seeds',
        'seed',
        'snapshots',
        'snapshot',
        'sources',
        'source',
        'tests',
        'test',
    )
    exposures = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ExposureNode'))),
        graphql_name='exposures',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
            )
        ),
    )
    exposure = sgqlc.types.Field(
        'ExposureNode',
        graphql_name='exposure',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'name',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name='name', default=None
                    ),
                ),
            )
        ),
    )
    macros = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null('MacroNode')),
        graphql_name='macros',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
            )
        ),
    )
    macro = sgqlc.types.Field(
        'MacroNode',
        graphql_name='macro',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'unique_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name='uniqueId',
                        default=None,
                    ),
                ),
            )
        ),
    )
    metrics = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('MetricNode'))),
        graphql_name='metrics',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
            )
        ),
    )
    metric = sgqlc.types.Field(
        'MetricNode',
        graphql_name='metric',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'unique_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name='uniqueId',
                        default=None,
                    ),
                ),
            )
        ),
    )
    models = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelNode'))),
        graphql_name='models',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'schema',
                    sgqlc.types.Arg(String, graphql_name='schema', default=None),
                ),
                (
                    'identifier',
                    sgqlc.types.Arg(String, graphql_name='identifier', default=None),
                ),
                (
                    'database',
                    sgqlc.types.Arg(String, graphql_name='database', default=None),
                ),
            )
        ),
    )
    model = sgqlc.types.Field(
        'ModelNode',
        graphql_name='model',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'unique_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name='uniqueId',
                        default=None,
                    ),
                ),
            )
        ),
    )
    model_by_environment = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ModelNode'))),
        graphql_name='modelByEnvironment',
        args=sgqlc.types.ArgDict(
            (
                (
                    'environment_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name='environmentId',
                        default=None,
                    ),
                ),
                (
                    'unique_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name='uniqueId',
                        default=None,
                    ),
                ),
                (
                    'last_run_count',
                    sgqlc.types.Arg(Int, graphql_name='lastRunCount', default=1),
                ),
                (
                    'with_catalog',
                    sgqlc.types.Arg(Boolean, graphql_name='withCatalog', default=False),
                ),
            )
        ),
    )
    seeds = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SeedNode'))),
        graphql_name='seeds',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
            )
        ),
    )
    seed = sgqlc.types.Field(
        'SeedNode',
        graphql_name='seed',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'unique_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name='uniqueId',
                        default=None,
                    ),
                ),
            )
        ),
    )
    snapshots = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SnapshotNode'))),
        graphql_name='snapshots',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
            )
        ),
    )
    snapshot = sgqlc.types.Field(
        'SnapshotNode',
        graphql_name='snapshot',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'unique_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name='uniqueId',
                        default=None,
                    ),
                ),
            )
        ),
    )
    sources = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('SourceNode'))),
        graphql_name='sources',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'schema',
                    sgqlc.types.Arg(String, graphql_name='schema', default=None),
                ),
                (
                    'identifier',
                    sgqlc.types.Arg(String, graphql_name='identifier', default=None),
                ),
                (
                    'database',
                    sgqlc.types.Arg(String, graphql_name='database', default=None),
                ),
            )
        ),
    )
    source = sgqlc.types.Field(
        'SourceNode',
        graphql_name='source',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'unique_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name='uniqueId',
                        default=None,
                    ),
                ),
            )
        ),
    )
    tests = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TestNode'))),
        graphql_name='tests',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
            )
        ),
    )
    test = sgqlc.types.Field(
        'TestNode',
        graphql_name='test',
        args=sgqlc.types.ArgDict(
            (
                (
                    'job_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int), graphql_name='jobId', default=None
                    ),
                ),
                ('run_id', sgqlc.types.Arg(Int, graphql_name='runId', default=None)),
                (
                    'unique_id',
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name='uniqueId',
                        default=None,
                    ),
                ),
            )
        ),
    )


class RunInfoNode(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = (
        'execution_time',
        'thread_id',
        'run_generated_at',
        'run_elapsed_time',
        'error',
        'status',
        'skip',
        'compile_started_at',
        'compile_completed_at',
        'execute_started_at',
        'execute_completed_at',
        'invocation_id',
        'args',
    )  # type: ignore
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    thread_id = sgqlc.types.Field(String, graphql_name='threadId')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    error = sgqlc.types.Field(String, graphql_name='error')
    status = sgqlc.types.Field(String, graphql_name='status')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    compile_completed_at = sgqlc.types.Field(
        DateTime, graphql_name='compileCompletedAt'
    )
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execute_completed_at = sgqlc.types.Field(
        DateTime, graphql_name='executeCompletedAt'
    )
    invocation_id = sgqlc.types.Field(String, graphql_name='invocationId')
    args = sgqlc.types.Field(JSON, graphql_name='args')


class ExposureNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = (
        'manifest_generated_at',
        'package_name',
        'owner_email',
        'owner_name',
        'exposure_type',
        'url',
        'maturity',
        'depends_on',
        'parents',
        'parents_sources',
        'parents_models',
    )  # type: ignore
    manifest_generated_at = sgqlc.types.Field(
        DateTime, graphql_name='manifestGeneratedAt'
    )
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    owner_email = sgqlc.types.Field(String, graphql_name='ownerEmail')
    owner_name = sgqlc.types.Field(String, graphql_name='ownerName')
    exposure_type = sgqlc.types.Field(String, graphql_name='exposureType')
    url = sgqlc.types.Field(String, graphql_name='url')
    maturity = sgqlc.types.Field(String, graphql_name='maturity')
    depends_on = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='dependsOn'
    )
    parents = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(NodeInterface)), graphql_name='parents'
    )
    parents_sources = sgqlc.types.Field(
        sgqlc.types.list_of('SourceNode'), graphql_name='parentsSources'
    )
    parents_models = sgqlc.types.Field(
        sgqlc.types.list_of('ModelNode'), graphql_name='parentsModels'
    )


class MacroNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = (
        'package_name',
        'path',
        'root_path',
        'original_file_path',
        'depends_on',
        'macro_sql',
    )  # type: ignore
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    path = sgqlc.types.Field(String, graphql_name='path')
    root_path = sgqlc.types.Field(String, graphql_name='rootPath')
    original_file_path = sgqlc.types.Field(String, graphql_name='originalFilePath')
    depends_on = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name='dependsOn'
    )
    macro_sql = sgqlc.types.Field(String, graphql_name='macroSql')


class MetricNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = (
        'package_name',
        'label',
        'type',
        'sql',
        'timestamp',
        'filters',
        'time_grains',
        'dimensions',
        'depends_on',
        'model',
    )  # type: ignore
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    label = sgqlc.types.Field(String, graphql_name='label')
    type = sgqlc.types.Field(String, graphql_name='type')
    sql = sgqlc.types.Field(String, graphql_name='sql')
    timestamp = sgqlc.types.Field(String, graphql_name='timestamp')
    filters = sgqlc.types.Field(
        sgqlc.types.list_of(MetricFilter), graphql_name='filters'
    )
    time_grains = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name='timeGrains'
    )
    dimensions = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name='dimensions'
    )
    depends_on = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name='dependsOn'
    )
    model = sgqlc.types.Field('ModelNode', graphql_name='model')


class ModelNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = (
        'database',
        'schema',
        'alias',
        'invocation_id',
        'args',
        'error',
        'status',
        'skip',
        'compile_started_at',
        'compile_completed_at',
        'execute_started_at',
        'execute_completed_at',
        'execution_time',
        'thread_id',
        'run_generated_at',
        'run_elapsed_time',
        'depends_on',
        'package_name',
        'type',
        'owner',
        'comment',
        'children_l1',
        'raw_sql',
        'compiled_sql',
        'materialized_type',
        'columns',
        'stats',
        'run_results',
        'parents_models',
        'parents_sources',
        'tests',
    )  # type: ignore
    database = sgqlc.types.Field(String, graphql_name='database')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    invocation_id = sgqlc.types.Field(String, graphql_name='invocationId')
    args = sgqlc.types.Field(JSON, graphql_name='args')
    error = sgqlc.types.Field(String, graphql_name='error')
    status = sgqlc.types.Field(String, graphql_name='status')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    compile_completed_at = sgqlc.types.Field(
        DateTime, graphql_name='compileCompletedAt'
    )
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execute_completed_at = sgqlc.types.Field(
        DateTime, graphql_name='executeCompletedAt'
    )
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    thread_id = sgqlc.types.Field(String, graphql_name='threadId')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    depends_on = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name='dependsOn'
    )
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    type = sgqlc.types.Field(String, graphql_name='type')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    children_l1 = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='childrenL1'
    )
    raw_sql = sgqlc.types.Field(String, graphql_name='rawSql')
    compiled_sql = sgqlc.types.Field(String, graphql_name='compiledSql')
    materialized_type = sgqlc.types.Field(String, graphql_name='materializedType')
    columns = sgqlc.types.Field(
        sgqlc.types.list_of(CatalogColumn), graphql_name='columns'
    )
    stats = sgqlc.types.Field(sgqlc.types.list_of(CatalogStat), graphql_name='stats')
    run_results = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(RunInfoNode)),
        graphql_name='runResults',
    )
    parents_models = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null('ModelNode')),
        graphql_name='parentsModels',
    )
    parents_sources = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null('SourceNode')),
        graphql_name='parentsSources',
    )
    tests = sgqlc.types.Field(sgqlc.types.list_of('TestNode'), graphql_name='tests')


class SeedNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = (
        'package_name',
        'database',
        'schema',
        'alias',
        'error',
        'status',
        'skip',
        'compile_started_at',
        'compile_completed_at',
        'execute_started_at',
        'execute_completed_at',
        'execution_time',
        'run_generated_at',
        'run_elapsed_time',
        'columns',
        'stats',
        'thread_id',
        'children_l1',
        'type',
        'owner',
        'comment',
        'raw_sql',
        'compiled_sql',
    )  # type: ignore
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    database = sgqlc.types.Field(String, graphql_name='database')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    error = sgqlc.types.Field(String, graphql_name='error')
    status = sgqlc.types.Field(String, graphql_name='status')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    compile_completed_at = sgqlc.types.Field(
        DateTime, graphql_name='compileCompletedAt'
    )
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execute_completed_at = sgqlc.types.Field(
        DateTime, graphql_name='executeCompletedAt'
    )
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    columns = sgqlc.types.Field(
        sgqlc.types.list_of(CatalogColumn), graphql_name='columns'
    )
    stats = sgqlc.types.Field(sgqlc.types.list_of(CatalogStat), graphql_name='stats')
    thread_id = sgqlc.types.Field(String, graphql_name='thread_id')
    children_l1 = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name='childrenL1'
    )
    type = sgqlc.types.Field(String, graphql_name='type')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    raw_sql = sgqlc.types.Field(String, graphql_name='rawSql')
    compiled_sql = sgqlc.types.Field(String, graphql_name='compiledSql')


class SnapshotNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = (
        'package_name',
        'database',
        'schema',
        'alias',
        'error',
        'status',
        'skip',
        'parents_models',
        'parents_sources',
        'compile_started_at',
        'compile_completed_at',
        'execute_started_at',
        'execute_completed_at',
        'execution_time',
        'thread_id',
        'run_generated_at',
        'run_elapsed_time',
        'columns',
        'stats',
        'children_l1',
        'type',
        'owner',
        'comment',
        'raw_sql',
        'compiled_sql',
    )  # type: ignore
    package_name = sgqlc.types.Field(String, graphql_name='packageName')
    database = sgqlc.types.Field(String, graphql_name='database')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    error = sgqlc.types.Field(String, graphql_name='error')
    status = sgqlc.types.Field(String, graphql_name='status')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    parents_models = sgqlc.types.Field(
        sgqlc.types.list_of(ModelNode), graphql_name='parentsModels'
    )
    parents_sources = sgqlc.types.Field(
        sgqlc.types.list_of('SourceNode'), graphql_name='parentsSources'
    )
    compile_started_at = sgqlc.types.Field(DateTime, graphql_name='compileStartedAt')
    compile_completed_at = sgqlc.types.Field(
        DateTime, graphql_name='compileCompletedAt'
    )
    execute_started_at = sgqlc.types.Field(DateTime, graphql_name='executeStartedAt')
    execute_completed_at = sgqlc.types.Field(
        DateTime, graphql_name='executeCompletedAt'
    )
    execution_time = sgqlc.types.Field(Float, graphql_name='executionTime')
    thread_id = sgqlc.types.Field(String, graphql_name='threadId')
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    columns = sgqlc.types.Field(
        sgqlc.types.list_of(CatalogColumn), graphql_name='columns'
    )
    stats = sgqlc.types.Field(sgqlc.types.list_of(CatalogStat), graphql_name='stats')
    children_l1 = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name='childrenL1',
    )
    type = sgqlc.types.Field(String, graphql_name='type')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    raw_sql = sgqlc.types.Field(String, graphql_name='rawSql')
    compiled_sql = sgqlc.types.Field(String, graphql_name='compiledSql')


class SourceNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = (
        'database',
        'schema',
        'identifier',
        'source_name',
        'source_description',
        'max_loaded_at',
        'snapshotted_at',
        'max_loaded_at_time_ago_in_s',
        'run_generated_at',
        'run_elapsed_time',
        'state',
        'freshness_checked',
        'criteria',
        'columns',
        'stats',
        'loader',
        'type',
        'owner',
        'comment',
        'children_l1',
        'tests',
    )  # type: ignore
    database = sgqlc.types.Field(String, graphql_name='database')
    schema = sgqlc.types.Field(String, graphql_name='schema')
    identifier = sgqlc.types.Field(String, graphql_name='identifier')
    source_name = sgqlc.types.Field(String, graphql_name='sourceName')
    source_description = sgqlc.types.Field(String, graphql_name='sourceDescription')
    max_loaded_at = sgqlc.types.Field(DateTime, graphql_name='maxLoadedAt')
    snapshotted_at = sgqlc.types.Field(DateTime, graphql_name='snapshottedAt')
    max_loaded_at_time_ago_in_s = sgqlc.types.Field(
        Float, graphql_name='maxLoadedAtTimeAgoInS'
    )
    run_generated_at = sgqlc.types.Field(DateTime, graphql_name='runGeneratedAt')
    run_elapsed_time = sgqlc.types.Field(Float, graphql_name='runElapsedTime')
    state = sgqlc.types.Field(FreshnessStatus, graphql_name='state')
    freshness_checked = sgqlc.types.Field(Boolean, graphql_name='freshnessChecked')
    criteria = sgqlc.types.Field(
        sgqlc.types.non_null(Criteria), graphql_name='criteria'
    )
    columns = sgqlc.types.Field(
        sgqlc.types.list_of(CatalogColumn), graphql_name='columns'
    )
    stats = sgqlc.types.Field(sgqlc.types.list_of(CatalogStat), graphql_name='stats')
    loader = sgqlc.types.Field(String, graphql_name='loader')
    type = sgqlc.types.Field(String, graphql_name='type')
    owner = sgqlc.types.Field(String, graphql_name='owner')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    children_l1 = sgqlc.types.Field(
        sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='childrenL1'
    )
    tests = sgqlc.types.Field(sgqlc.types.list_of('TestNode'), graphql_name='tests')


class TestNode(sgqlc.types.Type, CloudArtifactInterface, NodeInterface):
    __schema__ = schema
    __field_names__ = (
        'state',
        'column_name',
        'status',
        'error',
        'depends_on',
        'fail',
        'warn',
        'skip',
        'raw_sql',
        'compiled_sql',
    )  # type: ignore
    state = sgqlc.types.Field(String, graphql_name='state')
    column_name = sgqlc.types.Field(String, graphql_name='columnName')
    status = sgqlc.types.Field(String, graphql_name='status')
    error = sgqlc.types.Field(String, graphql_name='error')
    depends_on = sgqlc.types.Field(
        sgqlc.types.list_of(String), graphql_name='dependsOn'
    )
    fail = sgqlc.types.Field(Boolean, graphql_name='fail')
    warn = sgqlc.types.Field(Boolean, graphql_name='warn')
    skip = sgqlc.types.Field(Boolean, graphql_name='skip')
    raw_sql = sgqlc.types.Field(String, graphql_name='rawSql')
    compiled_sql = sgqlc.types.Field(String, graphql_name='compiledSql')


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = None
schema.subscription_type = None
