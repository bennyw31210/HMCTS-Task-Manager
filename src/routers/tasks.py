from fastapi import APIRouter, HTTPException
from models.task import TaskCreationModel, TaskResponseModel, TaskUpdateModel
from db.crud import create_task, read_all_tasks, read_task, update_task, delete_task

def raise_bad_request(REQUEST_ID: str):
    raise HTTPException(status_code=400, detail=f"No task exists with an id of '{REQUEST_ID}'.")

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponseModel)
async def post_task(TASK: TaskCreationModel) -> TaskResponseModel:
    return await create_task(TASK)

@router.get("/", response_model=list[TaskResponseModel])
async def get_all_tasks() -> TaskResponseModel:
    return await read_all_tasks()

@router.get("/{ID}/")
async def get_task(ID: str) -> TaskResponseModel:
    TASK = await read_task(ID)
    
    if TASK:
        return TASK
    raise_bad_request(ID)

@router.patch("/{ID}/")
async def patch_status(ID: str, TASK: TaskUpdateModel):
    UPDATE_RESULT = await update_task(ID, TASK)

    if UPDATE_RESULT:
        return UPDATE_RESULT
    raise_bad_request()

@router.delete("/{ID}/")
async def remove_task(ID: str):
    DELETE_RESULT = await delete_task(ID)

    if DELETE_RESULT:
        return DELETE_RESULT
    raise_bad_request()