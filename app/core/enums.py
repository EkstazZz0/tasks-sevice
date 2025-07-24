from enum import Enum


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class ApplicationEnvironment(str, Enum):
    production = "production"
    test = "test"
