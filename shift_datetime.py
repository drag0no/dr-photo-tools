import re
from datetime import datetime

import piexif

from core_utils import (
    get_file_path_list,
    get_updated_exif_data,
    update_files_exif
)

from _env import DIR_PATH, TIME_DELTA, FILE_REGEX


def get_date_from_exif_created(exif_dict: dict) -> datetime:
    src_date_exif = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
    return datetime.strptime(src_date_exif, '%Y:%m:%d %H:%M:%S')


def get_date_from_filename(file_path: str) -> datetime:
    src_date_filename = re.search(FILE_REGEX, file_path).group(1)
    return datetime.strptime(src_date_filename, '%Y%m%d_%H%M%S')


# noinspection PyUnusedLocal
def get_date(file_path: str, exif_dict: dict) -> bytes:
    src_date = get_date_from_exif_created(exif_dict)
    # src_date = get_date_from_filename(file_path)
    new_date = src_date + TIME_DELTA
    return new_date.strftime('%Y:%m:%d %H:%M:%S').encode('utf-8')


# noinspection PyUnusedLocal
def skip_file(file_path: str, exif_dict: dict) -> bool:
    # if '_IMG' not in file_path or not file_path.endswith('.JPG'):
    #     print(f'Skipping {i + 1}/{size}: {file_path}')
    #     continue
    return False


def main() -> None:
    file_path_list = get_file_path_list(DIR_PATH)
    updated_exif_data = get_updated_exif_data(file_path_list, get_date, skip_file)
    print('**********')
    update_files_exif(updated_exif_data)


if __name__ == '__main__':
    main()
