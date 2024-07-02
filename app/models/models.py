from pydantic import BaseModel


class ParsedData(BaseModel):
    inn_kpp: str
    invoice: str
    data_table: list[list[str]]
    total_without_tax: str
    amount_of_tax: str
    total_amount: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

