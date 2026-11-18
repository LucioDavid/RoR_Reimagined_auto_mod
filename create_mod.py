import argparse
import logging
import time

from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from genieutils.datfile import DatFile

from mods.helpers.files import (
    AOE2_DAT_FILE_PATH,
    ROR_DAT_FOLDER_PATH,
    ROR_DAT_FILE_PATH,
)
from mods import bowman_line

logger = logging.getLogger(__name__)


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

    ror_data_file_path = f'{getenv("BASE_AOE2_DIR")}\\{ROR_DAT_FILE_PATH}'
    logger.info(f"Loading dat file {ror_data_file_path}")
    ror_data = DatFile.parse(ror_data_file_path)

    aoe2_data_file_path = f'{getenv("BASE_AOE2_DIR")}\\{AOE2_DAT_FILE_PATH}'
    logger.info(f"Loading dat file {aoe2_data_file_path}")
    aoe2_data = DatFile.parse(aoe2_data_file_path)

    logger.info("Applying mods")
    bowman_line.mod(ror_data)

    Path(rf".\dist\{ROR_DAT_FOLDER_PATH}").mkdir(parents=True, exist_ok=True)

    output_dat_file_path = rf".\dist\{ROR_DAT_FILE_PATH}"
    logger.info(f"Saving dat file {output_dat_file_path}")
    ror_data.save(output_dat_file_path)

    end = time.time()
    logger.info(f"Took {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
