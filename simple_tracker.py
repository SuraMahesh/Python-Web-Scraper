import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime
from amazon_config import(
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_cetificate_error,
    set_browser_as_incognito,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRETORY
)

class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_cetificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):    
        print("Starting script...")
        print(f"Looking for {self.search_term} products...")
        links = self.get_products_links()
        if not links:
            print("Stopped script")
            return
        print(f"Got {len(links)} links to products...")
        print("Getting into about produts...")
        products = self.get_products_info(links)
        print(f"Got info about {len(products)} products...")
        self.driver.quit()
        return products

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_id('//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        result_list = self.driver.find_elements_by_class_name('s-result-list')

        links = []
        try:
            results = result_list[0].find_elements_by_xpath(
                "//div[1]/div[2]/div/span[3]"
            )
            
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Didn't get any products...")
            print(e)
            return links    
       

    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
            return products

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]        

    def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - geting data...")
        product_short_url = self.shorten_url(asin)
        self.driver.get(f'{product_short_url}?Language=en_GB')
        time.sleep(2)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()

        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': product_short_url,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"can't get title of a product - {self.driver.current_url}")
            return None

    def get_seller(self):
        try:
            return self.driver.find_element_by_id('bylineInfo').text
        except Exception as e:
            print(e)
            print(f"Can't get seller of a product - {self.driver.current_url}")
            return None 

    def get_price(self):
        return '99$'                   

    def shorten_url(self, asin):
        return self.base_url + './dp/' + asin



    

    def get_asin(self, product_link):
         return product_link[product_link.find('./dp/') + 4:product_link.find('./ref')]

    




if __name__ == '__main__':
    print("YOOO!!!")
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    amazon.run()

