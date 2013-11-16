"""
Some experiments

@author Kevin Wilson <khwilson@gmail.com>
"""
from crisis.parsers import ConversationIndex
from crisis.parsers import MessageIndex

import calendar
import numpy as np

def group_message_lines_by_c_id(message_lines):
	"""
	Given a list of lines from the message file, group the lines by
	conversation id. The output is a dict from conversation id to the
	list of lines (sorted by message time) which are in a conversation id
	"""
	s_message_lines = sorted(message_lines, key=lambda x: (x[MessageIndex.c_id],
													x[MessageIndex.msg_time]))
	output = {}
	for line in s_message_lines:
		this_list = output.setdefault(line[MessageIndex.c_id], [])
		this_list.append(line)

	return output

def intermessage_times(parsed_lines):
	"""
	Given the output of group_message_lines_by_c_id, return the intermessage
	times in a dict.
	"""
	return dict((c_id, np.ediff1d([calendar.timegm(line[MessageIndex.msg_time].timetuple())
									for line in lines])) for c_id, lines in parsed_lines.iteritems())

