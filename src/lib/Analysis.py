from entities.Empreendimento import Local, LocalContact, mock_local
from typing import Dict, List
import os, orjson

class Analysis:
  def get_all_json_files(self, path="../cache/") -> Dict[str, List[Local]]:
      dados = {}
      for filename in os.listdir(os.path.join(os.path.dirname(__file__), path)):
        if filename.endswith('.json'):  # Verifica se o arquivo é um arquivo JSON
            with open(os.path.join(os.path.dirname(__file__), path, filename), 'r') as f:  # Abre o arquivo
                locais_json = f.read()
                locais_dict = orjson.loads(locais_json)
                locais = [Local.from_dict(local_dict) for local_dict in locais_dict]
                print(locais)
                dados[filename.replace(".json", "")]: List[Local] = locais
      return dados