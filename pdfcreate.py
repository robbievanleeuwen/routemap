from fpdf import FPDF


class RouteMapPDF():
    """a."""

    def __init__(self, image, scale=1):
        """Init the RouteMapPDF class."""

        self.pdf = FPDF(orientation='P', unit='mm', format='A3')
        self.margin = 5
        self.printable_size = (297 - 2 * self.margin, 420 - 2 * self.margin)
        self.image = image
        self.CONV = 300 / 25.4 / scale  # convert 300dpi to mm
        self.profile_height = 75  # height of elevation profile

    def create_pdf(self, path, portrait=True):
        """Create a pdf."""

        if portrait:
            page_size = (
                int(self.printable_size[0] * self.CONV), int(self.printable_size[1] * self.CONV)
            )
        else:
            page_size = (
                int(self.printable_size[1] * self.CONV), int(self.printable_size[0] * self.CONV)
            )

        m = -(-self.image.size[1] // page_size[1])  # rows
        n = -(-self.image.size[0] // page_size[0])  # cols
        image_size = (self.image.size[0] / n, self.image.size[1] / m)

        top = 0

        for i in range(m):
            left = 0

            for j in range(n):
                box = (left, top, left + image_size[0], top + image_size[1])
                im = self.image.crop(box)
                im.save('temp/' + str(i) + str(j) + '.jpg')
                left += image_size[0]

            top += image_size[1]

        for i in range(m):
            for j in range(n):
                if portrait:
                    self.pdf.add_page(orientation='P')
                    x = 0.5 * (297 - image_size[0] / self.CONV)
                    y = 0.5 * (420 - image_size[1] / self.CONV)
                else:
                    self.pdf.add_page(orientation='L')
                    x = 0.5 * (420 - image_size[0] / self.CONV)
                    y = 0.5 * (297 - image_size[1] / self.CONV)

                im_path = 'temp/' + str(i) + str(j) + '.jpg'
                self.pdf.image(
                    im_path, x=x, y=y, w=image_size[0] / self.CONV, h=image_size[1] / self.CONV
                )

        self.pdf.output(path)
