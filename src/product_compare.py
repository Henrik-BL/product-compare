import json
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from src.globals import BROWSER_HEADERS
from src.model.product import Product
from src.model.product_match_result import ProductMatchResult


class ProductCompare:

    def __init__(self, base_product: Product, compare_product_url: str):
        self.search_chars_margin = 5
        self.attribute_length = self.get_attribute_length(base_product) + self.search_chars_margin
        self.brand_ex_list = ["Märke"]
        self.base_product = base_product
        self.compare_product_url = compare_product_url
        self._verify_url(compare_product_url)

    @staticmethod
    def _verify_url(url_string):
        try:
            result = urlparse(url_string)
            if all([result.scheme, result.netloc]):
                return True
            else:
                raise ValueError("Invalid URL: {}".format(url_string))
        except ValueError:
            raise ValueError("Invalid URL: {}".format(url_string))

    @staticmethod
    def get_attribute_length(product: Product):
        longest = 0
        for attribute in product.attributes:
            current_length = len(attribute.value)
            if current_length > longest:
                longest = current_length
        margin = 5
        longest += margin
        return longest

    def _get_web_page_content(self):
        try:
            response = requests.get(self.compare_product_url, headers=BROWSER_HEADERS, timeout=5)
            stripped_text = self._remove_html_tags(response.content)
            return stripped_text
        except Exception:
            print("Could not reach: {}".format(self.compare_product_url))
        return ""

    @staticmethod
    def _remove_html_tags(text):
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = soup.get_text(separator=" ")
        return stripped_text

    @staticmethod
    def get_simplified_string(input_string):
        simplified_string = input_string.lower()
        simplified_string = simplified_string.replace('\n', '')
        simplified_string = simplified_string.replace('\r', '')
        simplified_string = simplified_string.replace(' ', '')
        return simplified_string

    def _get_following_chars(self, full_string: str, sub_string: str, chars_after: int):
        full_string = self.get_simplified_string(full_string)
        sub_string = self.get_simplified_string(sub_string)
        _list = []
        result = full_string.split(sub_string)
        result.pop(0)
        for item in result:
            _list.append(item[:chars_after])
        return _list

    def _if_string_contains(self, full_string: str, sub_string: str):
        result = False
        full_string_lower = self.get_simplified_string(full_string)
        sub_string_lower = self.get_simplified_string(sub_string)
        amount_of_times = full_string_lower.count(sub_string_lower)
        if amount_of_times > 0:
            result = True
        return result

    def _match_title(self, web_page_content):
        product_title = self.base_product.title
        return self._if_string_contains(web_page_content, product_title)

    def _match_ean(self, web_page_content):
        product_ean = self.base_product.ean
        return self._if_string_contains(web_page_content, product_ean)

    def _match_model_number(self, web_page_content):
        product_brand = self.base_product.model_number
        return self._if_string_contains(web_page_content, product_brand)

    def _match_brand(self, web_page_content):
        product_brand_simplified = self.get_simplified_string(self.base_product.brand)
        chars_range = len(product_brand_simplified) + self.search_chars_margin
        result = False

        for brand_ex in self.brand_ex_list:
            result_list = self._get_following_chars(web_page_content, brand_ex, chars_range)
            for item in result_list:
                if product_brand_simplified in item:
                    result = True
                    break
        return result

    def _match_attributes(self, web_page_content):
        attribute_match_count = 0
        for attribute in self.base_product.attributes:
            result_list = self._get_following_chars(web_page_content, attribute.key, self.attribute_length)
            for item in result_list:
                if self.get_simplified_string(attribute.value) in item:
                    attribute_match_count += 1
                    break
        return attribute_match_count

    def run(self):
        web_page_content = self._get_web_page_content()
        title_match = self._match_title(web_page_content)
        ean_match = self._match_ean(web_page_content)
        model_number_match = self._match_model_number(web_page_content)
        brand_match = self._match_brand(web_page_content)
        attribute_match_count = self._match_attributes(web_page_content)
        result = ProductMatchResult(self.base_product, self.compare_product_url, title_match, ean_match,
                                    model_number_match, brand_match, attribute_match_count)
        json_result = result.to_json()
        json_formatted_str = json.dumps(json_result, indent=2, ensure_ascii=False)
        print(json_formatted_str)

