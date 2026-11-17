import logging
import time

from dotenv import load_dotenv
from os import getenv
from pathlib import Path
from genieutils.datfile import DatFile

from mods.helpers.files import AOE2_DAT_FILE_PATH, ROR_DAT_FILE_PATH


def main():
    start = time.time()

    load_dotenv()

    logging.basicConfig(filename="myapp.log", level=logging.INFO)

    ror_data_file_path = f'{getenv("BASE_AOE2_DIR")}\\{ROR_DAT_FILE_PATH}'
    logging.info(f"Loading dat file {ror_data_file_path}")
    ror_data = DatFile.parse(ror_data_file_path)

    aoe2_data_file_path = f'{getenv("BASE_AOE2_DIR")}\\{AOE2_DAT_FILE_PATH}'
    logging.info(f"Loading dat file {aoe2_data_file_path}")
    aoe2_data = DatFile.parse(aoe2_data_file_path)

    # logging.info(f'Applying mods')
    # for mod in args.mods:
    #     logging.info(f'Applying {mod}:')
    #     AVAILABLE_MODS[mod](data)

    Path(r".\dist").mkdir(exist_ok=True)
    output_dat_file_path = r".\dist\empires2_x2_p1.dat"
    logging.info(f"Saving dat file {output_dat_file_path}")
    ror_data.save(output_dat_file_path)

    end = time.time()
    logging.info(f"Took {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
