from collections import namedtuple
import sys

from PIL import Image, ImageDraw, ImageFont

import constants

Font = namedtuple('Font', 'ttf text color size offset')
ImageDetails = namedtuple('Image', 'left top size')

class Banner:
    def __init__(self, size=constants.DEFAULT_CANVAS_SIZE, bgcolor=constants.WHITE):
        '''Creating a new canvas'''
        self.size = size
        self.bgcolor = bgcolor
        self.image = Image.new('RGB', self.size, self.bgcolor)
        self.image_coords = []

    def add_image(self, image, resize=False, top=constants.DEFAULT_TOP_MARGIN, left=0, right=False):
        '''Adds (pastes) image on canvas
           If right is given calculate left, else take left
           Returns added img size'''
        img = Image.open(image)

        if resize:
            size = constants.DEFAULT_HEIGHT * 0.8
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

        # if not offset put text alongside first image
        if font.offset:
            offset = font.offset
        else:
            left_image_px = min(img.left + img.size[0] for img in self.image_coords)
            offset = (left_image_px + constants.TEXT_PADDING_HOR, constants.TEXT_PADDING_VERT)

        draw.text(offset, font.text, font.color, font=pillow_font)

    def save_image(self, output_file='out.png'):
        self.image.save(output_file)


if __name__ == '__main__':
    banner = Banner()
    banner.add_image(constants.FIRST_IMAGE)
    banner.add_image(constants.SECOND_IMAGE, resize=True, right=True)

    font = Font(ttf=constants.DEFAULT_TEXT_FONT_TYPE,
                text=constants.IMG_TEXT,
                color=constants.BLACK,
                size=constants.DEFAULT_TEXT_SIZE,
                offset=None)

    banner.add_text(font)
    banner.save_image()
