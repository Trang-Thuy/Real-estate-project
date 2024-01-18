import scrapy 
from scrapy import Spider
class BookspiderSpider(Spider):
    # name = 'bookspider'
    allowed_domains = ["nhadat24h.net"]
    start_urls = [
        'https://nhadat24h.net/ban-can-ho-chung-cu',]

    def parse(self, response):
        books = response.css('div.dv-item a.a-title ::attr(href)').getall()
        
        for book in books:
            book_url = 'https://nhadat24h.net'+ book
            yield response.follow(book_url, callback = self.parse_book_page)
                   
        next_page_url = 'https://nhadat24h.net'+ response.xpath("//div[@class='dv-pt-ttcm']/div/ul/li[@class='active']/following-sibling ::li[1]/a/@href").get()
        yield response.follow(next_page_url, callback = self.parse)
         
    def parse_book_page(self, response):
            home_detail = response.xpath("//div[@class='dv-time-dt']/p[1]//text()").getall()
            pro_url = response.css('div.detailUserName .info label.fullname a ::attr(href)').get()
            if pro_url is not None:
                contact_profile = 'https://nhadat24h.net' + response.css('div.detailUserName .info label.fullname a ::attr(href)').get()
            else:
                contact_profile = ''
            y = len(home_detail)
            price = ""
            square = ""
            for j in range(0, y-1): 
                if 'Cần bán' in home_detail[j]:
                    price = home_detail[j+1] + home_detail[j+2].replace(" -","")
                    square = home_detail[j+3] + home_detail[j+4]

            table = response.css('div.dv-tsbds .dv-tb-tsbds table tr ::text').getall()
            x = len(table)
            num_wc  = ""
            num_floor = ""
            num_bed = ""
            direction = ""
            gara = ""
            homefront = ""
            for i in range (0, x-1):
                if 'Số tầng' in table[i] and 'Hướng' not in table[i+1]:
                    if '\n' not in table[i]:
                        num_floor = table[i+1]
                    if '\n' in table[i]:
                        num_floor = table[i+2]
                if 'Hướng' in table[i] and 'Đường vào' not in table[i+1]:
                    if '\n' not in table[i]: 
                        direction = table[i+1]
                    if '\n' in table[i]:
                        direction = table[i+2]
                if 'Phòng Ngủ' in table[i]:
                    if '\n' not in table[i]:
                        num_bed = table[i+1]
                    if '\n' in table[i]:
                        num_bed = table[i+2]
                if 'Phòng WC' in table[i] and 'Số tầng' not in table[i+1]:
                    if '\n' not in table[i]:
                        num_wc = table[i+1]
                    if '\n' in table[i]:
                        num_wc = table[i+2]
                if 'Chỗ để xe' in table[i] and 'Mã BĐS'not in table[i+1]:
                    if '\n' not in table[i]:
                        gara = table[i+1]
                    if '\n' in table[i]:
                        gara = table[i+2]
                # if 'Đường vào' in table[i] and 'Mặt tiền' not in table[i+1]:
                #     homefront = table[i+1]
                if 'Mặt tiền' in table[i] and 'Chỗ để xe' not in table[i+1] :
                    homefront = table[i+1]
            
            date_post = response.xpath("//input[@id='txtNgaydang']/@value").get()
            address = response.xpath("//div[@class='dv-time-dt']/p[4]//text()").getall()
            add = ""
            z = len (address)
            for i in range(0, z):
                add += address[i].replace("\n","")
            
            home_type = response.xpath("//div[@class='dv-time-dt']/p[3]//text()").getall()
            new_type = ""
            for i in range (0, len(home_type)):
                new_type += home_type[i].replace("\n","") 
            
            new_name = ""
            contact_name = response.css('div.detailUserName div.info ::text').getall()
            for i in range(0, len(contact_name)):
                new_name += contact_name[i].replace("\n","")+ " "

            new_phone = ""
            contact_phone = response.css('div.dv-pt-item .panelActionContent a.call ::text').getall()
            for i in range(0, len(contact_phone)):
                new_phone += contact_phone[i].replace("\n","")+ " "
            
            new_description = ""
            description = response.css('div.detailmaincontent p ::text').getall()
            z = len(description)
            for i in range(0, len(description)):
                if 'Xem thêm :' not in description[i]:
                    new_description += description[i]
                else:
                    break
            img = response.css('div.myPanelClass ul li a img ::attr(data-src)').getall()
            for i in range(0, len(img)):
                img[i] = 'https://nhadat24h.net'+  img[i]
            yield{
                    'title': response.css('div.header h1 ::text').get(),
                    'date_post':date_post.replace ("Hôm nay", "15/11/2023"),
                    'price':price,
                    'square':square,
                    'address':add,
                    'legal': response.xpath("//div[@class='dv-time-dt']/p[2]//strong/text()").get(),
                    'home_type': new_type,
                    'number_bedroom': num_bed.replace("\n",""),
                    'number_floor': num_floor.replace("\n",""),
                    'number_wc': num_wc.replace("\n",""),
                    'direction': direction.replace("\n",""),
                    'homefront': homefront.replace("\n",""),
                    'gara': gara.replace("\n",""),
                    'img_src_url': img,
                    'url':  response.url,
                    'contact_name': new_name.replace("  ",""),           
                    'contact_phone': new_phone.replace("  ",""),
                    'contact_profile':contact_profile,
                    'description':new_description,                
       }
    
   