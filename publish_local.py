import argparse
import json
import logging
import shutil
import time

from pathlib import Path
from dotenv import load_dotenv
from os import getenv

from mods.helpers.files import (
    CIV_TECH_TREES_FILE_PATH,
    FUTURAVAILABLEUNITS_FILE_PATH,
    HOTKEYS_FILE_PATH,
    MODDED_STRINGS_FILE_PATH_EN,
    ROR_DAT_FOLDER_PATH,
    ROR_DAT_FILE_PATH,
)

logger = logging.getLogger(__name__)


def create_info_file(mod_path: str):
    load_dotenv()
    logger.info("Creating info file info.json")
    data = {
        "Author": "Unpublished",
        "CacheStatus": 0,
        "Description": "No Description",
        "Title": f"{getenv("MOD_NAME")}",
    }

    json_str = json.dumps(data, indent=None)
    with open(rf"{mod_path}\info.json", "w") as f:
        f.write(json_str)


def ensure_mod_local_folder(mod_path: str):
    logger.info(rf"Ensure local mod folder {mod_path}")
    Path(mod_path).mkdir(exist_ok=True)


def ensure_dat_folder(mod_path: str):
    logger.info(rf"Ensure dat folder {mod_path}\{ROR_DAT_FOLDER_PATH}")
    Path(rf"{mod_path}\{ROR_DAT_FOLDER_PATH}").mkdir(parents=True, exist_ok=True)


def ensure_civ_tech_trees_folder(mod_path: str):
    logger.info(rf"Ensure CivTechTrees folder {mod_path}\{ROR_DAT_FOLDER_PATH}\CivTechTrees")
    Path(rf"{mod_path}\{ROR_DAT_FOLDER_PATH}\CivTechTrees").mkdir(parents=False, exist_ok=True)


def ensure_language_en_folder(mod_path: str):
    logger.info(rf"Ensure language en folder {mod_path}\{Path(MODDED_STRINGS_FILE_PATH_EN).parent}")
    Path(rf"{mod_path}\{MODDED_STRINGS_FILE_PATH_EN}").parent.mkdir(parents=True, exist_ok=True)


def copy_dat_file(mod_path: str):
    logger.info("Copying dat file")

    shutil.copy2(
        rf"dist\{ROR_DAT_FILE_PATH}",
        rf"{mod_path}\{ROR_DAT_FILE_PATH}",
    )


def copy_hotkeys_file(mod_path: str):
    logger.info("Copying hotkeys file")

    shutil.copy2(
        rf"dist\{HOTKEYS_FILE_PATH}",
        rf"{mod_path}\{HOTKEYS_FILE_PATH}",
    )


def copy_civ_tech_trees_files(mod_path: str):
    logger.info("Copying CivTechTrees files")

    for _, civ_file_path in CIV_TECH_TREES_FILE_PATH.items():
        shutil.copy2(
            rf"dist\{ROR_DAT_FOLDER_PATH}\{civ_file_path}",
            rf"{mod_path}\{ROR_DAT_FOLDER_PATH}\{civ_file_path}",
        )


def copy_futuravailableunits_file(mod_path: str):
    logger.info("Copying futuravailableunits file")

    shutil.copy2(
        rf"dist\{FUTURAVAILABLEUNITS_FILE_PATH}",
        rf"{mod_path}\{FUTURAVAILABLEUNITS_FILE_PATH}",
    )


def copy_language_file_en(mod_path: str):
    logger.info("Copying language file en")

    shutil.copy2(
        rf"dist\{MODDED_STRINGS_FILE_PATH_EN}",
        rf"{mod_path}\{MODDED_STRINGS_FILE_PATH_EN}",
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
    ensure_mod_local_folder(mod_path)
    ensure_dat_folder(mod_path)
    ensure_civ_tech_trees_folder(mod_path)
    ensure_language_en_folder(mod_path)

    create_info_file(mod_path)
    copy_dat_file(mod_path)
    copy_hotkeys_file(mod_path)
    copy_civ_tech_trees_files(mod_path)
    copy_futuravailableunits_file(mod_path)
    copy_language_file_en(mod_path)

    end = time.time()
    logger.info(f"Took {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
