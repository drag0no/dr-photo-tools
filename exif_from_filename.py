import re
from datetime import datetime

from exif_core import main
from _exif import FILE_REGEX


# noinspection PyUnusedLocal
def get_date(file_path: str, exif_dict: dict) -> bytes:
    date_filename = re.search(FILE_REGEX, file_path).group(1)
    return datetime.strptime(date_filename, '%Y%m%d_%H%M%S').strftime('%Y:%m:%d %H:%M:%S').encode('utf-8')


# noinspection PyUnusedLocal
def skip_file(file_path: str, exif_dict: dict) -> bool:
    return False


if __name__ == '__main__':
    main(get_date, skip_file, True)
