def language_dll_creation_id(language_dll_name_id: int):
    return language_dll_name_id + 1000


def language_dll_help_id(language_dll_name_id: int):
    return language_dll_name_id + 21000


def language_name_string_id_unit(language_dll_name_id: int):
    """
    Used in a tech tree JSON file for units as "Name String ID".
    """
    return language_dll_name_id + 9000


def language_name_string_id_tech(language_dll_name_id: int):
    """
    Used in a tech tree JSON file for techs as "Name String ID".
    """
    return language_dll_name_id + 10000


def language_help_string_id(language_dll_name_id: int):
    """
    Used in a tech tree JSON file for units and techs as "Help String ID".
    """
    return language_dll_name_id + 100000


def id_for_string_index_list(language_dll_name_id: int):
    return language_dll_creation_id(language_dll_name_id) + 10000


def first_unused_id_from_id(ror_strings_en: dict, starting_id: int):
    unused_id = starting_id
    while str(unused_id) in ror_strings_en:
        unused_id += 1
    return unused_id


def first_used_id_from_id(ror_strings_en: dict, starting_id: int):
    used_id = starting_id
    while str(used_id) not in ror_strings_en:
        used_id += 1
    return used_id
