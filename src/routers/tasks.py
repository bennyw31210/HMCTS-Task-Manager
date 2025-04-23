from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from http import HTTPStatus
from ..models.tasks import TaskCreationModel, TaskResponseModel, TaskUpdateModel
from ..db.crud.crud import create_task, read_all_tasks, read_task, update_task, delete_task
from ..db.get_async_session import get_async_session


def raise_bad_request(REQUEST_ID: int):
    """
    Raises an HTTP 400 Bad Request error when a task with the given ID is not found.

    Args:
        REQUEST_ID (int): The task ID that could not be found.

    Raises:
        HTTPException: 400 error with a message indicating that the task doesn't exist.
    """
    raise HTTPException(status_code=400, detail=f"No task exists with an id of '{REQUEST_ID}'.")


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponseModel, 
             summary="Create a new task", 
             description="Create a new task with title, optional description, due date, and status.",
             responses={
                 HTTPStatus.OK: {"description": "Successful Response",
                        "content": {
                            "application/json": {
                                "example": {"id": 1, "title": "string", "description": "string", "status": "Pending", "due_date": "2025-04-23T16:19:35.730Z"}
                                }
                            }},
                            HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
             }
             )
async def post_task(TASK: TaskCreationModel, SESSION: AsyncSession = Depends(get_async_session)) -> TaskResponseModel:
    """
    Endpoint to create a new task.

    Args:
        TASK (TaskCreationModel): Task creation payload.
        SESSION (AsyncSession): Injected SQLAlchemy async session.

    Returns:
        TaskResponseModel: The newly created task.
    """
    return await create_task(TASK, SESSION)


@router.get("/", response_model=list[TaskResponseModel], 
            summary="Get all tasks", 
            description="Retrieve a list of all tasks currently stored in the database.",
             responses={
                 HTTPStatus.OK: {"description": "Successful Response",
                        "content": {
                            "application/json": {
                                "example": [{"id": 1, "title": "string", "description": "string", "status": "Pending", "due_date": "2025-04-23T16:19:35.730Z"}]
                                }
                            }},
                            HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
             }
            )
async def get_all_tasks(SESSION: AsyncSession = Depends(get_async_session)) -> TaskResponseModel:
    """
    Endpoint to retrieve all tasks.

    Args:
        SESSION (AsyncSession): Injected SQLAlchemy async session.

    Returns:
        list[TaskResponseModel]: A list of all tasks.
    """
    return await read_all_tasks(SESSION)


@router.get("/{ID}/", 
            response_model=TaskResponseModel, 
            summary="Get a task by ID", 
            description="Retrieve a single task using its numeric ID.",
             responses={
                 HTTPStatus.OK: {"description": "Successful Response",
                        "content": {
                            "application/json": {
                                "example": {"id": 1, "title": "string", "description": "string", "status": "Pending", "due_date": "2025-04-23T16:19:35.730Z"}
                                }
                            }},
                            HTTPStatus.BAD_REQUEST: {"description": "No task exists with the provided 'id'"},
                            HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
             })
async def get_task(ID: int, SESSION: AsyncSession = Depends(get_async_session)) -> TaskResponseModel:
    """
    Endpoint to retrieve a task by ID.

    Args:
        ID (int): Task ID.
        SESSION (AsyncSession): Injected SQLAlchemy async session.

    Returns:
        TaskResponseModel: The task with the specified ID.

    Raises:
        HTTPException: 400 (Bad Request) error if the task does not exist.
    """
    TASK = await read_task(ID, SESSION)
    
    if TASK:
        return TASK
    raise_bad_request(ID)


@router.patch("/{ID}/", 
              response_model=TaskResponseModel,
              summary="Update a task's status",
              description="Update the status of an existing task using its ID. Other fields remain unchanged.",
             responses={
                 HTTPStatus.OK: {"description": "Successful Response",
                        "content": {
                            "application/json": {
                                "example": {"id": 1, "title": "string", "description": "string", "status": "Pending", "due_date": "2025-04-23T16:19:35.730Z"}
                                }
                            }},
                            HTTPStatus.BAD_REQUEST: {"description": "No task exists with the provided 'id'"},
                            HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
             })
async def patch_status(ID: int, TASK: TaskUpdateModel, SESSION: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Endpoint to update the status of a task.

    Args:
        ID (int): ID of the task to be updated.
        TASK (TaskUpdateModel): The new status to apply.
        SESSION (AsyncSession): Injected SQLAlchemy async session.

    Returns:
        TaskResponseModel: The updated task.

    Raises:
        HTTPException: 400 (Bad Request) error if the task does not exist.
    """
    UPDATED_TASK = await update_task(ID, TASK, SESSION)

    if UPDATED_TASK:
        return UPDATED_TASK
    raise_bad_request()

@router.delete("/{ID}/", 
               summary="Delete a task", 
               description="Delete a task by its ID. Returns a success message if deletion was successful.",
             responses={
                 HTTPStatus.OK: {"description": "Successful Response",
                        "content": {
                            "application/json": {
                                "example": {"message": "Task with id '<ID>' deleted successfully."}
                                }
                            }},
                            HTTPStatus.BAD_REQUEST: {"description": "No task exists with the provided 'id'"},
                            HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"}
             })
async def remove_task(ID: int, SESSION: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Endpoint to delete a task by ID.

    Args:
        ID (int): ID of the task to delete.
        SESSION (AsyncSession): Injected SQLAlchemy async session.

    Returns:
        dict: A confirmation message upon successful deletion.

    Raises:
        HTTPException: 400 (Bad Request) error if the task does not exist.
    """
    DELETE_RESULT = await delete_task(ID, SESSION)

    if DELETE_RESULT:
        return {"message": f"Task with id '{ID}' deleted successfully."}
    raise_bad_request()