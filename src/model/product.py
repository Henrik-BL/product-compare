from src.model.product_attribute import ProductAttribute


class Product:

    def __init__(self, title=None, ean=None, model_number=None, brand=None, attributes=[]):
        self.title = title
        self.ean = ean
        self.model_number = model_number
        self.brand = brand
        self.attributes = attributes

    def add_attribute(self, key: str, value: str):
        self.attributes.append(ProductAttribute(key, value))