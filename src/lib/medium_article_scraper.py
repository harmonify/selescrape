from __future__ import annotations
import re
import time
from bs4 import BeautifulSoup
from lib import BaseScraper
from lib.utilities import Config


class MediumArticleScraper(BaseScraper):
    def __init__(self, url: str, file_name: str = "", config: str | Config = "") -> None:
        super().__init__(url, file_name, config, None, 0)

    def fetch_html(self) -> str:
        """
        Fetch the html dynamically using Selenium from the `url` attribute and
        return the html.
        """
        if self.driver is None:
            raise ValueError("Driver is needed to fetch the html")

        self.driver.get(self.url)
        time.sleep(1.5)
        # scroll to bottom of the page
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.html = self.driver.page_source
        return self.html

    def scrape_article_content(self) -> str:
        """
        Scrape the article content from the `html` attribute and return the response.
        It is recommended to use the `fetch_html` method and check the `html`
        attribute before scraping the html.
        """
        if len(self.html) == 0:
            print("No html to scrape")
            return

        # filter out scripts
        soup = BeautifulSoup(self.html, 'html.parser')
        for script in soup.find_all('script'):
            script.extract()

        # delete certain buggy elements when metered content is present
        metered_content_soup = soup.find("article", class_="meteredContent")
        if metered_content_soup:
            metered_content_soup.div.div.extract()

        # append url to bottom right of the article container
        soup.find("article").append(BeautifulSoup(
            f"<br><div style=\"z-index: 999\"><a href=\"{self.url}\" style=\"float: right\">View on Medium</a></div>", 'html.parser'))

        # remove all line endings (lf or crlf)
        self.html = re.sub(r"[\r\n]*", "", str(soup))
        return self.html
