import scrapy

class BookspiderSpider(scrapy.Spider):
    # name = "bookspider"
    allowed_domains = ["homedy.com"]
    start_urls = ['https://homedy.com/ban-can-ho-chung-cu']       

    def parse(self, response):
        books = response.css('div.product-item')

        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()
            book_url = 'https://homedy.com/'+ relative_url
            yield response.follow(book_url, callback = self.parse_book_page)
            
    def start_requests(self):
        for i in range(2, 200):
            next_page_url = 'https://homedy.com/ban-can-ho-chung-cu/p' + str(i)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
         
    def parse_book_page(self, response): 
            contact_url = ""
            cont_url = response.css('div.agent-inpage .info .extra-info a ::attr(href)').get()
            if cont_url is not None:
                 contact_url = 'https://homedy.com/' + cont_url
            square = response.xpath("//div[@class='option-bar']/div[1]/div[2]//strong//text()").getall()
            title =  response.css('div.content h1 ::text').get()
            date_post = response.xpath("//div[@class='product-info']/div[1]/p[2]/text()").get()
            price = response.xpath("//div[@class='option-bar']/div[1]/div[1]//text()").getall()
            new_price = ""
            for i in range (0, len(price)):
                new_price += price[i].replace("\n","")
            description = response.xpath("//div[@class='project-revew']/ul[@class='investor-constructor']/li[2]/p/span/text()").getall()
            new_des = ""
            if len(description) <= 1:
                description = response.css('div.description-content .description ::text').getall()
            for i in range (0, len(description)):
                    new_des += description[i].replace("\xa0"," ")
            home_detail = response.css("div.product-attributes .product-attributes--item span::text").getall()
            home_type =""
            direction = ""
            legal = ""
            num_bed = ""
            num_floor = ""
            home_furniture = ""
            for i in range(0, len(home_detail)-1):
                if 'Loại hình' in home_detail[i]:
                      home_type = home_detail[i+1]
                if 'Hướng nhà' in home_detail[i]:
                     direction = home_detail[i+1]
                if 'Tình trạng pháp lý' in home_detail[i]:
                    legal = home_detail[i+1]
                if 'Số phòng ngủ' in home_detail[i]:
                     num_bed = home_detail[i+1]
                if 'Số tầng' in home_detail[i]:
                     num_floor = home_detail[i+1]
                if 'Nội thất' in home_detail[i]:
                    home_furniture = home_detail[i+1]
            yield{
                    'title':title.replace("\n",""),
                    'date_post':date_post.replace(" ",""),
                    'exp_post': response.xpath("//div[@class='product-info']/div[2]/p[2]/text()").get(),
                    'url':  response.url,
                    'img_url_src':response.css('div.image-item a img::attr(data-src)').getall(),
                    'price':new_price,
                    'square':square[1] + square[2].replace("\n",""),
                    'address': response.css('div.address span ::text').getall(),
                    'contact_name': response.css('div.agent-inpage .info .flex-name h3 ::text').get(),
                    'contact_phone':response.css('div.agent-inpage .operation a.mobile-box').attrib['data-mobile'],
                    'contact_profile': contact_url,
                    'home_type': home_type,
                    'direction': direction,
                    'legal': legal,
                    'number_bed': num_bed,
                    'number_floor': num_floor,
                    'home_furniture': home_furniture,
                    'type_content': response.xpath("//div[@class='product-info']/div[3]/p[2]/text()").get(),
                    'home_type': response.css('div.project-revew ul.project-category li a ::text').get(),
                    'project': response.css('div.project-detail .info a ::text').get(),
                    'project_investor': response.xpath("//div[@class='project-revew']/ul[@class='investor-constructor']/li[1]/a/span/text()").get(),
                    'status': response.xpath("//div[@class='project-revew']/ul[@class='investor-constructor']/li[2]/p/span/text()").get(),
                    'description':new_des,

            }

        
       