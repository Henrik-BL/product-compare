# Example 1
# https://www.prisjakt.nu/produkt.php?p=5883921
# Lite Bulb Moments Smart Light Chain Globe Cone 50L (10m)
# competitor LifestyleStore.se


# Data provided by our customer
from src.model.product import Product

# This is given to us from our customer
from src.product_compare import ProductCompare

base_product = Product()
base_product.title = "Smart Light Chain - Globe Cone"
base_product.ean = "5714948300317"
base_product.model_number = "NSL911994"
base_product.brand = "Lite Bulb Moments"

base_product.add_attribute("Livslängd", "30 000 timmar")
base_product.add_attribute("Spänning", "5V")


compare_product_url = "https://www.lifestylestore.se/lite-bulb-moments/lite-bulb-moments-smart-light-chain-globe-cone/"
product_compare = ProductCompare(base_product, compare_product_url)
result = product_compare.run()

compare_product_url = "https://www.iphonebutiken.se/lite-bulb-moments-smart-light-chain-oval-globe-39070.html?utm_campaign=feed&utm_medium=feed&utm_source=Prisjakt"
product_compare = ProductCompare(base_product, compare_product_url)
result = product_compare.run()

compare_product_url = "https://cdon.se/hem-tradgard/lite-bulb-moments-smart-party-light-chain-c9-p102124163"
product_compare = ProductCompare(base_product, compare_product_url)
result = product_compare.run()

compare_product_url = "https://www.computersalg.se/i/8409579/led-ljuskedja-med-50-led-lampor-10-3meter-1-st?utm_source=prisjaktSe&utm_medium=prisjaktSeLINK&utm_campaign=prisjaktSe"
product_compare = ProductCompare(base_product, compare_product_url)
result = product_compare.run()