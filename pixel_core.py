import os
from dataclasses import dataclass
from typing import Callable

from core_utils import get_file_path_list
from _pixel import DIR_PATH


@dataclass
class RenameData:
    dir_path: str
    src_name: str
    new_name: str


@dataclass
class FailData:
    src_name: str
    reason: str


def rename_files(rename_map: list[RenameData]) -> list[FailData]:
    counter = 0
    failed = []
    for rename_entry in rename_map:
        dir_path = rename_entry.dir_path
        src_name = rename_entry.src_name
        new_name = rename_entry.new_name

        src_filepath = os.path.join(dir_path, src_name)
        new_filepath = os.path.join(dir_path, new_name)

        if os.path.exists(new_filepath):
            failed.append(FailData(src_name, f"{new_name} already exists in this folder!"))
            continue

        os.rename(src_filepath, new_filepath)
        print(f"✅ Renaming done: {src_name} -> {new_name}")
        counter += 1

    return failed


def print_result(skipped_list: list[FailData], failed_list: list[FailData]) -> None:
    if not skipped_list and not failed_list:
        print(f"Done! Successfully renamed all files.")
        return

    for entry in skipped_list:
        print(f"⏩ Skipped renaming `{entry.src_name}`: {entry.reason}")
    for entry in failed_list:
        print(f"❌ Cannot rename `{entry.src_name}`: {entry.reason}")


def main(prepare_rename_map: Callable[[list[str]], tuple[list[RenameData], list[FailData]]], dry_run: bool) -> None:
    file_path_list = get_file_path_list(DIR_PATH)
    rename_data, skipped_files = prepare_rename_map(file_path_list)
    if dry_run:
        failed_files = []
    else:
        print('**********')
        failed_files = rename_files(rename_data)
    print('**********')
    print_result(skipped_files, failed_files)
    if dry_run:
        print('**********')
        print('DRY-RUN is enabled!')
