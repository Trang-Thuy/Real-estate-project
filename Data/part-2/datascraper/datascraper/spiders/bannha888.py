import scrapy

class BookspiderSpider(scrapy.Spider):
    # name = "bookspider"
    allowed_domains = ["bannha888.com"]
    start_urls = ['https://bannha888.com/ban-can-ho-chung-cu/']

    def parse(self, response):
        books = response.css('div.box_tin_bds')
        for book in books:
            book_url = book.css('ul h3 a ::attr(href)').get()
            book_img = book.css('li a img::attr(src)').get()
            img_url_src = ''
            if 'bannha888' in book_img:
                img_url_src = book_img
            yield response.follow(book_url, callback = self.parse_book_page, meta={'img_url_src': img_url_src})
        
        page_url = response.url
        if 'page=6' not in page_url:  
            next_page = response.css('div.nums ul li a.stay ::attr(href)').getall()
            if next_page is not None:
                x = len(next_page)
                next_page_url = next_page[x-2]
                yield response.follow(next_page_url, callback = self.parse)
  
    def parse_book_page(self, response):
            home_detail = response.css("div.noidung_ct_bds_id ul h4 span ::text").getall()
            x = len(home_detail)
                  
            phone1 = response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[4]/td[2]/span/@v").get() 
            if phone1 is None:
                phone1 = ""
            else:
                phone1 = response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[4]/td[2]/span/@k").get() + response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[4]/td[2]/span/@v").get()
                 
            phone2 = response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[5]/td[2]/span/@v").get() 
            if phone2 is None:
                phone2 = ""
            else:
                phone2 = response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[5]/td[2]/span/@k").get() + response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[5]/td[2]/span/@v").get()
            
            info = response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[2]/td[2]/text()").getall()
            address = response.css('div.noidung_ct_bds_id ul p ::text').getall()
            description = response.css('div.showText ::text').getall()
            x = len(description)
            new_des = ""
            for i in range (0,x):
                 new_des += description[i].replace("  ","").replace("\n","").replace("\r","")
            
            yield{
                    'title': response.css('ul h3 ::text').get(),
                    'date_post':response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[4]/td[2]/text()").get(),
                    'exp_post':response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[5]/td[2]/text()").get(),
                    
                    
                    'price':home_detail[0],
                    'square':home_detail[1],
                    'address': address[1].replace("  ",""),
                    'contact_name': info[1],           
                    'contact_phone': phone1 + " " + phone2,
                    'direction': response.xpath("//div[@class='thongtin_lienhe']/table/tbody/tr[6]/td[2]/text()").get(),
                    'url':  response.url,
                    'img_url_src': response.meta['img_url_src'], 
                    'description': new_des,
            }

        
       