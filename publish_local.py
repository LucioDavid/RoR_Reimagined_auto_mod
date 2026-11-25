import argparse
import json
import logging
import shutil
import time

from pathlib import Path
from dotenv import load_dotenv
from os import getenv

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


def copy_dist_to_local_mod(mod_path: str):
    logger.info(rf"Copying dist/ to {mod_path}")
    shutil.copytree("dist", mod_path, dirs_exist_ok=True)


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

    copy_dist_to_local_mod(mod_path)
    create_info_file(mod_path)

    end = time.time()
    logger.info(f"Took {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
