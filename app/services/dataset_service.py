import os
from typing import List
from fastapi import UploadFile, HTTPException
from app.schemas.common_schemas import FileUpload
from app.utils.singleton import SingletonMeta
from app.utils.strings import Strings
from fastapi.responses import FileResponse
from datetime import datetime
import pandas as pd


class DatasetService(metaclass=SingletonMeta):
    def read_dataset(self, file_path: str, encoding: str, delimiter: str) -> pd.DataFrame:
        df = pd.read_csv(file_path, encoding=encoding, delimiter=delimiter)
        return df

    def prepare_dataset(self, file_path: str) -> pd.DataFrame:
        df = self.read_dataset(
            file_path=f'uploads/cleaned/{file_path}',
            encoding='utf-8',
            delimiter='|'
        )

        df['sentiment'] = df['sentiment'].replace(
            {
                'Positivo': '1',
                'Negativo': '-1',
                'Neutral': '0'
            }
        )

        return df

    def to_csv(self, df: pd.DataFrame, file_path: str) -> FileUpload:
        timestamp = int(datetime.timestamp(datetime.now()))
        file_path = f'{file_path[0: -4]}_{timestamp}.csv'

        df.to_csv(
            f'uploads/classified/{file_path}',
            index=False
        )

        return FileUpload(file_path=file_path)

    def upload_dataset(self, file: UploadFile) -> FileUpload:
        if file.content_type != 'text/csv':
            raise HTTPException(
                status_code=400, detail='DATASET_MUST_BE_A_CSV')

        timestamp = int(datetime.timestamp(datetime.now()))
        snack_name = Strings.to_snack_case(file.filename)
        file_path = f'{snack_name[0: -4]}_{timestamp}.csv'

        with open(f'uploads/{file_path}', 'wb') as f:
            f.write(file.file.read())

        return FileUpload(file_path=file_path)

    def get_datasets_list(self, path: str = None) -> List[FileUpload]:
        files = os.listdir(f'uploads/{path}' if path else 'uploads')

        if '.gitkeep' in files:
            files.remove('.gitkeep')

        if 'cleaned' in files:
            files.remove('cleaned')

        if 'classified' in files:
            files.remove('classified')

        return [
            FileUpload(file_path=f'{file_name}') for file_name in files
        ]

    def download_dataset(self, file_path: str) -> FileResponse:
        os.stat(f'uploads/{file_path}')
        return FileResponse(
            path=f'uploads/{file_path}',
            media_type='text/csv',
            filename=file_path
        )

    def summary_dataset(self, file_path: str, encoding: str, delimiter, target_column: str) -> dict:
        os.stat(f'uploads/cleaned/{file_path}')
        df = self.read_dataset(
            file_path=f'uploads/cleaned/{file_path}',
            encoding=encoding,
            delimiter=delimiter
        )
        return df[target_column].value_counts().to_dict()

    def get_metrics(self, df: pd.DataFrame, y_true: str, y_pred: str) -> dict:
        for index, row in df.iterrows():
            if row[y_true] == 1:
                pass
            elif row[y_true] == 0:
                pass
            elif row[y_true] == -1:
                pass

        from sklearn.metrics import accuracy_score, cohen_kappa_score, f1_score, r2_score

        accuracy = accuracy_score(df[y_true], df[y_pred])
        kappa = cohen_kappa_score(df[y_true], df[y_pred])
        f1 = f1_score(df[y_true], df[y_pred])
        f1 = r2_score(df[y_true], df[y_pred])
        print(f'accuracy: {accuracy}')
        print(f'kappa: {kappa}')
        print(f'f1: {f1}')
        print(f'r2: {r2}')
        return {}
