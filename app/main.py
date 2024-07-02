import io
import json
import logging
import PyPDF2
import uvicorn

from fastapi import FastAPI, UploadFile, Query, HTTPException
from typing import Annotated

from app.models.models import ParsedData, Item
from app.configs.settings import settings

app = FastAPI()

# Создаем главный объект logger
logger = logging.getLogger("myLogger")
logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи логов в файл (консольный обработчик работает от uvicorn по дефолту)
file_handler = logging.FileHandler(filename="data.log", encoding="utf-8", mode="w")
file_handler.setLevel(logging.DEBUG)

# Создаем формат для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Устанавливаем формат для файлового обработчика
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


@app.get("/")
async def main():
    logger.info("GET запрос к главной странице")
    return {"main": "page"}


# Отправка текстового файла
@app.post("/upload_txt/")
async def upload_file(uploaded_file: UploadFile):
    content = await uploaded_file.read()
    # Получаем название текстового файла
    file_name = uploaded_file.filename
    logger.info("Имя полученного txt файла: \t%s", file_name)
    with open(file=f'uploaded_files/txt_files/posted_{file_name}', mode='wb') as file:
        file.write(content)
    logger.info("Запись в файл была осуществлена!")
    return {"filename": uploaded_file.filename,
            "content": content}


# отправка pdf файла
@app.post("/upload_pdf/")
async def upload_file(uploaded_file: UploadFile):
    # В переменной content содержится байт-код содержимого pdf (полученного через POST запросы)
    content = await uploaded_file.read()
    logger.info("Загружено содержание pdf (байт-код)")
    # Записываем файл (сохраняем содержимое файла)
    pdf_writer = PyPDF2.PdfWriter()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    # Проходимся по каждой странице и добавляем ее к pdf_writer
    for page_num in range(len(pdf_reader.pages)):
        logger.debug("Добавилась страница: %s", page_num+1)
        pdf_writer.add_page(pdf_reader.pages[page_num])
    # Записываем полученное имя файла
    file_name = uploaded_file.filename
    logger.info("Имя полученного pdf файла: \t%s", file_name)
    with open(f'uploaded_files/pdf_files/posted_{file_name}', 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    return {'pdf_filename': file_name}


# Тестовая версия отправки данных в формате json
@app.post("/parsed_data/")
async def post_json(parsed_data: ParsedData):
    logger.info("parsed_data: \t%s", parsed_data)
    return parsed_data


# Тестовая версия получения данных в формате json
@app.get("/json_data/{json_file}")
async def get_json(json_file: str):
    with open(file=f'uploaded_files/json_files/{json_file}', mode='r', encoding='utf-8') as file:
        data = json.load(file)
        logger.info("Загружены данные из файла json:\t\n%s", data)
    return {
        "inn_kpp": data["inn_kpp"],
        "invoice": data["invoice"],
        "data_table": data["data_table"],
        "total_without_tax": data["total_without_tax"],
        "amount_of_tax":  data["amount_of_tax"],
        "total_amount": data["total_amount"]
    }


@app.post("/items/{item_id}")
async def get_item(item: Item, item_id: int, query: Annotated[str | None, Query(max_length=50)] = None):
    # Query(max_length=50) - означает, что значение запроса не может превышать больше 50 символов.
    file_name: str = f'temp_{item_id}.json'
    logger.info("Название файла: %s", file_name)

    item_dict: dict = {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax
    }
    if item.tax is not None:
        full_price: float = item.price + item.tax
        item_dict.update({"full_price": full_price})
        logger.info("Обновленная цена: %s", item_dict["full_price"])
    if query:
        item_dict.update({"query": query})

    with open(file=f'uploaded_files/json_files/{file_name}', mode='w', encoding='utf-8') as file:
        json.dump(obj=item_dict, fp=file, indent=2, ensure_ascii=False)
    return item_dict


if __name__ == '__main__':
    # Вот тут можно будет подключить (или изменить) логи и другие настройки.
    logger.info("Запуск сервера uvicorn")
    uvicorn.run(
        app="app.main:app",
        reload=settings.RELOAD,
        host=settings.HOST,
        port=settings.PORT,
        log_level="debug"
    )
    logger.info("Остановка сервера uvicorn")


