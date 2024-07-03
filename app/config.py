import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DATABASE_USER = "api_manager"
DATABASE_PASSWORD = "05051999"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_NAME = "api_list"

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
