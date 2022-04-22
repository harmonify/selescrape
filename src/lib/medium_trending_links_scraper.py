from __future__ import annotations
import os
import re
from typing import List
from bs4 import BeautifulSoup
from lib import BaseScraper
from lib.utilities import Config


class MediumTrendingLinksScraper(BaseScraper):
    def __init__(self, url: str, file_name: str = "", config: str | Config = "") -> None:
        super().__init__(url, file_name, config, None, 0)
        self.trending_links = []

    def scrape_trending_links(self) -> List[str]:
        """
        Scrape trending article links from the `html` attribute and return the response.
        It is recommended to use the `fetch_html` method and check the `html`
        attribute before scraping the html.
        """
        if len(self.html) == 0:
            print("No html to scrape")
            return []

        soup = BeautifulSoup(self.html, 'html.parser')
        # find all links in trending posts
        # implementation: find all article links in .pw-trending-post .am.cy and the second .hm.y
        print("Scraping trending links")
        for article in soup.find_all(class_="pw-trending-post"):
            link = article.find(class_="am cy").find_all(
                class_="hm y")[1].find("a").get("href")
            if re.match(r'^/[^@]', link):
                link = "https://medium.com" + link
            self.trending_links.append(link)
        print(f"Done. Found {len(self.trending_links)} links")
        return self.trending_links

    def save_trending_links(self, output_file_name=None) -> None:
        """
        Save the trending article links to a file. It is recommended to use the
        `scrape_trending_links` method and check the `trending_links` attribute
        before saving the links.
        """
        if len(self.trending_links) == 0:
            print("No trending links to save")
            return

        output_path = os.path.join(
            self.config.data["output_dir_path"], output_file_name or self.output_file_name) + ".txt"

        print(
            f"Saving {len(self.trending_links)} trending links to {output_path}")
        with open(f"{output_path}", 'w', newline="\n") as f:
            for link in self.trending_links:
                f.write(f"{link}\n")
        print("Done")
