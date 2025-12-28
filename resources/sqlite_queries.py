""" Queries for SQLite """

class starboard_queries:
	create_starboard_cache_table = """
CREATE TABLE IF NOT EXISTS starboard (
	message_id TEXT NOT NULL,
	starboard_message_id TEXT NOT NULL
)
"""

	search_cache = """
SELECT EXISTS(SELECT 1 FROM starboard WHERE message_id = "{message_id}" LIMIT 1);
"""

# 	search_cache = """
# SELECT COUNT(*) FROM starboard WHERE message_id = "{message_id}";
# """

	write_cache = """
INSERT INTO
	starboard (message_id, starboard_message_id)
VALUES
	({message_id}, {starboard_message_id});
"""
