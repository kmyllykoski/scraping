from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# =============================================================
# Scraping weather data from Foreca.fi for Porvoo
# Initial attemtpt used requests and BeautifulSoup, but the page
# content is generated dynamically after page is loaded in the browser.
# This can be verified by comparing the DOM content in the browser's
# developer tools and the HTML content fetched with requests.
# Therefore, we use Playwright to load the page in a headless browser
# and get the fully rendered HTML content to parse with BeautifulSoup.
#
# To run this script:
# - Install UV package management if not already installed: https://docs.astral.sh/uv/getting-started/installation/
# - uv init
# - uv add beautifulsoup4
# - uv add playwright
# - uv run playwright install 

do_get_from_web = False

# =============================================================
# Two options:
#   1. Get the HTML content from the web using Playwright
#   2. Read the HTML content from a saved local file
#
if do_get_from_web:
    with sync_playwright() as p:
        for browser_type in [p.chromium]:
            browser = browser_type.launch()
            page = browser.new_page()
            page.goto('https://www.foreca.fi/Finland/Porvoo')
            html = page.content()
            # print(html)
            browser.close()

            # save html to file
            with open('pw_foreca_porvoo.html', 'w', encoding='utf-8') as f:
                f.write(html)

else:
    # read the saved html file and parse with BeautifulSoup and lxml
    with open('pw_foreca_porvoo.html', 'r', encoding='utf-8') as f:
        html = f.read()

# =============================================================
# Parse the HTML content with BeautifulSoup and extract data:
# - current temperature
# - feels like temperature
# - date and time of the observation

# Parse with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# There is a div with id 'obscontainer' that contains the data needed
obs_container = soup.find('div', id='obscontainer')

# get date and time information from the second div class="r"
date_and_time = obs_container.find_all('div', class_='r')[1].text
print('-' * 40)
print(f"Viimeisin havainto: {date_and_time}")

# inside div id='obscontainer', there is a div with class 'temp' that contains temperature information
temp = obs_container.find('div', class_='temp')
# print(temp.prettify())

# get first p element inside div class="temp" that contains current temperature
p_temp = temp.find('p')
# print(p_temp.prettify())
temp_celcius_s = p_temp.text
temp_celcius_f = float(temp_celcius_s.split(' ')[0].replace(',', '.'))
print(temp_celcius_f)
print(f"Lämpötila Porvoossa: {temp_celcius_s}")

# get next p element inside div class="temp" that contains feels like temperature
p_feels_like = p_temp.find_next_sibling('p')
# print(p_feels_like.prettify())
feels_like_s = p_feels_like.text
# feels_like_f = float(feels_like_s.replace('Tuntuu kuin\xa0', '').replace('\xa0°C', ''))
feels_like_f = float(feels_like_s.split(' ')[2][:-1].replace(',', '.'))
print(feels_like_f)
print(f"{feels_like_s}")



