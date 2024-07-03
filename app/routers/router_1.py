import io
import json
import logging
import PyPDF2


from fastapi import APIRouter, UploadFile, Query
from typing import Annotated

from app.models.models import ParsedData, Item

router_1 = APIRouter()

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


@router_1.get("/")
async def router_main():
    # logger.info("GET запрос к главной странице")
    return {"router": "router_page"}


# Отправка текстового файла
@router_1.post("/upload_txt/", status_code=201)
async def upload_file(uploaded_file: UploadFile):
    content = await uploaded_file.read()
    # Получаем название текстового файла
    file_name = uploaded_file.filename
    logger.info("The name of txt file: \t%s", file_name)
    with open(file=f'uploaded_files/txt_files/posted_{file_name}', mode='wb') as file:
        file.write(content)
    logger.info("The file was written!")
    return {"filename": uploaded_file.filename,
            "content": content}


# отправка pdf файла
@router_1.post("/upload_pdf/", status_code=201)
async def upload_file(uploaded_file: UploadFile):
    # В переменной content содержится байт-код содержимого pdf (полученного через POST запросы)
    content = await uploaded_file.read()
    logger.info("The content of pdf was loaded")
    # Записываем файл (сохраняем содержимое файла)
    pdf_writer = PyPDF2.PdfWriter()
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
    # Проходимся по каждой странице и добавляем ее к pdf_writer
    for page_num in range(len(pdf_reader.pages)):
        logger.debug("Added page: %s", page_num+1)
        pdf_writer.add_page(pdf_reader.pages[page_num])
    # Записываем полученное имя файла
    file_name = uploaded_file.filename
    logger.info("The name of pdf file: \t%s", file_name)
    with open(f'uploaded_files/pdf_files/posted_{file_name}', 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    return {'pdf_filename': file_name}


# Тестовая версия отправки данных в формате json
@router_1.post("/parsed_data/", status_code=201)
async def post_json(parsed_data: ParsedData):
    logger.info("parsed_data: \t%s", parsed_data)
    return parsed_data


# Тестовая версия получения данных в формате json
@router_1.get("/json_data/{json_file}", status_code=201)
async def get_json(json_file: str):
    with open(file=f'uploaded_files/json_files/{json_file}', mode='r', encoding='utf-8') as file:
        data = json.load(file)
        logger.info("The data from JSON-file was loaded:\t\n%s", data)
    return {
        "inn_kpp": data["inn_kpp"],
        "invoice": data["invoice"],
        "data_table": data["data_table"],
        "total_without_tax": data["total_without_tax"],
        "amount_of_tax":  data["amount_of_tax"],
        "total_amount": data["total_amount"]
    }


@router_1.post("/items/{item_id}", status_code=201)
async def get_item(item: Item, item_id: int, query: Annotated[str | None, Query(max_length=50)] = None):
    # Query(max_length=50) - означает, что значение запроса не может превышать больше 50 символов.
    file_name: str = f'temp_{item_id}.json'
    logger.info("The filename is: %s", file_name)

    item_dict: dict = {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax
    }
    if item.tax is not None:
        full_price: float = item.price + item.tax
        item_dict.update({"full_price": full_price})
        logger.info("Updated price (full price) is: %s", item_dict["full_price"])
    if query:
        item_dict.update({"query": query})

    with open(file=f'uploaded_files/json_files/{file_name}', mode='w', encoding='utf-8') as file:
        json.dump(obj=item_dict, fp=file, indent=2, ensure_ascii=False)
    return item_dict
