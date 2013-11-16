"""
Parsers and index enums for the Crisis Text Line data
"""
import crisis.constants as constants

import datetime
import itertools as its
import logging
import xlrd

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

dt = datetime.datetime
DATE_FMT = '%m/%d/%Y %H:%M'

type_list = 'a_id,profile_id,area_code,actor_type,m_id,c_id,msg_chars,msg_time,conv_start,conv_end,conv_rating,crisis_center_id,specialist_id,specialist_gender,Q2_conv_type,Q3_conv_type,Q8_conv_resolution,Q13_issues,Q14_issues,Q15_presenting_issue,Q36_visitor_feeling,Q37_counselor_feeling2,texter_id,first_msg,last_msg,addedtoqueue,takenfromqueue'
type_list = type_list.split(',')
ConversationIndex = type('ConversationIndex', (object,), dict((z, i) for i, z in enumerate(type_list)))

"""
a_id,profile_id,area_code,actor_type,m_id,c_id,msg_chars,msg_time,conv_start,conv_end,conv_rating,crisis_center_id,specialist_id,specialist_gender,Q2_conv_type,Q3_conv_type,Q8_conv_resolution,Q13_issues,Q14_issues,Q15_presenting_issue,Q36_visitor_feeling,Q37_counselor_feeling2,texter_id,first_msg,last_msg,addedtoqueue,takenfromqueue
actor id,,(int = counselor),"MobileMessenger indicates a teen, internal is our automated system or a counselor",message id,conversation id,character count,,,,"rated by teen. -1=bad, 1=good, 2=great",crisis center that responded,id of specialist,gender of specialist,was this a crisis conversation or not,"if not a crisis conversation, what was it?",what happened at the end of the conversation?,what issues did the teen mention?,describe other,what was the first or main issue mentioned by the teen?,how does the counselor think the teen was feeling,how is the counselor feeling overall,id of texter (client/visitor),first message sent by texter,last message sent by texter,time added,time taken by counselor
"""

type_list = 'a_id,profile_id,area_code,actor_type,m_id,c_id,msg_chars,msg_time,conv_start,conv_end,conv_rating,crisis_center_id,specialist_id,specialist_gender,Q2_conv_type,Q3_conv_type,Q8_conv_resolution,Q13_issues,Q14_issues,Q15_presenting_issue,Q36_visitor_feeling,Q37_counselor_feeling2,texter_id,first_msg,last_msg,addedtoqueue,takenfromqueue'
type_list = type_list.split(',')
MessageIndex = type('MessageIndex', (object,), dict((z, i) for i, z in enumerate(type_list)))

"""
actor id,,(int = counselor),"MobileMessenger indicates a teen, internal is our automated system or a counselor",message id,conversation id,character count,,,,"rated by teen. -1=bad, 1=good, 2=great",crisis center that responded,id of specialist,,was this a crisis conversation or not,"if not a crisis conversation, what was it?",what happened at the end of the conversation?,what issues did the teen mention?,describe other,what was the first or main issue mentioned by the teen?,how does the counselor think the teen was feeling,how is the counselor feeling overall,id of texter (client/visitor),first message sent by texter,last message sent by texter,time added,time taken by counselor
"""

def parse_date(date):
	"""
	Given a date in the M/D/Y H:M format, return a datetime object representing
	it.
	"""
	return dt.strptime(date, DATE_FMT)

def caster(x):
	"""
	Given an object x, try to cast it appropriately. Fallback is a string.
	"""
	if isinstance(x, float):
		return float(x)

	if isinstance(x, int):
		return int(x)

	if isinstance(x, unicode):
		return caster(str(x))

	if isinstance(x, list):
		return [caster(y) for y in x]

	if isinstance(x, dict):
		return dict((caster(k), caster(v)) for k, v in x.iteritems())

	if isinstance(x, str):
		if '.' in x:
			try:
				x = float(x)
				if 40000 < x < 45000:
					return dt(*xlrd.xldate_as_tuple(x, 0))
				return float(x)
			except ValueError:
				pass

		try:
			x = int(x)
			if 40000 < x < 45000:
				return dt(*xlrd.xldate_as_tuple(x, 0))
			return x
		except ValueError:
			pass

		try:
			return parse_date(x)
		except ValueError:
			pass

		return x

	raise ValueError("I have no idea what is going on.")

def parse_line(line, counter=None):
	if counter is not None:
		c = counter.next()
		if c % 1000 == 0:
			LOGGER.debug("Read %d lines" % c)
	sline = line.strip().split(',')
	return caster(sline)

def parse_file(the_file):
	output = []
	counter = its.count()
	return [parse_line(line, counter=counter) for line in the_file]

def get_files():
	with open(constants.CONVERSATION_DATA_FILENAME, 'r') as the_file:
		conversation_data = parse_file(the_file)

	with open(constants.MESSAGE_DATA_FILENAME, 'r') as the_file:
		message_data = parse_file(the_file)

	return conversation_data, message_data
