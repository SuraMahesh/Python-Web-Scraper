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
        pass

if __name__ == '__main__':
    print("YOOO!!!")