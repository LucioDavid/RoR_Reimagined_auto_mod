def language_dll_creation_id(language_dll_name_id: int):
    return language_dll_name_id + 1000


def language_dll_help_id(language_dll_name_id: int):
    return language_dll_name_id + 21000


def language_tech_tree_unit_id(language_dll_name_id: int):
    return language_dll_name_id + 9000


def language_tech_tree_tech_id(language_dll_name_id: int):
    return language_dll_name_id + 10000


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
