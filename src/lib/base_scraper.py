from __future__ import annotations
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.utilities import Config, construct_file_name_from_url


class BaseScraper:
    """
    The base scraper class with basic functionality.

    Attributes:
    - `url`: the url to scrape
    - `output_file_name`: the file name to save the html
    - `config`: the configuration object (default: `Config('selescrape.json')`)
    - `wait_for_selector`: the css selector to wait for before returning the html
    - `wait_for_selector_timeout`: the timeout in seconds to wait for the element
    - `html`: the html content (available after calling `fetch_html`)
    - `output_file_path`: the file path to save the html
    - `driver`: the Selenium driver
    - `display_url`: the url to display in non-verbose mode
    - `display_output_file_path`: the file path to display in non-verbose mode

    Methods:
    - `fetch_html()`: fetch the html from the `url` attribute and return the html
    - `save_html()`: save the html to `{config["output_dir_path"]}/{output_file_name}`
    """

    def __init__(self, url: str, output_file_name: str = "", config: str | Config = "", wait_for_selector: str | None = None, wait_for_selector_timeout: int = 0) -> None:
        self._init_url_attribute(url)
        self.output_file_name = output_file_name or construct_file_name_from_url(
            url)
        self.wait_for_selector = wait_for_selector
        self.wait_for_selector_timeout = wait_for_selector_timeout or 0
        self.html = ""
        self._init_config_attribute(config)
        self._init_output_file_path_attribute()
        self._init_driver_attribute()
        self._init_display_attributes()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} url={self.url} output_file_name={self.output_file_name}>"

    def _init_url_attribute(self, url: str) -> None:
        """ Initialize the `url` attribute. """
        if not url or url.startswith("http://") or url.startswith("https://"):
            self.url = url
        else:
            self.url = f"https://{url}"

    def _init_config_attribute(self, config: str | Config) -> None:
        """ Initialize the `config` attribute. """
        if isinstance(config, str):
            self.config = Config(config or "selescrape.json")
        else:
            self.config = config

    def _init_output_file_path_attribute(self) -> None:
        """ Set the `output_file_path` from `output_file_name` attribute. """
        self.output_file_path = os.path.join(
            self.config.data["output_dir_path"],
            self.output_file_name.removesuffix(".html") + ".html"
        )

    def _init_driver_attribute(self) -> None:
        """ Initialize the Selenium driver and set the `driver`. """
        option = webdriver.FirefoxOptions()
        # I use the following options as my machine is a window subsystem linux.
        # I recommend to use the headless option at least, out of the 3
        option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-sh-usage')
        # replace \\ with / in path if in windows
        if os.name == "nt":
            driver_path = self.config.data["driver_path"].replace("\\", "/")
        self.driver = webdriver.Firefox(
            executable_path=driver_path, options=option)

    def _init_display_attributes(self) -> None:
        """ Initialize attributes for display purposes. """
        if not self.url:
            self.display_url = None
        else:
            self.display_url = self.url[:50] + \
                "..." if not self.config.data["verbose_mode"] else self.url
        self.display_output_file_path = self.output_file_path[:50] + \
            "..." if not self.config.data["verbose_mode"] else self.output_file_path

    def fetch_html(self) -> str:
        """
        Scrape the html from the given url and return the response. Use Selenium
        to fetch html dynamically when the `driver_path` config key is set.
        """
        if self.url == "" or self.url is None:
            raise ValueError("url is empty")

        print(f"Fetching html from {self.display_url}")
        if self.config.data["driver_path"]:
            self.html = self._fetch_html_with_selenium()
        else:
            self.html = self._fetch_html_with_requests()
        print("Done")
        return self.html

    def _fetch_html_with_requests(self) -> str:
        """
        Scrape the html from the given url with Python `requests` module
        and return the response.
        """
        return requests.get(self.url).content.decode("utf-8")

    def _fetch_html_with_selenium(self) -> str:
        """
        Scrape the html from the given url with Selenium and geckodriver
        (Firefox driver) and return the response.
        """
        self.driver.get(self.url)
        if self.wait_for_selector:
            WebDriverWait(self.driver, self.wait_for_selector_timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, self.wait_for_selector)))
        return self.driver.page_source

    def load_html(self, file_path: str) -> str:
        """
        Load the html from the given `file_path`, set the `html` attribute
        and return the html.
        """
        if self.config.data['verbose_mode']:
            display_file_path = file_path
        else:
            display_file_path = file_path[:50] + "..."

        print(f"Loading html from {display_file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            self.html = f.read()
        print("Done")
        return self.html

    def save_html(self) -> None:
        """
        Save the `html` attribute to the file using `output_file_path` attribute.
        Raise `FileExistsError` if the file already exists and user chooses
        to not overwrite the file.
        """
        print(f"Saving html to {self.display_output_file_path}")
        if os.path.exists(self.output_file_path):
            if input(f"{self.output_file_path} already exists. Overwrite? (y/n)") == "y":
                os.remove(self.output_file_path)
            else:
                raise FileExistsError(
                    f"{self.output_file_path} already exists")
        with open(self.output_file_path, 'w', encoding="utf-8", newline="\n") as f:
            f.write(self.html)
        print("Done")
