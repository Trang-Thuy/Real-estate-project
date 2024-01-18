import scrapy

class BookspiderSpider(scrapy.Spider):
#     name = "bookspider"
    allowed_domains = ["batdongsan.so"]
    start_urls = ['https://batdongsan.so/nha-dat-ban/can-ho-chung-cu#/']

    def parse(self, response):
        books = response.css('div.module-content article.float-re')

        for book in books:
            book_url = book.css('h3 a ::attr(href)').get()
            yield response.follow(book_url, callback = self.parse_book_page)     
        next_page_url = response.xpath("//div[@class='nav-pagination']/ul[@class='pagination']/li/a[@rel='next']/@href").get()
        yield response.follow(next_page_url, callback = self.parse)
         
    def parse_book_page(self, response):
            square = response.xpath("//div[@class='re-content']/p[2]/span/text()").getall()
            if square is None:
                 square = response.xpath("//div[@class='re-block']/ul[@class='re-property']/li//text()").getall()
            
            contact_name = response.xpath("//div[@class='re-block']/div[@class='re-contact-info']/div[@class='info']/a/text()").get()
            home_property = response.xpath("//div[@class='re-block']/ul[@class='re-property']/li//text()").getall()
            x = len(home_property)
            price = response.css('div.re-tab .re-district-price .re-price ::text').getall()
            y = len(price)
            if y == 3:
                 price = price[1] + price[2]
            else:
                 price = price[0]
            address = response.css('div.re-block .re-address ::text').getall()
            square=""
            contact_phone = response.xpath("//div[@class='re-block']/div[@class='re-contact-info']/div[@class='info']/div//home-post-phone/@phone").get()
            direction= ""
            num_floor = ""
            num_bedroom = ""
            num_wc = ""
            homefront = ""
            for i in range (0,x):
                if 'Diện tích:' in home_property[i]:   
                    square = home_property[i]
                if 'Hướng:' in home_property[i]:
                    direction = home_property[i]
                if 'Số tầng:' in home_property[i]:
                     num_floor =  home_property[i]
                if 'Số phòng ngủ:' in home_property[i]:
                     num_bedroom= home_property[i]
                if 'Số toilet:' in home_property[i]:
                     num_wc = home_property[i]
                if 'Mặt tiền:' in home_property[i]:
                     homefront = home_property[i]                     
            description = response.css('div.re-block .re-content ::text').getall()
            z = len(description)
            new_descript = ""
            for i in range(0,z):
                 new_descript += description[i].replace("\n","").replace("  ","").replace("\r","")
            yield{
                    'title': response.css('h1.re-title ::text').get(),
                    'date_post':response.css('div.col-md-12 ul.list2 li span.sp3 ::text').get(),
                    #'exp_post': response.xpath("//div[@class='product-info']/div[2]/p[2]/text()").get(),
                    'url':  response.url,
                    'img_url': response.css('div.item a img ::attr(src)').getall(),
                    'price':price,
                    'square':square,
                    'address': address[1].replace("\n","").replace("  ",""),
                    'direction': direction.replace("  ","").replace("\n",""),
                    'homefront': homefront.replace("  ","").replace("\n",""),
                    'number_floor': num_floor.replace("  ","").replace("\n","").replace("Số tầng: ",""),
                    'contact_name': contact_name.replace("  ","").replace("\n",""),
                    'contact_phone': contact_phone.replace(" ",""),
                    'contact_profile':response.xpath("//div[@class='re-block']/div[@class='re-contact-info']/div[@class='info']/a/@href").get(),
                    'number_bedroom': num_bedroom.replace("  ","").replace("\n","").replace("Số phòng ngủ: ",""),
                    'number_wc': num_wc.replace("  ","").replace("\n","").replace("Số toilet: ",""),    
                    'description':new_descript, 
            }

       