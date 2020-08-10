'''
Store configuration in YAML format,
in user's configuration directory.
'''


class Configuration:
    def __init__(self):
        self.config_file_name = "config.yaml"
        #self.app_name = "pricedb"
        self.app_name = __name__
        self.create_config_file()
        self.config = self.read_config_content()

    def read_config_content(self):
        ''' Read configuration file '''
        import yaml

        path = self.getConfigPath()
        content = ''
        with open(path, 'r') as stream:
            try:
                content = yaml.safe_load(stream)
                # print(content)
            except yaml.YAMLError as exc:
                print(exc)

        return content

    def create_config_file(self):
        ''' create the config file if it does not exist '''
        from usersconfig.configuration import Configuration

        cfg = Configuration(__name__)
        cfg.create_default_config_file()

    # @property
    def get_config_dir(self):
        from xdg.BaseDirectory import xdg_config_home
        from os.path import sep

        return xdg_config_home + sep + self.app_name

    # @property
    def getConfigPath(self):
        ''' assembles the path to the config file '''
        from os.path import sep

        return self.get_config_dir() + sep + self.config_file_name
