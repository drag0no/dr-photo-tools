from os import listdir
from os.path import expanduser, isfile, join


def get_file_path_list(path: str) -> list[str]:
    f_path = expanduser(path)
    return [join(f_path, f) for f in listdir(f_path) if isfile(join(f_path, f))]
