from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

from fastapi.staticfiles import StaticFiles
from http import HTTPStatus
from logger import log_internal_server_error
from routers import tasks
from db.tables.task import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the HMCTS Task Manager application. Initialises the database connection 
    engine and session maker, and ensures proper cleanup during application shutdown.
    
    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Executes the application lifecycle and ensures cleanup at the end.
    
    Notes:
        - The method loads environment variables from a .env file.
        - The PostgreSQL engine and session are created and disposed of within this context.
    """
    # Load environment variables
    load_dotenv(find_dotenv())

    POSTGRES_URI_PREFIX = os.getenv("POSTGRES_URI_PREFIX")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_CONTAINER_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    # Create async SQLAlchemy engine
    POSTGRES_ENGINE = create_async_engine(f"{POSTGRES_URI_PREFIX}{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}", echo=True)

    # Create session maker for asynchronous database access
    AsyncSessionLocal = sessionmaker(
        bind=POSTGRES_ENGINE, class_=AsyncSession, expire_on_commit=False
    )

    # Store engine and session in FastAPI app state for access throughout the app
    app.state.POSTGRES_ENGINE = POSTGRES_ENGINE
    app.state.ASYNC_SESSION = AsyncSessionLocal

    # Yield control back to FastAPI for processing requests
    yield
 
    # Dispose of engine and close connections when the app shuts down
    await POSTGRES_ENGINE.dispose()


def show_error(STATUS_CODE: int, DESCRIPTION: str, DETAIL: str) -> JSONResponse:
    """
    Generates a standardised error response for HTTP exceptions.

    Args:
        STATUS_CODE (int): The HTTP status code.
        DESCRIPTION (str): A brief description of the error.
        DETAIL (str): Detailed information about the error.

    Returns:
        JSONResponse: A formatted error response to be returned by FastAPI.
    """
    return JSONResponse(status_code=STATUS_CODE, content={
        "status_code": STATUS_CODE,
        "description": DESCRIPTION,
        "detail": DETAIL
    })

# Initialise the FastAPI application
app = FastAPI(title="HMCTS Task Manager Backend", lifespan=lifespan)

# Include the task router from the 'routers' module
app.include_router(tasks.router)

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware to allow cross-origin requests from the frontend
app.add_middleware(CORSMiddleware, 
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.exception_handler(HTTPException)
def http_exception_handler(REQUEST: Request, EXCEPTION: HTTPException) -> JSONResponse:
    """
    Custom exception handler for HTTPException. Converts it to a formatted JSON response.

    Args:
        REQUEST (Request): The incoming request object.
        EXCEPTION (HTTPException): The HTTP exception raised during request processing.

    Returns:
        JSONResponse: A formatted JSON response containing the status code, description, and detail of the exception.
    """
    return show_error(EXCEPTION.status_code, HTTPStatus(EXCEPTION.status_code).phrase, EXCEPTION.detail)

@app.exception_handler(404)
def http_404_handler(REQUEST: Request, EXCEPTION) -> JSONResponse:
    """
    Custom exception handler for 404 errors. Converts them to a formatted JSON response.

    Args:
        REQUEST (Request): The incoming request object.
        EXCEPTION: The exception or error raised when the resource is not found.

    Returns:
        JSONResponse: A formatted JSON response for a 404 error with details about the missing resource.
    """
    return show_error(HTTPStatus.NOT_FOUND, HTTPStatus.NOT_FOUND.phrase, "The requested resource could not be found.")

@app.exception_handler(Exception)
def general_exception_handler(REQUEST: Request, EXCEPTION: Exception):
    """
    General exception handler for all unhandled exceptions. Logs the error and returns a formatted error response with status code 500.

    Args:
        REQUEST (Request): The incoming request object.
        EXCEPTION (Exception): The unhandled exception raised during request processing.

    Returns:
        JSONResponse: A standardized 500 Internal Server Error response, with the exception details logged.
    """
    log_internal_server_error(EXCEPTION)
    return show_error(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, "Something went wrong...")

@app.get("/", 
         summary="Root endpoint. Retrieve's the app's frontend.", 
         description="Root endpoint. Retrieve's the app's frontend.",
)
def read_root(response_class=HTMLResponse) -> dict:
    """
    Root endpoint to serve up the frontend application web page.

    Returns:
        HTMLResponse: The frontend application web page.
    """
    with open("static/index.html") as f:
        content = f.read()
    return HTMLResponse(content=content)