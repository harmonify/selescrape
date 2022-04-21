import datetime
from urllib.parse import urlparse


def get_file_name_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    # construct normalized url
    return "".join([
        parsed_url.netloc,
        parsed_url.path.replace("/", "_"),
        parsed_url.query,
        parsed_url.fragment
    ]) + datetime.datetime.now().strftime("_%Y_%m_%d_%H_%M_%S")
