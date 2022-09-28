# stdlib
import enum


class JobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30

<<<<<<< HEAD
<<<<<<< HEAD
class JobRunStrategies(str, enum.Enum):
=======

class JobRunModes(str, enum.Enum):
>>>>>>> ccea05c462706133260a7fbd7e2b9d45aa2b16a6
=======
class JobRunStrategies(str, enum.Enum):
>>>>>>> feat/model-validation
    STANDARD = 'standard'
    RESTART = 'restart_from_failure'
    AUTOSCALE = 'autoscale'
