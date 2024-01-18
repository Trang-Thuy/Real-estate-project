import scrapy

class BookspiderSpider(scrapy.Spider):
    # name = "bookspider"
    allowed_domains = ["bds123.vn"]
    start_urls = ["https://bds123.vn/ban-can-ho-chung-cu.html"]

    def parse(self, response):
        books = response.css('li.item a::attr(href)').getall()

        for book in books:
            book_url = 'https://bds123.vn' + book
            yield response.follow(book_url, callback = self.parse_book_page)
            
        next_page_url = response.xpath("//ul[@class='pagination']/li[@class='page-item']/a[@rel='next']/@href").get()
        yield response.follow(next_page_url, callback = self.parse)

    def parse_book_page(self, response):
            price = response.css('div.item div.meta strong.price ::text').get()
            description = response.xpath("//div[@class='item']/div[@class='body']/div[@class='content']/p/text()").getall()
            new_des = ""
            direction= ""
            num_bedroom=""
            num_wc= ""
            address= ""
            square=""
            x = len(description)
            for i in range(0,x):
                 new_des += description[i].replace("\r\n","")
            home_property = response.xpath("//div[@class='item']/div[@class='body']/div[2]/ul//text()").getall()
            y = len(home_property)
            for i in range (0,y-1):
                if 'Diện tích:' in home_property[i]:   
                    square = home_property[i+1]
                if 'Hướng nhà:' in home_property[i]:
                     direction =  home_property[i+1]
                if 'Phòng ngủ:' in home_property[i]:
                     num_bedroom= home_property[i+1]
                if 'Phòng WC:' in home_property[i]:
                     num_wc = home_property[i+1]
                if 'Địa chỉ:' in home_property[i]:
                    address = home_property[i+1]
            yield{
                'title': response.css('h1.page-h1 ::text').get(),
                'date_post':response.css('span time ::text').get(),
                'direction': direction,
                'address': response.css("div.the-post p.post-address span::text").get(),
                'url':  response.url,
                'price':price.replace("\t","").replace("\n",""),
                'square': square,
                'number_bedroom': num_bedroom,
                'number_wc': num_wc,
                'contact_name': response.xpath("//div[@class='item']/div[@class='header']/div[2]/a/text()").get(),
                'contact_phone':response.css('div.phone a::text').getall(),
                'contact_email': response.css('div.email a::text').getall(),
                'contact_profile': response.xpath("//div[@class='item']/div[@class='header']/div[2]/a/@href").get(),
                'description':new_des,
            }

        
       