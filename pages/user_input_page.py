import streamlit as st
import asyncio
import uuid
import logging
import pandas as pd

def create_new_task(yet_another_row):
    try:
        df = pd.DataFrame({'uid':[yet_another_row[0]],
                           'starttime':[yet_another_row[1]],
                           'sources': [yet_another_row[2]],
                           'tasktype':[yet_another_row[3]],
                           'targets':[yet_another_row[4]],
                           'test':[yet_another_row[5]],
                           'parsing':[yet_another_row[6]],
                           'semantic':[yet_another_row[7]],
                           'summ':[yet_another_row[8]],
                           'status':[yet_another_row[9]],
                           'endtime':[yet_another_row[10]]})
        df.to_csv(f'ldb/tasks/{yet_another_row[0]}.csv')

        logging.info(f'Creating new task. Success.')

    except Exception as e:
        logging.error(f'Creating new task. Failed. {e}')

st.title("Streamlit App")

# Ввод переменных от пользователя
chanel_user_input = st.text_input("Введите каналы для отслеживания", "")
keyword_user_input = st.text_input("Введите ключ для отслеживания", "")


# Кнопка для запуска внешнего скрипта
if st.button("Запрос статистики по каналам"):
    task = (uuid.uuid4(), 'time', chanel_user_input, 'task-type', 'targets', 'test', 0, 0, 0, 'in progress', 'endtime')
    create_new_task(task)


if st.button('Обработка данных нейросетью'):
    pass