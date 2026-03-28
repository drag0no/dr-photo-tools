from os import listdir
from os.path import expanduser, isfile, join
from typing import Callable

import piexif


def get_file_path_list(path: str) -> list[str]:
    f_path = expanduser(path)
    return [join(f_path, f) for f in listdir(f_path) if isfile(join(f_path, f))]


def get_updated_exif_data(
        file_path_list: list[str],
        date_fetcher: Callable[[str, dict], bytes],
        skip_check: Callable[[str, dict], bool]
) -> dict[str, dict]:
    size = len(file_path_list)
    result = {}
    for i, file_path in enumerate(file_path_list):
        exif_dict = piexif.load(file_path)
        if skip_check(file_path, exif_dict):
            print(f'Skipping {i + 1}/{size}: {file_path}')
            continue

        print(f'Processing {i + 1}/{size}: {file_path}')
        date_exif = date_fetcher(file_path, exif_dict)

        exif_dict['0th'][piexif.ImageIFD.DateTime] = date_exif
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_exif
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date_exif

        # del exif_dict['Exif'][piexif.ExifIFD.ExposureBiasValue]
        # del exif_dict['Exif'][41728]
        # del exif_dict['Exif'][41729]

        result[file_path] = exif_dict

    return result


def update_files_exif(file_exif_dict: dict[str, dict]) -> None:
    size = len(file_exif_dict)
    for i, (file_path, exif_dict) in enumerate(file_exif_dict.items()):
        # noinspection PyTypeChecker
        print(f'Updating {i + 1}/{size}: {file_path}')
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, file_path)
