import datetime
from urllib.parse import urlparse


def construct_file_name_from_url(url: str) -> str:
    """
    Construct a file name from the given url.
    """
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if not url:
        return now

    parsed_url = urlparse(url)
    return "".join([
        parsed_url.netloc,
        parsed_url.path.replace("/", "_"),
        parsed_url.query,
        parsed_url.fragment
    ]) + f"_{now}"
