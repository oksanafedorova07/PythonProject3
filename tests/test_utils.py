import os

import pytest

from src.utils import load_data_from_json

# Получаем абсолютный путь к файлу
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_FILE_PATH = os.path.join(BASE_DIR, "data", "products.json")


# Фикстура для загрузки данных из JSON-файла
@pytest.fixture
def loaded_categories():
    return load_data_from_json(JSON_FILE_PATH)


# Проверка загрузки данных из файла
def test_load_data_from_json(loaded_categories):
    """
    Проверяем, что функция возвращает список объектов Category.
    """
    assert isinstance(loaded_categories, list)
    assert len(loaded_categories) == 2  # В файле 2 категории


#  Проверка атрибутов категорий
def test_category_attributes(loaded_categories):
    """
    Проверяем названия и описания категорий.
    """
    # Проверяем первую категорию (Смартфоны)
    assert loaded_categories[0].name == "Смартфоны"
    assert (
        loaded_categories[0].description
        == "Смартфоны, как средство не только коммуникации, но и получение дополнительных функций для удобства жизни"
    )

    # Проверяем вторую категорию (Телевизоры)
    assert loaded_categories[1].name == "Телевизоры"
    assert (
        loaded_categories[1].description
        == "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником"
    )


# Проверка атрибутов товаров
def test_product_attributes(loaded_categories):
    """
    Проверяем атрибуты товаров.
    """
    # Проверяем товары в первой категории (Смартфоны)
    products = loaded_categories[0].get_products()
    assert len(products) == 3  # В категории 3 товара

    # Проверяем первый товар (Samsung Galaxy C23 Ultra)
    assert products[0].name == "Samsung Galaxy C23 Ultra"
    assert products[0].description == "256GB, Серый цвет, 200MP камера"
    assert products[0].price == 180000.0
    assert products[0].quantity == 5

    # Проверяем второй товар (Iphone 15)
    assert products[1].name == "Iphone 15"
    assert products[1].description == "512GB, Gray space"
    assert products[1].price == 210000.0
    assert products[1].quantity == 8

    # Проверяем третий товар (Xiaomi Redmi Note 11)
    assert products[2].name == "Xiaomi Redmi Note 11"
    assert products[2].description == "1024GB, Синий"
    assert products[2].price == 31000.0
    assert products[2].quantity == 14

    # Проверяем товары во второй категории (Телевизоры)
    products = loaded_categories[1].get_products()
    assert len(products) == 1  # В категории 1 товар

    # Проверяем товар (55" QLED 4K)
    assert products[0].name == '55" QLED 4K'
    assert products[0].description == "Фоновая подсветка"
    assert products[0].price == 123000.0
    assert products[0].quantity == 7


# Проверка обработки ошибок (файл не найден)
def test_file_not_found():
    """
    Проверяем, что функция выбрасывает исключение, если файл не найден.
    """
    with pytest.raises(FileNotFoundError):
        load_data_from_json("non_existent_file.json")
