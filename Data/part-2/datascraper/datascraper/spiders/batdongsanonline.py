import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["batdongsanonline.vn"]
    start_urls = ["https://batdongsanonline.vn/ban-can-ho-chung-cu/"]
    for i in range(2, 444):
            next_page_url = 'https://batdongsanonline.vn/ban-can-ho-chung-cu/page-' + str(i)
            start_urls.append(next_page_url)

    def parse(self, response):
        books = response.css('div.w7 a ::attr(href)').getall()
        if len(books) != 0:
            for book in books:
                book_url = 'https://batdongsanonline.vn/' + book
                yield response.follow(book_url, callback = self.parse_book_page)
        else:
            books = response.css('div.p-0 .block_ct .main_ct1 .chinh a::attr(href)').getall()   
            for i in range (0, 40,2):
                book = books[i]
                book_url = 'https://batdongsanonline.vn/' + book
                yield response.follow(book_url, callback = self.parse_book_page)

    def parse_book_page(self, response):
            # table_rows = response.css("table tr")
            post_info = response.css("div.text-left div.col-md-4 ::text").getall()
            date_post = post_info[1].replace("\t","").replace("\n","").replace("  ","")
            
            home_info = response.css("div.short-detail-wrap ul.short-detail-2 li span ::text").getall()
            price = ""
            square = ""
            for i in range(0,len(home_info)-3):
                if 'Mức giá:' in home_info[i]:
                    price = home_info[i+3]
                if 'Diện tích:' in home_info[i]:
                    square = home_info[i+2]
            description = response.css("div.f-detail-content1 ::text").getall()
            new_des = ""
            for i in range (0, len(description)):
                new_des += description[i].replace("\r","").replace("\n","")
            
            home_fur = ""
            status = ""
            num_floor = ""
            num_bed = ""
            num_wc = ""
            direction = ""
            home_a = response.css("div ul.listTienich li ::text").getall()
            home_b = response.css("div.f-detail span.list_vndes ::text").getall()
            home_detail = ""
            if len(home_a) != 0:
                home_detail = home_a
                for i in range (0, len(home_detail)):
                    if 'Nội thất' in home_detail[i]:
                        home_fur = home_detail[i+2]
                    if 'Tình trạng BDS' in home_detail[i]:
                        status = home_detail[i+2]
                    if 'Tầng số' in home_detail[i]:
                        num_floor = home_detail[i+2]
                    if 'Hướng cửa chính' in home_detail[i]:
                        direction = home_detail[i+2]
            elif len(home_b) != 0:
                home_detail = home_b
                for i in range (0, len(home_detail)):
                    if 'Nội thất' in home_detail[i]:
                        home_fur = home_detail[i+1]
                    if 'Tình trạng BDS' in home_detail[i]:
                        status = home_detail[i+1]
                    if 'Tầng' in home_detail[i]:
                        num_floor = home_detail[i+1]
                    if 'Phòng ngủ' in home_detail[i]:
                        num_bed = home_detail[i+1]
                    if 'Phòng tắm' in home_detail[i]:
                        num_wc = home_detail[i+1]
                    if 'Hướng' in home_detail[i]:
                        direction = home_detail[i+1]

            contact_name = response.css("div.our_list span.name ::text").get()
            contact_phone = response.css("div.our_list div.contact-info a.tag-phone").attrib['data-phone']
            contact_url = response.css('div.main_sb span.name a::attr(href)').get()
            if contact_url is not None:
                contact_profile = 'https://batdongsanonline.vn/' + contact_url

            img_url = response.xpath("//div//img/@data-src").getall()
            filtered_img_url = [url for url in img_url if "uploadUsers/" in url]
            yield{
              
                'title': response.css('h1 ::text').get(),
                'date_post': date_post.replace(" Ngày đăng : ",""),
                'price': price,
                'square': square,
                'address': response.css("p.Viethoa1 ::text").get(),
                'direction': direction,
                'number_floor': num_floor,
                'number_bedroom': num_bed,
                'number_wc': num_wc,
                'home_fur': home_fur,
                'status': status,
                'contact_name': contact_name.replace("\t","").replace("\n",""),
                'contact_phone': contact_phone,
                'contact_profile': contact_profile,
                'img_url_src': filtered_img_url,
                'url':  response.url,
                
                
                'description': new_des.replace("\r\n",""),
                
            }
                
 
       