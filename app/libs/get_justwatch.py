# Queries Justwatch.com using selenium to get titles

import geopy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm


def get_JUSTWATCH_COUNTRIES():
    return {
        'united arab emirates': 'ae',
        'argentina': 'ar',
        'austria': 'at',
        'australia': 'au',
        'belgium': 'be',
        'brazil': 'br',
        'canada': 'ca',
        'switzerland': 'ch',
        'chile': 'cl',
        'colombia': 'co',
        'czech republic': 'cz',
        'germany': 'de',
        'denmark': 'dk',
        'ecuador': 'ec',
        'estonia': 'ee',
        'spain': 'es',
        'finland': 'fi',
        'france': 'fr',
        'united kingdom': 'gb',
        'greece': 'gr',
        'hong kong': 'hk',
        'hungary': 'hu',
        'indonesia': 'id',
        'ireland': 'ie',
        'india': 'in',
        'italy': 'it',
        'japan': 'jp',
        'south korea': 'kr',
        'lithuania': 'lt',
        'latvia': 'lv',
        'mexico': 'mx',
        'malaysia': 'my',
        'netherlands': 'nl',
        'norway': 'no',
        'new zealand': 'nz',
        'peru': 'pe',
        'philippines': 'ph',
        'poland': 'pl',
        'portugal': 'pt',
        'romania': 'ro',
        'russia': 'ru',
        'sweden': 'se',
        'singapore': 'sg',
        'slovakia': 'sk',
        'thailand': 'th',
        'turkey': 'tr',
        'taiwan': 'tw',
        'england': 'uk',
        'united states': 'us',
        'venezuela': 've',
        'south africa': 'za'
    }


def get_JUSTWATCH_GENRES():
    return {
        'action': 'act',
        'animation': 'ani',
        'comedy': 'cmy',
        'crime': 'crm',
        'documentary': 'doc',
        'drama': 'drm',
        'fantasy': 'fnt',
        'horror': 'hrr',
        'history': 'hst',
        'music': 'msc',
        'romance': 'rma',
        'science-fiction': 'scf',
        'sport': 'spt',
        'thriller': 'trl',
        'war': 'war',
        'western': 'wsn',
        'family': 'fml',
        'reality tv': 'rly',
        'adventure': 'adv',
        'biography': 'bio',
        'news': 'nws',
        'reality': 'rly',
        'short': 'shr',
        'soap': 'sof',
        'talk show': 'tlv'
    }


def get_JUSTWATCH_PROVIDERS():
    return {
        'netflix': 'nfx',
        'prime': 'prv',
        'disney': 'dnp',
        'apple': 'itu',
        'crunchyroll': 'cru',
        'mubi': 'mbi',
        'hayu': 'hay',
    }


def get_justwatch_query_url(country, service, genre=None, release_year_from=None, release_year_until=None):
    #  example "https://www.justwatch.com/uk/provider/amazon-prime-video?genres=ani&release_year_from=1923&release_year_until=1957"
    # get country
    JUSTWATCH_COUNTRIES_DICT = get_JUSTWATCH_COUNTRIES()
    country = JUSTWATCH_COUNTRIES_DICT[country.lower()]

    # TODO get one of their service providers randomly or get chatgpt to return one?
    JUSTWATCH_SERVICES_DICT = get_JUSTWATCH_PROVIDERS()
    service = JUSTWATCH_SERVICES_DICT[service.lower()]

    url = f"https://www.justwatch.com/{country}?providers={service}"

    try:

        if genre is not None:
            JUSTWATCH_GENRES_DICT = get_JUSTWATCH_GENRES()
            url = url + f"&genres={JUSTWATCH_GENRES_DICT[genre.lower()]}"

        if release_year_from is not None:
            url = url+f"&release_year_from={release_year_from}"

        if release_year_until is not None:
            url = url+f"&release_year_until={release_year_until}"

        return url
    except Exception as e:
        print(e)

        return f"Error {e}"


def get_movie_list(country, service, genre=None, release_year_from=None, release_year_until=None, headless=True):
    # get url
    url = get_justwatch_query_url(
        country, service, genre, release_year_from, release_year_until)

    if headless:
        # Set as headless
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        # Set up the Selenium WebDriver
        driver = webdriver.Chrome(options=chrome_options)

    else:
        # Set up the Selenium WebDriver
        driver = webdriver.Chrome()

        # Load the webpage
    driver.get(url)

    # Wait until elements are loaded (adjust the class name based on the actual structure)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "title-list-grid__item"))
    )

    # Initialize variables
    items_to_load = 200
    loaded_items = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    while loaded_items < items_to_load:
        # Scroll down
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load

        # Get current page content
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all title items
        title_items = soup.find_all('div', class_='title-list-grid__item')
        loaded_items = len(title_items)
        print(f"Loaded items: {loaded_items}")

        # Check scroll position
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    movies = []
    # Process items
    for item in title_items[:items_to_load]:
        try:
            # Find the image element
            img = item.find('img', class_='picture-comp__img')

            
            if img:
                title = img.get('alt', 'No title')
                image_url = img.get('src', 'No image')
                link = item.find('a')['href']

                print(f"Title: {title}")
                print(f"Image URL: {image_url}")
                print(f"Link to info page: {link}")
                print("-" * 40)

                movies.append({"title":title,"image_url":image_url,"info_url":link})
        except Exception as e:
            print(f"Error processing item: {e}")

    driver.quit()

    selected_movies_with_description = random_movies_description(movies_list=movies)

    return selected_movies_with_description

# TODO get random movie from list, get information and return all info.

def get_movie_info(info_url):
    # info_url has country/movie name e.g. /uk/movie/gift-wrapped")


    chrome_options = Options()
    chrome_options.add_argument("--headless=new")

    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    description = None

    try:
        # Load the page
        driver.get("https://www.justwatch.com"+info_url)

        # Wait for the description element to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text-wrap-pre-line"))
        )

        # Get the page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the description element
        description = soup.find('p', class_='text-wrap-pre-line')

        if description:
            description = description.text.strip()
            print("Description:", description)
            return description
        else:
            print("Description not found")
            return "ERROR"
            

    except Exception as e:
        print(f"An error occurred: {e}")
        return "{e}"

    finally:
        driver.quit()


    

def random_movies_description(movies_list):
    """Pick 5 movies, or less if there is less than that in the returned list, and get movie descriptions for them, for chatgpt to pick"""
    final_list = []
    
    # min between movie list length and 5
    iter =min(len(movies_list),5)

    for i in tqdm(range(iter)):
        movie = movies_list[random.randrange(iter)]
        info = get_movie_info(movie["info_url"])
        movie["description"] = info
        final_list.append(movie)

        i+=1
    
    return final_list


if __name__ == "__main__":
    import random

    movies = get_movie_list(country="thailand", service="Netflix",
                   genre="Action", release_year_from=2000, release_year_until=2014)
    
    print(movies)
    

    # movie_info = get_movie_info(movies[random.randrange(1,len(movies))]["info_url"])
    
    
