import re
from app.utils.singleton import SingletonMeta
from app.utils import datasets
from app.config import logger
from textblob import TextBlob

GENERATED_COLUMNS = [
    'length', 'cc', 'vbp', 'cd', 'dt', 'ex', 'fw', 'inn', 'jj', 'jjr', 'jjs',
    'ls', 'md', 'nn', 'nns', 'nnp', 'nnps', 'pdt', 'posss', 'prp', 'rb', 'rbr',
    'rp', 'to', 'uh', 'vb', 'vbd', 'vbg', 'vbn', 'vbz', 'wdt', 'wp', 'wps',
    'wrb', 'pos_length', 'neg_length', 'pos_acumulado', 'neg_acumulado',
    'polarity', 'cant_caracteres'
]


class CleaningService(metaclass=SingletonMeta):
    def get_unwanted_words(self):
        pass

    def remove_unwanted_words(self, sentence: str):
        pass

    def remove_yes_no_answers(self, sentence: str):
        pass

    def remove_non_alphabetic(self, sentence: str):
        pass

    def generate_clean_row(self, text: str) -> str:
        cc = 0  # Conjunción de coordinación
        cd = 0  # Dígito cardinal
        dt = 0  # Determinador
        ex = 0  # Existencial (allí)
        fw = 0  # Palabra extranjera
        inn = 0  # IN Preposición/junta subordinación
        jj = 0  # Adjetivo
        jjr = 0  # Adjetivo comparativo
        jjs = 0  # Adjetivo superlativo
        ls = 0  # Marcador de lista
        md = 0  # Modal (podría, podrá)
        nn = 0  # Sustantivo singular
        nns = 0  # Sustantivo plural
        nnp = 0  # Sustantivo propio
        nnps = 0  # Sustantivo propio plural
        pdt = 0  # Predeterminado
        posss = 0  # Posesivo
        prp = 0  # Pronombre personal
        # PrP = 0  # PRP$ Pronombre posesivo
        rb = 0  # RB Adverbio
        rbr = 0  # Adverbio comparativo
        # rbs? # Adverbio superlativo
        rp = 0  # Particular
        to = 0  # Particular de infinitivo
        uh = 0  # Interjección
        vb = 0  # Verbo
        vbd = 0  # VBD ?
        vbg = 0  # VBG ?
        vbn = 0  # Verbo participio
        Vbp = 0  # Verbo presente
        vbz = 0  # Verbo tercera persona
        wdt = 0  # Wh-determiner
        wp = 0  # Pronombre de pregunta (quién, qué)
        wps = 0  # WP$ Posesivo con pronombre (cuyo)
        wrb = 0  # Wh-adverb (dónde, cuándo)
        palabras_pos = 0
        palabras_neg = 0
        acumulado_pos = 0
        acumulado_neg = 0

        # PASO 1: QUITAR URLS Y @
        url = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        url2 = '(www\.)(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        emoticons = "['\&\-\.\/()=:;]+"
        patron = re.compile(
            '_|•|-|#|@|[¿?]|' + url + '|' + url2 + '|' + emoticons)
        entrada_m = patron.sub(' ', text)

        # PASO 2: CONVERTIR TEXTO EN MINUSCULAS
        texto = TextBlob(entrada_m)
        minusculas = texto.correct()
        minusculas = texto.lower()

        # PASO 3: ETIQUETAS TIPO DE PALABRA
        for word, pos in minusculas.tags:
            if (pos == "CC"):
                cc = cc + 1
            if (pos == "VBP"):
                Vbp = Vbp + 1
            if (pos == "CD"):
                cd = cd + 1
            if (pos == "DT"):
                dt = dt + 1
            if (pos == "EX"):
                ex = ex + 1
            if (pos == "FW"):
                fw = fw + 1
            if (pos == "IN"):
                inn = inn + 1
            if (pos == "JJ"):
                jj = jj + 1
            if (pos == "JJR"):
                jjr = jjr + 1
            if (pos == "JJS"):
                jjs = jjs + 1
            if (pos == "LS"):
                ls = ls + 1
            if (pos == "MD"):
                md = md + 1
            if (pos == "NN"):
                nn = nn + 1
            if (pos == "NNS"):
                nns = nns + 1
            if (pos == "NNP"):
                nnp = nnp + 1
            if (pos == "NNPS"):
                nnps = nnps + 1
            if (pos == "PDT"):
                pdt = pdt + 1
            if (pos == "POS"):
                posss = posss + 1
            if (pos == "PRP$"):
                prp = prp + 1
            if (pos == "RB"):
                rb = rb + 1
            if (pos == "RBR"):
                rbr = rbr + 1
            if (pos == "RP"):
                rp = rp + 1
            if (pos == "TO"):
                to = to + 1
            if (pos == "UH"):
                uh = uh + 1
            if (pos == "VB"):
                vb = vb + 1
            if (pos == "VBG"):
                vbd = vbd + 1
            if (pos == "VBN"):
                vbn = vbn + 1
            if (pos == "VBZ"):
                vbz = vbz + 1
            if (pos == "WDT"):
                wdt = wdt + 1
            if (pos == "WP"):
                wp = wp + 1
            if (pos == "WP$"):
                wps = wps + 1
            if (pos == "WRB"):
                wrb = wrb + 1
            verf = TextBlob(word)
            w_sent = verf.sentiment.polarity
            if (w_sent > 0):
                palabras_pos = palabras_pos + 1
                acumulado_pos = acumulado_pos + w_sent
            if (w_sent < 0):
                palabras_neg = palabras_neg + 1
                acumulado_neg = acumulado_neg + w_sent

        # PASO 4: Tokens
        palabras = minusculas.words
        cantidad = len(palabras)

        # PASO 5: A. Sentimiento
        Polari = minusculas.sentiment.polarity

        # PASO 6: Cantidad de caracteres
        cant_caracteres = len(text)

        # PASO 7: Generación de fila para dataset
        Ten = minusculas.lower()
        CanPala = cantidad
        new_row = f'{Ten}|{CanPala}|{cc}|{Vbp}|{cd}|{dt}|{ex}|{fw}|{inn}|{jj}|' +\
            f'{jjr}|{jjs}|{ls}|{md}|{nn}|{nns}|{nnp}|{nnps}|{pdt}|{posss}|' +\
            f'{prp}|{rb}|{rbr}|{rp}|{to}|{uh}|{vb}|{vbd}|{vbg}|{vbn}|{vbz}|' +\
            f'{wdt}|{wp}|{wps}|{wrb}|{palabras_pos}|{palabras_neg}|' +\
            f'{acumulado_pos}|{acumulado_neg}|{Polari}|{cant_caracteres}\n'
        return new_row

    def clean_dataset(self, file_path: str) -> str:
        # Define dataset configuration
        encoding = 'utf-8'
        delimiter = ','
        target_column = ''
        text_column = ''  # TODO: Fill this data

        # Read original dataset
        original_file_path = f'uploads/{file_path}'
        original_df = datasets.read_dataset(original_file_path, 'utf-8', ',')
        original_length = original_df.shape[0]

        # New dataset file name
        file_path = f'uploads/{file_path[0: -4]}_cleaned.csv'

        # Open file in write mode
        file = open(file_path, 'w', encoding='utf-8')

        # Header columns generation
        headers = f'{target_column}|{text_column}'

        # Write header columns
        file.write(headers)

        # Iterate original dataset and write calculated values for the new one
        for index, row in original_df.iterrows():
            logger.debug(f'Cleaning row {index + 1}/{original_length}')
            new_row = self.generate_clean_row(row[text_column])
            logger.debug(new_row)

        # End file writting
        file.close()
        return file_path
