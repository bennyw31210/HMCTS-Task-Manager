from dotenv import load_dotenv, find_dotenv
import motor.motor_asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from http import HTTPStatus
from logger import log_internal_server_error
from routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load environment variables
    load_dotenv(find_dotenv())

    # Initialize the MongoDB client
    MONGO_CLIENT = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))

    # Get the database from the client
    HMCTS_DB = MONGO_CLIENT[os.getenv("MONGO_DB_NAME")]

    app.state.HMCTS_DB = HMCTS_DB

    yield
 
    MONGO_CLIENT.close()

def show_error(STATUS_CODE: int, DESCRIPTION: str, DETAIL: str) -> JSONResponse:
    return JSONResponse(status_code=STATUS_CODE, content={
        "status_code": STATUS_CODE,
        "description": DESCRIPTION,
        "detail": DETAIL
    })

app = FastAPI(title="HMCTS Task Manager Backend", lifespan=lifespan)

app.include_router(tasks.router)

app.add_middleware(CORSMiddleware, 
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.exception_handler(HTTPException)
def http_exception_handler(REQUEST: Request, EXCEPTION: HTTPException) -> JSONResponse:
    return show_error(EXCEPTION.status_code, HTTPStatus(EXCEPTION.status_code).phrase, EXCEPTION.detail)

@app.exception_handler(404)
def http_404_handler(REQUEST: Request, EXCEPTION) -> JSONResponse:
    return show_error(HTTPStatus.NOT_FOUND, HTTPStatus.NOT_FOUND.phrase, "The requested resource could not be found.")

@app.exception_handler(Exception)
def general_exception_handler(REQUEST: Request, EXCEPTION: Exception):
    log_internal_server_error(EXCEPTION)
    return show_error(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, "Something went wrong...")

@app.get("/")
def read_root() -> dict:
    return {"message": "Server is alive."}