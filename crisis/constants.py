"""
Constants for the Crisis Text Line data.

@author Kevin Wilson <khwilson@gmail.com>
"""
import os


this_dir = os.path.dirname(os.path.abspath(__file__))
this_repo_dir = os.path.abspath(os.path.join(this_dir, '..'))
CONVERSATION_DATA_FILENAME = 'data/dk_conversation_level_1311114.csv'
MESSAGE_DATA_FILENAME = 'data/dk_message_level_131114.csv'
