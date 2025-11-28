"""Handles setup on the first startup. Simply importing the module is enough"""

import os

from resources.shared import PATH
from resources.colour import YELLOW, MAGENTA, SEAFOAM, RESET

import scripts.tools.journal as journal

def __createFolder(subpath:str) -> None:
	os.mkdir(f"{PATH}{subpath}")

	journal.log(f"{SEAFOAM}Setup: {{reset_colour}}Created {MAGENTA}{subpath}", 5)

if not os.path.isdir(PATH + "/logs"):        __createFolder("/logs")
if not os.path.isdir(PATH + "/logs/system"): __createFolder("/logs/system")
if not os.path.isdir(PATH + "/logs/guilds"): __createFolder("/logs/guilds")
if not os.path.isdir(PATH + "/logs/users"):  __createFolder("/logs/users")
if not os.path.isdir(PATH + "/cache"):       __createFolder("/cache")
if not os.path.isdir(PATH + "/cache/qr"):    __createFolder("/cache/qr")
if not os.path.isdir(PATH + "/config"):      __createFolder("/config")
if not os.path.isdir(PATH + "/plugins"):     __createFolder("/plugins")
