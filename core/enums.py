from enum import Enum


class BookStatus(Enum):
    IN_STOCK ='в наличии'
    OUT_OF_STOCK = "нет в наличии"