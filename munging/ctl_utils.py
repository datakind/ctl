"""

To run:

pip install pandas
pip install sklearn

"""


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import locale
import numpy as np

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
		parse_dates= [7,8,9],
		converters={ 'm_id' : convert_to_int, 'c_id' : convert_to_int,
            'specialist_id' : convert_to_int },
        skiprows=[1],
		)
	return data

def convert_to_int(x):
	try:
		return np.int(x)
	except:
		return np.nan

"""
Adds binary flag for each issue

"""
def add_issue_columns(messages):
	v = CountVectorizer(binary=True)
	issue_matrix = v.fit_transform([str(x) for x in messages['Q13_issues']]).toarray()
	issues = v.get_feature_names()
	for (i, issue) in enumerate(issues):
		messages[issue] = pd.Series(issue_matrix[:,i])


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
