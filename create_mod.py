import argparse
import json
import logging
import time

from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from genieutils.datfile import DatFile

from mods.helpers.files import (
    AOE2_DAT_FILE_PATH,
    HOTKEYS_FILE_PATH,
    ROR_DAT_FILE_PATH,
    ROR_DAT_FOLDER_PATH,
)
from mods import bowman_line

logger = logging.getLogger(__name__)


def load_dat_file(file_path: Path) -> DatFile:
    logger.info(f"Loading dat file {file_path}")
    return DatFile.parse(file_path)


def load_json_file(file_path: Path) -> dict:
    logger.info(f"Loading JSON file {file_path}")
    with open(file_path) as json_data:
        return json.load(json_data)


def save_json_file(file_path: Path, data: dict, indent_size: int | None):
    logger.info(f"Saving JSON file {file_path}")
    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent_size)


def main():
    start = time.time()
    parser = argparse.ArgumentParser(
        prog="create_mod",
        description="Programmatically mod Genie engine dat files of "
        " Age of Empires II Definitive Edition: Return of Rome",
    )
    parser.add_argument("--logfile", type=Path, required=False)
    args = parser.parse_args()

    load_dotenv()

    log_filename = args.logfile
    logging.basicConfig(filename=log_filename, level=logging.INFO)

    ror_data = load_dat_file(rf'{getenv("BASE_AOE2_DIR")}\{ROR_DAT_FILE_PATH}')
    # aoe2_data = load_dat_file(rf'{getenv("BASE_AOE2_DIR")}\{AOE2_DAT_FILE_PATH}')

    ror_hotkeys = load_json_file(rf'{getenv("BASE_AOE2_DIR")}\{HOTKEYS_FILE_PATH}')

    logger.info("Applying mods")
    ror_hotkeys = bowman_line.mod(data=ror_data, hotkeys=ror_hotkeys)

    Path(rf".\dist\{ROR_DAT_FOLDER_PATH}").mkdir(parents=True, exist_ok=True)

    output_dat_file_path = rf".\dist\{ROR_DAT_FILE_PATH}"
    logger.info(f"Saving dat file {output_dat_file_path}")
    ror_data.save(output_dat_file_path)

    save_json_file(rf".\dist\{HOTKEYS_FILE_PATH}", data=ror_hotkeys, indent_size=3)

    end = time.time()
    logger.info(f"Took {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
