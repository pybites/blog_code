from collections import namedtuple
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ASSET_DIR = 'assets'
DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 150
DEFAULT_CANVAS_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
DEFAULT_OUTPUT_FILE = 'out.png'
RESIZE_PERCENTAGE = 0.8
DEFAULT_TOP_MARGIN = int(((1 - 0.8) * DEFAULT_HEIGHT) / 2)
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
TEXT_SIZE = 24
TEXT_FONT_TYPE = os.path.join(ASSET_DIR, 'SourceSansPro-Regular.otf')
TEXT_PADDING_HOR, TEXT_PADDING_VERT = 20, 40

Font = namedtuple('Font', 'ttf text color size offset')
ImageDetails = namedtuple('Image', 'left top size')


class Banner:
    def __init__(self, size=DEFAULT_CANVAS_SIZE,
                 bgcolor=WHITE, output_file=DEFAULT_OUTPUT_FILE):
        '''Creating a new canvas'''
        self.size = size
        self.bgcolor = bgcolor
        self.output_file = output_file
        self.image = Image.new('RGBA', self.size, self.bgcolor)
        self.image_coords = []

    def _image_gt_canvas_size(self, img):
        return img.size[0] > self.image.size[0] or \
               img.size[1] > self.image.size[1]

    def add_image(self, image, resize=False,
                  top=DEFAULT_TOP_MARGIN, left=0, right=False):
        '''Adds (pastes) image on canvas
           If right is given calculate left, else take left
           Returns added img size'''
        img = Image.open(image)

        if resize or self._image_gt_canvas_size(img):
            size = DEFAULT_HEIGHT * RESIZE_PERCENTAGE
            img.thumbnail((size, size), Image.ANTIALIAS)

        if right:
            left = self.image.size[0] - img.size[0]
        else:
            left = left

        offset = (left, top)
        self.image.paste(img, offset)

        img_details = ImageDetails(left=left, top=top, size=img.size)
        self.image_coords.append(img_details)

    def add_text(self, font):
        '''Adds text on a given image object'''
        draw = ImageDraw.Draw(self.image)
        pillow_font = ImageFont.truetype(font.ttf, font.size)

        if font.offset:
            offset = font.offset
        else:
            # if no offset given put text alongside first image
            left_image_px = min(img.left + img.size[0]
                                for img in self.image_coords)
            offset = (left_image_px + TEXT_PADDING_HOR,
                      TEXT_PADDING_VERT)

        draw.text(offset, font.text, font.color, font=pillow_font)

    def save_image(self):
        self.image.save(self.output_file)


def main(args):
    image1 = args[0]
    image2 = args[1]
    text = args[2]

    banner = Banner()
    banner.add_image(image1)
    banner.add_image(image2, resize=True, right=True)

    font = Font(ttf=TEXT_FONT_TYPE,
                text=text,
                color=BLACK,
                size=TEXT_SIZE,
                offset=None)

    banner.add_text(font)

    banner.save_image()


if __name__ == '__main__':
    script = sys.argv.pop(0)
    args = sys.argv

    if len(args) != 3:
        print('Usage: {} img1 img2 text'.format(script))
        sys.exit(1)

    main(args)
