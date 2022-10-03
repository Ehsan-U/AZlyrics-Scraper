from scrapy import cmdline
from rich.console import Console
con = Console()
from rich.prompt import Prompt
from pyfiglet import Figlet,figlet_format

f = Figlet(font='big')
print('\r',f.renderText('Ehsan U.'),end='')
con.print("[bold green][+][reset] @Author: https://www.upwork.com/freelancers/~018fe27cd797e8a786")
import os
term_size = os.get_terminal_size()
print('=' * term_size.columns)

def get_songs():
    artist = Prompt.ask(" \n[bold purple][+][reset] Enter an artist name", default='Ed Sheeran')
    artist = artist.replace(' ','%20')
    filename = Prompt.ask("[bold purple][+][reset] Enter the output filename", default='Songs')
    # stop = Prompt.ask("[bold purple][+][reset] Enter the number of songs to extract", default='10')
    print("[+] Crawling process started..")
    cmdline.execute(f'scrapy crawl splash_spider -a artist={artist} -a stop=1 -o {filename}.csv'.split())
    
get_songs()
print("\n[+] Finished\n")
# import requests 
# proxies = {
#     'http':'http://ehsan:ehsan123@geo.iproyal.com:22323',
#     'https':'http://ehsan:ehsan123@geo.iproyal.com:22323'
# }
# print(requests.get('http://httpbin.org/ip',proxies=proxies).text)