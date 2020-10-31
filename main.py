import logging

from flask import request, Flask
from datetime import date, datetime

from config import CovidConfig, ServerConfig
from services.mail import MailService
from services.pdf_services import generate_covid_pdf

logging.basicConfig(level=logging.INFO)


class AttestationGeneratorServer(object):

    def __init__(self, mail: MailService, conf: ServerConfig):
        self.mail = mail
        self.app = Flask(__name__)

        @self.app.route("/get-attestation")
        def get_attest():
            firstname = request.args.get("firstname")
            lastname = request.args.get("lastname")
            address = request.args.get("address")
            birthdate = request.args.get("birthdate")
            place_birth = request.args.get("place_birth")
            sign_place = request.args.get("sign_place")
            receiver_email = request.args.get("receiver_email")
            sign_date = date.today().strftime("%d/%m/%y")
            sign_time = datetime.now().strftime("%H:%M:%S")
            pdf = generate_covid_pdf(firstname, lastname, birthdate, place_birth, address, sign_place, sign_date,
                                     sign_time)
            self.mail.send_mail(attachment=pdf, recipient=receiver_email)
            return "hello world"

        self.app.run(host=conf.host, port=conf.port)


if __name__ == '__main__':
    conf = CovidConfig()
    mailService = MailService(conf.get_mail_conf())
    attestation = AttestationGeneratorServer(mailService, conf.get_server_conf())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
