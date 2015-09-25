import scraperwiki
import re 
from bs4 import BeautifulSoup

if scraperwiki.sqlite.select('name FROM sqlite_master WHERE type="table" AND name="swdata"'):
    scraperwiki.sqlite.execute('DROP TABLE `swdata`')

url = 'http://www.stjohns.ca/city-hall/about-city-hall/council'
soup = BeautifulSoup(scraperwiki.scrape(url))
base = 'http://www.stjohns.ca/'

rows = soup.findAll("div", "views-row")
for row in rows:
    fields = row.findAll(class_="field-content")
    record = {}
    record["source_url"] = url
    if "Ward" in fields[0].string:
        record["district_name"] = fields[0].string
    img = fields[1].find_next("img")
    if img:
        record["photo_url"] = img["src"]
    parts = fields[2].string.split()
    if 'Councillor' in fields[2].string:
        upto = 3
    elif 'Deputy Mayor' in fields[2].string:
        upto = 2
    else:
        upto = 1
    if 'Councillor' in fields[2].string:
        record["elected_office"] = 'Councillor'
    else:
        record["elected_office"] = ' '.join(parts[0:upto])        
    record["name"] = " ".join(parts[upto:])
    # offices.tel fields[3].string
    record["email"] = fields[4].find_next("a")["href"].replace("mailto:", "").strip()
    record["url"] = "http://www.stjohns.ca" + fields[2].find_next("a")["href"]
    if "district_name" not in record:
        record["boundary_url"] = "/boundaries/census-subdivisions/1001519/"

    scraperwiki.sqlite.save(["name"], record)
