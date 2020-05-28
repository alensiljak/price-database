'''
Store configuration in YAML format,
in user's configuration directory.
'''


class Configuration:
    def __init__(self):
        self.config_file_name = "config.yaml"
        self.app_name = "pricedb"
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
        import os

        # Create the config folder
        dir = self.get_config_dir()
        if not os.path.exists(dir) and not os.path.isdir(dir):
            os.makedirs(dir)
        # Create file
        path = self.getConfigPath()
        if os.path.exists(path):
            return

        with open(path, "w") as config_file:
            content = self.get_template()
            config_file.write(content)

    def get_template(self):
        return '''# Configuration
export_destination: 
        '''

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

    @property
    def export_destination(self):
        value = self.config["export_destination"]
        return value
