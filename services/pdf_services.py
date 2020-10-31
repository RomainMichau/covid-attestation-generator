from fpdf import FPDF  # fpdf class
import yaml


def generate_covid_pdf(firstname,
                       lastname,
                       birthdate,
                       place_birth,
                       address,
                       sign_place,
                       sign_date,
                       sign_hour):
    field_data = {"name": f"{firstname} {lastname}",
                  "birthday": birthdate,
                  "place_of_birth": place_birth,
                  "address":  address,
                  "sign_place": sign_place,
                  "sign_date": sign_date,
                  "sigh_hour": sign_hour}
    pdf = PDF(field_data)
    return pdf.output(f"covid_attestation.pdf", 'S')


class PDF(FPDF):
    def __init__(self, field_data):
        super().__init__(format='A4', unit='mm', orientation='P')
        self.set_auto_page_break(True)
        with open('pdf_content.yaml') as yaml_file:
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
        self.style = data['style']
        self.font_size = data['font_size']
        self.__text = data['text']
        self.align = data['align']
        self.border = data['border']
        self.fill_id = data['fill_id']

    def get_text(self, data):
        if self.fill_id is None:
            return self.__text
        if data[self.fill_id] is None:
            print(f"{self.fill_id} is missing")
        return self.__text.replace("<TEXT>", data[self.fill_id])


res = generate_covid_pdf("romain", "michau", "31/01/1996", "Neuilly", "1 rue du general foy", "paris", "31/01/1655", "145")