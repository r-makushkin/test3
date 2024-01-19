import csv
import logging
import datetime

# Указываем путь к файлу лога и формат записей
log_file_path = 'ldb/app.log'
logging.basicConfig(level=logging.INFO, filename=log_file_path, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

def create_new_task(yet_another_row):
    try:
        with open('ldb/task-story.csv', 'a', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(yet_another_row)

        logging.info(f'Creating new task. Success. Time: {datetime.time}, date: {datetime.date}')

    except Exception as e:
        logging.error(f'Creating new task. Failed. Time: {datetime.time}, date: {datetime.date}. {e}')

