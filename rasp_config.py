import yaml
import os
import logging
from config import PdfConfig

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class RaspConfig:
   def __init__(self):
        conf_file = os.getenv("COVID_ATTEST_RASP_CONF_FILE", "config.rasp.yaml")
        conf_file = os.path.join(ROOT_DIR, conf_file)
        logging.info(f'Reading rasperry config from file {conf_file}')
        self.content: dict[int, PdfConfig] = {}
        with open(conf_file, 'rt', encoding="utf8") as yaml_file:
            data = yaml.safe_load(yaml_file)
            for conf in data.get('rasp_config'):
                self.content[conf['pin_id']] = PdfConfig(conf)

            

