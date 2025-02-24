from abc import ABC, abstractmethod


class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price  # Защищенный атрибут вместо приватного
        self.quantity = quantity

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, value):
        pass


class LoggingMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(
            f"Создан объект класса {self.__class__.__name__} с параметрами: {args}, {kwargs}"
        )


class Product(LoggingMixin, BaseProduct):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name, description, price, quantity)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")

        if hasattr(self, "_price") and value < self._price:
            print("Цена снижается. Подтвердите действие (y/n):")  # Убедитесь, что это сообщение выводится
            confirmation = input()
            if confirmation.lower() != "y":
                return

        self._price = value

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Можно складывать только товары одного класса.")
        return self.price * self.quantity + other.price * other.quantity


class Category:
    total_categories = 0
    total_products = 0

    def __init__(self, name: str, description: str, products: list[Product] = None):
        self.name = name
        self.description = description
        self.__products = products or []
        Category.total_categories += 1
        Category.total_products += len(self.__products)

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product")
        if product.quantity == 0:
            raise ZeroQuantityError()
        self.__products.append(product)
        Category.total_products += 1
        print(f"Товар {product.name} успешно добавлен.")
        print("Обработка добавления товара завершена.")

    def __str__(self):
        return f"{self.name}, количество продуктов: {sum(p.quantity for p in self.__products)} шт."

    def get_products(self) -> list[Product]:
        return self.__products

    @property
    def products(self) -> str:
        return "\n".join(str(product) for product in self.__products)

    def __iter__(self):
        return CategoryIterator(self)

    def average_price(self) -> float:
        try:
            total_price = sum(
                product.price * product.quantity for product in self.__products
            )
            total_quantity = sum(product.quantity for product in self.__products)
            return total_price / total_quantity
        except ZeroDivisionError:
            return 0


class CategoryIterator:
    def __init__(self, category):
        """
        Конструктор итератора.
        """
        self.category = category
        self.index = 0

    def __iter__(self):
        """
        Возвращает сам объект как итератор.
        """
        return self

    def __next__(self):
        """
        Возвращает следующий товар в категории.
        """
        if self.index < len(self.category.get_products()):
            product = self.category.get_products()[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: int,
        color: str,
    ):
        """
        Конструктор класса Smartphone.
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        """
        Строковое представление смартфона.
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт. (Модель: {self.model}, Цвет: {self.color})"


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        """
        Конструктор класса LawnGrass.
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        """
        Строковое представление травы газонной.
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт. (Страна: {self.country}, Цвет: {self.color})"


class ZeroQuantityError(Exception):
    """Исключение для товаров с нулевым количеством."""

    def __init__(self, message="Товар с нулевым количеством не может быть добавлен"):
        super().__init__(message)
