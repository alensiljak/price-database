"""
Vanguard Australia
"""
import logging


class VanguardAuDownloader:
    """
    Downloads prices from Vanguard Australia
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def download(self, namespace: str, symbol: str, currency: str):
        """ Download price """
        if namespace != "Vanguard":
            raise ValueError("Only Vanguard namespace is handled by this agent.")
