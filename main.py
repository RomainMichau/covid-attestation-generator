import logging

from flask import request, Flask
from datetime import date, datetime

from config import CovidConfig, ServerConfig
from services.mail import MailService
from services.pdf_services import PdfService
from rasp_config import RaspConfig
logging.basicConfig(level=logging.INFO)


class AttestationGeneratorServer(object):

    def __init__(self, mail: MailService, server_conf: ServerConfig, pdf_service: PdfService):
        self.mail = mail
        self.app = Flask(__name__)
        self.pdf_service = pdfService

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
            checked = request.args.get("reasons")
            if checked is not None:
                checked = checked.split(',')
            pdf = self.pdf_service.generate_covid_pdf(sign_date=sign_date, sign_hour=sign_time, firstname=firstname,
                                                      lastname=lastname, place_birth=place_birth, sign_place=sign_place,
                                                      address=address, birthdate=birthdate, checked=checked)
            self.mail.send_mail(attachment=pdf, recipient=receiver_email)
            return "done"

        self.app.run(host=server_conf.host, port=server_conf.port)


if __name__ == '__main__':
    conf = CovidConfig()
    rasp_config = RaspConfig()
    mailService = MailService(conf.get_mail_conf())
    pdfService = PdfService(conf.get_pdf_config())
    attestation = AttestationGeneratorServer(mailService, conf.get_server_conf(), pdfService)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
