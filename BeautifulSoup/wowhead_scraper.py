#!python3
# wowhead_scraper.py is a simple web scraper to check for the latest headlines
# on Wowhead.

import requests
import bs4

# URL of site we want to scrape
URL = "http://www.wowhead.com"
header_list = []

def main():
	raw_site_page = requests.get(URL) #Pull down the site.
	raw_site_page.raise_for_status()  #Confirm site was pulled. Error if not
	
	#Create BeautifulSoup object
	soup = bs4.BeautifulSoup(raw_site_page.text, 'html.parser')
	html_header_list = soup.select('.heading-size-1')
	for headers in html_header_list:
		header_list.append(headers.getText())
	for headers in header_list:
		print(headers)

if __name__ == "__main__":
    main()
