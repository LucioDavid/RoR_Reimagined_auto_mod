import argparse
import json
import logging
import shutil
import time

from pathlib import Path
from dotenv import load_dotenv
from os import getenv

from mods.helpers.files import ROR_DAT_FOLDER_PATH, ROR_DAT_FILE_PATH

logger = logging.getLogger(__name__)


def create_info_file(mod_path: Path, mod_name: str):
    logger.info(rf"Creating info file info.json")
    data = {
        "Author": "Unpublished",
        "CacheStatus": 0,
        "Description": "No Description",
        "Title": f"{mod_name}",
    }

    json_str = json.dumps(data, indent=None)
    with open(rf"{mod_path}\info.json", "w") as f:
        f.write(json_str)


def copy_dat_file():
    logger.info("Copying dat file")
    load_dotenv()

    dat_file_folder = (
        rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}\{ROR_DAT_FOLDER_PATH}"
    )
    Path(dat_file_folder).mkdir(parents=True, exist_ok=True)

    shutil.copy2(
        rf".\dist\{ROR_DAT_FILE_PATH}",
        rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}\{ROR_DAT_FILE_PATH}",
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

    mod_path = rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}"
    logger.info(rf"Creating local mod folder {mod_path}")
    Path(mod_path).mkdir(exist_ok=True)

    create_info_file(mod_path, getenv("MOD_NAME"))
    copy_dat_file()

    end = time.time()
    logger.info(f"Took {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
