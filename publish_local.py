import argparse
import json
import logging
import shutil
import time

from pathlib import Path
from dotenv import load_dotenv
from os import getenv

from mods.helpers.files import HOTKEYS_FILE_PATH, ROR_DAT_FOLDER_PATH, ROR_DAT_FILE_PATH

logger = logging.getLogger(__name__)


def create_info_file():
    load_dotenv()
    mod_path = rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}"
    logger.info(rf"Creating info file {mod_path}\info.json")
    data = {
        "Author": "Unpublished",
        "CacheStatus": 0,
        "Description": "No Description",
        "Title": f"{getenv("MOD_NAME")}",
    }

    json_str = json.dumps(data, indent=None)
    with open(rf"{mod_path}\info.json", "w") as f:
        f.write(json_str)


def ensure_mod_local_folder():
    load_dotenv()
    mod_path = rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}"
    logger.info(rf"Ensure local mod folder {mod_path}")
    Path(mod_path).mkdir(exist_ok=True)


def ensure_dat_folder():
    load_dotenv()
    dat_file_folder = (
        rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}\{ROR_DAT_FOLDER_PATH}"
    )
    logger.info(rf"Ensure dat folder {dat_file_folder}")
    Path(dat_file_folder).mkdir(parents=True, exist_ok=True)


def copy_dat_file():
    logger.info("Copying dat file")
    load_dotenv()

    shutil.copy2(
        rf".\dist\{ROR_DAT_FILE_PATH}",
        rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}\{ROR_DAT_FILE_PATH}",
    )


def copy_hotkeys_file():
    logger.info("Copying hotkeys file")
    load_dotenv()

    shutil.copy2(
        rf".\dist\{HOTKEYS_FILE_PATH}",
        rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}\{HOTKEYS_FILE_PATH}",
    )


def main():
    start = time.time()
    parser = argparse.ArgumentParser(
        prog="publish_local",
        description="Programmatically publish AoE2:RoR mod to local folder",
    )
    parser.add_argument("--logfile", type=Path, required=False)
    args = parser.parse_args()

    load_dotenv()

    log_filename = args.logfile
    logging.basicConfig(filename=log_filename, level=logging.INFO)

    ensure_mod_local_folder()
    ensure_dat_folder()

    create_info_file()
    copy_dat_file()
    copy_hotkeys_file()

    end = time.time()
    logger.info(f"Took {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
