#...imports....#
class ESpider(BaseSpider):
    #Unique spider name, a project can have multiple spiders
    name = 'espider'
    #Domains the spider can crawl, it will ignore any URLs that do not belong
    #to the following domains
    allowed_domains = ['ebay.co.uk']

    #The parse method determines what happens when an HTTP response is received
    #by the spider
    def parse(self, response):
        #Scrapy uses HTML Xpath selectors to extract data from a page
        hxs = HtmlXPathSelector(response)
        #Empty dictionary of items that will be populated once an image is
        #found on the current page
        items = []
        #Select images contained in <img> tags
        images = hxs.select('//img/@src').extract()
        for image in images:
            if re.match('(.*)ebayimg(.*)JPG', image, re.IGNORECASE):
                item = MyImageItem()
                item['image_urls'] = []
                #If URL is absolute, leave it as is
                if re.match('^http+', image):
                    imgurl = image
                else:
                #If URL is relative create an absolute URL
                    imgurl = urlparse.urljoin(response.url, image)
                item['image_urls'].append(imgurl)
                yield item
