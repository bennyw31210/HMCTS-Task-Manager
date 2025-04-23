from sqlalchemy import Column, Integer, String, Text, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from utils.global_constants import StatusTypes


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
    
    Methods:
        to_dict(): Convert the model to a dictionary.
    """
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(StatusTypes), nullable=False, default=StatusTypes.PENDING)
    due_date = Column(DateTime, nullable=False)

    def to_dict(self) -> dict:
        """
        Convert the model to a dictionary.

        Returns:
            dict: The dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "due_date": self.due_date
        }