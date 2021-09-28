import scrapy
from scrapy_dangdang.items import ScrapyDangdangItem

class DangSpider(scrapy.Spider):
    name = 'dang'
    # 如果是多页下载的话，那么必须要调整的是allowed_domains的范围 一般情况下只写域名
    allowed_domains = ['category.dangdang.com']
    start_urls = ['http://category.dangdang.com/cp01.01.02.00.00.00.html']

    base_url = 'https://category.dangdang.com/pg'
    page = 1

    def parse(self, response):
        # src = //ul[@id="component_59"]/li//img/@src
        # alt = //ul[@id="component_59"]/li//img/@alt
        # price = //ul[@id="component_59"]/li//p[@class="price"]/span[1]/text()
        # 所有的selector的对象都可以再次调用xpath方法
        li_list = response.xpath('//ul[@id="component_59"]/li')

        for li in li_list:
            src = li.xpath('.//img/@data-original').extract_first()

            if src:
                src=  src
            else:
                src = li.xpath('.//img/@src').extract_first()

            name = li.xpath('.//img/@alt').extract_first()
            price = li.xpath('.//p[@class="price"]/span[1]/text()').extract_first()

            book = ScrapyDangdangItem(src = src,name=name,price=price)

            # 获取一个book就将book交给pipelines
            yield book
        if self.page < 100:
            self.page = self.page + 1
            url = self.base_url + str(self.page) + '-cp01.01.02.00.00.00.html'
        # 怎么去调用parse方法？
        # scrapy.Request就是scrapy的get请求
        #     url就是请求地址
        #     callback就是你要执行的那个函数，注意不要加括号
            yield scrapy.Request(url = url,callback=self.parse)
        # 每一页的爬取业务逻辑全都是一样的，所以我们只需要将执行的那个页的请求再次调用parse方法就可以了
