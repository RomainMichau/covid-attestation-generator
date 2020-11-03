import yaml
import os
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class MailConfig:
    def __init__(self, data: dict):
        if "sender_email" not in data.keys():
            raise MissingConfException("sender_mail")
        self.sender_email = data["sender_email"]
        if "password" not in data.keys():
            raise MissingConfException("mail_config.password")
        self.password = data["password"]
        self.default_receiver = data.get("default_receiver")
        self.default_subject = data.get("default_subject", "attestation_covid")
        self.default_body = data.get("default_body", "attestation covid")
        self.default_attachment_name = data.get("default_attachment_name", "attestation.pdf")


class PdfConfig:
    def __init__(self, data: dict):
        self.default_firstname = data.get("firstname")
        self.default_lastname = data.get("lastname")
        self.default_address = data.get("address")
        self.default_birth_date = data.get("birth_date")
        self.default_place_of_birth = data.get("place_of_birth")
        self.default_sign_place = data.get("sign_place")
        self.default_reasons = data.get("default_reasons", [2, 6])


class ServerConfig:
    def __init__(self, data: dict):
        self.port = data.get("port", 5050)
        self.host = data.get("host", "0.0.0.0")


class CovidConfig:
    def __init__(self):
        conf_file = os.getenv("COVID_ATTEST_CONF_FILE", "config.yaml")
        conf_file = os.path.join(ROOT_DIR, conf_file)
        logging.info(f'Reading config from file {conf_file}')
        with open(conf_file, 'rt', encoding="utf8") as yaml_file:
            data = yaml.safe_load(yaml_file)
            self.__server_config = ServerConfig(data["server_config"])
            self.__mail_config = MailConfig(data["mail_config"])
            self.__pdf_config = PdfConfig(data["pdf_default_value"])

    def get_mail_conf(self) -> MailConfig:
        return self.__mail_config

    def get_server_conf(self) -> ServerConfig:
        return self.__server_config

    def get_pdf_config(self) -> PdfConfig:
        return self.__pdf_config


class MissingConfException(Exception):
    def __init__(self, field_name: str):
        super().__init__(f"{field_name} must be defined in config.yaml")
