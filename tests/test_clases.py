import sys
import unittest
from io import StringIO
from unittest.mock import patch

import pytest

from src.clases import BaseProduct, Category, LawnGrass, Product, Smartphone


class TestBaseProduct(unittest.TestCase):
    def test_abstract_methods(self):
        with self.assertRaises(TypeError):
            BaseProduct("Test", "Desc", 10.0, 5)


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Test Product", "Test Description", 100.0, 10)

    def test_initialization(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "Test Description")
        self.assertEqual(self.product.price, 100.0)
        self.assertEqual(self.product.quantity, 10)

    def test_price_setter_negative_value(self):
        with self.assertRaises(ValueError):
            self.product.price = -50

    @patch("builtins.input", return_value="y")
    def test_price_decrease_confirmation_yes(self, mock_input):
        self.product.price = 90
        self.assertEqual(self.product.price, 90)

    @patch("builtins.input", return_value="n")
    def test_price_decrease_confirmation_no(self, mock_input):
        self.product.price = 90
        self.assertEqual(self.product.price, 100)

    def test_str_representation(self):
        expected_str = "Test Product, 100.0 руб. Остаток: 10 шт."
        self.assertEqual(str(self.product), expected_str)

    def test_add_method_same_type(self):
        product2 = Product("Test 2", "Desc", 200.0, 5)
        total = self.product + product2
        self.assertEqual(total, 100 * 10 + 200 * 5)

    def test_add_method_different_type(self):
        class OtherProduct(Product):
            pass

        product2 = OtherProduct("Test 2", "Desc", 200.0, 5)
        with self.assertRaises(TypeError):
            self.product + product2


class TestCategory(unittest.TestCase):
    def setUp(self):
        Category.total_categories = 0
        Category.total_products = 0
        self.product = Product("Test", "Desc", 100.0, 5)
        self.category = Category("Test Category", "Test Description", [self.product])

    def test_initialization(self):
        self.assertEqual(Category.total_categories, 1)
        self.assertEqual(Category.total_products, 1)

    def test_add_product(self):
        new_product = Product("New", "Desc", 50.0, 3)
        self.category.add_product(new_product)
        self.assertEqual(Category.total_products, 2)

    def test_add_invalid_product(self):
        with self.assertRaises(TypeError):
            self.category.add_product("Invalid product")

    def test_str_representation(self):
        self.assertEqual(
            str(self.category), "Test Category, количество продуктов: 5 шт."
        )

    def test_products_property(self):
        expected_str = "Test, 100.0 руб. Остаток: 5 шт."
        self.assertEqual(self.category.products, expected_str)

    def test_iterator(self):
        products = list(self.category)
        self.assertEqual(len(products), 1)
        self.assertIsInstance(products[0], Product)


class TestSmartphone(unittest.TestCase):
    def setUp(self):
        self.smartphone = Smartphone(
            "iPhone", "Smartphone", 1000.0, 5, "High", "13 Pro", 256, "Black"
        )

    def test_initialization(self):
        self.assertEqual(self.smartphone.model, "13 Pro")
        self.assertEqual(self.smartphone.memory, 256)

    def test_str_representation(self):
        expected_str = (
            "iPhone, 1000.0 руб. Остаток: 5 шт. (Модель: 13 Pro, Цвет: Black)"
        )
        self.assertEqual(str(self.smartphone), expected_str)


class TestLawnGrass(unittest.TestCase):
    def setUp(self):
        self.lawn_grass = LawnGrass(
            "Grass", "Lawn", 50.0, 20, "USA", "2 weeks", "Green"
        )

    def test_initialization(self):
        self.assertEqual(self.lawn_grass.country, "USA")
        self.assertEqual(self.lawn_grass.germination_period, "2 weeks")

    def test_str_representation(self):
        expected_str = "Grass, 50.0 руб. Остаток: 20 шт. (Страна: USA, Цвет: Green)"
        self.assertEqual(str(self.lawn_grass), expected_str)


class TestLoggingMixin(unittest.TestCase):
    def test_logging_on_init(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            product = Product("Test", "Desc", 100.0, 5)
            self.assertIn(
                "Создан объект класса Product с параметрами: ('Test', 'Desc', 100.0, 5), {}",
                fake_out.getvalue(),
            )


if __name__ == "__main__":
    unittest.main()
