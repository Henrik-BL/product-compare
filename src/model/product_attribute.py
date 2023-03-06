
class ProductAttribute:

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def to_json(self):
        return {
            "key": self.key,
            "value": self.value
        }