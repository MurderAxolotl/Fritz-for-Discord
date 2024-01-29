import os
from sqlite_utils import Database

from resources.shared import PATH, database

CONFIG_FILE = PATH + "/config.db"

def __load_db(): return Database(CONFIG_FILE)

def setup(server_id):
	database["server_settings"].insert([{"id":server_id, "administrators":"[]", "allow_ai":True}])

def add_administrator(server_id, user_id):
	NotImplemented
