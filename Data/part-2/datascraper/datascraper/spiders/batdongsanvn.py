import scrapy

class BookspiderSpider(scrapy.Spider):
    # name = "bookspider"
    allowed_domains = ["batdongsan.vn"]
    start_urls = ["https://batdongsan.vn/ban-can-ho-chung-cu"]

    def parse(self, response):
        books = response.css('div.datalist .item')

        for book in books:
            relative_url = book.css('div.item .body .name a ::attr(href)').get()
            if 'chu-dau-tu-cong-ty' not in relative_url:
                book_url = relative_url
                yield response.follow(book_url, callback = self.parse_book_page)
            
        next_page_url = response.xpath("//div[@class='wrapper']/ul[@class='uk-pagination']/li/a[@rel='next']/@href").get()
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
                'title': response.css('h1 span::text').get(),
                'date_post':response.css('span time ::text').get(),
                'direction': direction,
                'address': address,
                
                'price':price.replace("\t","").replace("\n",""),
                'square': square,
                'number_bedroom': num_bedroom,
                'number_wc': num_wc,
                'contact_name': response.xpath("//div[@class='item']/div[@class='header']/div[2]/a/text()").get(),
                'contact_phone':response.css('div.phone a::text').getall(),
                'url':  response.url,
                'img_url_src': response.css("div.wrapper .item .image a img::attr(src)").get(),
                'contact_email': response.css('div.email a::text').getall(),
                'contact_profile': response.xpath("//div[@class='item']/div[@class='header']/div[2]/a/@href").get(),
                'description':new_des,
            }

        
       