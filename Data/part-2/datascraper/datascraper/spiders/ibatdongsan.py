import scrapy

class BookspiderSpider(scrapy.Spider):
    # name = "bookspider"
    # allowed_domains = ["i-batdongsan.com"]
    # start_urls = ["https://i-batdongsan.com/can-ban-can-ho-chung-cu.htm"]

    allowed_domains = ["nhadat24h.net"]
    start_urls = [
        # 'https://nhadat24h.net/ban-can-ho-chung-cu',
                  "https://nhadat24h.net/ban-can-ho-chung-cu/page3"]

    def parse(self, response):
        books = response.css('div.dv-item a.a-title ::attr(href)').getall()
        
        for book in books:
            book_url = 'https://nhadat24h.net'+ book
            # books = ['https://nhadat24h.net/ban-chung-cu-quan-tan-phu/950tr-55m2-can-3pn-3wc-o-lien-luy-ban-bich-vay-duoc-o9oi-32i-244-ID4066456','https://nhadat24h.net/ban-chung-cu-quan-tan-binh/cat-lo-sau-880tr-56m2-o-lien-3pn-vinh-vien-bay-hien-o9oi-32i-244-ID4063917',
            #          'https://nhadat24h.net/ban-chung-cu-thanh-pho-thuan-an/san-gio-hang-can-2pn-gia-tot-splus-riverview-truoc-ngay-ban-giao-ls-uu-dai-ID4067072',
            #          'https://nhadat24h.net/ban-chung-cu-chung-cu-eden-riverside/chinh-chu-can-sang-can-ho-48m2-vista-riverside-ID4066949']
            yield response.follow(book_url, callback = self.parse_book_page)
                   
        next_page_url = 'https://nhadat24h.net'+ response.xpath("//div[@class='dv-pt-ttcm']/div/ul/li[@class='active']/following-sibling ::li[1]/a/@href").get()
        yield response.follow(next_page_url, callback = self.parse)
         
    def parse_book_page(self, response):
            home_detail = response.xpath("//div[@class='dv-time-dt']/p[1]//text()").getall()
            contact_profile = 'https://nhadat24h.net' + response.css('div.detailUserName .info label.fullname a ::attr(href)').get()
            y = len(home_detail)
            price = ""
            square = ""
            for j in range(0, y-1): 
                if 'Cần bán' in home_detail[j]:
                    price = home_detail[j+1] + home_detail[j+2] 
                    square = home_detail[j+3] + home_detail[j+4]
            # price = home_detail[1] + home_detail[2].replace("-","")
            # square = home_detail[3] + home_detail[4]
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
                    num_floor = table[i+1]
                if 'Hướng' in table[i] and 'Đường vào' not in table[i+1]:
                    direction = table[i+1]
                if 'Phòng Ngủ' in table[i]:
                    num_bed = table[i+1]
                if 'Phòng WC' in table[i] and 'Số tầng' not in table[i+1]:
                    num_wc = table[i+1]
                if 'Chỗ để xe' in table[i] and 'Mã BĐS'not in table[i+1]:
                    gara = table[i+1]
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
            # contact_name = response.css('div.detailUserName .info label.fullname ::text').get()
            yield{
                    'title': response.css('div.header h1 ::text').get(),
                    'date_post':date_post.replace ("Hôm nay", "4/1/2023"),
                    'url':  response.url,
                    'price':price,
                    'square':square,
                    'address':add,
                    'legal': response.xpath("//div[@class='dv-time-dt']/p[2]//strong/text()").get(),
                    'home_type': new_type,
                    # 'contact_name': contact_name,           
                    # 'contact_phone': response.css('div.dv-pt-item .panelActionContent a.call ::text').get(),
                    'number_bedroom': num_bed,
                    'number_floor': num_floor,
                    'number_wc': num_wc,
                    'direction': direction,
                    'homefront': homefront,
                    'gara': gara,
                    'contact_profile':contact_profile,
                    'description':response.css('div.detailmaincontent p ::text').getall(),                
            }
    # def parse(self, response):
    #     books = response.css('div.content-item')

    #     for book in books:
    #         relative_url = book.css('div.text .ct_title a ::attr(href)').get()
    #         book_url = 'https://i-batdongsan.com'+ relative_url
    #         yield response.follow(book_url, callback = self.parse_book_page)

    #     next_page_url = 'https://i-batdongsan.com'+ response.xpath("//div[@class='page']/a[@class='active']/following-sibling ::a[1]/@href").get()
    #     yield response.follow(next_page_url, callback = self.parse)

    # def parse_book_page(self, response):
    #         table_rows = response.css("table tr")
    #         description =response.css('div.text-content ::text').get()
    #         price = table_rows[0].xpath("//tr[7]/td[4]/text()").get()
    #         dining = ""
    #         kitchen = ""
    #         roof_top = ""
    #         gara = ""
    #         owner = ""
    #         dining = table_rows[0].xpath("//tr[2]/td[6]/img").get()
    #         if dining is not None:
    #              dining = 'yes'
    #         kitchen = table_rows[0].xpath("//tr[3]/td[6]/img").get()
    #         if kitchen is not None:
    #             kitchen = 'yes'
    #         roof_top = table_rows[0].xpath("//tr[4]/td[6]/img").get()
    #         if roof_top is not None:
    #             roof_top = 'yes'
    #         gara = table_rows[0].xpath("//tr[5]/td[6]/img").get()
    #         if gara is not None:
    #             gara = 'yes'
    #         owner = table_rows[0].xpath("//tr[6]/td[6]/img").get()
    #         if owner is not None:
    #             owner = 'yes'
    #         img_src = response.css('div.image-list ul li img ::attr(src)').getall()
    #         for i in range (0, len(img_src)):
    #             img_src[i] = 'https://i-batdongsan.com'+ img_src[i]

            
    #         yield{
    #             'title': response.css('div.title h1 ::text').get(),
    #             'date_post':table_rows[0].xpath("//tr[1]/td[2]/text()").get(),
    #             'url':  response.url,
    #             'img_url_src': img_src,
    #             'price':price.replace(" ",""),
    #             'square':table_rows[1].xpath("//tr[7]/td[2]/text()").get(),
    #             'address': response.css('div.contact .address span.value ::text').get(),
    #             'direction': table_rows[0].xpath("//tr[2]/td[4]/text()").get(),
    #             'dining': dining,
    #             'type_content': table_rows[1].xpath("//tr[3]/td[2]/text()").get(),
    #             'kitchen':kitchen,
    #             'home_type': table_rows[1].xpath("//tr[4]/td[2]/text()").get(),
    #             'legal':table_rows[0].xpath("//tr[4]/td[4]/text()").get(),
    #             'roof_top': roof_top,
    #             'width':table_rows[1].xpath("//tr[5]/td[2]/text()").get(),
    #             'number_floor':table_rows[0].xpath("//tr[5]/td[4]/text()").get(),
    #             'gara':gara,
    #             'height': table_rows[1].xpath("//tr[6]/td[2]/text()").get(),
    #             'number_bedroom': table_rows[0].xpath("//tr[6]/td[4]/text()").get(),
    #             'owner':owner,
    #             'contact_name': response.css('div.contact-info .content .name ::text').get(),
    #             'contact_phone':response.css('div.contact-info .content .fone ::text').getall(),
    #             'description':description.replace("\r\n",""),
    #         }
                

        
       