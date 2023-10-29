#!/usr/bin/env python3
"""
Web Scrapper Project
"""

__author__ = "TutorFx & yhellemy"
__version__ = "0.1.0"
__license__ = "MIT"

import lib.Scrap as Scrap

def main():
    """ Main entry point of the app """
    coletor = Scrap.ColetorDeLocais()
    print("Collecting Proxyes")
    coletor.proxy_collector.scrap_proxies()
    print("Running...")
    coletor.coletar_locais_em_threads("vivareal")



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()