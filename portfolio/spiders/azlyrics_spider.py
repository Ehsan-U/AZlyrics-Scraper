import scrapy
from scrapy_splash import SplashRequest
import json
from scrapy.spidermiddlewares.httperror import HttpError

class TestSplashSpider(scrapy.Spider):
    name = 'splash_spider'
    allowed_domains = ['azlyrics.com']
    count = 0
    lua_artist = """
    function main(splash, args)
        local host = 'geo.iproyal.com'
        local port = 22323
        local user = 'ehsan'
        local pass = 'ehsan123'
        splash:on_request(function(request)
            request:set_proxy{host,port,username=user,password=pass}
            end)
        splash.js_enabled = true
        splash.images_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(args.wait))
        return {
            html = splash:html()
        }
    end
    """
    artist_songs = """
    function main(splash, args)
        local host = 'geo.iproyal.com'
        local port = 22323
        local user = 'ehsan'
        local pass = 'ehsan123'
        splash:on_request(function(request)
            request:set_proxy{host,port,username=user,password=pass}
            end)
        splash.js_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(args.wait))
        return {
            html = splash:html()
        }
    end
    """
    artist_urls ="""
    function main(splash, args)
        local host = 'geo.iproyal.com'
        local port = 22323
        local user = 'ehsan'
        local pass = 'ehsan123'
        splash:on_request(function(request)
            request:set_proxy{host,port,username=user,password=pass}
            end)
        base_url = 'https://www.azlyrics.com'
        splash.js_enabled = true
        splash.images_enabled = false
        assert(splash:go(args.url))
        assert(splash:wait(args.wait))
        urls = {}
        local btns = splash:select_all(".listalbum-item a")
        for _, link in ipairs(btns) do
            urls[#urls+1] =  base_url .. link.node.attributes.href
        end
        return urls
    end
    """

    def start_requests(self):
        self.artist =self.artist
        self.stop = int(self.stop)
        url = f'https://search.azlyrics.com/suggest.php?q={self.artist}'
        yield SplashRequest(url, callback=self.parse_artist, endpoint='execute', args={'lua_source':self.lua_artist,'wait':1,'timeout':60,'resource_timeout':20})


    def parse_artist(self, response):
        sel = scrapy.Selector(text=response.text)
        try:
            _body = sel.xpath("//body/text()").get()
            resp = json.loads(_body)
        except Exception as e:
            print("[+] Retrying lua_artist")
            yield SplashRequest(url=response.url, callback=self.parse_artist, endpoint='execute', args={'lua_source':self.lua_artist,'wait':1,'timeout':60,'resource_timeout':20})
        else:
            artists = resp.get("artists")
            for artist in artists:
                name = artist.get("autocomplete")
                if name.lower().replace(' ','').replace('-','') == self.artist.lower().replace(' ','').replace('-','').replace('%20',''):
                    url = artist.get("url").replace('\\','')
                    self.artist = name
                    yield SplashRequest(url, callback=self.parse_main, endpoint='execute', args={'wait':1,'lua_source':self.artist_urls,'timeout':60,'resource_timeout':20})

    def parse_main(self, response):
        urls = json.loads(response.text)
        urls = dict(urls)
        for url in list(urls.values()):
            yield SplashRequest(url, callback=self.parse_song, endpoint='execute', args={'wait':0.5,'lua_source':self.artist_songs,'timeout':60,'resource_timeout':20})
    
    def parse_song(self, response):
        sel = scrapy.Selector(text=response.text)
        try:
            song = sel.xpath("//div[@class='div-share']//text()").get().replace('"','').replace("lyrics",'').strip()
        except:
            # print(response.text)
            # print("PARSE_ITEM ERROR >> ",sel.xpath("//div[@class='div-share']//text()").get())
            print("[+] Retrying artist_songs")
            yield SplashRequest(url=response.url, callback=self.parse_song, endpoint='execute', args={'wait':0.5,'lua_source':self.artist_songs,'timeout':60,'resource_timeout':20})
        else:
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

    def handle_failure(self, failure):
        if failure.check(HttpError):
            print(failure.value.response.text)