from http import HTTPStatus
import pytest
from datetime import datetime, timedelta
from utils.global_constants import StatusTypes


# create_task accepts task with 'Pending' status
@pytest.mark.anyio
async def test_create_task_valid_with_pending_status(CLIENT):
    DUE_DATE = (datetime.now() + timedelta(days=1)).isoformat()
    RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Test Task",
        "description": "Testing",
        "status": StatusTypes.PENDING,
        "due_date": DUE_DATE
    })
    assert RESPONSE.status_code == HTTPStatus.OK
    data = RESPONSE.json()
    assert data["title"] == "Test Task"
    assert data["status"] == StatusTypes.PENDING
    assert data["description"] == "Testing"
    assert data["due_date"] == DUE_DATE

# create_task accepts task with "In Progress" status
@pytest.mark.anyio
async def test_create_task_valid_with_in_progress_status(CLIENT):
    DUE_DATE = (datetime.now() + timedelta(days=1)).isoformat()
    RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Test Task",
        "description": "Testing",
        "status": StatusTypes.IN_PROGRESS,
        "due_date": DUE_DATE
    })
    assert RESPONSE.status_code == HTTPStatus.OK
    data = RESPONSE.json()
    assert data["title"] == "Test Task"
    assert data["status"] == StatusTypes.IN_PROGRESS
    assert data["description"] == "Testing"
    assert data["due_date"] == DUE_DATE

# create_task accepts task with "Done" status
@pytest.mark.anyio
async def test_create_task_valid_with_done_status(CLIENT):
    DUE_DATE = (datetime.now() + timedelta(days=1)).isoformat()
    RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Test Task",
        "description": "Testing",
        "status": StatusTypes.DONE,
        "due_date": DUE_DATE
    })
    assert RESPONSE.status_code == HTTPStatus.OK
    data = RESPONSE.json()
    assert data["title"] == "Test Task"
    assert data["status"] == StatusTypes.DONE
    assert data["description"] == "Testing"
    assert data["due_date"] == DUE_DATE

# create_task accepts task with no description
@pytest.mark.anyio
async def test_create_task_valid_with_no_description(CLIENT):
    DUE_DATE = (datetime.now() + timedelta(days=1)).isoformat()
    RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Test Task",
        "status": StatusTypes.DONE,
        "due_date": DUE_DATE
    })
    assert RESPONSE.status_code == HTTPStatus.OK
    data = RESPONSE.json()
    assert data["title"] == "Test Task"
    assert data["status"] == StatusTypes.DONE
    assert data["description"] == None
    assert data["due_date"] == DUE_DATE

# Test get_all_tasks returns a list of tasks
@pytest.mark.anyio
async def test_get_all_tasks(CLIENT):
    RESPONSE = await CLIENT.get("/tasks/")
    assert RESPONSE.status_code == HTTPStatus.OK
    assert isinstance(RESPONSE.json(), list)

# INVALID: Test create_task doesn't accept task with missing title
@pytest.mark.anyio
async def test_create_task_invalid_missing_title(CLIENT):
    RESPONSE = await CLIENT.post("/tasks/", json={
        "description": "No title",
        "status": StatusTypes.PENDING,
        "due_date": (datetime.now() + timedelta(days=1)).isoformat()
    })
    assert RESPONSE.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

# INVALID: test create_task doesn't accept invalid status string
@pytest.mark.anyio
async def test_create_task_invalid_status(CLIENT):
    RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Invalid Status Task",
        "description": "Invalid status",
        "status": "Garbage",
        "due_date": (datetime.now() + timedelta(days=1)).isoformat()
    })
    assert RESPONSE.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

# INVALID: create_task does not accept past due date
@pytest.mark.anyio
async def test_create_task_invalid_past_due_date(CLIENT):
    RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Past Due Task",
        "description": "This is in the past",
        "status": StatusTypes.PENDING,
        "due_date": (datetime.now() - timedelta(days=1)).isoformat()
    })
    assert RESPONSE.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

# get_task retrieves a single existing task
@pytest.mark.anyio
async def test_get_task_valid(CLIENT):
    # First, create a task
    RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Get Me",
        "status": StatusTypes.PENDING,
        "due_date": (datetime.now() + timedelta(days=1)).isoformat()
    })
    TASK_ID = RESPONSE.json()["id"]

    # Fetch the task
    FETCH_RESPONSE = await CLIENT.get(f"/tasks/{TASK_ID}/")
    assert FETCH_RESPONSE.status_code == HTTPStatus.OK
    assert FETCH_RESPONSE.json()["id"] == TASK_ID

# INVALID: get_task handles a non-existent task appropriately
@pytest.mark.anyio
async def test_get_task_invalid_not_found(CLIENT):
    RESPONSE = await CLIENT.get("/tasks/999999/")   # We're never going to write this many tasks during testing
    assert RESPONSE.status_code == HTTPStatus.BAD_REQUEST
    assert "No task exists with an id of '999999'." in RESPONSE.json()["detail"]

# patch_task updates an existing task with a new valid status
@pytest.mark.anyio
async def test_patch_task_valid_status(CLIENT):
    # First, create a task
    CREATE_RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Patch Me",
        "status": StatusTypes.PENDING,
        "due_date": (datetime.now() + timedelta(days=1)).isoformat()
    })
    TASK_ID = CREATE_RESPONSE.json()["id"]

    # Patch the task
    PATCH_RESPONSE = await CLIENT.patch(f"/tasks/{TASK_ID}/", json={"status": StatusTypes.DONE})
    assert PATCH_RESPONSE.status_code == HTTPStatus.OK
    assert PATCH_RESPONSE.json()["status"] == StatusTypes.DONE

# INVALID: patch_task does not update an existing task with a new invalid status
@pytest.mark.anyio
async def test_patch_task_invalid_status(CLIENT):
    # First, create a task
    CREATE_RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Patch Me",
        "status": StatusTypes.PENDING,
        "due_date": (datetime.now() + timedelta(days=1)).isoformat()
    })
    TASK_ID = CREATE_RESPONSE.json()["id"]

    # Patch the task
    PATCH_RESPONSE = await CLIENT.patch(f"/tasks/{TASK_ID}/", json={"status": "Overdue"})
    assert PATCH_RESPONSE.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

# INVALID: patch_task handles a non-existent task appropriately
@pytest.mark.anyio
async def test_patch_task_invalid_not_found(CLIENT):
    RESPONSE = await CLIENT.patch("/tasks/999999/", json={"status": StatusTypes.DONE})
    assert RESPONSE.status_code == HTTPStatus.BAD_REQUEST
    assert "No task exists with an id of '999999'." in RESPONSE.json()["detail"]

# remove_task deletes an existing task
@pytest.mark.anyio
async def test_remove_task_valid_success(CLIENT):
    # First, create a task to delete
    CREATE_RESPONSE = await CLIENT.post("/tasks/", json={
        "title": "Delete Me",
        "status": StatusTypes.PENDING,
        "due_date": (datetime.now() + timedelta(days=1)).isoformat()
    })
    TASK_ID = CREATE_RESPONSE.json()["id"]

    DELETE_RESPONSE = await CLIENT.delete(f"/tasks/{TASK_ID}/")
    assert DELETE_RESPONSE.status_code == HTTPStatus.OK
    assert f"Task with id '{TASK_ID}' deleted successfully." in DELETE_RESPONSE.json()["message"]

# INVALID: remove_task handles a task that doesn’t exist appropriately
@pytest.mark.anyio
async def test_delete_task_invalid_not_found(CLIENT):
    RESPONSE = await CLIENT.delete("/tasks/999999/")
    assert RESPONSE.status_code == HTTPStatus.BAD_REQUEST
    assert "No task exists with an id of '999999'." in RESPONSE.json()["detail"]

# Test read_root method in main.py returns appropriate response
@pytest.mark.anyio
async def test_read_root(CLIENT):
    RESPONSE = await CLIENT.get("/")
    assert RESPONSE.status_code == 200
    assert RESPONSE.json() == {"message": "Server is alive."}