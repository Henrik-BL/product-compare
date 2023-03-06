from src.model.product import Product


class ProductMatchResult:

    def __init__(self, base_product: Product, compare_url, title_match, ean_match, model_number_match, brand_match,
                 attribute_match_count):
        self.base_product = base_product
        self.compare_url = compare_url
        self.title_match = title_match
        self.ean_match = ean_match
        self.model_number_match = model_number_match
        self.brand_match = brand_match
        self.attribute_match_count = attribute_match_count

    def to_json(self):
        attribute_list = []
        for att in self.base_product.attributes:
            attribute_list.append(att.to_json())

        json = {
            "product": {
                "title": self.base_product.title,
                "ean": self.base_product.ean,
                "model_number": self.base_product.model_number,
                "brand": self.base_product.brand,
                "attributes": attribute_list
            },
            "compare_url": self.compare_url,
            "title_match": self.title_match,
            "ean_match": self.ean_match,
            "model_number_match": self.model_number_match,
            "brand_match": self.brand_match,
            "attributes_count": len(self.base_product.attributes),
            "attributes_match": self.attribute_match_count
        }
        return json
