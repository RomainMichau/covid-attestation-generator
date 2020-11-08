
from rasp_config import RaspConfig
from services.pdf_services import PdfService
from services.mail import MailService
class RaspService:
    def __init__(self, conf: RaspConfig, mail: MailService, pdf: PdfService):
        self.mail_service = mail
        self.pdf_service = pdf
        for pin in conf:
    
    def callback(self, id):
        pdf = self.pdf_service.generate_covid_pdf(sign_date=sign_date, sign_hour=sign_time, firstname=firstname,
                                                      lastname=lastname, place_birth=place_birth, sign_place=sign_place,
                                                      address=address, birthdate=birthdate, checked=checked)
        self.mail_service.send_mail(attachment=pdf, recipient=receiver_email)


