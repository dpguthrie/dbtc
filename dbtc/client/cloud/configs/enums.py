import enum

class JobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30

class JobRunStrategies(str, enum.Enum):
    STANDARD = 'standard'
    RESTART = 'restart_from_failure'
    AUTOSCALE = 'autoscale'
