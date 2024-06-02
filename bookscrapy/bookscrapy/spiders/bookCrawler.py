import scrapy
from bookscrapy.items import BookscrapyItem


class BookcrawlerSpider(scrapy.Spider):
    name = "bookCrawler"
    allowed_domains = ["books.toscrape.com"]
    
    """
        Cào dữ liệu bình thường, lấy hết
    """    
    start_urls = ["https://books.toscrape.com/"]
    def parse(self, response):
        bookList = response.xpath('/html/body/div/div/div/div/section/div/descendant::ol/li/article/div/a/@href').getall()
        for book in bookList:
            item = BookscrapyItem()
            item['BookUrl'] = response.urljoin(book)
            request = scrapy.Request(url = response.urljoin(book), callback=self.parseCourseDetailPage)
            request.meta['datacourse'] = item
            yield request

        # nextButton = response.xpath('/html/body/div/div/div/div/section/div[2]/div/ul/li[last()]/a/@href').get()
        # if(nextButton != ''):
        #     yield scrapy.Request(url=response.urljoin(nextButton), callback=self.parse)
    
    """
        Cào dữ liệu theo danh mục, Default, Mystery
        Lấy link danh mục bằng cách lấy tên danh mục trước /index.html
        Vd: https://books.toscrape.com/catalogue/category/books/poetry_23/index.html
        Trước /index.html chính là tên của danh mục cần cào chính là "poetry_23", copy vào biến list_catal
    """
    # listCrawl = []
    # # Cào thể loại Poetry và Mystery
    # list_catal = ['poetry_23', 'mystery_3']
    # for catal in list_catal:
    #     page_url = "https://books.toscrape.com/catalogue/category/books/{}/".format(catal)
    #     listCrawl.append(page_url)

    # start_urls = listCrawl #["https://books.toscrape.com/catalogue/category/books/christian_43/index.html"]

    # def parse(self, response):
    #     bookList = response.xpath('/html/body/div/div/div/div/section/div/descendant::ol/li/article/div[1]/a/@href').getall()
    #     for book in bookList:
    #         item = BookscrapyItem()
    #         item['BookUrl'] = response.urljoin(book)
    #         request = scrapy.Request(url = response.urljoin(book), callback=self.parseCourseDetailPage)
    #         request.meta['datacourse'] = item
    #         yield request

    #     nextButton = response.xpath('/html/body/div/div/div/div/section/div[2]/div/ul/li[last()]/a/@href').get()
    #     if(nextButton != ''):
    #         yield scrapy.Request(url=response.urljoin(nextButton), callback=self.parse)
    
    """
        Cào dữ liệu theo trang yêu cầu, từ trang a đến trang b
    """
    # listCrawl = []
    # page_start = 2
    # page_end = 4

    # listpage = range(page_start, page_end+1)
    # for page in listpage:
    #     page_url = "https://books.toscrape.com/catalogue/page-{}.html".format(page)
    #     listCrawl.append(page_url)
    # start_urls = listCrawl

    # def parse(self, response):
    #     bookList = response.xpath('/html/body/div/div/div/div/section/div/descendant::ol/li/article/div/a/@href').getall()
    #     for book in bookList:
    #         item = BookscrapyItem()
    #         item['BookUrl'] = response.urljoin(book)
    #         request = scrapy.Request(url = response.urljoin(book), callback=self.parseCourseDetailPage)
    #         request.meta['datacourse'] = item
    #         yield request

    
    
    def parseCourseDetailPage(self, response):
        item = response.meta['datacourse']        
        item['product_main'] = response.xpath('normalize-space(string(//div[@class="col-sm-6 product_main"]/h1))').get()
        item['price'] = response.xpath('normalize-space(translate(string(//div[@class="col-sm-6 product_main"]/p[@class="price_color"]), "£", ""))').get()
        item['in_stock'] = response.xpath('substring-before(substring-after(normalize-space(string(//th[text()="Availability"]/following-sibling::td)), "("), ")")').get()
        item['star'] = response.xpath("substring-after(//div[contains(@class, 'product_main')]/p[contains(@class, 'star-rating')]/@class, 'star-rating ')").extract_first()
        item['upc'] = response.xpath('normalize-space(string(//th[text()="UPC"]/following-sibling::td))').get()
        item['product_type'] = response.xpath('normalize-space(string(//th[text()="Product Type"]/following-sibling::td))').get()
        item['price_exc'] = response.xpath('normalize-space(translate(substring-after(//th[text()="Price (excl. tax)"]/following-sibling::td, "£"), ",", ""))').get()
        item['price_inc'] = response.xpath('normalize-space(translate(substring-after(//th[text()="Price (incl. tax)"]/following-sibling::td, "£"), ",", ""))').get()
        item['tax'] = response.xpath('normalize-space(translate(substring-after(//th[text()="Tax"]/following-sibling::td, "£"), ",", ""))').get()
        item['availability'] = response.xpath('translate(substring-before(substring-after(normalize-space(string(//th[text()="Availability"]/following-sibling::td)), "("), ")"), "available", "")').get().strip()
        item['nor'] = response.xpath('normalize-space(string(//th[text()="Number of reviews"]/following-sibling::td))').get()
        item["type_of_book"] = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()  
        item['description'] = response.xpath('normalize-space(string(//article[@class="product_page"]/p))').get()
        yield item
        
    
    
