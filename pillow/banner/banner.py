import os
import sys

from PIL import Image, ImageDraw, ImageFont

ASSET_DIR = 'assets'
PB_CHALLENGE_IMG = os.path.join(ASSET_DIR, 'pybites-challenges.png')
PILLOW_IMG = os.path.join(ASSET_DIR, 'pillow-logo.png')
DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 150
DEFAULT_CANVAS_SIZE = (DEFAULT_WIDTH, DEFAULT_HEIGHT)
DEFAULT_TOP_MARGIN = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_FONT_TYPE = os.path.join(ASSET_DIR, 'SourceSansPro-Regular.otf')
TEXT_SIZE = 24
TEXT_PADDING_HOR = 20
TEXT_PADDING_VERT = 40
IMG_TEXT = 'Code Challenge 31:\nImage Manipulation With Pillow'

image = Image.new('RGB', DEFAULT_CANVAS_SIZE, WHITE)

pb_logo = Image.open(PB_CHALLENGE_IMG)
pb_logo_offset = (0, DEFAULT_TOP_MARGIN)
image.paste(pb_logo, pb_logo_offset)
pb_logo_width, pb_logo_height = pb_logo.size

second_img = Image.open(PILLOW_IMG)
second_img.thumbnail(pb_logo.size, Image.ANTIALIAS)

offset_second_img = (DEFAULT_WIDTH - pb_logo_width, DEFAULT_TOP_MARGIN)
image.paste(second_img, offset_second_img)

draw = ImageDraw.Draw(image)
font = ImageFont.truetype(TEXT_FONT_TYPE, TEXT_SIZE)
offset_text = (pb_logo_width + TEXT_PADDING_HOR, TEXT_PADDING_VERT)
draw.text(offset_text, IMG_TEXT, BLACK, font=font)

image.save('out.png')
