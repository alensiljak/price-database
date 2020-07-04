'''
CLI for configuration manipulation
'''
import click
import click_log
import logging

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group("cfg")
@click_log.simple_verbosity_option(logger)
def config_cli():
    """ Configuration management """
    pass


@click.command("show")
def show_config():
    ''' Display the current configuration '''
    from pricedb.config import package_name
    from usersconfig.configuration import Configuration

    reader = Configuration(package_name)
    cfg = reader.load()

    print(cfg)

####


config_cli.add_command(show_config)
