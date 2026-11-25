import argparse
import json
import logging
import shlex
import time

from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from genieutils.datfile import DatFile

from mods.helpers.files import (
    AOE2_DAT_FILE_PATH,
    AOE2_STRINGS_FILE_PATH_EN,
    AOE2_UI_FOLDER_PATH,
    CIV_TECH_TREES_FILE_PATH,
    FUTURAVAILABLEUNITS_FILE_PATH,
    HOTKEYS_FILE_PATH,
    MODDED_STRINGS_FILE_PATH_EN,
    ROR_DAT_FILE_PATH,
    ROR_DAT_FOLDER_PATH,
    ROR_STRINGS_FILE_PATH_EN,
    ROR_UI_FOLDER_PATH,
    ROR_UNIT_GRAPHICS_FOLDER_PATH,
)
from mods import bowman_line, spearman_line

logger = logging.getLogger(__name__)


def load_dat_file(file_str_path: str) -> DatFile:
    logger.info(f"Loading dat file {file_str_path}")
    return DatFile.parse(file_str_path)


def load_json_file(file_str_path: str) -> dict:
    logger.info(f"Loading JSON file {file_str_path}")
    with open(file_str_path) as json_data:
        return json.load(json_data)


def load_json_files(file_str_paths: dict[str, str], base_path: Path) -> dict[str, dict]:
    data = {}
    for key, file_str_path in file_str_paths.items():
        data[key] = load_json_file(rf"{base_path}\{file_str_path}")
    return data


def load_en_key_value_strings(file_str_path: str) -> dict:
    ron_en_strings = {}
    with open(file_str_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            lexer = shlex.shlex(line, posix=True)
            lexer.whitespace_split = True
            lexer.commenters = "//"
            parts = list(lexer)[:2]
            if len(parts) != 2:
                raise ValueError(f"Line {line_number} with unexpected format.\n{parts}")
            key, value = parts
            ron_en_strings[key] = value
    return ron_en_strings


def save_json_file(file_path: Path, data: dict, indent_size: int | None):
    logger.info(f"Saving JSON file {file_path}")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent_size)


def save_json_files(file_paths: dict[str, Path], base_path: Path, data: dict, indent_size: int | None):
    for key, file_path in file_paths.items():
        save_json_file(Path(rf"{base_path}\{file_path}"), data[key], indent_size)


def save_language_file(file_path: Path, data: dict):
    logger.info(f"Saving language file {file_path}")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as f:
        for key, value in data.items():
            f.write(f'{key} "{value}"\n')


def ensure_dist_drs_graphics_folder():
    logger.info(rf"Ensure language en folder {ROR_UNIT_GRAPHICS_FOLDER_PATH}")
    Path(rf"dist\{ROR_UNIT_GRAPHICS_FOLDER_PATH}").mkdir(parents=True, exist_ok=True)


def main():
    start = time.time()
    parser = argparse.ArgumentParser(
        prog="create_mod",
        description="Programmatically mod Genie engine dat files of "
        " Age of Empires II Definitive Edition: Return of Rome",
    )
    parser.add_argument("--logfile", type=Path, required=False)
    parser.add_argument("--loglevel", choices=["info", "debug"], required=False, default="info")
    args = parser.parse_args()

    log_level = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
    }

    load_dotenv()

    log_filename = args.logfile
    logging.basicConfig(filename=log_filename, level=log_level[args.loglevel])

    aoe2_data = load_dat_file(rf'{getenv("BASE_AOE2_DIR")}\{AOE2_DAT_FILE_PATH}')
    ror_data = load_dat_file(rf'{getenv("BASE_AOE2_DIR")}\{ROR_DAT_FILE_PATH}')

    ror_hotkeys = load_json_file(rf'{getenv("BASE_AOE2_DIR")}\{HOTKEYS_FILE_PATH}')
    ror_civ_tech_trees = load_json_files(CIV_TECH_TREES_FILE_PATH, rf'{getenv("BASE_AOE2_DIR")}\{ROR_DAT_FOLDER_PATH}')
    ror_futuravailableunits = load_json_file(rf'{getenv("BASE_AOE2_DIR")}\{FUTURAVAILABLEUNITS_FILE_PATH}')
    aoe2_strings_en = load_en_key_value_strings(rf'{getenv("BASE_AOE2_DIR")}\{AOE2_STRINGS_FILE_PATH_EN}')
    ror_strings_en = load_en_key_value_strings(rf'{getenv("BASE_AOE2_DIR")}\{ROR_STRINGS_FILE_PATH_EN}')
    ror_modded_strings_en = {}
    aoe2_icons = load_json_file(rf'{getenv("BASE_AOE2_DIR")}\{AOE2_UI_FOLDER_PATH}\icons.json')
    ror_icons = load_json_file(rf'{getenv("BASE_AOE2_DIR")}\{ROR_UI_FOLDER_PATH}\icons.json')

    Path(rf"dist\{ROR_DAT_FOLDER_PATH}").mkdir(parents=True, exist_ok=True)
    ensure_dist_drs_graphics_folder()

    logger.info("Applying mods")
    new_units = {}
    new_techs = {}

    bowman_line.mod(
        ror_data, ror_hotkeys, ror_civ_tech_trees, ror_futuravailableunits, ror_strings_en, ror_modded_strings_en
    )
    spearman_line.mod(
        aoe2_data,
        ror_data,
        ror_hotkeys,
        ror_civ_tech_trees,
        ror_futuravailableunits,
        aoe2_strings_en,
        ror_modded_strings_en,
        new_units,
        new_techs,
        aoe2_icons,
        ror_icons,
    )

    # TODO: tech tree preview

    output_dat_file_path = rf"dist\{ROR_DAT_FILE_PATH}"
    logger.info(f"Saving dat file {output_dat_file_path}")
    ror_data.save(output_dat_file_path)

    save_json_file(Path(rf"dist\{HOTKEYS_FILE_PATH}"), data=ror_hotkeys, indent_size=3)
    save_json_files(
        file_paths=CIV_TECH_TREES_FILE_PATH,
        base_path=rf"dist\{ROR_DAT_FOLDER_PATH}",
        data=ror_civ_tech_trees,
        indent_size=2,
    )
    save_json_file(Path(rf"dist\{FUTURAVAILABLEUNITS_FILE_PATH}"), data=ror_futuravailableunits, indent_size=2)
    save_language_file(Path(rf"dist\{MODDED_STRINGS_FILE_PATH_EN}"), ror_modded_strings_en)
    save_json_file(Path(rf"dist\{ROR_UI_FOLDER_PATH}\icons.json"), data=ror_icons, indent_size=2)

    end = time.time()
    logger.info(f"Took {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
