"""
Some experiments

@author Kevin Wilson <khwilson@gmail.com>
"""
from crisis.parsers import ConversationIndex
from crisis.parsers import MessageIndex

import calendar
import datetime
import itertools as its
import numpy as np

dt = datetime.datetime
td = datetime.timedelta

def c_id_to_rating(conversation_lines):
	"""
	Given a list with the parsed lines of the conversation file, return
	a dict from c_id to the rating. Only return those conversations with
	nonempty ratings
	"""
	return dict(
		(line[ConversationIndex.c_id], line[ConversationIndex.conv_rating])
			for line in conversation_lines
			if type(line[ConversationIndex.conv_rating]) is int)

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

def join_ratings_and_distributions(message_lines, conversation_lines):
	"""
	Given the parsed lines from the conversation database and the parsed lines
	from the message database, return pairs of ratings vs. distributions of
	intermessage times.
	"""
	grouped_messages = group_message_lines_by_c_id(message_lines)

def group_conversations_by_counselor(grouped_messages):
	output = {}
	for c_id, conversation in grouped_messages.iteritems():
		counselor = -1
		for msg in conversation:
			if (msg[MessageIndex.actor_type] == 'Internal' and
					msg[MessageIndex.a_id] != 1):
				counselor = msg[MessageIndex.a_id]
		counselor_convos = output.setdefault(counselor, {})
		counselor_convos[c_id] = conversation
	return output

def filter_for_counselor_messages(line):
	if line[MessageIndex.actor_type] == 'Internal':
		return line[MessageIndex.a_id] != 1
	return False

def get_overlaps(conversations):
	"""
	Given a list of conversations, return the number of conversations a
	counselor is maintaining at one time.
	"""
	conversation_intervals = []
	intervals = []
	for conversation in conversations:
		conversation = filter(filter_for_counselor_messages, conversation)
		if len(conversation) == 0:
			return []

		first_message = conversation[0]
		cur_begin = first_message[MessageIndex.msg_time]
		cur_end = cur_begin + td(seconds=1)
		for message in conversation[1:]:
			this_time = message[MessageIndex.msg_time]
			if this_time - cur_end < td(minutes=10):
				cur_end = this_time
			else:
				intervals.append((cur_begin, cur_end))
				cur_begin = this_time
				cur_end = this_time + td(seconds=1)
		intervals.append((cur_begin, cur_end))

	begin_times, end_times = zip(*intervals)
	all_times = sorted(its.chain([(t, 1) for t in begin_times], [(t, -1) for t in end_times]))
	output = []
	cur_time = all_times.pop(0)[0]
	cur_count = 1
	for time, delta in all_times:
		if time != cur_time:
			output.append((time, cur_count))
		cur_count += delta
		cur_time = time
	output.append((cur_time, cur_count))

	return output
