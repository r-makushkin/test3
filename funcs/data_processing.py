import pandas as pd
import re
import logging
import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification, MBartForConditionalGeneration, MBartTokenizer
from config import minus_words

log_file_path = 'ldb/app.log'
logging.basicConfig(level=logging.INFO, filename=log_file_path, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def get_data(path):
    df = pd.read_csv(path)
    uid = path.split('/')[-1].split('.')[0]    # Читаем uid, оптимальнее не придумал
    df_minus = pd.DataFrame()
    for word in minus_words:
        df_temp = df[df['text'].str.contains(word, case=False, na=False)]
        df_minus = pd.concat([df_minus, df_temp])
    # Удаление дубликатов строк, если они есть
    df_minus = df_minus.drop_duplicates()
    # Удаление строк, содержащих любое из минус-слов
    for word in minus_words:
        df = df[~df['text'].str.contains(word, case=False, na=False)]
    def clean_text(text):
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)  # Удаление ссылок
        text = re.sub(r'<.*?>', ' ', text)  # Удаление HTML тегов
        return text
    df['text'] = df['text'].apply(clean_text)
    # так как предыдущими действиями мы скорее всего удалили только ссылки, но оставили обёртки, удаляем обёртки
    df['text'] = df['text'].str.replace('<a href="', ' ')
    df = df.dropna(subset=['text'])

    # ОПРЕДЕЛЕНИЕ ТОНАЛЬНОСТИ

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    logging.info(f'device: {device}')

    # Загрузка модели и токенизатора "MonoHime/rubert-base-cased-sentiment-new"
    model = AutoModelForSequenceClassification.from_pretrained('models').to(device)
    tokenizer = AutoTokenizer.from_pretrained('models/local_tokenizer')

    # Установка размера пакета (batch size)
    batch_size = 16

    # Функция для подготовки пакетов данных
    def preprocess_texts(texts):
        return tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors="pt")


    # Инициализация массива для хранения предсказаний
    predicted_classes = torch.tensor([], dtype=torch.int64, device=device)

    # Обработка текстов пакетами и получение предсказаний
    for i in range(0, len(df['text']), batch_size):
        batch_texts = df['text'][i:i + batch_size].tolist()
        encoded_input = preprocess_texts(batch_texts)
        # Убедитесь, что данные находятся на GPU
        encoded_input = {k: v.to(device) for k, v in encoded_input.items()}

        with torch.no_grad():
            batch_predictions = model(**encoded_input)
            batch_predicted_classes = torch.argmax(batch_predictions.logits, dim=1)
            predicted_classes = torch.cat((predicted_classes, batch_predicted_classes), 0)

    # Добавление предсказаний в DataFrame
    df['predicted_class'] = predicted_classes.tolist()
    
    df.to_csv(f'ldb/SAcompleted/{uid}.csv', index=False)