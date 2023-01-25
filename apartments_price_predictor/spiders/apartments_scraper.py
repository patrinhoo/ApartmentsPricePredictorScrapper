import scrapy
from scrapy import signals
from scrapy_selenium import SeleniumRequest
import json


class BuildingScraperSpider(scrapy.Spider):
    name = 'apartments_scraper'

    def remove_characters(self, value):
        return value.strip(',. \n')

    def __init__(self):
        self.output_data = []

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def spider_closed(self, spider):
        with open('apartments.json', 'w', encoding='utf-8') as file:
            json.dump(self.output_data, file, ensure_ascii=False)

        spider.logger.info('Spider closed: %s' % spider.name)

    def start_requests(self):
        yield SeleniumRequest(
            url='https://gratka.pl/nieruchomosci/mieszkania?page=1',
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response):
        for plot in response.xpath("//div[@class='listing__content']/div/article"):

            link = plot.xpath("../a/@href").get()

            yield SeleniumRequest(
                url=link,
                wait_time=5,
                callback=self.parse_plot
            )

        next_page = response.xpath(
            "//a[@class='pagination__nextPage']/@href").get()

        if next_page:
            absolute_url = f"{next_page}"
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=5,
                callback=self.parse
            )

    def parse_plot(self, response):
        title = self.remove_characters(response.xpath(
            "//h1[@class='sticker__title']/text()").get())
        price = self.remove_characters(response.xpath(
            "//span[@class='priceInfo__value']/text()").get())
        price_m2 = self.remove_characters(response.xpath(
            "//span[@class='priceInfo__additional']/text()").get())

        attributes = response.xpath(
            "//ul[@class='parameters__singleParameters']/li")

        scraped_data = {
            "title": title,
            "price": price,
            "price/m2": price_m2
        }

        location = attributes[0].xpath(
            ".//b/a[@class='parameters__locationLink']")

        scraped_data['town'] = self.remove_characters(location.xpath("../text()").get())

        loc_list = ['district', 'voivodeship']

        for i, loc in enumerate(location):
            scraped_data[loc_list[i]] = loc.xpath(".//text()").get()

        for attribute in attributes[1:]:
            name = attribute.xpath(".//span/text()").get()
            value = attribute.xpath(
                ".//b[@class='parameters__value']/text()").get()

            if value:
                scraped_data[name] = value

        self.output_data.append(scraped_data)

        yield scraped_data
