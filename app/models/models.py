from pydantic import BaseModel


class ParsedData(BaseModel):
    """
    Для обработки json-файлов
    """
    inn_kpp: str
    invoice: str
    data_table: list[list[str]]
    total_without_tax: str
    amount_of_tax: str
    total_amount: str

