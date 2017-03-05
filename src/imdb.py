from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import re

def getImdbRating(imdb):
    br = Browser()
    link = br.open("http://www.imdb.com/title/" + imdb)
    soup = BeautifulSoup(link.read())
    #try :
    i = 0
    rating = soup.find('span',attrs={'itemprop' : 'ratingValue'}).text
    return float(rating)


def getImdbID(nfo):
    p = re.compile('tt\d{7}')  # Pattern for finding imdb id
    with open(nfo,'r') as f:
        nfoFile = ''.join(f.readlines())
    found = p.search(nfoFile)
    return found.group() if found else None

