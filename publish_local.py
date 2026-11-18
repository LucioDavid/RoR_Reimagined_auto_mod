import json
import shutil

from pathlib import Path
from dotenv import load_dotenv
from os import getenv

from mods.helpers.files import ROR_DAT_FOLDER_PATH, ROR_DAT_FILE_PATH


def create_info_file(mod_path: Path, mod_name: str):
    data = {
        "Author": "Unpublished",
        "CacheStatus": 0,
        "Description": "No Description",
        "Title": f"{mod_name}",
    }

    json_str = json.dumps(data, indent=None)
    with open(f"{mod_path}\\info.json", "w") as f:
        f.write(json_str)


def copy_dat_file():
    load_dotenv()

    Path(
        rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}\{ROR_DAT_FOLDER_PATH}"
    ).mkdir(parents=True, exist_ok=True)

    shutil.copy2(
        rf".\dist\{ROR_DAT_FILE_PATH}",
        rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}\{ROR_DAT_FILE_PATH}",
    )


def main():
    load_dotenv()

    mod_path = rf"{getenv("MODS_LOCAL_DIR")}\{getenv("MOD_NAME")}"
    Path(mod_path).mkdir(exist_ok=True)

    create_info_file(mod_path, getenv("MOD_NAME"))
    copy_dat_file()


if __name__ == "__main__":
    main()
