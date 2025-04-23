from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from datetime import datetime, timezone
from ..utils.global_constants import StatusTypes

class TaskUpdateModel(BaseModel):
    """
    Schema for updating a task's status.

    Attributes:
        status (str): The new status of the task. 
                      Must be one of: 'PENDING', 'IN_PROGRESS', or 'DONE'.
                      Defaults to 'PENDING'.
    """
    status: Literal[StatusTypes.PENDING, StatusTypes.IN_PROGRESS, StatusTypes.DONE] = StatusTypes.PENDING


class TaskCreationModel(TaskUpdateModel):
    """
    Schema for creating a new task.

    Inherits from TaskUpdateModel, and adds additional required fields
    needed at creation.

    Attributes:
        title (str): The title of the task. Required.
        description (Optional[str]): An optional description of the task.
        due_date (datetime): The due date and time of the task (must be set in the future).
    """
    title: str
    description: Optional[str] = None
    due_date: datetime

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, VALUE: datetime) -> datetime:
        """
        Validates that the due date is set in the future.

        Parameters:
            VALUE (datetime): The datetime to validate.

        Returns:
            datetime: The validated datetime.

        Raises:
            ValidationError: If 'VALUE' is not a datetime set in the future.
        """
        if VALUE <= datetime.now(timezone.utc):
            raise ValueError("Due date must be in the future.")
        return VALUE


class TaskResponseModel(TaskCreationModel):
    """
    Schema for returning task details in API responses.

    Inherits from TaskCreationModel and adds the task ID.

    Attributes:
        id (int): Unique identifier of the task.
    """
    id: int