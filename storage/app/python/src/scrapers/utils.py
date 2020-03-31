# -*- encoding: utf-8 -*-

import json
import re
from datetime import datetime, date, timedelta

import tweepy

import requests
from bs4 import BeautifulSoup
import numpy as np

import asyncio
from pyppeteer import launch

consumer_key = "F2pIrutjymGr9vZuqTeViAymw"
consumer_secret = "QFLTXwFJZNuR6i00IswAZIgaKsKl5AtmPufoSaRnR57ER2yVxS"
access_token = "879408865997201408-QJDeVNKYBsTdp97caK0qFV454YYwRLp"
access_token_secret = "gLNfeVRjT7LrDaWWSgCX0ZRu6TeTPBquTxlYKQ4hUzAka"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def remove_emoji(msg):
    """Remove emojis characters from an input string.

    Note:
        Code obtained from https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python

    Args:
        msg (str): Message to remove emojis.

    Returns:
        Same msg (str) with removed emojis.
    """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', msg)


def get_tweets_by_hashtag(hashtag, date, lang='en'):
    """Get tweets from a day with a hashtag filter.

    Notes:
        The hashtag parameter is for search a city.

    Args:
        hashtag (str): Some hashtag to search in twitter.
        date (str): Date in YYYY-mm-dd format.
        lang (str): Restricts tweets to the given language, given by an ISO 639-1 code.
    """
    query = '#' + hashtag + ' AND #travel OR #viaje -filter:retweets'
    for tweet in tweepy.Cursor(api.search, q=query, since=date, lang=lang, tweet_mode='extended').items():
        ee = {
            'date': tweet.created_at.strftime("%Y-%m-%d"),
            'comment': remove_emoji(tweet.full_text)
        }
        print(json.dumps(ee, ensure_ascii=False))


def select_date_tu_tiempo(day, month, year):
    today = date.today()
    select_date = date(year, month, day)

    if (today - select_date).days > 0:
        date_list = [(select_date + timedelta(days=d)).strftime("%Y-%m-%d")
                        for d in range((today - select_date).days)]

    for dat in date_list:
        tu_tiempo(dat[8:10], dat[5:7], dat[0:4])



def tu_tiempo(day, month, year):
    months = ['', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre',
              'noviembre', 'diciembre']
    wind_directions = np.array(
        ['En calma', 'Norte', 'Nordeste', 'Este', 'Sureste', 'Sur', 'Suroeste', 'Oeste', 'Noroeste', 'Variable'])

    page = requests.get('https://www.tutiempo.net/registros/lemd/' + day + '-' + months[int(month)] + '-' +
                        year + '.html')

    soup = BeautifulSoup(page.content, 'html.parser')
    tr = soup.find('div', class_='last24 thh mt10').findAll('tr')

    for i in range(len(tr)):
        if 1 < i < len(tr) - 2 and i % 2 == 0:
            td = tr[i].findAll('td')
            wind_direction = np.where(wind_directions == [td[3].find('img').get('title')])[0]

            speed = 0
            if td[3].getText() != 'En calma':
                speed = re.findall(r"[\d]+", td[3].getText())[0]

            response = {
                'date': day + '-' + month + '-' + year,
                'hour': td[0].getText(),
                'temperature': re.findall(r"[-]*[\d]+", td[2].getText())[0],
                'wind_speed': speed,
                'wind_direction': str(wind_direction[0]),
                'humidity': re.findall(r"[\d]+", td[4].getText())[0],
                'pressure': re.findall(r"[\d]+", td[5].getText())[0]
            }
            print(response)

def el_tiempo():
    today = str(date.today())
    page = requests.get("https://www.eltiempo.es/madrid.html?v=por_hora")
    soup = BeautifulSoup(page.content, 'html.parser')

    html = list(soup.children)[2]
    body = list(html.children)[3]

    # Contenido tabla mañana
    table = body.find_all('div', class_='m_table_weather_hour_detail by_hour')[1]  # accedo a la tabla de mañana
    #fila = data-expand-tablechild-item, primera 3, ultima 49

    #diccionarios
    array_hour = []
    array_temperature = []
    array_wind_direction = []
    array_wind_speed = []
    array_humidity = []
    array_pressure = []

    for i in range(1, 25):
        horas = table.find_all('div', class_='m_table_weather_hour_detail_hours')[i].get_text()
        prevision = table.find_all('div', class_='m_table_weather_hour_detail_pred')[i].get_text()

        velocidad = table.find_all('div', class_='m_table_weather_hour_detail_med')[i].get_text()

        #viento
        wind = table.find_all('div', class_='m_table_weather_hour_detail_wind')[i]  # icono
        wind2 = list(wind)[1]  # span
        wind3 = list(wind2)[1]  # i

        north = len(wind2.find_all('i', class_='north'))
        south = len(wind2.find_all('i', class_='south'))
        east = len(wind2.find_all('i', class_='east'))
        west = len(wind2.find_all('i', class_='west'))
        northEast = len(wind2.find_all('i', class_='north-east'))
        northWest = len(wind2.find_all('i', class_='north-west'))
        southEast = len(wind2.find_all('i', class_='south-east'))
        southWest = len(wind2.find_all('i', class_='south-west'))

        windDir = 0  # id

        if north > 0:
            windDir = 2
        if south > 0:
            windDir = 6
        if east > 0:
            windDir = 4
        if west > 0:
            windDir = 8
        if northEast > 0:
            windDir = 3
        if northWest > 0:
            windDir = 9
        if southEast > 0:
            windDir = 5
        if southWest > 0:
            windDir = 7

        #aniado
        array_hour.append(horas)
        array_temperature.append(prevision)
        array_wind_speed.append(velocidad)
        array_wind_direction.append(windDir)

    for j in range(0, 24):
        humedad = table.find_all('div', class_='m_table_weather_hour_detail_hum')[j]
        humidity = humedad.find_all('span')[1].get_text()
        presion = table.find_all('div', class_='m_table_weather_hour_detail_preas')[j]
        preas = presion.find_all('span')[1].get_text()

        # aniado
        array_humidity.append(humidity)
        array_pressure.append(preas)

    for i in range(len(array_hour)): #24
        response = {
            'date': today[8:10] + '-' + today[5:7] + '-' + today[0:4],
            'hour': array_hour[i],
            'temperature': re.findall(r"[-]*[\d]+",array_temperature[i])[0],
            'wind_speed': re.findall(r"[\d]+",array_wind_speed[i])[0],
            'wind_direction': array_wind_direction[i],
            'humidity': re.findall(r"[\d]+",array_humidity[i])[0],
            'pressure': re.findall(r"[\d]+",array_pressure[i])[0]
        }
        print(response)
        # --------------------------------------------------------------regex----------------------------------------------------------
        #regex = r"(date).+(hour).+([0-9]{2}:[0-9]{2}).+(temperature).+([0-9])°.+(wind_speed).+([0-9])\skm\/h.+(wind_direction)..\s([0-9]{1,}).+(humidity)..\s.([0-9]{1,})%.+(pressure)..\s.([0-9]{1,})\shPa"
        #test_str = str(response)
        #print(re.findall(regex, test_str)[0])

def select_historical_date(day, month, year):
    today = date.today()
    select_date = date(year, month, day)

    if (today - select_date).days > 5:
        select_date = today - timedelta(days=5)
        date_list = [(select_date + timedelta(days=d)).strftime("%Y-%m-%d")
                        for d in range((today - select_date).days)]
    else:
        date_list = [(select_date + timedelta(days=d)).strftime("%Y-%m-%d")
                        for d in range((today - select_date).days)]

    for dat in date_list:
        asyncio.get_event_loop().run_until_complete(select_url(dat[8:10], dat[5:7], dat[0:4]))

def select_future_date():
    today = str(date.today())
    asyncio.get_event_loop().run_until_complete(select_url(today[8:10], today[5:7], today[0:4]))

async def select_url(day, month, year):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.airportia.com/spain/madrid-barajas-international-airport/departures/')
    await page.select('.flightsFilter-select--date', year + month + day)
    await page.select('.flightsFilter-select--fromTime', '0000')
    await page.select('.flightsFilter-select--toTime', '2359')

    await page.click('.flightsFilter-submit')
    await page.waitFor(4000)
    html = await page.evaluate('new XMLSerializer().serializeToString(document.doctype) + '
                               'document.documentElement.outerHTML')
    scraper_airportia(html, day, month, year)
    await browser.close()

def scraper_airportia(html, day, month, year):
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find('table', class_='flightsTable').findAll('tr')
    i = 0
    for tr in trs:
        if i != 0:
            identifier = tr.find('td', class_='flightsTable-number')
            if identifier is not None:
                td = tr.findAll('td')
                delay = 0
                if td[5].find('div') is not None:
                    if td[5].find('div').getText() == 'Cancelled' or td[5].find('div').getText() == 'Unknown':
                        delay = 2
                    elif td[5].find('div').getText() == 'Landed Late':
                        delay = 0

                response = {
                    'id': identifier.find('a').getText(),
                    'date': day + '-' + month + '-' + year,
                    'airline': td[2].getText(),
                    'destination': td[1].find('span').getText(),
                    'delay': delay,  # 0->ok, 1->late, 2->cancelled
                    'expected_departure_time': td[3].getText(),
                }
                print(response)
        i = i + 1

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    get_tweets_by_hashtag(hashtag='Madrid', date=today, lang='es')