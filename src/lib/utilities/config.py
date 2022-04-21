from __future__ import annotations
import json
import os


class Config:
    def __init__(self, name: str = "selescrape.json") -> None:
        """
        Initialize the config.

        Attributes:
        name: the config file name (default: selescrape.json) in the root directory
        __location__: the path of the config script

        Methods:
        read_config: read the config file and return the config dict
        initialize_config: initialize the config file and return the config dict
        """
        self.__location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.__project_root__ = os.path.realpath(
            os.path.join(self.__location__, "..", "..", ".."))
        self.name = name
        # file_path: the path of the config file (defaulting to selescrape.json
        # in the project root directory)
        self.file_path = os.path.join(self.__project_root__, self.name)
        self.data = self.read_config()

    def __repr__(self) -> str:
        return f"Config('{self.name}')"

    def read_config(self) -> dict[str, str]:
        """ Read the config file and return the data. """
        try:
            print(f"Reading {self.file_path}")
            if os.path.isdir(self.file_path):
                raise FileNotFoundError(
                    f"{self.file_path} is a directory, not a file")
            elif os.path.isfile(self.file_path):
                print(f"{self.file_path} is a file")
                with open(self.file_path, "r") as f:
                    data = json.loads(f.read())
            else:
                print(f"{self.file_path} does not exist")
                data = self.initialize_config()
            print("Done")
            return data
        except FileNotFoundError as e:
            print(e)
            exit(1)
        except json.JSONDecodeError:
            print(f"{self.file_path} is not a valid JSON file")
            exit(1)

    def initialize_config(self) -> dict[str, str]:
        """ Initialize the config file and return the data. """
        print(f"Initializing {self.name}")
        # constants
        data = {
            "app": "selescrape",
            "version": "1.0",
        }

        # user input
        data["output_dir_path"] = self._input_output_dir_path()
        data["driver_path"] = self._input_driver_path()
        data["verbose_mode"] = self._input_verbose_mode()

        # write config
        with open(self.file_path, "w") as f:
            f.write(json.dumps(data))
        print(f"{self.file_path} is created")
        return data

    def _input_output_dir_path(self) -> str:
        """
        Input the output directory path.

        Returns:
        The output directory path.
        """
        while True:
            print(
                "\nEnter the output directory path (e.g. /home/user/selescrape-output)")
            print("Default: '<script-location>/selescrape-output/'")
            output_dir = input(": ") or os.path.join(
                self.__project_root__, "selescrape-output")

            # check if user specify a relative path or absolute path
            if os.path.isabs(output_dir):
                output_dir_path = os.path.realpath(output_dir)
            else:
                output_dir_path = os.path.realpath(
                    os.path.join(os.getcwd(), *output_dir.split("/")))

            if not os.path.isdir(output_dir_path):
                print(f"{output_dir_path} is not a directory")
                if input("Create directory (y/n)? ") == "y":
                    os.makedirs(output_dir_path)
                    print(f"{output_dir_path} is created")
                    break
            else:
                print(f"\n{output_dir_path} is a directory")
                if input("Is this the right path (y/n)? ") == "y":
                    break
        return output_dir_path

    def _input_driver_path(self) -> str | None:
        """
        Input the driver path.

        Returns:
        The driver path.
        """
        print("\nDo you want to use Selenium and WebDriver to scrape? (y/n)")
        if input(": ") == "y":
            while True:
                print("\nEnter the path of the driver (e.g. /home/user/geckodriver)")
                driver_path = input(": ")

                # check if user specify a relative path or absolute path
                if os.path.isabs(driver_path):
                    driver_path = os.path.realpath(driver_path)
                else:
                    driver_path = os.path.realpath(
                        os.path.join(os.getcwd(), *driver_path.split("/")))

                if not os.path.isfile(driver_path):
                    print(f"{driver_path} is not a file")
                else:
                    print(f"{driver_path} is a file")
                    if input("Is this the right path (y/n)? ") == "y":
                        break
            return driver_path

    def _input_verbose_mode(self) -> bool:
        """
        Input the is verbose logging.

        Returns:
        The verbose logging.
        """
        print("\nDo you want to enable verbose logging? (y/n)")
        print("Default: False")
        if input(": ") == "y":
            return True
        else:
            return False


def main(args=None):
    try:
        config = Config("selescrape.json")
        print("==========================")
        print(config.initialize_config())
        print("==========================\n")

        print("==========================")
        print(config.read_config())
        print("==========================\n")
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == '__main__':
    main()
