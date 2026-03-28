import os

import piexif

from pixel_core import RenameData, FailData, main
from _pixel import PHOTO_PATTERN


def prepare_rename_map(file_path_list: list[str]) -> (list[RenameData], list[FailData]):
    result = []
    skipped = []
    for i, file_path in enumerate(file_path_list):
        src_name = os.path.basename(file_path)
        match = PHOTO_PATTERN.match(src_name)
        if not match:
            continue

        original_ms = match.group(3)
        exif_dict = piexif.load(file_path)

        make_bytes = exif_dict.get("0th", {}).get(piexif.ImageIFD.Make, b"")
        make_str = make_bytes.decode('utf-8', 'ignore').strip()
        if "Google" not in make_str:
            skipped.append(FailData(src_name, f"Not a Google photo (Make: '{make_str}')"))
            continue

        dt_bytes = exif_dict.get("Exif", {}).get(piexif.ExifIFD.DateTimeOriginal)
        if not dt_bytes:
            skipped.append(FailData(src_name, "No DateTimeOriginal EXIF tag found."))
            continue

        dt_str = dt_bytes.decode('utf-8', 'ignore').strip()
        formatted_dt = dt_str.replace(":", "").replace(" ", "_")

        new_name = f"{formatted_dt}_{original_ms}.jpg"
        dir_path = os.path.dirname(file_path)
        res_entry = RenameData(dir_path, src_name, new_name)
        result.append(res_entry)
        print(f"✅ Renaming found: {src_name} -> {new_name}")

    return result, skipped


if __name__ == '__main__':
    main(prepare_rename_map, True)
