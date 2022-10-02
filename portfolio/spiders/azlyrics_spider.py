import json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule,Spider
from rich.console import Console
import re


class AZ_Spider(Spider):
    name = 'az_spider'
    allowed_domains = ['azlyrics.com']
    con = Console()
    count = 0
    
    def start_requests(self):
        self.artist = self.artist
        url = f'https://search.azlyrics.com/suggest.php?q={self.artist}'
        yield scrapy.Request(url, callback=self.parse_artist)

    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths="//div[@id='listAlbum']/div[@class='listalbum-item']/a"), callback='parse_item', follow=True),
    # )

    def parse_item(self, response):
        print(" PARSE ITEM")
        sel = scrapy.Selector(text=response.text)
        song = re.match(r'(?:")(.*?)"',sel.xpath("//div[@class='div-share']//text()").get()).group(1)
        album = sel.xpath("//div[@class='songinalbum_title']/b/text()").get()
        if album:
            album = album.replace('"','')
        else:
            pass
        lyrics = "".join(sel.xpath("(//div[@class='ringtone']/following-sibling::div)[1]/text()").getall())
        item = {'Artist':self.artist.replace('%20',' '),'Song':song,'Album':album,'Lyrics':lyrics.strip()}
        self.count +=1
        print(f'\r[+] Scraped items: {self.count}',end='')
        yield item

    def parse_artist(self, response):
        sel = scrapy.Selector(text=response.text)
        try:
            resp = json.loads(response.text)
        except:
            pass
        else:
            artists = resp.get("artists")
            for artist in artists:
                name = artist.get("autocomplete")
                if name.lower().replace(' ','').replace('-','') == self.artist.lower().replace(' ','').replace('-','').replace('%20',''):
                    url = artist.get("url").replace('\\','')
                    self.artist = name
                    print(f"\n {self.artist} {url} \n")
                    yield scrapy.Request(url, callback=self.parse_songs, dont_filter=True)

    def parse_songs(self, response):
        print(" PARSE SONGS")
        sel = scrapy.Selector(text=response.text)
        for link in sel.xpath("//div[@id='listAlbum']/div[@class='listalbum-item']/a"):
            url = response.urljoin(link.xpath("./@href").get())
            yield scrapy.Request(url, callback=self.parse_item)