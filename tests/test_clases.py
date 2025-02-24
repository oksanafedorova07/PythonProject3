import sys
import unittest
from io import StringIO
from unittest.mock import patch

import pytest

from src.clases import BaseProduct, Category, LawnGrass, Product, Smartphone


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Тестовый товар", "Описание", 100.0, 10)

    def test_product_initialization(self):
        self.assertEqual(self.product.name, "Тестовый товар")
        self.assertEqual(self.product.description, "Описание")
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.quantity, 10)

    def test_price_setter(self):
        self.product.price = 150.0
        self.assertEqual(self.product.price, 150.0)

    def test_price_setter_invalid_value(self):
        with self.assertRaises(ValueError):
            self.product.price = -10.0

    @patch("builtins.input", return_value="y")  # Мок для input, возвращающий 'y'
    def test_price_setter_decrease_confirmation(self, mock_input):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.product.price = 50.0  # Уменьшаем цену
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        print(output)  # Для отладки: выводим захваченный вывод
        self.assertIn("Цена снижается. Подтвердите действие (y/n):", output)
        self.assertEqual(self.product.price, 50.0)

    def test_add_products(self):
        product2 = Product("Тестовый товар 2", "Описание", 200.0, 5)
        total_value = self.product + product2
        self.assertEqual(total_value, 100.0 * 10 + 200.0 * 5)

    def test_add_products_different_classes(self):
        smartphone = Smartphone(
            "Смартфон", "Описание", 500.0, 5, "Высокая", "Модель", 64, "Черный"
        )
        with self.assertRaises(TypeError):
            total_value = self.product + smartphone


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.product1 = Product("Товар 1", "Описание", 100.0, 10)
        self.product2 = Product("Товар 2", "Описание", 200.0, 5)
        self.category = Category(
            "Категория", "Описание", [self.product1, self.product2]
        )

    def test_category_initialization(self):
        self.assertEqual(self.category.name, "Категория")
        self.assertEqual(self.category.description, "Описание")
        self.assertEqual(len(self.category.get_products()), 2)

    def test_add_product(self):
        product3 = Product("Товар 3", "Описание", 300.0, 3)
        self.category.add_product(product3)
        self.assertEqual(len(self.category.get_products()), 3)

    def test_add_product_zero_quantity(self):
        with self.assertRaises(ValueError) as context:
            product4 = Product("Товар 4", "Описание", 400.0, 0)
        self.assertEqual(
            str(context.exception), "Товар с нулевым количеством не может быть добавлен"
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Категория, количество продуктов: 15 шт.")

    def test_category_iteration(self):
        products = [product for product in self.category]
        self.assertEqual(len(products), 2)

    def test_average_price(self):
        self.assertEqual(self.category.average_price(), (100.0 * 10 + 200.0 * 5) / 15)

    def test_average_price_no_products(self):
        empty_category = Category("Пустая категория", "Описание")
        self.assertEqual(empty_category.average_price(), 0)


class TestSmartphone(unittest.TestCase):
    def setUp(self):
        self.smartphone = Smartphone(
            "Смартфон", "Описание", 500.0, 5, "Высокая", "Модель", 64, "Черный"
        )

    def test_smartphone_initialization(self):
        self.assertEqual(self.smartphone.name, "Смартфон")
        self.assertEqual(self.smartphone.price, 500.0)
        self.assertEqual(self.smartphone.quantity, 5)
        self.assertEqual(self.smartphone.model, "Модель")
        self.assertEqual(self.smartphone.color, "Черный")

    def test_smartphone_str(self):
        self.assertEqual(
            str(self.smartphone),
            "Смартфон, 500.0 руб. Остаток: 5 шт. (Модель: Модель, Цвет: Черный)",
        )


class TestLawnGrass(unittest.TestCase):
    def setUp(self):
        self.lawn_grass = LawnGrass(
            "Трава газонная", "Описание", 50.0, 20, "Россия", "2 недели", "Зеленый"
        )

    def test_lawn_grass_initialization(self):
        self.assertEqual(self.lawn_grass.name, "Трава газонная")
        self.assertEqual(self.lawn_grass.price, 50.0)
        self.assertEqual(self.lawn_grass.quantity, 20)
        self.assertEqual(self.lawn_grass.country, "Россия")
        self.assertEqual(self.lawn_grass.color, "Зеленый")

    def test_lawn_grass_str(self):
        self.assertEqual(
            str(self.lawn_grass),
            "Трава газонная, 50.0 руб. Остаток: 20 шт. (Страна: Россия, Цвет: Зеленый)",
        )


if __name__ == "__main__":
    unittest.main()
