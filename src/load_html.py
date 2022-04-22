import os
from lib import BaseScraper


def main(args=None):
    """
    Main function.

    Command line syntax:
    python load_html.py <url> [file_name] [config] [wait_for] [wait_timeout]

    <> are required arguments
    [] are optional arguments
    """
    try:
        # initialize scraper
        url = None
        input_file_path = args[0] if args else input(
            "Enter html file path to load: ")
        output_file_name = args[1] if len(args) >= 2 else input(
            "Enter output file name (default is auto-generated): ")
        config = args[2] if len(args) >= 3 else input(
            "Enter config name (default: selescrape.json): ")
        wait_for = None
        wait_timeout = 0
        scraper = BaseScraper(url, output_file_name, config,
                              wait_for, wait_timeout)
        # run scraper
        scraper.load_html(os.path.abspath(input_file_path))
        if input("Print html? (y/n): ") == "y":
            print(scraper.html)
        if input("Save html? (y/n): ") == "y":
            scraper.save_html()
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
