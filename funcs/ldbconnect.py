import csv
import logging
import datetime
import pandas as pd

# Указываем путь к файлу лога и формат записей
log_file_path = 'ldb/.log'
logging.basicConfig(level=logging.INFO, filename=log_file_path, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def create_new_task(yet_another_row):
    try:
        df = pd.DataFrame({'uid':yet_another_row[0],
                           'starttime':yet_another_row[1],
                           'sources': yet_another_row[2],
                           'tasktype':yet_another_row[3],
                           'targets':yet_another_row[4],
                           'test':yet_another_row[5],
                           'parsing':yet_another_row[6],
                           'semantic':yet_another_row[7],
                           'summ':yet_another_row[8],
                           'status':yet_another_row[9],
                           'endtime':yet_another_row[10]})
        df.to_csv(f'ldb/tasks/{yet_another_row[0]}.csv')

        logging.info(f'Creating new task. Success.')

    except Exception as e:
        logging.error(f'Creating new task. Failed. {e}')


