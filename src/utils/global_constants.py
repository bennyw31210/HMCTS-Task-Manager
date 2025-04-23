from .immutable_meta_class import ImmutableMeta
from enum import Enum

class StatusTypes(str, Enum):
    """
    Enum representing the possible statuses of a task in the HMCTS Task Manager.

    Attributes:
        PENDING (str): The task has been created but not yet started.
        IN_PROGRESS (str): The task is currently being worked on.
        DONE (str): The task has been completed.
    """
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    DONE = "Done"