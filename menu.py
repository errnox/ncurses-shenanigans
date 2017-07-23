from collections import deque
from menustructure import menustructure
from configparser import pre_process, parse


def generatemenu(choice):
    """Generates a submenu list that includes all leafe lists"""
    return _clean_leaves(_generatemenu(choice))

def generaterawmenu(choice):
    """Generates a leafe list free submenu list"""
    submenu = _generatemenu(choice)
    # from logger import log
    # log("debug.log", "raw menu = "+str(submenu))
    return submenu

def _generatemenu(choice):
    """
    Processes the menu configuration file and generates a submenu for choice.
    """
    # Load nested list directly from menustructure.py
    # mstruct = menustructure
    # Generate nested list from config file
    processed = pre_process("menu.conf")
    mstruct = parse(processed)
    # 1. Short version
    # submenu = [b for a, b in collect_all(mstruct) if a == choice][0]
    # 2. Long version
    submenu = []
    all_submenus = [m for m in collect_all(mstruct)]

    for lst in all_submenus:
        if lst[0] == choice:
            submenu.append(lst[1])

    if len(submenu) > 0:
        submenu = submenu[0] # Messy

    return submenu


def _clean_leaves(submenu):
    # Look at all the entries in the submenu and replace each entry
    # which is a dict with the key in the dict
    # Every dict consists of one key and one value only by conventions (Messy!)
    for i, entry in enumerate(submenu):
        if isinstance(entry, dict):
            submenu[i] =  submenu[i].keys()[0]
    from logger import log
    log("debug.log", "submenu = "+str(submenu))

    return submenu


def generate_leave_list():
    processed = pre_process("menu.conf")
    mstruct = parse(processed)
    submenus = collect_all(mstruct)
    tmp_list = []

    leave_list = []

    for m in submenus:
        if isinstance(m[0], dict):
            tmp_list.append(m[0])

    # Make a list of tuples instead of dicts
    for i, dictionary in enumerate(tmp_list):
        leave_list.append(tmp_list[i].items()[0])

    return leave_list


def collect_all(menu):
    """
    Generates a list of all submenus.
    Submenus are represented as lists themselves. The first element of
    every submenu list is the parent entry.
    """
    entries = []
    to_visit = deque([menu])
    while to_visit:
        some_menu = to_visit.popleft()
        children = some_menu[1:]
        entries.append((some_menu[0], [child[0] for child in children]))
        to_visit.extend(children)
    return entries


# print '\n'.join(repr(m) for m in collect_all(menu))

