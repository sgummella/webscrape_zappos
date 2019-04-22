from scrapy import Spider, Request
from zappos.items import ZapposItem
import re

class ZapposSpider(Spider):
	name = 'zappos_spider'
	allowed_urls = ['https://www.zappos.com/']
	start_urls = ['https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=recentSalesStyle/desc/']

	def parse(self,response):
		# Find the total number of pages in the result so that we can decide how many urls to scrape next
		# Sample 500 out of 9451 shoes, 100 items per page
		total = 200
		num_per_page = 100
		number_pages = total // num_per_page
		#List comprehension to construct all the urls
		result_urls = ['https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=recentSalesStyle%2Fdesc%2F'] + ['https://www.zappos.com/men-sneakers-athletic-shoes/CK_XARC81wHAAQLiAgMBAhg.zso?s=recentSalesStyle%2Fdesc%2F&p={}'.format(x) for x in range(1,number_pages)]
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
			yield Request(url='https://www.zappos.com/' + url, callback = self.parse_detail_page)


	def parse_detail_page(self,response):
		# This function parses the product detail page.
		# The link to the first page of reviews.
		first_review_page = response.xpath('//div[@class="meuM26H58j"]/div/a/@href').extract_first()
		reviews_per_page = 25
		total_reviews = response.xpath('//div[@class="meuM26H58j"]/div/a/span/span[@class="GXj9Grji93"]/span/text()').extract_first()
		if ("," in total_reviews) and (total_reviews != None):
			total_reviews = int(total_reviews.replace(",",""))
		else:
			total_reviews = int(total_reviews)

		review_pages = total_reviews//reviews_per_page
		all_review_pages = [first_review_page + '/page/{}'.format(x) for x in range(1,review_pages+1)]
		Price = response.xpath('//div[@class="_2J1pzjWwbD"]/span/text()').extract_first()[1:]
		Price = float(Price)
		Brand = response.xpath('//div[@class="_28vMLCnTJ3"]/span/h1/span/a/span/text()').extract_first()
		Product = response.xpath('//div[@class="_28vMLCnTJ3"]/span/h1/span[@class="_3geE2f9xsy"]/text()').extract_first()
		for page in all_review_pages:
			yield Request(url = 'https://www.zappos.com/' + page, meta = {'Brand': Brand, 'Product': Product, 'Price': Price}, callback = self.parse_review_page)

			
		
		
	def parse_review_page(self,response):

		Brand = response.meta['Brand']
		Product = response.meta['Product']
		Price = response.meta['Price']
		print(Brand,Product,Price)
		print('='*50)
		True_size_feeling = response.xpath('//p[./span/text() ="Felt true to size"]/span/text()').extract_first()
		True_width_feeling = response.xpath('//p[./span/text()="Felt true to width"]/span/text()').extract_first()
		Arch_support = response.xpath('//p[./span/text()="Moderate arch support"]/span/text()').extract_first()
		reviews = response.xpath('//div[@class="_2F8k1pmMQO"]/div[@class="_3Yhmk9BHrO"]')
		print(len(reviews))
		# words = ['Runs Small', 'Runs Large', 'Runs Narrow', 'Runs Wide' 'Poor Support', 'Great Support']
		
		for index, review in enumerate(reviews):
		# for i in range(len(reviews)):
			Overall_rating = review.xpath('//div[@class="_2KyNqn_amI" and ./em/text() = "Overall"]/span[@class="_1KtF6mB36O _3nOXU_cIFA _3FmiLq-lF9"]/span[@class="_31sBtRAS6y"]/text()').extract()[index]
			Comfort_rating = review.xpath('//div[@class="_2KyNqn_amI" and ./em/text() = "Comfort"]/span[@class="_1KtF6mB36O _3nOXU_cIFA _3FmiLq-lF9"]/span[@class="_31sBtRAS6y"]/text()').extract()[index]
			Style_rating = review.xpath('//div[@class="_2KyNqn_amI" and ./em/text() = "Style"]/span[@class="_1KtF6mB36O _3nOXU_cIFA _3FmiLq-lF9"]/span[@class="_31sBtRAS6y"]/text()').extract()[index]

			# Overall_rating = response.xpath('//div[@class="_2F8k1pmMQO"]/div[' + str(i) + ']/div/div[2]/div[1]/div[3]/div[1]/span[2]/span/text()').extract_first() 
			# Comfort_rating = response.xpath('//div[@class="_2F8k1pmMQO"]/div[' + str(i) + ']/div/div[2]/div[1]/div[3]/div[2]/span[2]/span/text()').extract_first()
			# Style_rating = response.xpath('//div[@class="_2F8k1pmMQO"]/div[' + str(i) + ']/div/div[2]/div[1]/div[3]/div[3]/span[2]/span/text()').extract_first()
			Review_text = response.xpath('//div[@class="_2F8k1pmMQO"]/div[' + str(index) +']/div/div[2]/div[1]/div[7]/div[@class="vK9cxHN6fc _1YfU3jRKIN"]/div/text()').extract_first()
			if isinstance(Review_text,str) and Review_text != None:
				Review_text = Review_text.strip()
			else:
				pass
			
			# Width_rating=-5
			# Size_rating=-5
			# Arch_rating=-5
			# for j in range(3):
			# 	# pattern = response.xpath('//div[@class="_2F8k1pmMQO"]/div[' + str(i) + ']/div/div[2]/div[1]/div[6]/div/div[' + str(j) + ']/div/span/text()').extract() 
			# 	# pattern2 = response.xpath('//div[@class="_2F8k1pmMQO"]/div[' + str(i) + ']/div/div[2]/div[1]/div[6]/div/div[' + str(j) + ']/div[2]/div[2]/span/@class').extract()
			# 	try:	
			# 		pattern = response.xpath('//div[@class="_2F8k1pmMQO"]/div[' + str(i) + ']/div/div[2]/div[1]/div[6]/div/div[' + str(j) + ']/div/span/text()').extract() 
			# 		pattern2 = response.xpath('//div[@class="_2F8k1pmMQO"]/div[' + str(i) + ']/div/div[2]/div[1]/div[6]/div/div[' + str(j) + ']/div[2]/div[2]/span/@class').extract()
			# 		rating = pattern2.index('_3111JQbBDo _35OWMRRaIz') - 2
			# 	except:
			# 		rating = -5
			# 	if pattern == words[:2]:
			# 		Size_rating = rating
			# 	elif pattern == words[2:4]:
			# 		Width_rating = rating
			# 	elif pattern == words[4:]:
			# 		Arch_rating = rating


			# sr = review.xpath('//div[@class="_23Bkht6KtK" and ./div/span/text() = "Runs Small"]/div/div/span/@class').extract()
			# wr = review.xpath('//div[@class="_23Bkht6KtK" and ./div/span/text() = "Runs Narrow"]/div/div/span/@class').extract()
			# ar = review.xpath('//div[@class="_23Bkht6KtK" and ./div/span/text() = "Poor Support"]/div/div/span/@class').extract()
			# #pattern = review.xpath('//div[@class = "_23Bkht6KtK"]/div[@class="_1tSt0LVc5l"]/span/text()') 
			# #= "Runs Small"
			# #if review.xpath('//div[@class="_23Bkht6KtK"]/div[@class="_1tSt0LVc5l"]/span/text()').extract_first() is None:
			# #	ratings[]
			# s = [sr[x:y] for x,y in zip(range(0,121,5),range(5,126,5))]
			# w = [wr[x:y] for x,y in zip(range(0,121,5),range(5,126,5))]
			# a = [ar[x:y] for x,y in zip(range(0,121,5),range(5,126,5))]
			# sr_indices=[]
			# for ind,lis in enumerate(s):
			# 	if len(lis) == 0:
			# 		sr_indices.append(None)
			# 		continue	 
			# 	for ind_,elem in enumerate(lis):
			# 		if elem == '_3111JQbBDo _35OWMRRaIz':
			# 			sr_indices.append(ind_)
			# wr_indices=[]
			# for ind,lis in enumerate(w):
			# 	if len(lis) == 0:
			# 		wr_indices.append(None)
			# 		continue
			# 	for ind_,elem in enumerate(lis):
			# 		if elem == '_3111JQbBDo _35OWMRRaIz':
			# 			wr_indices.append(ind_)
			# ar_indices=[]
			# for ind,lis in enumerate(a):
			# 	if len(lis) == 0:
			# 		ar_indices.append(None)
			# 		continue
			# 	for ind_,elem in enumerate(lis):
			# 		if elem == '_3111JQbBDo _35OWMRRaIz':
			# 			ar_indices.append(ind_)
			# for i in range(len(reviews)):
			# 	if sr_indices[i] == None:
			# 		continue
			# 	else:
			# 	sr_indices[i] = sr_indices[i] - 2

		item = ZapposItem()
		item['Brand'] = Brand
		item['Product'] = Product
		item['Price'] = Price
		item['True_size_feeling'] = True_size_feeling
		item['True_width_feeling'] = True_width_feeling
		item['Arch_support'] = Arch_support
		item['Comfort_rating'] = Comfort_rating
		item['Style_rating'] = Style_rating
		item['Overall_rating'] = Overall_rating
		# item['Size_rating'] = Size_rating
		# item['Width_rating'] = Width_rating
		# item['Arch_rating'] = Arch_rating
		item['Review_text'] = Review_text
		yield item


