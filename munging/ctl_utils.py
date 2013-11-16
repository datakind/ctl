"""

To run:

pip install pandas
pip install sklearn

"""

import crisis.parsers

import pandas as pd
import locale
import numpy as np
from datetime import datetime, timedelta

def parse_messages(path='dk_message_level_131114.csv'):
    data = pd.read_csv(path,
            parse_dates= [7,8,9, 23, 4],
            converters={ 'm_id' : convert_to_int, 'c_id' : convert_to_int,
                         'specialist_id' : convert_to_int },
            skiprows=[1],
            )
    return data

def parse_conversations(path='dk_conversation_level_1311114.csv'):
    data = pd.read_csv(path,
            #parse_dates= [7,8,9],
            converters={ 'm_id' : convert_to_int, 'c_id' : convert_to_int,
                         'specialist_id' : convert_to_int,
                         'conv_start': convert_to_date,
                         'conv_end': convert_to_date,
                         'first_msg': convert_to_date,
                         'last_msg': convert_to_date,
                         'addedtoqueue': convert_to_date,
                         'takenfromqueue': convert_to_date},
            skiprows=[1],
            )
    return data

def convert_to_int(x):
	try:
		return np.int(x)
	except:
		return np.nan


def convert_to_date(x):
    """Converter for dates.
    """
    x = crisis.parsers.caster(x)
    if not isinstance(x, datetime):
        x = np.nan
    return x


"""
Adds binary flag for each issue

"""
def add_issue_columns(messages):
	from sklearn.feature_extraction.text import CountVectorizer
	v = CountVectorizer(binary=True)
	issue_matrix = v.fit_transform([str(x) for x in messages['Q13_issues']]).toarray()
	issues = v.get_feature_names()
	for (i, issue) in enumerate(issues):
		messages[issue] = pd.Series(issue_matrix[:,i])


def add_duration_columns(conversations):
        """Add columns to the Conversations data frame to represent durations:
        how long a message spends in the queue, how long the conversation lasts,
        and how long between a message comes in and the conselor responds.

        This last value has some issues; in particular, it appears to be off by
        4 hours by default, and even after adjusting by 4 hours, there are many
        outliers where the queue time is before the first message time.
        """
        C = conversations
        C['duration_queue'] = C['takenfromqueue'] - C['addedtoqueue']
        C['duration_msg'] = C.last_msg - C.first_msg

        # These are off by at least 4 hours
        C['duration_to_first_resp'] = C.takenfromqueue - C.first_msg
        C['duration_to_first_resp'] = C['duration_to_first_resp'].dropna().apply(lambda td: td + np.timedelta64(4, 'h'))

        C['duration_to_first_resp_nonneg'] = C['duration_to_first_resp']
        C['duration_to_first_resp_nonneg'][C['duration_to_first_resp_nonneg'] < 0] = np.nan

        return C

"""
Function to mark simultaneous conversations


NOTE: noticing issues, first conversation in group won't be marked as simultaneous if it overlaps in time frame
"""
def mark_simultaneous_conversations(conversations):
	specialist_conversations = conversations.groupby(['specialist_id'])
	for name, conversation_group in specialist_conversations:
		ordered_messages = conversation_group.sort('conv_start')
		min_start = None
		max_end = None
		for ix, message in ordered_messages.iterrows():
			start_time = message['conv_start']
			end_time = message['conv_end']
			if start_time and end_time and start_time >= min_start and start_time <= max_end:
				message['is_simultaneous'] = True
			if not min_start or start_time >= max_end:
				min_start = start_time
			if not max_end or end_time >= max_end:
				max_end = end_time
	return conversations


if __name__ == '__main__':
	data = parse_messages()
