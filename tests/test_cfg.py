'''
Test configuration management
'''
#import click
from click.testing import CliRunner

runner = CliRunner()

class TestCfg:
    # def __init__(self):
    #     super().__init__()
    #     self.runner = CliRunner()

    def test_read_config(self):
        from pricedb.config_cli import config_cli

        result = runner.invoke(config_cli, ['show'])

        assert result.exit_code == 0
        assert result.output is not None


def test_read_fixerio_api_key():
    from pricedb.config import Configuration, ConfigKeys

    cfg = Configuration()
    result = cfg.fixerio_api_key

    assert result is not None
