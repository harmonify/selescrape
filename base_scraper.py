from __future__ import annotations
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.config import Config
from utilities.get_file_name_from_url import get_file_name_from_url


class BaseScraper:
    def __init__(self, url: str, file_name: str = "", config_name: str = "", wait_for: str | None = None, wait_timeout: int = 0) -> None:
        """
        Initialize the scraper.

        Attributes:
        url: the url to scrape
        file_name: the file name to save the html
        config_name: the config file name (default: selescrape.json)
                     in the same directory
        wait_for: the css selector to wait for before scraping
        wait_timeout: the timeout in seconds to wait for the element

        Methods:
        fetch_html: fetch the html from the `url` attribute and return the html
        save_html: save the html to `{config["output_dir_path"]}/{file_name}`
        get_file_path: get the file path from `file_name` attribute
        """
        self.url = url
        self.file_name = file_name or get_file_name_from_url(url)
        self.config_name = config_name or "selescrape.json"
        self.wait_for = wait_for
        self.wait_timeout = wait_timeout or 0
        self.html = ""
        self.config = Config(self.config_name).data
        self.file_path = self.get_file_path()
        self.display_url = self.url[:50] + \
            "..." if not self.config["verbose_mode"] else self.url
        self.display_file_path = self.file_path[:50] + \
            "..." if not self.config["verbose_mode"] else self.file_path

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} url={self.url} file_name={self.file_name}>"

    def fetch_html(self) -> str:
        """
        Scrape the html from the given url and return the response. Use Selenium
        to fetch html dynamically when the `driver_path` config key is set.
        """
        print(f"Fetching html from {self.display_url}")
        if self.config["driver_path"]:
            self.html = self._fetch_html_with_selenium(
                self.url, self.wait_for, self.wait_timeout)
        else:
            self.html = self._fetch_html_with_requests(self.url)
        print("Done")
        return self.html

    def _fetch_html_with_requests(self, url: str) -> str:
        """
        Scrape the html from the given url with Python `requests` module
        and return the response.
        """
        return requests.get(url).content.decode("utf-8")

    def _fetch_html_with_selenium(self, url: str, wait_for: str | None, wait_timeout: int) -> str:
        """
        Scrape the html from the given url with Selenium and geckodriver
        (Firefox driver) and return the response.
        """
        option = webdriver.FirefoxOptions()
        # I use the following options as my machine is a window subsystem linux.
        # I recommend to use the headless option at least, out of the 3
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-sh-usage')
        # replace \\ with / in path if in windows
        if os.name == "nt":
            driver_path = self.config["driver_path"].replace("\\", "/")
        driver = webdriver.Firefox(executable_path=driver_path, options=option)

        # Getting page HTML through request
        driver.get(url)
        if wait_for:
            WebDriverWait(driver, wait_timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, wait_for)))
        return driver.page_source

    def save_html(self) -> None:
        """ Save the html to the file. """
        print(f"Saving html to {self.display_file_path}")
        with open(self.file_path, 'w', encoding="utf-8") as f:
            f.write(self.html)
        print("Done")

    def get_file_path(self) -> str:
        """ Get the file path from `file_name` attribute. """
        file_path = os.path.join(self.config["output_dir_path"], self.file_name.removesuffix(
            ".html") + ".html")
        if os.path.exists(file_path):
            if input(f"{file_path} already exists. Overwrite? (y/n)") == "y":
                os.remove(file_path)
            else:
                raise FileExistsError(f"{file_path} already exists")
        return file_path


def main(args=None):
    """
    Main function.

    Command line syntax:
    python base_scraper.py <url> [file_name] [config_name] [wait_for] [wait_timeout]

    <> are required arguments
    [] are optional arguments
    """
    try:
        # initialize scraper
        url = ""
        while url == "":
            url = args[0] if len(args) >= 1 else input("Enter URL: ")
        file_name = args[1] if len(args) >= 2 else input(
            "Enter file name (default is auto-generated): ")
        config_name = args[2] if len(args) >= 3 else input(
            "Enter config name (default: selescrape.json): ")
        wait_for = args[3] if len(args) >= 4 else input(
            "Enter wait for selector when fetching html (default: None): ")
        wait_timeout = args[4] if len(args) >= 5 else input(
            "Enter wait timeout when fetching html (default: 0): ")
        scraper = BaseScraper(url, file_name, config_name,
                              wait_for, wait_timeout)

        # run scraper
        scraper.fetch_html()
        scraper.save_html()
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
