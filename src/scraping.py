import re
import requests, zipfile, io, os
from bs4 import BeautifulSoup

URL = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
page = requests.get(URL)
html_content = page.content

soup = BeautifulSoup(html_content, 'html.parser')

year_pattern = re.compile(r'(\d{4})/')
links_with_year = soup.find_all('a', href = year_pattern)

years = []

for link in links_with_year:
    years.append(link.get('href'))

years.sort(reverse = True)

urls_to_download = []
got_all_urls = False

for year in years:
    year_url = URL + year
    year_page = requests.get(year_url)
    year_html_content = year_page.content
    year_soup = BeautifulSoup(year_html_content, 'html.parser') 
    year_links = year_soup.find_all('a')
    zip_files_refs = []

    for year_link in year_links:
        file_ref = year_link.get('href')
        if '.zip' in file_ref:
            zip_files_refs.append(file_ref)
        

    zip_files_refs.sort(reverse=True)
    for zip_file_ref in zip_files_refs:
        zip_url = year_url + zip_file_ref
        urls_to_download.append(zip_url)
        if len(urls_to_download) == 3:
            got_all_urls = True
            break

    if(got_all_urls):
        break

destination_dir = './data/raw'
os.makedirs(destination_dir, exist_ok=True)

for zip_file_url in urls_to_download:
    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(destination_dir)
    