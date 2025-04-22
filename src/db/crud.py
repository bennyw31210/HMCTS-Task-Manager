from pymongo.results import UpdateResult, DeleteResult
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from bson.errors import InvalidId
from main import app
from models.task import TaskCreationModel, TaskUpdateModel, TaskResponseModel
from utils.global_constants import GlobalConstants


COLLECTION = app.state.HMCTS_DB.Tasks

async def create_task(TASK: TaskCreationModel) -> TaskResponseModel:
    INSERTED_TASK = await COLLECTION.insert_one(jsonable_encoder(TASK))

    if not INSERTED_TASK.inserted_id:
        raise Exception("An error occured when writing to the HMCTS Task Manager database.")
    CREATED_TASK = await COLLECTION.find_one({GlobalConstants.MONGO_ID_FIELD_NAME: INSERTED_TASK.inserted_id})
    return await TaskResponseModel.model_validate(CREATED_TASK)

async def read_all_tasks() -> list[TaskResponseModel]:
    CURSOR = COLLECTION.find({})

    tasks = []
    
    async for task in CURSOR:
        tasks.append(TaskResponseModel.model_validate(task))
    
    return tasks

async def read_task(ID: str) -> TaskResponseModel:
    try:
        TASK = await COLLECTION.find_one({GlobalConstants.MONGO_ID_FIELD_NAME: ObjectId(ID)})

        if TASK:
            return TaskResponseModel.model_validate(TASK)
    # If an id of an invalid format for MongoDB is passed to 'ID'
    except InvalidId:
        return None

async def update_task(ID: str, TASK: TaskUpdateModel) -> UpdateResult:
    UPDATE_RESULT = await COLLECTION.update_one({GlobalConstants.MONGO_ID_FIELD_NAME: ObjectId(ID)}, {"$set": jsonable_encoder(TASK)})

    if UPDATE_RESULT.match_count == 0 or UPDATE_RESULT.modified_count == 0:
        raise Exception(f"An error occured when attempting to update a record with an _id of '{ID}' in the HMCTS Task Manager database.")
    return UPDATE_RESULT

async def delete_task(ID: str) -> DeleteResult:
    DELETE_RESULT = await COLLECTION.delete_one({GlobalConstants.MONGO_ID_FIELD_NAME: ObjectId(ID)})

    if DELETE_RESULT.delete_count == 0:
        raise Exception(f"An error occured when attempting to delete a record with an _id of '{ID}' in the HMCTS Task Manager database.")
    return DELETE_RESULT