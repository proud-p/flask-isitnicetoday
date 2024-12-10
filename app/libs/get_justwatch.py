# Queries Justwatch.com using selenium to get titles

import geopy
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
from multiprocessing import Pool

multiprocessing.freeze_support()


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
        'united kingdom': 'uk',
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
    # Generate the URL for JustWatch
    url = get_justwatch_query_url(country, service, genre, release_year_from, release_year_until)

    # Set up the WebDriver with optional headless mode
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Load the webpage
        driver.get(url)

        # Wait until elements are loaded
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "title-list-grid__item"))
        )

        # FIXME not sure why this is not paginating, so it's loading 100 eventhough I put 200. But moving on for now
        # Initialize variables
        items_to_load = 200  # Target number of items to load
        loaded_items = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        retries = 5  # Stop if no new items load after 5 attempts
        retry_count = 0

        while loaded_items < items_to_load and retry_count < retries:
            # Scroll to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Allow time for content to load

            # Parse the page content
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all movie items
            title_items = soup.find_all('div', class_='title-list-grid__item')
            new_loaded_items = len(title_items)

            if new_loaded_items == loaded_items:
                # No new items loaded
                retry_count += 1
                print(f"No new items loaded. Retry {retry_count}/{retries}")
            else:
                # New items found
                loaded_items = new_loaded_items
                retry_count = 0
                print(f"Loaded items: {loaded_items}")

            # Check scroll height to prevent infinite scrolling
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Process the loaded movies
        movies = []
        for item in title_items[:items_to_load]:
            try:
                # Extract movie details
                img = item.find('img', class_='picture-comp__img')
                if img:
                    title = img.get('alt', 'No title')
                    image_url = img.get('src', 'No image')
                    link = item.find('a')['href']

                    print(f"Title: {title}")
                    print(f"Image URL: {image_url}")
                    print(f"Link to info page: {link}")
                    print("-" * 40)

                    movies.append({"title": title, "image_url": image_url, "info_url": link})
            except Exception as e:
                print(f"Error processing item: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    # Fetch descriptions for a subset of movies (5 or fewer)
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


def fetch_movie_info_process(movie):
    """
    Helper function to fetch movie description in a process-safe manner.
    """
    try:
        movie["description"] = get_movie_info(movie["info_url"])
        return movie
    except Exception as e:
        print(f"Error processing movie {movie['title']}: {e}")
        return None

def random_movies_description(movies_list):
    """
    Fetch descriptions for up to 5 movies using multiprocessing for parallel execution.
    """
    final_list = []
    iter_count = min(len(movies_list), 5)  # Fetch up to 5 movies

    # Randomly sample movies if the list is longer than 5
    sampled_movies = random.sample(movies_list, iter_count)

    # Determine number of processes (use fewer processes than CPU cores)
    num_processes = min(multiprocessing.cpu_count() - 1, iter_count)
    num_processes = max(1, num_processes)  # Ensure at least 1 process

    try:
        with Pool(processes=num_processes) as pool:
            # Use tqdm to show progress
            results = list(tqdm(
                pool.imap(fetch_movie_info_process, sampled_movies),
                total=len(sampled_movies),
                desc="Fetching movie descriptions"
            ))

            # Filter out None results and add successful ones to final list
            final_list = [result for result in results if result is not None]

    except Exception as e:
        print(f"Error in multiprocessing: {e}")

    return final_list

def driver_example(country, service, genre=None, release_year_from=None, release_year_until=None, headless=True):
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
    items_to_load = 500  # Target number of items
    loaded_items = 0
    retries = 5  # Number of retries to stop if no more items are loading
    retry_count = 0

    while loaded_items < items_to_load and retry_count < retries:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for content to load

        # Get current page content
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all title items
        title_items = soup.find_all('div', class_='title-list-grid__item')
        new_loaded_items = len(title_items)

        # Check if new items were loaded
        if new_loaded_items == loaded_items:
            retry_count += 1
            print(f"No new items loaded. Retry {retry_count}/{retries}")
        else:
            loaded_items = new_loaded_items
            retry_count = 0  # Reset retry count if new items are loaded
            print(f"Loaded items: {loaded_items}")

    # Process the items
    movies = []
    for item in tqdm(title_items[:items_to_load]):
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

                movies.append({"title": title, "image_url": image_url, "info_url": link})
        except Exception as e:
            print(f"Error processing item: {e}")

    driver.quit()
    return movies




if __name__ == "__main__":
    import random

    # driver_example(country="thailand", service="Netflix",
    #                genre="Action", release_year_from=2000, release_year_until=2014, headless=False)

    # movies = get_movie_list(country="thailand", service="Netflix",
    #                genre="Action", release_year_from=2000, release_year_until=2014, headless=False)
    
    # print(movies)
    

    # movie_info = get_movie_info(movies[random.randrange(1,len(movies))]["info_url"])


    import multiprocessing
    multiprocessing.freeze_support()

    try:
        movies = get_movie_list(
            country="thailand", 
            service="Netflix",
            genre="Action", 
            release_year_from=2000, 
            release_year_until=2014, 
            headless=True
        )
        print(f"Found {len(movies)} movies with descriptions")
        
        print(movies)
    except Exception as e:
        print(f"Error in main execution: {e}")
    
    