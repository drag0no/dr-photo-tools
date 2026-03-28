import re

DIR_PATH = '~/syncthing/dcim/Camera/'
PHOTO_PATTERN = re.compile(r"^(?:PXL_)?(\d{8})_(\d{6})(\d{3})(\..*)?(~\d+)?\.jpe?g$", re.IGNORECASE)
VIDEO_PATTERN = re.compile(r"^(?:PXL_)?(\d{8})_(\d{6})(\d{3})(~\d+)?\.mp4$", re.IGNORECASE)
GPS_REGEX = rb'([+-]\d+\.\d+)([+-]\d+\.\d+)'
