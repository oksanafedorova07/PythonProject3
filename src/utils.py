import json
import os

from src.clases import Category, Product

# Получаем абсолютный путь к файлу
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_FILE_PATH = os.path.join(BASE_DIR, "data", "products.json")


def load_data_from_json(file_path: str) -> list[Category]:
    """
    Загружает данные из JSON-файла и создает объекты классов Category и Product.
    """
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    # Чтение JSON-файла
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Список для хранения объектов Category
    categories = []

    # Проходим по данным и создаем объекты
    for category_data in data:
        # Создаем список товаров для категории
        products = []
        for product_data in category_data["products"]:
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            products.append(product)

        # Создаем объект Category
        category = Category(
            name=category_data["name"],
            description=category_data["description"],
            products=products,
        )
        categories.append(category)

    return categories
