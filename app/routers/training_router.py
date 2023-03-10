from fastapi import APIRouter
from app.schemas.file_schemas import FileUpload
from app.services.dataset_service import DatasetService
from app.services.training_service import TrainingService
from app.config import logger

router = APIRouter(prefix='/training', tags=['Training'])

dataset_service = DatasetService()
training_service = TrainingService()


@router.post('/naive_bayes_bernoulli', response_model=FileUpload)
def train_naive_bayes_bernoulli(file_path: str):
    logger.debug('train_naive_bayes_bernoulli()')

    result = training_service.naive_bayes(
        file_path=f'resources/cleaned/{file_path}',
        encoding='utf-8',
        delimiter=','
    )

    return dataset_service.to_csv(
        df=result.df,
        file_path=f'resources/classified/nbb_{file_path}'
    )


@router.post('/logistic_regression', response_model=FileUpload)
def train_logistic_regression(file_path: str):
    logger.debug('train_logistic_regression()')

    result = training_service.logistic_regression(
        file_path=f'resources/cleaned/{file_path}',
        encoding='utf-8',
        delimiter=','
    )

    return dataset_service.to_csv(
        df=result.df,
        file_path=f'resources/classified/lgr_{file_path}'
    )


@router.post('/svm', response_model=FileUpload)
def train_svm(file_path: str):
    logger.debug('train_svm()')

    result = training_service.logistic_regression(
        file_path=f'resources/cleaned/{file_path}',
        encoding='utf-8',
        delimiter=','
    )

    return dataset_service.to_csv(
        df=result.df,
        file_path=f'resources/classified/svm_{file_path}'
    )


@router.post('/assemble', response_model=FileUpload)
def train_all(file_path: str):
    logger.debug('train_all()')

    result = training_service.assemble(
        file_path=f'resources/cleaned/{file_path}',
        encoding='utf-8',
        delimiter=','
    )

    return dataset_service.to_csv(
        df=result.df,
        file_path=f'resources/classified/all_{file_path}'
    )
