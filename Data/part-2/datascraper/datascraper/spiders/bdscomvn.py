import scrapy
class BookspiderSpider(scrapy.Spider):
    # name = "bookspider"
    allowed_domains = ["bds.com.vn"]
    start_urls = ['https://bds.com.vn/mua-ban-can-ho-chung-cu-page2']

    def parse(self, response):
        books = response.css('div.item-nhadat')

        for book in books:
            book_url = book.css('div.clearfix a.image-item-nhadat ::attr(href)').get()
            yield response.follow(book_url, callback = self.parse_book_page)       
             
        next_page_url = 'https://bds.com.vn'+ response.css('a.next-page ::attr(href)').get()
        yield response.follow(next_page_url, callback = self.parse)
         
    def parse_book_page(self, response):

            description = response.css('div.ct-pr-sum::text').getall()
            y = len(description)
            new_des = ""
            for i in range (0, y):
                 new_des += description[i].replace("\n","").replace("\r","").replace("bb","").replace("  ","").replace("==","").replace("--","")
                 
            home_detail = response.css('ul.list-attr-hot li span ::text').getall()
            x = len(home_detail)          
            number_bedroom = 'null'
            number_floor =  'null'
            number_wc =  'null'
            square = ""
            price = ""
            date_post = ""
            for i in range (0,x-1):
                if 'Diện tích' in home_detail[i]:   
                    square = home_detail[i+1]
                if 'Giá' in home_detail[i]:
                    price = home_detail[i+1]
                if 'Ngày đăng' in home_detail[i]:
                     date_post =  home_detail[i+1]
                if 'Số phòng ngủ' in home_detail[i]:
                     number_bedroom = home_detail[i+1]
                if 'Số toilet' in home_detail[i]:
                     number_wc = home_detail [i + 1]
                if 'Tầng' in home_detail[i]:
                     number_floor = home_detail[i+1]
            
            info = response.css('div.col-item-info ::text').getall()
            yield{
                    'title': response.css('h1.title-product ::text').get(),
                    'price':price,
                    'date_post':date_post,
                    'square':square,
                                 
                    'address': response.css('div.product_base ul.breadcrumb li a ::text').getall(),
                    'number_floor':number_floor,
                    'number_bedroom':number_bedroom,
                    'number_wc': number_wc,
                    'contact_name': info [3],
                    'contact_phone': response.css('ul.list-attr-member li a ::attr(href)').getall(),
                    'img_url_src': response.css('div.fotorama img::attr(src)').getall(),
                    'url': response.url,       
                    'contact_profile':response.css('a.view-all-post ::attr(href)').get(),
                    
                    'description':new_des,
            }

        
       