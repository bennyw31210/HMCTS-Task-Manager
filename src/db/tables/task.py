from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from ...utils.global_constants import StatusTypes


Base = declarative_base()

class Task(Base):
    """
    SQLAlchemy model representing a task in the HMCTS Task Manager.

    Attributes:
        id (int): Primary key identifier for the task.
        title (str): A brief title or summary of the task.
        description (str | None): Optional detailed description of the task.
        status (StatusTypes): The current status of the task, constrained by an Enum.
        due_date (datetime): The deadline by which the task should be completed.
    """
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(StatusTypes), nullable=False, default=StatusTypes.PENDING)
    due_date = Column(DateTime, nullable=False)