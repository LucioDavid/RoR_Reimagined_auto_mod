import logging

# from pathlib import Path

from genieutils.tech import ResearchLocation
from genieutils.datfile import DatFile
from genieutils.unit import ResourceCost, TrainLocation

from mods.helpers.ids_ror import (
    UNIT_BOWMAN,
    UNIT_IMPROVED_BOWMAN,
    UNIT_COMPOSITE_BOWMAN,
    TECH_IMPROVED_BOW,
    TECH_COMPOSITE_BOW,
    TYPE_FOOD,
    TYPE_GOLD,
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


# def modify_bowman_line_upgrades_default_hotkey(hotkeys_file_path: Path):
# logger.info("Changing Composite Bow and Improved Bow techs default hotkey")


# def modify_bowman_line_tech_tree_view(tech_tree_file_path: Path)


# def modify_futuravailable_bowman_line_upgrades(futuravailableunits_file_path: Path)


def mod(data: DatFile):
    logger.info("Applying Bowman-line modifications:")
    modify_bowman(data, food=40, gold=20)
    modify_improved_bowman(data)
    modify_composite_bowman(data)
    # modify_bowman_line_upgrades_default_hotkey(hotkeys_file_path)
    # modify_bowman_line_tech_tree_view(tech_tree_file_path)
    # modify_futuravailable_bowman_line_upgrades(futuravailableunits_file_path)
