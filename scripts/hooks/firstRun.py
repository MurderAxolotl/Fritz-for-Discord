"""Handles setup on the first startup. Simply importing the module is enough"""

import os

from resources.shared import PATH
from resources.colour import *

if not os.path.isdir(PATH + "/logs"): os.mkdir(PATH + "/logs"); print(SEAFOAM + "FIRSTRUN: Created /logs" + RESET)
if not os.path.isdir(PATH + "/logs/system"): os.mkdir(PATH + "/logs/system"); print(SEAFOAM + "FIRSTRUN: Created /logs/system" + RESET)
if not os.path.isdir(PATH + "/logs/guilds"): os.mkdir(PATH + "/logs/guilds"); print(SEAFOAM + "FIRSTRUN: Created /logs/guilds" + RESET)
if not os.path.isdir(PATH + "/logs/users"): os.mkdir(PATH + "/logs/users"); print(SEAFOAM + "FIRSTRUN: Created /logs/users" + RESET)
if not os.path.isdir(PATH + "/cache"): os.mkdir(PATH + "/cache"); print(SEAFOAM + "FIRSTRUN: Created /cache" + RESET)
if not os.path.isdir(PATH + "/cache/qr"): os.mkdir(PATH + "/cache/qr"); print(SEAFOAM + "FIRSTRUN: Created /cache/qr" + RESET)