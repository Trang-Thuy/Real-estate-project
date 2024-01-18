import scrapy

class BookspiderSpider(scrapy.Spider):
    # name = "bookspider"
    allowed_domains = ["meeyland.com"]
    start_urls = ["https://meeyland.com/ban-can-ho-chung-cu"]
    for i in range(2, 250):
            next_page_url = 'https://meeyland.com/ban-can-ho-chung-cu?page=' + str(i)
            start_urls.append(next_page_url)

    def parse(self, response):
        books = response.css('div.grid-cols-1 a div.border-b a::attr(href)').getall()

        for book in books:
            if book is not None:
                book_url = 'https://meeyland.com' + book
                yield response.follow(book_url, callback = self.parse_book_page)

    def parse_book_page(self, response):
            
            home_detail = response.css('p.line-clamp-2 ::text').getall()
            address = home_detail[0]
            date_post = home_detail[1]
            square = ""
            num_bed = ""
            num_wc = ""
            direction = ""
            project_name = ""
            legal = ""
            project_investor = ""
            home_info = response.xpath("//div/p//text()").getall()
            for i in range(0, len(home_info)-1):
                if 'Diện tích' in home_info[i] and ':' in home_info[i+1]:
                    square = home_info[i+2]
                if 'Số phòng ngủ' in home_info[i]and ':' in home_info[i+1]:
                    num_bed = home_info[i+2]
                if 'Số phòng tắm/ Toilet' in home_info[i]and ':' in home_info[i+1]:
                    num_wc = home_info[i+2]
                if 'Hướng nhà' in home_info[i]and ':' in home_info[i+1]:
                    direction = home_info[i+2]
                if 'Tên dự án' in home_info[i] and ':' in home_info[i+1]:
                    project_name = home_info[i+2]
                if 'Chủ đầu tư' in home_info[i] and ':' in home_info[i+1]:
                    project_investor = home_info[i+2]
                if 'Giấy tờ pháp lý' in home_info[i] and ':' in home_info[i+1]:
                    legal = home_info[i+2]
            yield{
              
                'title': response.css('div.px-4 h1 ::text').get(),
                'date_post': date_post,
                'address': address,
                'price': response.css('div.px-4 .text-black-v6 .border-l h5::text').get(),
                'square': square,
                'direction': direction,
                'contact_name': response.css('div.space-x-3 .flex-col .break-word ::text').get(),
                'contact_phone': response.css('div.px-4 .grid-cols-1 button.button-primary span::text').get(),
                'contact_date_join': response.css('div.px-4 .grid-cols-1 .text-black-v8 .mt-4 span span.font-medium ::text').get(),              
                'number_bedroom': num_bed,
                'number_wc':num_wc,
                'legal': legal,
                'project_name': project_name,
                'project_investor': project_investor,
                'img_url_src': response.css('div.relative img ::attr(src)').getall(),
                'url':  response.url,
                'description':response.css('div.px-4 .py-6 .text-black-v8 .overflow-hidden .text-base ::text').getall(),
               
            }
                
 
       