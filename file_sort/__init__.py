"""
Sort images by exif or file data.
"""

__version__ = '1.0.0'

import locale
import logging
# de_DE.UTF-8
locale.setlocale(locale.LC_ALL, 'deu_deu')

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
