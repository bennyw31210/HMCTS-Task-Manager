from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum
from datetime import datetime
from utils.global_constants import GlobalConstants


class TaskUpdateModel(BaseModel):
    class StatusTypes(str, Enum):
        TO_DO = "To Do"
        IN_PROGRESS = "In Progress"
        DONE = "Done"

    status: Literal[StatusTypes.TO_DO, StatusTypes.IN_PROGRESS, StatusTypes.DONE]

class TaskCreationModel(TaskUpdateModel):
    title: str
    description: Optional[str] = None
    due_date_and_time: datetime

class TaskResponseModel(TaskCreationModel):
    class MongoObjectId(ObjectId):
        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def validate(cls, VALUE):
            if not ObjectId.is_valid(VALUE):
                raise ValueError("Invalid ObjectId")
            return ObjectId(VALUE)

        @classmethod
        def __get_pydantic_json_schema__(cls, FIELD_SCHEMA):
            FIELD_SCHEMA.update(type="string")

    id: MongoObjectId = Field(default_factory=MongoObjectId, alias=GlobalConstants.MONGO_ID_FIELD_NAME) # Maps "_id" as defined in MongoDB to "id" as defined in this model

    class Config:
        # Allows "_id" field as defined in MongoDB to be referred to as "id" in the model 
        # (Python doesn't allow underscores to prefix variable names)
        populate_by_name = True
        # Allow MongoObjectId to be used in the model (not a type natively supported by pydantic)
        arbitrary_types_allowed = True
        # Encode MongoObjectId to string form when serialising to a client response
        json_encoders = {ObjectId: str}