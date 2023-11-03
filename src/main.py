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
    coletor.gerenciador.carregar_locais()
    print(coletor.gerenciador)
    print("Collecting Proxyes")
    coletor.proxy_collector.scrap_proxies()
    print("Running...")
    coletor.set_estado("São Paulo")
    coletor.set_cidade("Campinas")
    coletor.enfileirar_locais("zap", 5) # 500x100
    coletor.enfileirar_locais("vivareal", 22)
    coletor.processar_fila()
    coletor.gerenciador.salvar_locais()



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()