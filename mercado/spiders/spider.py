# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from mercado.items import MercadoItem

class MercadoSpider(CrawlSpider):
	name = 'mercado'
	item_count = 0
	allowed_domain = ['www.mercadolibre.com.ve']
	start_urls = ['https://listado.mercadolibre.com.ve/trajes-de-bano/_DisplayType_LF_GENDER_female']

	rules = {
		# Para cada item
		Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="pagination__next"]/a'))),
		Rule(LinkExtractor(allow =(), restrict_xpaths = ('//h2[contains(@class,"item__title")]/a')),
							callback = 'parse_item', follow = False)
	}

	def parse_item(self, response):
		ml_item = MercadoItem()
		#info de producto
		ml_item['titulo'] = response.xpath('normalize-space(//h1/text())').extract_first()
		ml_item['precio'] = response.xpath('normalize-space(//span[@class="price-tag-fraction"]/text())').extract()
		ml_item['condicion'] = response.xpath('normalize-space(//div[@class="item-conditions"]/text())').extract()
		ml_item['ventas_producto'] = response.xpath('normalize-space(//div[@class="item-conditions"]/text())').extract()
		ml_item['envio'] = response.xpath('normalize-space(//p[contains(@class, "shipping-method-title")]/text())').extract()
		ml_item['ubicacion'] = response.xpath('normalize-space(//p[@class="custom-address"]/strong/text())').extract()
		ml_item['opiniones'] = response.xpath('normalize-space(//span[@class="review-summary-average"]/text())').extract()
		#imagenes del producto
		# ml_item['image_urls'] = response.xpath('//figure[contains(@class, "gallery-image-container")]/a/img/@src').extract()
		# ml_item['image_name'] = response.xpath('normalize-space(//h1[@class="item-title__primary "]/text())').extract_first()
		#info de la tienda o vendedor
		ml_item['vendedor_url'] = response.xpath('/html/body/main/div/div/div[1]/div[2]/div[1]/section[2]/a/@href').extract()
		ml_item['tipo_vendedor'] = response.xpath('normalize-space(//div[contains(@class, "seller-status")]/p/text())').extract()
		ml_item['reputacion_vendedor'] = response.xpath('normalize-space(//dd[contains(@class, "reputation-relevant")]/strong/text())').extract()
		ml_item['experiencia_vendedor'] = response.xpath('normalize-space(//strong[contains(@class, "history-data")]/text())').extract()
		ml_item['ventas_vendedor'] = response.xpath('normalize-space(//dd[contains(@class, "reputation-relevant")]/strong/text())').extract()
		self.item_count += 1
		if self.item_count > 30:
			raise CloseSpider('item_exceeded')
		yield ml_item
