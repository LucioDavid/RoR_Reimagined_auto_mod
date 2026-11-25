import logging

from genieutils.datfile import DatFile
from genieutils.effect import EffectCommand, Effect
from genieutils.tech import ResearchLocation, ResearchResourceCost, Tech
from genieutils.unit import TrainLocation

from mods.helpers.ids_aoe2 import ACHAEMENIDS_CIV_ID, UNIT_SPEARMAN
from mods.helpers.ids_ror import (
    AGE_ID_TOOL,
    BUILDING_BARRACKS,
    HOTKEY_GROUP_BARRACKS,
    LANGUAGE_DLL_NAME_UNIT_ELITE_GUARDSMAN,
    LANGUAGE_DLL_NAME_UNIT_GUARDSMAN,
    LANGUAGE_DLL_NAME_UNIT_SPEARMAN,
    STRING_HOTKEY_SPEARMAN_TRAIN,
    TECH_TOOL_AGE,
    TYPE_ENABLE_UNIT,
)
from mods.helpers.lang_helper import (
    id_for_string_index_list,
    language_dll_creation_id,
    language_dll_help_id,
    language_help_string_id,
    language_name_string_id_unit,
)
from mods.helpers.util import clone, copy_aoe2_sld_sprites_file

logger = logging.getLogger(__name__)


def add_spearman(
    aoe2_data: DatFile,
    ror_data: DatFile,
    hotkeys: dict,
    civ_tech_trees: dict,
    futuravailableunits: dict,
    aoe2_strings_en: dict,
    ror_modded_strings_en: dict,
    new_units: dict,
    new_techs: dict,
    aoe2_icons: dict,
    ror_icons: dict,
):
    logger.info("Adding Spearman to all civs")

    spearman_dead_id = len(ror_data.civs[1].units)
    spearman_dead = clone(
        aoe2_data.civs[ACHAEMENIDS_CIV_ID].units[aoe2_data.civs[ACHAEMENIDS_CIV_ID].units[UNIT_SPEARMAN].dead_unit_id],
        version=aoe2_data.version,
    )
    spearman_dead.id = spearman_dead_id
    spearman_dead.name = "Spearman (Dead)"
    for civ in ror_data.civs:
        logger.debug(f"Adding Spearman (Dead) for civ {civ.name} with ID {spearman_dead_id}")
        civ.units.append(spearman_dead)
        civ.unit_pointers.append(1)

    spearman_id = len(ror_data.civs[1].units)
    spearman = clone(aoe2_data.civs[ACHAEMENIDS_CIV_ID].units[UNIT_SPEARMAN], version=aoe2_data.version)
    spearman.id = spearman_id
    spearman.enabled = 0
    spearman.name = "Spearman"
    spearman.language_dll_name = LANGUAGE_DLL_NAME_UNIT_SPEARMAN
    spearman.language_dll_creation = language_dll_creation_id(LANGUAGE_DLL_NAME_UNIT_SPEARMAN)
    spearman.dead_unit_id = spearman_dead_id

    ror_modded_strings_en[f"{LANGUAGE_DLL_NAME_UNIT_SPEARMAN}"] = spearman.name
    ror_modded_strings_en[f"{language_dll_creation_id(LANGUAGE_DLL_NAME_UNIT_SPEARMAN)}"] = f"Train {spearman.name}"
    ror_modded_strings_en[f"{language_dll_help_id(LANGUAGE_DLL_NAME_UNIT_SPEARMAN)}"] = (
        rf"Train <b>{spearman.name}<b> (<cost>)\nAnti-cavalry infantry. Strong vs. Mounted Units, especially elephants. Weak vs. Ranged Soldiers and infantry.\n<GREY><i>Upgrades: attack, armor, pierce armor (Storage Pit); population space (Government Center); to Guardsman (Barracks).<i><DEFAULT>\n<hp> <attack> <armor> <piercearmor> <range>"
    )
    ror_modded_strings_en[f"{language_name_string_id_unit(LANGUAGE_DLL_NAME_UNIT_SPEARMAN)}"] = spearman.name
    ror_modded_strings_en[f"{STRING_HOTKEY_SPEARMAN_TRAIN}"] = f"{spearman.name}-line"

    create_spearman_hotkey = {
        "data_name": "BARRACKS_CREATE_SPEARMAN",
        "name_string_id": STRING_HOTKEY_SPEARMAN_TRAIN,
        "defaults_list": [{"name": "definitive", "key": "R"}, {"name": "left handed", "key": "O"}],
        "string_index_list": [
            id_for_string_index_list(LANGUAGE_DLL_NAME_UNIT_SPEARMAN),
            id_for_string_index_list(LANGUAGE_DLL_NAME_UNIT_GUARDSMAN),
            id_for_string_index_list(LANGUAGE_DLL_NAME_UNIT_ELITE_GUARDSMAN),
        ],
    }

    hotkeys["hotkey_group_list"][HOTKEY_GROUP_BARRACKS]["hotkey_list"].append(create_spearman_hotkey)

    spearman.creatable.train_locations = [
        TrainLocation(
            train_time=spearman.creatable.train_locations[0].train_time,
            unit_id=BUILDING_BARRACKS,
            button_id=4,
            hot_key_id=id_for_string_index_list(LANGUAGE_DLL_NAME_UNIT_SPEARMAN),
        )
    ]

    logger.debug(f"Adding Antiquity Spearman icon from AoE2")
    new_icon_id = len(ror_icons["Units"])
    ror_icons["Units"][f"{new_icon_id}"] = aoe2_icons["Units"][f"{spearman.icon_id}"]
    spearman.icon_id = new_icon_id

    for civ in ror_data.civs:
        logger.debug(f"Adding Spearman for civ {civ.name} with ID {spearman_id}")
        civ.units.append(spearman)
        civ.unit_pointers.append(1)

    effect_command = EffectCommand(type=TYPE_ENABLE_UNIT, a=spearman_id, b=1, c=-1, d=0.0)

    effect = Effect(name="Spearman (make avail)", effect_commands=[effect_command])
    effect_id = len(ror_data.effects)
    ror_data.effects.append(effect)

    tech = Tech(
        required_techs=(TECH_TOOL_AGE, -1, -1, -1, -1, -1),
        resource_costs=(
            ResearchResourceCost(type=-1, amount=0, flag=0),
            ResearchResourceCost(type=-1, amount=0, flag=0),
            ResearchResourceCost(type=-1, amount=0, flag=0),
        ),
        required_tech_count=1,
        civ=-1,
        full_tech_mode=1,
        language_dll_name=0,
        language_dll_description=0,
        effect_id=effect_id,
        type=0,
        icon_id=0,
        language_dll_help=0,
        language_dll_tech_tree=0,
        name="Spearman (make avail)",
        repeatable=1,
        research_locations=[
            ResearchLocation(location_id=-1, research_time=0, button_id=0, hot_key_id=0),
        ],
    )
    spearman_tech_id = len(ror_data.techs)
    logger.info(f"Adding Spearman Tech with id {spearman_tech_id}")
    ror_data.techs.append(tech)

    logger.info("Copying Spearman graphics from AoE2")
    standing_graphics_a_id = aoe2_data.civs[ACHAEMENIDS_CIV_ID].units[UNIT_SPEARMAN].standing_graphic[0]
    dying_graphic_id = aoe2_data.civs[ACHAEMENIDS_CIV_ID].units[UNIT_SPEARMAN].dying_graphic
    walking_graphic_id = aoe2_data.civs[ACHAEMENIDS_CIV_ID].units[UNIT_SPEARMAN].dead_fish.walking_graphic
    attack_graphic_id = aoe2_data.civs[ACHAEMENIDS_CIV_ID].units[UNIT_SPEARMAN].type_50.attack_graphic
    special_graphic_id = aoe2_data.civs[ACHAEMENIDS_CIV_ID].units[UNIT_SPEARMAN].creatable.special_graphic
    decay_id = (
        aoe2_data.civs[ACHAEMENIDS_CIV_ID]
        .units[aoe2_data.civs[ACHAEMENIDS_CIV_ID].units[UNIT_SPEARMAN].dead_unit_id]
        .standing_graphic[0]
    )
    for graphic_id in (
        standing_graphics_a_id,
        dying_graphic_id,
        walking_graphic_id,
        attack_graphic_id,
        special_graphic_id,
        decay_id,
    ):
        ror_data.graphics[graphic_id] = aoe2_data.graphics[graphic_id]
        copy_aoe2_sld_sprites_file(aoe2_data.graphics[graphic_id].file_name)

    logger.debug("Adding Spearman to tech tree view of all civs")
    for _, civ in civ_tech_trees.items():
        civ["civ_techs_units"].append(
            {
                "Name": f"{spearman.name}",
                "Node Type": "Unit",
                "Link Node Type": "BuildingTech",
                "Draw Node Type": "UnitTech",
                "Use Type": "Unit",
                "Node Status": "ResearchedCompleted",
                "Name String ID": language_name_string_id_unit(LANGUAGE_DLL_NAME_UNIT_SPEARMAN),
                "Age ID": AGE_ID_TOOL,
                "Building ID": BUILDING_BARRACKS,
                "Help String ID": language_help_string_id(LANGUAGE_DLL_NAME_UNIT_SPEARMAN),
                "Node ID": spearman.id,
                "Picture Index": spearman.icon_id,
            }
        )

    # TODO: parei aqui -- falta corrigir áudios

    new_units["Spearman"] = spearman_id
    new_techs["Spearman"] = spearman_tech_id


def add_guardsman(
    aoe2_data: DatFile,
    ror_data: DatFile,
    hotkeys: dict,
    civ_tech_trees: dict,
    futuravailableunits: dict,
    aoe2_strings_en: dict,
    ror_modded_strings_en: dict,
):
    logger.info("Adding Guardsman to all civs")
    pass


def add_elite_guardsman(
    aoe2_data: DatFile,
    ror_data: DatFile,
    hotkeys: dict,
    civ_tech_trees: dict,
    futuravailableunits: dict,
    aoe2_strings_en: dict,
    ror_modded_strings_en: dict,
):
    logger.info("Adding Elite Guardsman to all civs")
    pass


def mod(
    aoe2_data: DatFile,
    ror_data: DatFile,
    hotkeys: dict,
    civ_tech_trees: dict,
    futuravailableunits: dict,
    aoe2_strings_en: dict,
    ror_modded_strings_en: dict,
    new_units: dict,
    new_techs: dict,
    aoe2_icons: dict,
    ror_icons: dict,
):
    logger.info("🆕 Adding Spearman-line:")
    add_spearman(
        aoe2_data,
        ror_data,
        hotkeys,
        civ_tech_trees,
        futuravailableunits,
        aoe2_strings_en,
        ror_modded_strings_en,
        new_units,
        new_techs,
        aoe2_icons,
        ror_icons,
    )
    # add_guardsman(
    #     aoe2_data, ror_data, hotkeys, civ_tech_trees, futuravailableunits, aoe2_strings_en, ror_modded_strings_en
    # )
    # add_elite_guardsman(
    #     aoe2_data, ror_data, hotkeys, civ_tech_trees, futuravailableunits, aoe2_strings_en, ror_modded_strings_en
    # )
