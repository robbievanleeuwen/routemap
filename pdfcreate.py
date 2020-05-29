from fpdf import FPDF


class RouteMapPDF():
    def __init__(self):
        self.pdf = FPDF(orientation='P', unit='mm', format='A3')
        self.pdf.add_page()
        self.pdf.set_font('Arial', 'B', 16)
        # self.pdf.cell(40, 10, 'Hello World!', 1)
        w = 3530
        h = 3542
        conv = 300 / 25.4
        self.pdf.image('routes/out/bell_to_wollangambe_crater.jpg', w=w/conv, h=h/conv)

    def create_pdf(self, path):
        self.pdf.output(path)
