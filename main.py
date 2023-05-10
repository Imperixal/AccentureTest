from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test1():
    # Write a program in Python or Java that counts backwards from 100 to 1 and prints: “Agile” if the number is
    # divisible by 5, “Software” if the number is divisible by 3, “Testing” if the number is divisible by both,
    # or prints just the number if none of those cases are true.

    for i in range(100, 0, -1):
        if i % 3 == 0 and i % 5 == 0:
            print("Testing")
        elif i % 3 == 0:
            print("Software")
        elif i % 5 == 0:
            print("Agile")
        else:
            print(i)


class Product:
    def __init__(self, element):
        self.element = element
        self.name = self.get_name()
        self.price = self.get_price()

    def get_name(self):
        return self.element.find_element(By.XPATH, ".//*[contains(@class,'listing-item__headline')]").text

    def get_price(self):
        price_text = self.element.find_element(By.XPATH, ".//span[@class='price-current']").text
        return int(price_text.replace("Kč", "").replace(" ", ""))

    def add_to_cart(self):
        add_to_cart_button = self.element.find_element(By.XPATH, ".//button[@type = 'submit']")
        add_to_cart_button.click()


class ShopTest:
    def __init__(self):
        self.driver = self.create_driver()
        self.product_list = []

    def create_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-extensions")
        return webdriver.Chrome(options=chrome_options)

    def load_products(self):
        self.driver.get("https://www.gsm-market.cz/Mobily-tablety/Chytre-telefony/?f[skladem]=1")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Nejdražší')]"))).click()

        elements = self.driver.find_elements(By.XPATH, "//li[@class='listing-cell']")
        self.product_list = [Product(element) for element in elements]

    def get_most_expensive_products(self, n):
        return sorted(self.product_list, key=lambda p: p.price, reverse=True)[:n]

    def add_products_to_cart(self, products):
        for product in products:
            product.add_to_cart()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class,'js_zavritDialog')]"))).click()

    def validate_cart(self, products):
        self.driver.get("https://www.gsm-market.cz/Kosik")
        cart_items = self.driver.find_elements(By.XPATH, "//div[@id='kosik-tabulka']/div[@class='product']")

        items_in_cart = len(cart_items)
        assert items_in_cart == 2, f"Expected two items in the shopping cart, but got: {items_in_cart}"

        for i, (product, cart_item) in enumerate(zip(products, cart_items), start=1):
            cart_item_name = cart_item.find_element(By.XPATH, ".//*[@class='product-title']").text
            cart_item_price = cart_item.find_element(By.XPATH, ".//span[contains(@class,'js_kosCena')]").text
            cart_item_price = int(cart_item_price.replace("Kč", "").replace(" ", ""))

            print(f"Validating item {i}:")
            print(f"  - Product name: {product.name} == {cart_item_name}")
            print(f"  - Product price: {product.price} Kč == {cart_item_price} Kč")

            assert product.name == cart_item_name, f"Expected {product.name} == {cart_item_name}, but got {product.name} instead."
            assert product.price == cart_item_price, f"Expected {product.price} Kč == {cart_item_price} Kč, but got {product.price} Kč instead."

    def quit(self):
        self.driver.quit()

    def step_1_load_products(self):
        print("Step 1: Loading products...")
        self.load_products()

    def step_2_find_most_expensive_products(self):
        print("Step 2: Finding two most expensive products...")
        most_expensive_products = self.get_most_expensive_products(2)
        for i, product in enumerate(most_expensive_products, start=1):
            print(f"Product {i}: {product.name} - {product.price} Kč")
        return most_expensive_products

    def step_3_add_products_to_cart(self, products):
        print("Step 3: Adding products to the cart...")
        self.add_products_to_cart(products)

    def step_4_validate_cart(self, products):
        print("Step 4: Validating the shopping cart...")
        self.validate_cart(products)

    def run_test(self):
        try:
            self.step_1_load_products()
            most_expensive_products = self.step_2_find_most_expensive_products()
            self.step_3_add_products_to_cart(most_expensive_products)
            self.step_4_validate_cart(most_expensive_products)
            print("Test passed!")
        except AssertionError as e:
            print(f"Test failed! {e}")
        finally:

            self.quit()


if __name__ == "__main__":
    test1()
    test = ShopTest()
    test.run_test()
