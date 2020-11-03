from fpdf import FPDF  # fpdf class
import yaml
import os
from config import PdfConfig

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class PdfService:

    def __init__(self, conf: PdfConfig):
        self.conf = conf

    def generate_covid_pdf(self,
                           sign_date,
                           sign_hour,
                           firstname=None,
                           lastname=None,
                           address=None,
                           birthdate=None,
                           place_birth=None,
                           sign_place=None,
                           checked=None) -> str:
        name = self.conf.default_firstname + " " + self.conf.default_lastname
        if firstname is not None and lastname is not None:
            name = firstname + " " + lastname
        field_data = {"name": name,
                      "birthday": birthdate or self.conf.default_birth_date,
                      "place_of_birth": place_birth or self.conf.default_place_of_birth,
                      "address": address or self.conf.default_address,
                      "sign_place": sign_place or self.conf.default_sign_place,
                      "sign_date": sign_date,
                      "sigh_hour": sign_hour,
                      "checked": checked or self.conf.default_reasons}
        pdf = PDF(field_data)
        return pdf.output(f"covid_attestation.pdf", 'S')


class PDF(FPDF):
    def __init__(self, field_data):
        super().__init__(format='A4', unit='mm', orientation='P')
        self.set_auto_page_break(True)
        page_content = os.path.join(ROOT_DIR, '../pdf_content.yaml')
        with open(page_content, 'rt', encoding="utf8") as yaml_file:
            self.add_page()
            data = yaml.safe_load(yaml_file)
            for text in data['text_content']:
                content = TextContent(text)
                self.set_xy(content.x, content.y)
                self.set_font(family='helvetica', size=content.font_size, style=content.style)
                self.multi_cell(content.w, content.h, align=content.align, txt=content.get_text(field_data),
                                border=content.border)


class TextContent:
    def __init__(self, data):
        self.x = data['x']
        self.y = data['y']
        self.w = data['w']
        self.h = data['h']
        self.font_size = data['font_size']
        self.border = data['border']
        # Optionals Param
        self.align = data.get('align', '')
        self.style = data.get('style', '')
        self.fill_id = data.get('fill_id')
        self.__text = data.get('text', '')
        self.check_id = data.get('check_id')

    def get_text(self, data):
        if self.fill_id is None and self.check_id is None:
            return self.__text
        if self.fill_id is not None and data[self.fill_id] is None:
            print(f"{self.fill_id} is missing")
        if str(self.check_id) in data["checked"] or self.check_id in data["checked"]:
            return "X"
        elif self.check_id is not None:
            return self.__text
        return self.__text.replace("<TEXT>", data[self.fill_id]).encode('latin-1', 'replace').decode('latin-1')
