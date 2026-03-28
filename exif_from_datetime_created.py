import piexif

from exif_core import main


# noinspection PyUnusedLocal
def get_date(file_path: str, exif_dict: dict) -> bytes:
    return exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')


# noinspection PyUnusedLocal
def skip_file(file_path: str, exif_dict: dict) -> bool:
    return False


if __name__ == '__main__':
    main(get_date, skip_file, True)
