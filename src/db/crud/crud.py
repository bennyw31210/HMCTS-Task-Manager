from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.exc import NoResultFound
from db.tables.task import Task
from models.tasks import TaskCreationModel, TaskUpdateModel, TaskResponseModel


async def create_task(TASK: TaskCreationModel, SESSION: AsyncSession) -> TaskResponseModel:
    """
    Create a new task record in the database.

    Args:
        TASK (TaskCreationModel): The task data to be inserted.
        SESSION (AsyncSession): The active SQLAlchemy async session.

    Returns:
        TaskResponseModel: The newly created task, including its generated ID.
    """
    NEW_TASK = Task(**TASK.model_dump())
    SESSION.add(NEW_TASK)
    await SESSION.commit()
    await SESSION.refresh(NEW_TASK)
    return TaskResponseModel.model_validate(NEW_TASK.to_dict())

async def read_all_tasks(SESSION: AsyncSession) -> list[TaskResponseModel]:
    """
    Retrieve all tasks from the database.

    Args:
        SESSION (AsyncSession): The active SQLAlchemy async session.

    Returns:
        list[TaskResponseModel]: A list of all task records.
    """
    RESULT = await SESSION.execute(select(Task))
    TASKS = RESULT.scalars().all()
    return [TaskResponseModel.model_validate(task.to_dict()) for task in TASKS]

async def read_task(ID: int, SESSION: AsyncSession) -> TaskResponseModel | None:
    """
    Retrieve a single task by its ID.

    Args:
        ID (int): The ID of the task to retrieve.
        SESSION (AsyncSession): The active SQLAlchemy async session.

    Returns:
        TaskResponseModel | None: The task if found, otherwise None.
    """
    RESULT = await SESSION.execute(select(Task).where(Task.id == ID))
    TASK = RESULT.scalar_one_or_none()
    if TASK:
        return TaskResponseModel.model_validate(TASK.to_dict())
    return None

async def update_task(ID: int, TASK_DATA: TaskUpdateModel, SESSION: AsyncSession) -> TaskResponseModel | None:
    """
    Update the status of a task identified by its ID.

    Args:
        ID (int): The ID of the task to update.
        TASK_DATA (TaskUpdateModel): The updated task data (status).
        SESSION (AsyncSession): The active SQLAlchemy async session.

    Returns:
        TaskResponseModel | None: The updated task if successful, otherwise None.
    """
    STATEMENT = sqlalchemy_update(Task).where(Task.id == ID).values(TASK_DATA.model_dump(exclude_unset=True))
    RESULT = await SESSION.execute(STATEMENT)
    
    if RESULT.rowcount == 0:
        return None

    await SESSION.commit()
    return await read_task(ID, SESSION)

async def delete_task(ID: int, SESSION: AsyncSession) -> bool:
    """
    Delete a task from the database by its ID.

    Args:
        ID (int): The ID of the task to delete.
        SESSION (AsyncSession): The active SQLAlchemy async session.

    Returns:
        bool: True if the task was deleted, False if not found.
    """
    RESULT = await SESSION.execute(select(Task).where(Task.id == ID))
    TASK = RESULT.scalar_one_or_none()

    if TASK is None:
        return False

    await SESSION.delete(TASK)
    await SESSION.commit()
    return True