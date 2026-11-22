import logging

from genieutils.datfile import DatFile
from genieutils.effect import EffectCommand, Effect
from genieutils.tech import ResearchLocation
from genieutils.unit import AttackOrArmor, ResourceCost, TrainLocation

from mods.helpers.ids_ror import (
    AGE_ID_IRON,
    BUILDING_ARCHERY_RANGE,
    EFFECT_COMPOSITE_BOW,
    EFFECT_IMPROVED_BOW,
    HOTKEY_GROUP_ARCHERY_RANGE,
    LANGUAGE_DLL_NAME_TECH_IMPROVED_BOW,
    LANGUAGE_DLL_NAME_UNIT_BOWMAN,
    STRING_HOTKEY_BOWMAN_UPGRADES,
    TECH_IMPROVED_BOW,
    TECH_COMPOSITE_BOW,
    TECH_IRON_AGE,
    TYPE_FOOD,
    TYPE_GOLD,
    UNIT_BOWMAN,
    UNIT_IMPROVED_BOWMAN,
    UNIT_COMPOSITE_BOWMAN,
)
from mods.helpers.lang_helper import language_dll_help_id

logger = logging.getLogger(__name__)


def modify_bowman(data: DatFile, ror_strings_en: dict, ror_modded_strings_en: dict, food: int, gold: int):
    logger.info("Changing Bowman cost of all civs")
    for civ in data.civs:
        bowman = civ.units[UNIT_BOWMAN]
        bowman.creatable.resource_costs = (
            ResourceCost(type=TYPE_FOOD, amount=food, flag=1),
            ResourceCost(type=TYPE_GOLD, amount=gold, flag=1),
            bowman.creatable.resource_costs[2],
        )

    logger.info("Changing Bowman language help to mention upgrade to Improved Bowman")
    logger.info("[Old]: %s" % ror_strings_en[f"{language_dll_help_id(LANGUAGE_DLL_NAME_UNIT_BOWMAN)}"])
    ror_modded_strings_en[f"{language_dll_help_id(LANGUAGE_DLL_NAME_UNIT_BOWMAN)}"] = (
        r"Train <b>Bowman<b> (<cost>)\nRanged unit. Strong vs. units at long range. Weak vs. Slingers and units at close range.\n<GREY><i>Upgrades: armor (Storage Pit); range (Market), attack, accuracy (Government Center); to Improved Bowman (Range).<i><DEFAULT>\n<hp> <attack> <armor> <piercearmor> <range>"
    )
    logger.info("[New]: %s" % ror_modded_strings_en[f"{language_dll_help_id(LANGUAGE_DLL_NAME_UNIT_BOWMAN)}"])


def modify_improved_bowman(data: DatFile, ror_strings_en: dict, ror_modded_strings_en: dict):
    logger.info("Changing Improved Bowman train button, hotkey and stats of all civs")
    for civ in data.civs:
        improved_bowman = civ.units[UNIT_IMPROVED_BOWMAN]
        improved_bowman.creatable.train_locations = [
            TrainLocation(
                train_time=improved_bowman.creatable.train_locations[0].train_time,
                unit_id=improved_bowman.creatable.train_locations[0].unit_id,
                button_id=1,
                hot_key_id=16083,
            )
        ]

        improved_bowman.type_50.attacks[0] = AttackOrArmor(class_=3, amount=5)
        improved_bowman.type_50.displayed_attack = 5

    logger.info("Changing Improved Bow tech button")
    improved_bow = data.techs[TECH_IMPROVED_BOW]
    improved_bow.research_locations = [
        ResearchLocation(
            location_id=improved_bow.research_locations[0].location_id,
            research_time=improved_bow.research_locations[0].research_time,
            button_id=6,
            hot_key_id=improved_bow.research_locations[0].hot_key_id,
        )
    ]

    logger.info("Making Improved Bow upgrade Bowman into Improved Bowman")
    improved_bow_effect = data.effects[EFFECT_IMPROVED_BOW]
    improved_bow_effect.effect_commands = [EffectCommand(type=3, a=UNIT_BOWMAN, b=UNIT_IMPROVED_BOWMAN, c=-1, d=0.0)]

    logger.info("Changing Improved Bow language help accordingly")
    logger.info("[Old]: %s" % ror_strings_en[f"{language_dll_help_id(LANGUAGE_DLL_NAME_TECH_IMPROVED_BOW)}"])
    ror_modded_strings_en[f"{language_dll_help_id(LANGUAGE_DLL_NAME_TECH_IMPROVED_BOW)}"] = (
        r"Upgrade to <b>Improved Bow<b> (<cost>)\nUpgrades your Bowmen and lets you train Improved Bowmen, which are stronger."
    )
    logger.info("[New]: %s" % ror_modded_strings_en[f"{language_dll_help_id(LANGUAGE_DLL_NAME_TECH_IMPROVED_BOW)}"])


def modify_composite_bowman(data: DatFile):
    logger.info("Changing Composite Bowman train button, hotkey and stats of all civs")
    for civ in data.civs:
        composite_bowman = civ.units[UNIT_COMPOSITE_BOWMAN]
        composite_bowman.creatable.train_locations = [
            TrainLocation(
                composite_bowman.creatable.train_locations[0].train_time,
                composite_bowman.creatable.train_locations[0].unit_id,
                button_id=1,
                hot_key_id=16083,
            )
        ]

        composite_bowman.type_50.attacks[0] = AttackOrArmor(class_=3, amount=7)
        composite_bowman.type_50.displayed_attack = 7

    logger.info("Changing Composite Bow tech button")
    composite_bow = data.techs[TECH_COMPOSITE_BOW]
    composite_bow.research_locations = [
        ResearchLocation(
            location_id=composite_bow.research_locations[0].location_id,
            research_time=composite_bow.research_locations[0].research_time,
            button_id=6,
            hot_key_id=composite_bow.research_locations[0].hot_key_id,
        )
    ]

    logger.info("Moving Composite Bow tech to Iron Age")
    composite_bow.required_techs = (TECH_IMPROVED_BOW, TECH_IRON_AGE, -1, -1, -1, -1)

    logger.info("Making Composite Bow upgrade Bowman into Composite Bowman")
    composite_bow_effect = data.effects[EFFECT_COMPOSITE_BOW]
    composite_bow_effect.effect_commands.append(
        EffectCommand(type=3, a=UNIT_BOWMAN, b=UNIT_COMPOSITE_BOWMAN, c=-1, d=0.0)
    )


def modify_bowman_line_upgrades_default_hotkey(hotkeys: dict):
    logger.info("Changing Composite Bow and Improved Bow techs default hotkey")
    hotkey = next(
        (
            item
            for item in hotkeys["hotkey_group_list"][HOTKEY_GROUP_ARCHERY_RANGE]["hotkey_list"]
            if item["name_string_id"] == STRING_HOTKEY_BOWMAN_UPGRADES
        ),
        None,
    )
    hotkey["defaults_list"] = [
        {"name": "definitive", "key": "A"},
        {"name": "left handed", "key": "H"},
    ]


def modify_bowman_line_tech_tree_view(civ_tech_trees: dict):
    logger.info("Changing Bowman-line tech tree view of all civs")

    for _, civ in civ_tech_trees.items():
        imp_bowman = next(
            (item for item in civ["civ_techs_units"] if item["Node ID"] == UNIT_IMPROVED_BOWMAN),
            None,
        )
        imp_bowman["Node Type"] = "UnitUpgrade"
        imp_bowman["Link Node Type"] = "Unit"
        imp_bowman["Link ID"] = UNIT_BOWMAN
        imp_bowman["Trigger Tech ID"] = TECH_IMPROVED_BOW
        imp_bowman.pop("Prerequisite IDs")
        imp_bowman.pop("Prerequisite Types")

        comp_bowman = next(
            (item for item in civ["civ_techs_units"] if item["Node ID"] == UNIT_COMPOSITE_BOWMAN),
            None,
        )
        comp_bowman["Age ID"] = AGE_ID_IRON
        comp_bowman["Link Node Type"] = "UnitUpgrade"


def modify_futuravailable_bowman_line_upgrades(futuravailableunits: dict):
    logger.info("Changing Bowman-line futuravailableunits of all civs")
    for _, civ in futuravailableunits.items():
        archery_range = next(
            (item for item in civ["Buildings"] if item["ID"] == BUILDING_ARCHERY_RANGE),
            None,
        )
        if archery_range is None:
            continue

        techs = archery_range.get("Techs")
        if techs is not None:
            comp_bow = next(
                (item for item in techs if item["ID"] == TECH_COMPOSITE_BOW),
                None,
            )
            if comp_bow is not None:
                comp_bow["RequiredAge"] = AGE_ID_IRON

        units = archery_range["Units"]
        imp_bowman = next(
            (item for item in units if item["ID"] == UNIT_IMPROVED_BOWMAN),
            None,
        )

        if imp_bowman is not None:
            units.remove(imp_bowman)


def mod(
    data: DatFile,
    hotkeys: dict,
    civ_tech_trees: dict,
    futuravailableunits: dict,
    ror_strings_en: dict,
    ror_modded_strings_en: dict,
):
    logger.info("🔧 Applying Bowman-line modifications:")
    modify_bowman(data, ror_strings_en, ror_modded_strings_en, food=40, gold=20)
    modify_improved_bowman(data, ror_strings_en, ror_modded_strings_en)
    modify_composite_bowman(data)
    modify_bowman_line_upgrades_default_hotkey(hotkeys)
    modify_bowman_line_tech_tree_view(civ_tech_trees)
    modify_futuravailable_bowman_line_upgrades(futuravailableunits)
