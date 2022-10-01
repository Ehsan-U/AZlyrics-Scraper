import json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from rich.console import Console
import re

class TestComSpider(CrawlSpider):
    name = 'az_spider'
    allowed_domains = ['azlyrics.com']
    con = Console()
    
    def start_requests(self):
        self.artist = self.artist
        url = f'https://search.azlyrics.com/suggest.php?q={self.artist}'
        yield scrapy.Request(url, callback=self.parse)

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@id='listAlbum']/div[@class='listalbum-item']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = scrapy.Selector(text=response.text)

        song = re.match(r'(?:")(.*?)"',sel.xpath("//div[@class='div-share']//text()").get()).group(1)
        album = sel.xpath("//div[@class='songinalbum_title']/b/text()").get()
        if album:
            album = album.replace('"','')
        else:
            pass
        lyrics = "".join(sel.xpath("(//div[@class='ringtone']/following-sibling::div)[1]/text()").getall())

        item = {'Artist':self.artist,'Song':song,'Album':album,'Lyrics':lyrics}
        return item

    def parse(self, response):
        # self.con.print(response.text)
        sel = scrapy.Selector(text=response.text)
        resp = json.loads(response.text)
        # self.con.print(resp)
        artists = resp.get("artists")
        for artist in artists:
            name = artist.get("autocomplete")
            if name.lower().replace(' ','').replace('-','') == self.artist.lower().replace(' ','').replace('-','').replace('%20',''):
                url = artist.get("url")
                self.artist = name
                yield scrapy.Request(url)