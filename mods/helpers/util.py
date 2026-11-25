import logging
import shutil

# from pathlib import Path
from dotenv import load_dotenv
from os import getenv

from genieutils.common import GenieClass, ByteHandler
from genieutils.versions import Version

from mods.helpers.files import AOE2_UNIT_GRAPHICS_FOLDER_PATH, ROR_UNIT_GRAPHICS_FOLDER_PATH

logger = logging.getLogger(__name__)


def clone(item: GenieClass, version: str) -> GenieClass:
    packed = item.to_bytes(Version(version))
    byte_handler = ByteHandler(memoryview(packed))
    byte_handler.version = Version(version)
    return item.__class__.from_bytes(byte_handler)


def copy_aoe2_sld_sprites_file(sld_file_name: str):
    logger.debug(rf"Copying SLD file {sld_file_name}")

    load_dotenv()

    shutil.copy2(
        rf"{getenv("BASE_AOE2_DIR")}\{AOE2_UNIT_GRAPHICS_FOLDER_PATH}\{sld_file_name}.sld",
        rf"dist\{ROR_UNIT_GRAPHICS_FOLDER_PATH}\{sld_file_name}.sld",
    )
