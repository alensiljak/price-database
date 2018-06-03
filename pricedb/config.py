"""
Configuration handling
The config file is stored in data directory and is located by using Resources.
Ref: http://peak.telecommunity.com/DevCenter/setuptools#non-package-data-files
"""
import io
import os.path
import shutil
from configparser import ConfigParser
from enum import Enum, auto
import logging

from pkg_resources import Requirement, resource_filename

package_name = "PriceDb"
template_path = "pricedb/templates/"
config_filename = "pricedb.ini"
SECTION = "Default"


class ConfigKeys(Enum):
    price_database = auto(),
    alphavantage_api_key = auto()
    fixerio_api_key = auto()


class Config:
    """ Reads and writes Asset Allocation config file """

    def __init__(self, ini_path: str = None):
        self.logger = logging.getLogger(__name__)

        # Read the config file on creation of the object.
        self.config = ConfigParser()

        if not ini_path:
            # use the default path.
            file_path = os.path.abspath(self.get_config_path())
            # copy the template if file does not yet exist
            if not os.path.exists(file_path):
                self.__create_user_config()
        else:
            file_path = os.path.abspath(ini_path)

        self.__read_config(file_path)

    def delete_user_config(self):
        """ Delete current user's config file """
        file = self.get_config_path()
        os.remove(file)

    def __read_config(self, file_path: str):
        """ Read the config file """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File path not found: {file_path}")
        # check if file exists
        if not os.path.isfile(file_path):
            self.logger.error(f"file not found: {file_path}")
            raise FileNotFoundError(f"configuration file not found {file_path}")

        self.config.read(file_path)

    def __get_config_template_path(self) -> str:
        """ gets the default config path from resources """
        filename = resource_filename(
            Requirement.parse(package_name),
            template_path + config_filename)
        return filename

    def __get_user_path(self) -> str:
        """ Returns the current user's home directory """
        return os.path.expanduser("~")

    def __create_user_config(self):
        """ Copy the config template into user's directory """
        src_path = self.__get_config_template_path()
        src = os.path.abspath(src_path)

        if not os.path.exists(src):
            message = f"Config template not found {src}"
            self.logger.error(message)
            raise FileNotFoundError(message)

        dst = os.path.abspath(self.get_config_path())

        shutil.copyfile(src, dst)

        if not os.path.exists(dst):
            raise FileNotFoundError("Config file could not be copied to user dir!")

    def get_config_path(self) -> str:
        """
        Returns the path where the active config file is expected.
        This is the user's profile folder.
        """
        dst_dir = self.__get_user_path()
        dst = dst_dir + "/" + config_filename
        return dst

    def get_contents(self) -> str:
        """ Reads the contents of the config file """
        content = None
        # with open(file_path) as cfg_file:
        #     contents = cfg_file.read()

        # Dump the current contents into an in-memory file.
        in_memory = io.StringIO("")
        self.config.write(in_memory)
        in_memory.seek(0)
        content = in_memory.read()
        #     log(DEBUG, "config content: %s", content)
        in_memory.close()
        return content

    def set(self, option: ConfigKeys, value):
        """ Sets a value in config """
        assert isinstance(option, ConfigKeys)

        # As currently we only have 1 section.
        section = SECTION
        self.config.set(section, option.name, value)
        self.save()

    def get(self, option: ConfigKeys):
        """ Retrieves a config value """
        assert isinstance(option, ConfigKeys)

        # Currently only one section is used
        section = SECTION
        return self.config.get(section, option.name)

    def save(self):
        """ Save the config file """
        file_path = self.get_config_path()
        contents = self.get_contents()
        with open(file_path, mode='w') as cfg_file:
            cfg_file.write(contents)
