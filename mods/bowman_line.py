import logging

# from pathlib import Path

from genieutils.datfile import DatFile
from genieutils.effect import EffectCommand, Effect
from genieutils.tech import ResearchLocation
from genieutils.unit import ResourceCost, TrainLocation

from mods.helpers.ids_ror import (
    EFFECT_COMPOSITE_BOW,
    EFFECT_IMPROVED_BOW,
    HOTKEY_GROUP_ARCHERY_RANGE,
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

logger = logging.getLogger(__name__)


def modify_bowman(data: DatFile, food: int, gold: int):
    logger.info("Changing Bowman cost of all civs")
    for civ in data.civs:
        bowman = civ.units[UNIT_BOWMAN]
        bowman.creatable.resource_costs = (
            ResourceCost(type=TYPE_FOOD, amount=food, flag=1),
            ResourceCost(type=TYPE_GOLD, amount=gold, flag=1),
            bowman.creatable.resource_costs[2],
        )


def modify_improved_bowman(data: DatFile):
    logger.info("Changing Improved Bowman train button and hotkey of all civs")
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

        # TODO: change Improved Bowman stats

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
    improved_bow_effect.effect_commands = [
        EffectCommand(type=3, a=UNIT_BOWMAN, b=UNIT_IMPROVED_BOWMAN, c=-1, d=0.0)
    ]


def modify_composite_bowman(data: DatFile):
    logger.info("Changing Composite Bowman train button and hotkey of all civs")
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

        # TODO: change Composite Bowman stats

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
            for item in hotkeys["hotkey_group_list"][HOTKEY_GROUP_ARCHERY_RANGE][
                "hotkey_list"
            ]
            if item["name_string_id"] == STRING_HOTKEY_BOWMAN_UPGRADES
        ),
        None,
    )
    hotkey["defaults_list"] = [
        {"name": "definitive", "key": "A"},
        {"name": "left handed", "key": "H"},
    ]

    return hotkeys


# def modify_bowman_line_tech_tree_view(tech_tree_file_path: Path)


# def modify_futuravailable_bowman_line_upgrades(futuravailableunits_file_path: Path)


def mod(data: DatFile, hotkeys: dict):
    logger.info("🔧 Applying Bowman-line modifications:")
    modify_bowman(data, food=40, gold=20)
    modify_improved_bowman(data)
    modify_composite_bowman(data)
    hotkeys = modify_bowman_line_upgrades_default_hotkey(hotkeys)
    # modify_bowman_line_tech_tree_view(tech_tree_file_path)
    # modify_futuravailable_bowman_line_upgrades(futuravailableunits_file_path)
    return hotkeys
