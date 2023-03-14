# in cmd: scrapy crawl get_quotes -o quotes.json # файли будуть завжди конкатуватись
# in cmd: scrapy crawl get_quotes -O quotes.json # файли будуть завжди перезаписуватись
"""
ModuleNotFoundError: No module named '_lzma'

Hi, I came across this issue after installing python from source.
It seems that I installed python without liblzma-dev.
After installing liblzma-dev and installing python again, the import error was gone.
+
In Ubuntu 20.04, I had to install lzma lzma-dev and liblzma-dev
reinstall python 3....
"""
import scrapy


class GetQuotesSpider(scrapy.Spider):
    name = "get_quotes"
    # https://docs.scrapy.org/en/latest/topics/settings.html
    # custom_settings = {"FEED_URI": "../jsons_files/quotes.json",}  # custom_settings = {'SOME_SETTING': 'some value',}
    # https://docs.scrapy.org/en/2.4/topics/feed-exports.html
    # https://stackoverflow.com/questions/65112996/how-to-enable-overwriting-output-files-in-scrapy-settings-py
    custom_settings = {
                       "FEEDS": {
                                "../jsons_files/quotes.json": {
                                                                "format": "json",
                                                                'encoding': 'utf8',
                                                                "overwrite": True,
                                                                }
                                }
                        }
    
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):  # async?
        for quote in response.xpath("/html//div[@class='quote']"):  # .css(...)  ...=from .select
            yield {  # .get = new methods result in a more concise and readable code  .strip()
                "quote": quote.xpath("span[@class='text']/text()").get().strip(),
                # .extract = old methods (list)[0] it's only example
                "author": quote.xpath("span/small/text()").extract()[0].strip(),
                # отримати тільки текст з тегів= додати /text():
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
            }
        # if exist link to next page:
        if (next_link := response.xpath("//li[@class='next']/a/@href").get()):
            # https://docs.scrapy.org/en/2.4/topics/request-response.html?highlight=scrapy.Request#scrapy.http.Request
            # If the URL is invalid, a ValueError exception is raised. try-except? !!!:
            yield scrapy.Request(self.start_urls[0][:-1] + next_link)

# scrapy crawl get_quotes -O ../jsons_files/quotes.json
# scrapy crawl get_quotes
