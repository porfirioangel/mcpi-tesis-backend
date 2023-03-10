import joblib
from app.patterns.singleton import SingletonMeta
from app.services.dataset_service import DatasetService
from app.services.nltk_service import NltkService
from app.services.preprocessing_service import PreprocessingService
from app.services.wordcloud_service import WordcloudService
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

dataset_service = DatasetService()
nltk_service = NltkService()
wordcloud_service = WordcloudService()
preprocessing_service = PreprocessingService()

questions = {
    'Q_ADAPTATION': 'Do you have other climate adaptation ideas? Submit here:',
    'Q_MITIGATION': 'Do you have other climate mitigation ideas? Submit here:',
    'Q_EQUITY': 'Do you have other ideas for environmental equity, justice,'
    + ' and community resilience? Submit here:',
    'Q_POLICY': 'Do you have other policy ideas? Submit here:',
    'Q_SUSTAINABLE': 'Are you interested in participating in any other ways'
    + ' to help make Tucson environmentally sustainable? Submit here:',
    'Q_OTHER': 'Is there anything else you would like to share that was not'
    + ' already addressed?'
}


class AnalysisService(metaclass=SingletonMeta):
    def execute_algorithm(
        self,
        file_path: str,
        encoding: str,
        delimiter: str,
        model_file_path: str
    ):
        df = dataset_service.read_dataset(
            file_path=file_path,
            encoding=encoding,
            delimiter=delimiter,
        )

        model = joblib.load(model_file_path)

        # Read the term document matrix used to train the models
        training_tdm_df = dataset_service.read_dataset(
            file_path='resources/cleaned/'
            + 'tdm_bal_lab_respuestas_form_1671774115.csv',
            encoding='utf-8',
            delimiter=','
        )

        neg_serie_data = {}
        pos_serie_data = {}

        for question in questions:
            q_df = pd.DataFrame()
            q_df['answer'] = df[questions[question]].values.tolist()
            q_df = q_df.replace(r'\n', ' ', regex=True)
            q_df = q_df.replace('(?i)tucson', '', regex=True)
            q_df = q_df.replace('(?i)city', '', regex=True)
            q_df = q_df.replace('(?i)city', '', regex=True)
            q_df = q_df.replace(r'^\s*no\s*$', '', regex=True)
            q_df = q_df.replace(r'^\s*NO\s*$', '', regex=True)
            q_df = q_df.replace(r'^\s*No\s*$', '', regex=True)
            q_df = q_df.replace(r'^\s*nO\s*$', '', regex=True)
            q_df = q_df.replace(r'^\s*-\s*$', '', regex=True)
            nan_value = float("NaN")
            q_df.replace('', nan_value, inplace=True)
            q_df = q_df.dropna()
            text = ', '.join(str(x) for x in q_df['answer'].values.tolist())

            # Generate wordcloud for all question answers
            wordcloud_service.generate_wordcloud(
                text=text,
                title=questions[question],
                file_path=f'resources/wordclouds/{question}.png'
            )

            # Get word column names
            word_columns = training_tdm_df.columns[2:].to_list()

            new_rows = []

            for index, row in q_df.iterrows():
                row_data = {}
                for column in word_columns:
                    if column in row['answer']:
                        row_data[column] = 'Yes'
                    else:
                        row_data[column] = 'No'
                new_rows.append(row_data)

            # Create a new dataframe with classification results
            target_tdm_df = pd.DataFrame(
                columns=word_columns,
                data=new_rows
            )

            # Convert word columns to categories
            for column in word_columns:
                target_tdm_df[column] = target_tdm_df[column].astype(
                    'category').cat.codes

            # Do the predictions
            predictions = model.predict(target_tdm_df)

            positives = []
            negatives = []

            for i in range(len(predictions)):
                prediction = predictions[i]

                if prediction == 1:
                    positives.append(q_df['answer'].values[i])
                elif prediction == -1:
                    negatives.append(q_df['answer'].values[i])

            # Generate wordcloud for question positive answers
            wordcloud_service.generate_wordcloud(
                text=', '.join(str(x) for x in positives),
                title=questions[question],
                file_path=f'resources/wordclouds/{question}_POS.png'
            )

            # Generate wordcloud for question negative answers
            wordcloud_service.generate_wordcloud(
                text=', '.join(str(x) for x in negatives),
                title=questions[question],
                file_path=f'resources/wordclouds/{question}_NEG.png'
            )

            print(question)
            print(f'pos: {len(positives)}')
            print(f'neg: {len(negatives)}')
            print()

            pos_serie_data[question] = len(positives)
            neg_serie_data[question] = len(negatives)

        pos_serie = pd.Series(pos_serie_data, name='Positives')
        neg_serie = pd.Series(neg_serie_data, name='Negatives')

        plt.figure(figsize=(15, 9))

        pos_serie.plot.bar(color='blue')
        neg_serie.plot.bar(color='orange')

        plt.title('Total of answers by question')
        plt.xlabel("Question")
        plt.ylabel("Total")
        plt.legend()
        plt.savefig('resources/metrics/total_by_question.png')
        plt.close()

    def logistic_regression(
        self,
        file_path: str,
        encoding: str,
        delimiter: str
    ):
        return self.execute_algorithm(
            file_path=file_path,
            encoding=encoding,
            delimiter=delimiter,
            model_file_path='resources/models/lgr.sav'
        )

    def naive_bayes(
        self,
        file_path: str,
        encoding: str,
        delimiter: str
    ):
        return self.execute_algorithm(
            file_path=file_path,
            encoding=encoding,
            delimiter=delimiter,
            model_file_path='resources/models/nbb.sav'
        )

    def svm(
        self,
        file_path: str,
        encoding: str,
        delimiter: str
    ):
        return self.execute_algorithm(
            file_path=file_path,
            encoding=encoding,
            delimiter=delimiter,
            model_file_path='resources/models/svm.sav'
        )

    def assemble(
        self,
        file_path: str,
        encoding: str,
        delimiter: str
    ):
        self.logistic_regression(
            file_path=file_path,
            encoding=encoding,
            delimiter=delimiter
        )

        self.naive_bayes(
            file_path=file_path,
            encoding=encoding,
            delimiter=delimiter
        )

        self.svm(
            file_path=file_path,
            encoding=encoding,
            delimiter=delimiter
        )
