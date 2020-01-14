import redis
import requests
from bs4 import BeautifulSoup


def parse_and_populate_redis():
   """
   """
   # Start redis
   db = redis.Redis("localhost")
   
   # Retrieve and parse the xml file, populate redis
   url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
   response = requests.get(url)
   if response and response.status_code == 200:
      soup = BeautifulSoup(response.content, features='html.parser')
      cubes_time = soup.select('cube[time]')
      for ct in cubes_time:
         time = ct.get('time', '')
         for cc in ct.select('cube[currency]'):
            key = time + '|' + cc.get('currency', '')
            db.set(key, cc.get('rate'))


if __name__ == '__main__':
   parse_and_populate_redis()

