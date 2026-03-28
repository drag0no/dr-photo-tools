import os
import re
from mmap import mmap, ACCESS_READ
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from timezonefinder import TimezoneFinder

from pixel_core import RenameData, FailData, main
from _pixel import VIDEO_PATTERN, GPS_REGEX


def prepare_rename_map(file_path_list: list[str]) -> (list[RenameData], list[FailData]):
    tf = TimezoneFinder()
    result = []
    skipped = []
    for i, file_path in enumerate(file_path_list):

        src_name = os.path.basename(file_path)
        match = VIDEO_PATTERN.match(src_name)
        if not match:
            continue

        with open(file_path, "rb") as f:
            with mmap(f.fileno(), 0, access=ACCESS_READ) as mm:
                index = mm.find(b'\xa9xyz')
                if index == -1:
                    skipped.append(FailData(src_name, "No GPS data found in binary."))
                    continue

                chunk = mm[index:index + 50]
                gps_match = re.search(GPS_REGEX, chunk)
                if not gps_match:
                    skipped.append(FailData(src_name, f"Found GPS tag, but couldn't parse coordinates -> {chunk}"))
                    continue

                lat = float(gps_match.group(1))
                lon = float(gps_match.group(2))

        tz_name = tf.timezone_at(lat=lat, lng=lon)
        if not tz_name:
            skipped.append(FailData(src_name, f"Could not determine timezone for coordinates ({lat}, {lon})"))
            continue

        date_str = match.group(1)
        time_str = match.group(2)
        original_ms = match.group(3)

        utc_dt = datetime.strptime(f"{date_str}{time_str}", "%Y%m%d%H%M%S")
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)

        local_tz = ZoneInfo(tz_name)
        local_dt = utc_dt.astimezone(local_tz)

        formatted_dt = local_dt.strftime("%Y%m%d_%H%M%S")
        new_name = f"{formatted_dt}_{original_ms}.mp4"
        dir_path = os.path.dirname(file_path)
        res_entry = RenameData(dir_path, src_name, new_name)
        result.append(res_entry)
        print(f"✅ Renaming found: {src_name} -> {new_name}")

    return result, skipped


if __name__ == '__main__':
    main(prepare_rename_map, True)
