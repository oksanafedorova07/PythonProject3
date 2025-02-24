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
        super().__init__(name, description, price, quantity)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")

        if hasattr(self, "_price") and value < self._price:
            confirmation = input("Цена снижается. Подтвердите действие (y/n): ")
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
        self.__products.append(product)
        Category.total_products += 1

    def __str__(self):
        return f"{self.name}, количество продуктов: {sum(p.quantity for p in self.__products)} шт."

    def get_products(self) -> list[Product]:
        """
        Возвращает список товаров в категории.
        """
        return self.__products

    @property
    def products(self) -> str:
        """
        Геттер для получения списка товаров в виде строки.
        """
        return "\n".join(str(product) for product in self.__products)

    def __iter__(self):
        """
        Возвращает итератор для товаров категории.
        """
        return CategoryIterator(self)


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
