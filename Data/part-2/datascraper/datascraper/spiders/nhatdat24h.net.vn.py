import scrapy 
from scrapy import Spider
class BookspiderSpider(Spider):   
    # name = "bookspider"
    allowed_domains = ["nhadat24h.net.vn"]
    start_urls = ['https://nhadat24h.net.vn/danh-muc/can-ho-chung-cu/52']

    def parse(self, response):
        books = response.css('div.item .ct-title a::attr(href)').getall()

        for book in books:
            if book:
                book_url = book    
                yield response.follow(book_url, callback=self.parse_book_page)

        next_page_url = response.css("ul.pagination li.page-item a[rel='next']::attr(href)").get()
        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)
    def parse_book_page(self, response):
          
            description = response.css('table.table-bordered tr p::text').getall()
            z = len(description)
            new_des = ""
            for i in range(0, z):
                new_des += description[i].replace("  ","").replace("--","")

            home_detail = response.css('div.thong-tin-chi-tiet ::text').getall()
            x = len(home_detail)
            square = ""
            type_content = ""
            home_type = ""
            price = ""
            address = ""
            for i in range (0, x-1):
                if 'DTSD' in home_detail[i]:
                    square = home_detail[i+1]
                if 'Danh mục' in home_detail[i]:
                    type_content = home_detail[i +1]
                if 'Loại BDS' in home_detail[i]:
                    home_type = home_detail[i+1]
                if 'Giá:' in home_detail[i]:
                    price = home_detail[i+1]
                if 'Địa chỉ cụ thể' in home_detail[i]:
                    address = home_detail[i+1]

            table = response.css('table.table-bordered tr ::text').getall() 
            y = len(table)
            width = ""
            height = ""
            legal = ""
            num_bed ="" 
            num_floor =""
            num_living =""
            num_wc = ""
            direction ="" 
            kitchen = ""
            roof_top = ""
            gara = ""
            homefront ="" 
            contact_phone ="" 
            contact_name = ""
            for i in range (0, y-1):
                if 'Chiều rộng' in table[i]:
                    width = table[i+1]
                if 'Chiều dài' in table[i]:
                    height = table[i+1]
                if 'Giấy tờ' in table[i]:
                    legal = table[i+1]
                if 'Số tầng' in table[i]:
                    num_floor = table[i+1]
                if 'Hướng' in table[i]:
                    direction = table[i+1]
                if 'Phòng ngủ' in table[i]:
                    num_bed = table[i+1]
                if 'Phòng khách:' in table[i]:
                    num_living = table[i+1]
                if 'Phòng bếp' in table[i]:
                    kitchen = table[i+1]
                if 'Sân thượng' in table[i]:
                    roof_top = table[i+1]
                if 'Chỗ để xe hơi:' in table[i]:
                    gara = table[i+1]
                if 'Phòng tắm/vệ sinh' in table[i]:
                    num_wc = table[i+1]
                if 'Đường trước nhà' in table[i]:
                    homefront = table[i+1]
                if 'Điện thoại' in table[i]:
                    contact_phone = table[i+4]
                if 'Người liên hệ' in table[i]:
                    contact_name = table[i +3]
            yield{
                    'title': response.css("h1.h1title ::text").get(),
                    
                    'price':price.replace("\n","").replace("  ",""),
                    'square':square,
                    'address':address.replace("\n","").replace("  ",""),
                    'type_content': type_content,
                    'width': width,
                    'height': height,
                    'legal': legal,
                    'home_type': home_type,
                    'direction': direction.replace("\n","").replace("  ",""),
                    'number_bedroom': num_bed,
                    'number_floor': num_floor,
                    'kitchen': kitchen,
                    'number_wc': num_wc,
                    'number_living': num_living,
                    'gara': gara,
                    'homefront':  homefront,
                    'roof_top': roof_top,
                    'contact_name': contact_name,           
                    'contact_phone': contact_phone,
                    'img_url_src':response.css('div.slide_main a img ::attr(src)').getall(),
                    'url':  response.url,
                    # 'contact_profile':contact_profile,
                    'description':new_des.replace("\n","").replace('\xa0',' ').replace("  ",""),
            }

        
          
       