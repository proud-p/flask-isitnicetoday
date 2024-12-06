# Queries Justwatch.com using selenium to get titles

import geopy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options

def get_JUSTWATCH_COUNTRIES():
    return {
    'ae': 'United Arab Emirates',
    'ar': 'Argentina',
    'at': 'Austria',
    'au': 'Australia',
    'be': 'Belgium',
    'br': 'Brazil',
    'ca': 'Canada',
    'ch': 'Switzerland',
    'cl': 'Chile',
    'co': 'Colombia',
    'cz': 'Czech Republic',
    'de': 'Germany',
    'dk': 'Denmark',
    'ec': 'Ecuador',
    'ee': 'Estonia',
    'es': 'Spain',
    'fi': 'Finland',
    'fr': 'France',
    'gb': 'United Kingdom',
    'gr': 'Greece',
    'hk': 'Hong Kong',
    'hu': 'Hungary',
    'id': 'Indonesia',
    'ie': 'Ireland',
    'in': 'India',
    'it': 'Italy',
    'jp': 'Japan',
    'kr': 'South Korea',
    'lt': 'Lithuania',
    'lv': 'Latvia',
    'mx': 'Mexico',
    'my': 'Malaysia',
    'nl': 'Netherlands',
    'no': 'Norway',
    'nz': 'New Zealand',
    'pe': 'Peru',
    'ph': 'Philippines',
    'pl': 'Poland',
    'pt': 'Portugal',
    'ro': 'Romania',
    'ru': 'Russia',
    'se': 'Sweden',
    'sg': 'Singapore',
    'sk': 'Slovakia',
    'th': 'Thailand',
    'tr': 'Turkey',
    'tw': 'Taiwan',
    'uk': 'United Kingdom',
    'uk': 'England',
    'us': 'United States',
    've': 'Venezuela',
    'za': 'South Africa'
    }

def get_JUSTWATCH_GENRES():
    return {
    'act': 'Action',
    'ani': 'Animation',
    'cmy': 'Comedy',
    'crm': 'Crime',
    'doc': 'Documentary',
    'drm': 'Drama',
    'fnt': 'Fantasy',
    'hrr': 'Horror',
    'hst': 'History',
    'msc': 'Music',
    'rma': 'Romance',
    'scf': 'Science-Fiction',
    'spt': 'Sport',
    'trl': 'Thriller',
    'war': 'War',
    'wsn': 'Western',
    'fml': 'Family',
    'rly': 'Reality TV',
    'adv': 'Adventure',
    'bio': 'Biography',
    'nws': 'News',
    'rly': 'Reality',
    'shr': 'Short',
    'sof': 'Soap',
    'tlv': 'Talk Show'
    }

def create_query(country,service,genres=None,release_year_from=None,release_year_until=None,headless=True):
    url = "https://www.justwatch.com/"
    try:
        if genres is not None:

            # TODO


def get_movie_list(country,service,genres=None,release_year_from=None,release_year_until=None,headless=True):
    # example "https://www.justwatch.com/uk/provider/amazon-prime-video?genres=ani&release_year_from=1923&release_year_until=1957"
    if headless:
        # Set as headless
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")

        # Set up the Selenium WebDriver
        driver = webdriver.Chrome(options=chrome_options)

    
    else:
        # Set up the Selenium WebDriver
        driver = webdriver.Chrome()

    
            

    










