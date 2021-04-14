import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import PpromericaItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class PpromericaSpider(scrapy.Spider):
	name = 'promerica'
	start_urls = ['https://www.promerica.fi.cr/quienes-somos/noticias-promerica/']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = "Date is not published"
		title = response.xpath('//h2/text()').get()
		content = response.xpath('(//div[@class="col-xs-12"])[last()]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=PpromericaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
