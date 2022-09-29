'''
    --------------------------------------------
    deep-to-surface
    ===============
      a very (very) minimal tor-site grabber
      (may work, may not)
    
      Prep :
        > Windows
          - https://www.torproject.org/dist/torbrowser/11.5.2/tor-win32-0.4.7.10.zip
            - after extracting run ``TOR/tor.exe``

        > Linux
          - tor
            - ``systemctl start tor``

      USAGE : python3 tor.py "http://<site>.onion"

      @deathpicnic
    --------------------------------------------
'''

import requests, sys
import json, lxml, os
from bs4 import BeautifulSoup as bs

os.system("cls||clear")

# URL = 'http://tortaxi7axhn2fv4j475a6blv7vwjtpieokolfnojwvkhsnj7sgctkqd.onion/' # tor.taxi
try:
    URL = str(sys.argv[1])
except IndexError:
    print ('USAGE : python3 tor.py "http://<site>.onion"')
    exit(1)

if not '://' in URL:
    URL = f'http://{URL}'

TLD = str(URL.split('://')[1].split('/')[0].split('.')[-1].lower().strip())

if TLD != 'onion':
    print('not an onion site bruh!!')
    exit()

url = URL
protocol = f"{url.split('://')[0]}://" # http{,s}
base_url = f"{url.split('://')[1].split('/')[0]}" # 3mcm3xxxxxxvgwfyd.onion

proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

def get_ip():

   return requests.get('https://httpbin.org/ip', proxies = proxies, timeout = 20).json()['origin']

def get_content(url = None, file=None, timeout=30):

    if not url: return None
    data = requests.get(url, proxies = proxies, timeout = timeout)
    soup = bs(data.content, 'lxml')
    
    if file: 
        with open(f"{file}", "w", encoding="utf-8") as test:
            test.write(soup.prettify())
    return soup

def crawl(s):
    links = s.find_all('a', href=True)
    for link in links:

        href = link['href'].strip()
        if href == '/': continue
        if href.split('://')[0].lower() in ('http', 'https'):
            if href.split('://')[1].split('/')[0] not in (url): continue
        if len(href.split('.')) == 1:
            href_ = protocol + base_url + href 
            endpoint = href_.split(base_url)[1].split('/')[-1]
            print(f'{href_}:{endpoint}.html')
            get_content(href_, f'{endpoint}.html')
            try: s.replace(f'href="{href}"', f'href="{href_}"')
            except: pass
            for a in s.find_all('a', href=True):
                try:
                    if a['href'] == href:
                        a['href'] = f'{endpoint}.html'
                except: pass

         
print ("\n\tdeep-to-surface")
print ("\t===============")
print ("\n\t @deathpicnic\n")

if not base_url in os.listdir(): # mkdir -p 3mcm3xxxxxxvgwfyd.onion
    os.mkdir(base_url)
os.chdir(os.path.join(os.getcwd(), base_url)) # cd 3mcm3xxxxxxvgwfyd.onion/

print(f"Accessing with IP : {get_ip()}")

soup = get_content(url)
soup_ = soup.prettify()
crawl(soup)

with open('index.html', 'w', encoding="utf-8") as f:
    f.write(soup.prettify())
    f.close()