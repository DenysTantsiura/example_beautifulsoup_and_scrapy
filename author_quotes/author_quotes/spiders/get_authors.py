# in cmd: scrapy crawl get_authors -o quotes.json # файли будуть завжди конкатуватись
# in cmd: scrapy crawl get_authors -O quotes.json # файли будуть завжди перезаписуватись
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


class GetAuthorsSpider(scrapy.Spider):
    name = "get_authors"
    # https://docs.scrapy.org/en/latest/topics/settings.html
    # custom_settings = {"FEED_URI": "../jsons_files/authors.json",} # custom_settings = {'SOME_SETTING': 'some value',}
    # https://docs.scrapy.org/en/2.4/topics/feed-exports.html
    # https://stackoverflow.com/questions/65112996/how-to-enable-overwriting-output-files-in-scrapy-settings-py
    custom_settings = {
                       "FEEDS": {
                                "../jsons_files/authors.json": {
                                                                "format": "json",
                                                                'encoding': 'utf8',
                                                                "overwrite": True,
                                                                }
                                }
                        }
    
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):  # async?
        # https://docs.scrapy.org/en/latest/topics/selectors.html
        links_to_about_author = response.xpath('//a[contains(@href, "author")]/@href').getall()  # a(href)
        # ! 1 by 1: /following-sibling::dd
        # links_to_about_author=response.xpath('//div[@class="quote"]/span/small[@class="author"]/following-sibling::a')
        # print(f'\n{links_to_about_author=}\n')
        for about_author_next_page in links_to_about_author:
            # https://docs.scrapy.org/en/latest/topics/request-response.html?highlight=follow#scrapy.http.TextResponse.follow
            # https://docs.scrapy.org/en/latest/intro/tutorial.html#response-follow-example
            yield response.follow(about_author_next_page, callback=self.parse_author)  # await?

        # if exist link to next page:
        if (next_link := response.xpath("//li[@class='next']/a/@href").get()):
            # https://docs.scrapy.org/en/2.4/topics/request-response.html?highlight=scrapy.Request#scrapy.http.Request
            yield scrapy.Request(self.start_urls[0][:-1]+next_link, callback=self.parse)

    # static?
    def parse_author(self, response):  # async?
        fullname = response.xpath(
            "/html//div[@class='author-details']/h3[@class='author-title']/text()").get().strip()
        born_date = response.xpath(
            "/html//div[@class='author-details']/p/span[@class='author-born-date']/text()").get().strip()
        born_location = response.xpath(
            "/html//div[@class='author-details']/p/span[@class='author-born-location']/text()").get().strip()
        description = response.xpath(
            "/html//div[@class='author-details']/div[@class='author-description']/text()").get().strip()
        yield {
            "fullname": fullname,
            "born_date": born_date,
            "born_location": born_location,
            "description": description,
            }

# scrapy crawl get_authors
