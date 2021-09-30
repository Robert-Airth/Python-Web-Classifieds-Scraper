from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox
from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import WebElement
from bs4 import BeautifulSoup
import time
import re


class SearchOptionPageScraper:
    def __init__(self, output, site):
        self.output_type = output
        self.site = site
        if self.output_type == "file" and self.site == "craigslist":
            self.write_search_options()

    def write_search_options(self):
        driver = webdriver.Firefox(executable_path=r"./driver/geckodriver.exe")
        driver.get("http://craigslist.org/about/sites")

        time.sleep(1)

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        page = driver.page_source
        html_soup = BeautifulSoup(page, "html.parser")

        file = open("CLSearchOptions.txt", "w")

        cl_links = html_soup.find_all("a", {"href": re.compile(r"craigslist\.org/")})
        continent_names = html_soup.find_all("h1")
        continents_container = html_soup.find_all("div", {"class": "colmask"})

        for continent_name, continent in zip(continent_names, continents_container):
            file.write(
                "\n++++++++++++++++++++++++++\n        "
                + continent_name.text
                + "\n++++++++++++++++++++++++++\n"
            )
            states = continent.findChildren("h4")
            cities_lists = continent.findChildren("ul")
            for state, state_cities in zip(states, cities_lists):
                file.write(
                    "\n-------------------------\n"
                    + "            "
                    + state.text
                    + "\n-------------------------\n"
                )
                cities = state_cities.findChildren("li")
                for city in cities:
                    file.write(city.text + "\n    " + city.a.get("href") + "\n\n")

        file.close()


SearchOptionPageScraper("file", "craigslist")
