from scrapy import Spider, Request
from zappos.items import ZapposItem
import re

class ZapposSpider(Spider):
	name = 'zappos_spider'
	allowed_urls = ['https://www.zappos.com/']
	start_urls = ['https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=recentSalesStyle/desc/']

	def parse(self):
		# Find the total number of pages in the result so that we can decide how many urls to scrape next
		# Sample 500 out of 9451 shoes, 100 items per page
		total = 500
		num_per_page = 100
		number_pages = total // num_per_page
		#List comprehension to construct all the urls
		result_urls = ['https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=recentSalesStyle/desc/'] + ['https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=recentSalesStyle/desc/&p={}'.format(x) for x in range(1,number_pages + 1)]
		# Yield the requests to different search result urls, 
		# using parse_result_page function to parse the response.
		for url in result_urls:
			yield Request(url = url, callback = self.parse_result_page)

	def parse_result_page(self, response):
		# This function parses the search result page.
		# We are looking for url of the detail page.
		detail_urls = response.xpath('//article[@class="XFukpz5aok _3mcJv9m1io _2wq5jaQJ4m _2qMtPUUyGP _3HwbzyixvG searchThreeWideMobile"]/a/@href').extract()
		print(len(detail_urls))
		print("-"*50)

		# Yield the requests to the details pages, 
    	# using parse_detail_page function to parse the response.
    	for url in detail_urls:
    		yield Request(url = 'https://www.zappos.com/' + url, callback = self.parse_detail_page)

    def parse_detail_page(self,response):
    	# This function parses the product detail page.
    	# The link to the first page of reviews.
		first_review_page = response.xpath('//div[@class="meuM26H58j"]/div/a/@href').extract()
		price = response.xpath('//div[@class="_2J1pzjWwbD"]/span/text()').extract_first()[1:]
		price = float(price)
		brand = response.xpath('//div[@class="_28vMLCnTJ3"]/span/h1/span/a/span/text()').extract_first()
		product = response.xpath('//div[@class="_28vMLCnTJ3"]/span/h1/span[@class="_3geE2f9xsy"]/text()').extract_first()
		yield Request(url = 'https://www.zappos.com/' + first_review_page, meta = {'brand': brand, 'product': product, 'price': price}, callback = self.parse_review_page)

	def parse_review_page(self,response):

		brand = response.meta['brand']
		product = response.meta['product']
		price = response.meta['price']
		print(brand,product,price)
		print('='*50)
		true_to_size = response.xpath('//p[./span/text() ="Felt true to size"]/span/text()').extract_first()
		true_to_width = response.xpath('//p[./span/text()="Felt true to width"]/span/text()').extract_first()
		arch_support = response.xpath('//p[./span/text()="Moderate arch support"]/span/text()').extract_first()
	
		reviews = response.xpath('//div[@class="_2F8k1pmMQO"]/div[@class="_3Yhmk9BHrO"]')
		print(len(reviews))

		for review in reviews:
			#overall_rating = review.xpath('//div[@class="_2KyNqn_amI"]/em[@class="_3RifWHN9Zx"]/text() = "Overall" and /span[@class="_1KtF6mB36O _3nOXU_cIFA _3FmiLq-lF9"]/span[@class="_31sBtRAS6y"]/text()').extract()
			overall_rating = review.xpath('//div[@class="_2KyNqn_amI" and ./em/text() = "Overall"]/span[@class="_1KtF6mB36O _3nOXU_cIFA _3FmiLq-lF9"]/span[@class="_31sBtRAS6y"]/text()').extract()
			comfort_rating = review.xpath('//div[@class="_2KyNqn_amI" and ./em/text() = "Comfort"]/span[@class="_1KtF6mB36O _3nOXU_cIFA _3FmiLq-lF9"]/span[@class="_31sBtRAS6y"]/text()').extract()
			style_rating = review.xpath('//div[@class="_2KyNqn_amI" and ./em/text() = "Style"]/span[@class="_1KtF6mB36O _3nOXU_cIFA _3FmiLq-lF9"]/span[@class="_31sBtRAS6y"]/text()').extract
			size_rating = review.xpath('//div[@class="_23Bkht6KtK" and ./div/span/text() = "Runs Small"]/div/div/span/@class')
			s = [size_rating[x:y] for x,y in zip(range(0,120,5),range(5,125,5))]
			indices=[]
			for lis in s:
				for ind,elem in enumerate(lis):
					if elem = '_3111JQbBDo _35OWMRRaIz':
						indices.append(ind)

			