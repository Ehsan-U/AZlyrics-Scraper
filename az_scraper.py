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
    cmdline.execute(f'scrapy crawl az_spider -a artist={artist} -o {filename}.csv'.split())
get_songs()