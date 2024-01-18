import scrapy
class BookspiderSpider(scrapy.Spider):
#     name = "bookspider"
    allowed_domains = ["mogi.vn"]
    start_urls = ['https://mogi.vn/mua-can-ho-chung-cu']

    def parse(self, response):
        books = response.css('div.prop-info')

        for book in books:
            book_url = book.css('a.link-overlay ::attr(href)').get()
            yield response.follow(book_url, callback = self.parse_book_page)
        
        next_page_url = response.xpath("///ul[@class='pagination']/li/a[@gtm-act='next']/@href").get()
        yield response.follow(next_page_url, callback = self.parse)
        
    def parse_book_page(self, response):
            home_detail = response.css('div.info-attrs .info-attr')
            date_post = home_detail[4].css("span::text").getall()
            square = home_detail[0].css(" span::text").getall()
            legal = home_detail[3].css("span::text").getall()
            contact_phone = response.css('div.agent-contact a').attrib['ng-href']
            contact_phone = contact_phone.replace("':'#'}}","")
            number_wc = home_detail[2].css("span::text").getall()
            number_bedroom = home_detail[1].css("span::text").getall()
            contact_link = response.css('div.agent-info .agent-name a ::attr(href)').get()
            if contact_link is not None:
                 contact_link = 'https://mogi.vn/' + response.css('div.agent-info .agent-name a ::attr(href)').get()
            else:
                 contact_link = " "
            contact_name = response.css('div.agent-info .agent-name ::text').getall()
            new_name = ""
            x = len(contact_name)
            x = x//2
            for i in range(0,x):
                 new_name += contact_name[i].replace("\n","").replace("  ","").replace("\r","")
            yield{
                    'title': response.css("div.title h1 ::text").get(),
                    'date_post':date_post[1],
                    
                    'price':response.css("div.price ::text").get() ,
                    'square':square[1],
                    'address':response.css("div.address ::text").get().replace("  ",""),
                    'legal': legal[1],
                    'number_bedroom': number_bedroom[1] ,
                    'number_wc': number_wc[1],
                    'contact_name': new_name,           
                    'contact_phone': contact_phone.replace ("{{IsMobile() ? 'tel:",""),
                    'contact_profile':contact_link, 
                    'url':  response.url,
                    'img_url_src':response.css('div.media-item img::attr(data-src)').getall() + response.css('div.media-item img::attr(src)').getall(),
                    'description':response.css("div.info-content-body ::text").getall(),       
            }

        
       