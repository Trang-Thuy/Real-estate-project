# import scrapy

# class BookspiderSpider(scrapy.Spider):
#     # name = "bookspider"
#     allowed_domains = ["alonhadat.com.vn"]
#     start_urls = ["https://alonhadat.com.vn/nha-dat/can-ban/can-ho-chung-cu.html"]

#     def parse(self, response):
#         books = response.css('div.content-item')

#         for book in books:
#             relative_url = book.css('div.ct_title a ::attr(href)').get()
#             if relative_url is not None:
#                 book_url = 'https://alonhadat.com.vn' + relative_url
#                 yield response.follow(book_url, callback = self.parse_book_page)
            
#         next_page = response.xpath("//div[@class='page']/a[2]/@href").get()
#         # if next_page is not None:
#         #     if 'catalogue/' in next_page:
#         if next_page is not None:
#             next_page_url = 'https://alonhadat.com.vn' + next_page
#         #     else:
#         #         next_page_url = 'https://alonhadat.com.vn' + next_page

#             yield response.follow(next_page_url, callback = self.parse)

#     def parse_book_page(self, response):
#             table_rows = response.css("table tr")
#             date_post = response.css('div.title span ::text').get()
#             description = response.css('div.detail ::text').get()
#             contact_url = response.css('div.contact-info .view-more a ::attr(href)').get()
#             if contact_url is not None:
#                  contact_url = 'https://alonhadat.com.vn' + response.css('div.contact-info .view-more a ::attr(href)').get()
#             # contact_rate = ""
#             # star_rate = response.css('div.contact-info span.rate').attrib['style']
#             # if star_rate is not None:
#             #      contact_rate = star_rate
#             yield{
              
#                 'title': response.css('h1 ::text').get(),
#                 'date_post': date_post.replace("Hôm nay","15/11/2023").replace("Hôm qua","14/11/2023"),
                
#                 'url':  response.url,
#                 'price': response.css('div.moreinfor span.price span.value ::text').get(),
#                 'square': response.css('div.moreinfor span.square span.value ::text').get(),
#                 'address': response.css('div.address span.value ::text').get(),
#                 'contact_name': response.css('div.contact-info div.name ::text').get(),
#                 'contact_phone': response.css('div.contact-info div.fone a::text').getall(),
#                 # 'contact_star_rate': contact_rate,
#                 'contact_profile': response.css('div.contact-info .view-more a ::attr(href)').get(),
#                 'direction': table_rows[0].xpath("td[4]/text()").get(),
#                 'dining': table_rows[0].xpath("td[6]/text()").get(),
#                 'type_content': table_rows[1].xpath("td[2]/text()").get(),
#                 'homefront': table_rows[1].xpath("td[4]/text()").get(),
#                 'kitchen': table_rows[1].xpath("td[6]/text()").get(),
#                 'home_type':table_rows[2].xpath("td[2]/text()").get(),
#                 'legal':  table_rows[2].xpath("td[4]/text()").get(),
#                 'roof_top': table_rows[2].xpath("td[6]/text()").get(),
#                 'width': table_rows[3].xpath("td[2]/text()").get(),
#                 'number_floor': table_rows[3].xpath("td[4]/text()").get(),
#                 'gara': table_rows[3].xpath("td[6]/text()").get(),
#                 'height': table_rows[4].xpath("td[2]/text()").get(),
#                 'number_bedroom': table_rows[4].xpath("td[4]/text()").get(),
#                 'owner': table_rows[4].xpath("td[6]/text()").get(),
#                 'description': description.replace("\r\n",""),

#                 #book_item['title': response.css('.product_main h1 ::text').get(),
#                 # book_item['product_type':table_rows[1].css("td ::text").get(),
#                 # book_item['price_excl_tax'] = table_rows[2].css("td ::text").get(),
#                 # book_item['price_incl_tax'] =table_rows[3].css("td ::text").get(),
#                 # book_item['tax'] =table_rows[4].css("td ::text").get(),
#                 # book_item['stars'] =response.css("p.star-rating").attrib['class'],
#                 # book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling ::li[1]/a/text()").get(),
#                 # #book_item['description'] =response.xpath("//div[@id='content_inner']/article/p/text()").get(),
#                 #book_item['price'] = response.css('p.price_color ::text').get(),
#             }
                
 
       