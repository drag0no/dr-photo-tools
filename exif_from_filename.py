import re
from datetime import datetime

from core_utils import (
    get_file_path_list,
    get_updated_exif_data,
    update_files_exif
)

from _env import DIR_PATH, FILE_REGEX


# noinspection PyUnusedLocal
def get_date(file_path: str, exif_dict: dict) -> bytes:
    date_filename = re.search(FILE_REGEX, file_path).group(1)
    return datetime.strptime(date_filename, '%Y%m%d_%H%M%S').strftime('%Y:%m:%d %H:%M:%S').encode('utf-8')


# noinspection PyUnusedLocal
def skip_file(file_path: str, exif_dict: dict) -> bool:
    return False


def main() -> None:
    file_path_list = get_file_path_list(DIR_PATH)
    updated_exif_data = get_updated_exif_data(file_path_list, get_date, skip_file)
    print('**********')
    update_files_exif(updated_exif_data)


if __name__ == '__main__':
    main()
