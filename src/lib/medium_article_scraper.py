from __future__ import annotations
from bs4 import BeautifulSoup
from lib import BaseScraper


class MediumArticleScraper(BaseScraper):
    def __init__(self, url: str, file_name: str = "", config_name: str = "", wait_for: str | None = None, wait_timeout: int = 0) -> None:
        super().__init__(url, file_name, config_name, wait_for, wait_timeout)

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

        # append url to article container
        # TODO: as metered content can't be fetch directly for now
        soup.find("article").append(BeautifulSoup(
            f"<br><div style=\"z-index: 999\"><a href=\"{self.url}\" style=\"float: right\">View on Medium</a></div>", 'html.parser'))

        self.html = str(soup)
        return self.html
