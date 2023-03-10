from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import logger
from app.routers.preprocessing_router import router as preprocessing_router
from app.routers.training_router import router as training_router
from app.routers.analysis_router import router as analysis_router
from app.routers.file_router import router as file_router
from app.services.nltk_service import NltkService

app = FastAPI(
    title='Tesis MCPI',
    description='Proyecto de desarrollo para la tesis de la Maestría en '
    + 'Ciencias del Procesamiento de la Información.',
    version='1.0.0',
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router)
app.include_router(preprocessing_router)
app.include_router(training_router)
app.include_router(analysis_router)

nltk_service = NltkService()


@app.on_event('startup')
def on_startup():
    logger.info('on_startup')
    nltk_service.download()


@app.on_event('shutdown')
def on_shutdown():
    logger.info('on_shutdown')


@app.exception_handler(Exception)
async def catch_exception(request: Request, exc: Exception):
    logger.error(exc)
    return JSONResponse(status_code=400, content={'detail': 'UNKNOWN_ERROR'})


@app.exception_handler(FileNotFoundError)
async def catch_file_not_found_error(request: Request, exc: FileNotFoundError):
    logger.error(exc)
    return JSONResponse(status_code=400, content={'detail': 'FILE_NOT_FOUND'})


@app.exception_handler(ValueError)
async def catch_value_error(request: Request, exc: ValueError):
    logger.error(exc)
    return JSONResponse(status_code=400, content={'detail': 'VALUE_ERROR'})
