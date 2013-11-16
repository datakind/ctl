"""
Tests for some experiments functions.

@author Kevin Wilson <khwilson@gmail.com>
"""
import crisis.experiments as undertest
import crisis.parsers as parsers

import calendar
import datetime
import unittest

class TestExperiments(unittest.TestCase):
	def setUp(self):
		self.test_lines = [[0] * 10, [0] * 10, [0] * 10]
		self.first_convo_idx = 7
		self.second_convo_idx = 9
		self.first_convo_first_time = datetime.datetime(2013, 8, 5, 15, 00)
		self.first_convo_second_time = datetime.datetime(2013, 8, 6, 12, 00)
		self.second_convo_time = datetime.datetime(2013, 8, 1, 12, 10)
		self.test_lines[0][parsers.MessageIndex.c_id] = self.first_convo_idx
		self.test_lines[0][parsers.MessageIndex.msg_time] = \
			self.first_convo_second_time
		self.test_lines[1][parsers.MessageIndex.c_id] = self.second_convo_idx
		self.test_lines[1][parsers.MessageIndex.msg_time] = \
			self.second_convo_time
		self.test_lines[2][parsers.MessageIndex.c_id] = self.first_convo_idx
		self.test_lines[2][parsers.MessageIndex.msg_time] = \
			self.first_convo_first_time

	def test_group_messages_by_line(self):
		test_sort = undertest.group_message_lines_by_c_id(self.test_lines)

		self.assertEqual(set([self.first_convo_idx, self.second_convo_idx]),
							set(test_sort.keys()))
		self.assertEqual(self.first_convo_first_time,
			test_sort[self.first_convo_idx][0][parsers.MessageIndex.msg_time])
		self.assertEqual(self.first_convo_second_time,
			test_sort[self.first_convo_idx][1][parsers.MessageIndex.msg_time])
		self.assertEqual(self.second_convo_time,
			test_sort[self.second_convo_idx][0][parsers.MessageIndex.msg_time])

	def test_intermessage_times(self):
		test_sort = undertest.group_message_lines_by_c_id(self.test_lines)
		test_output = undertest.intermessage_times(test_sort)
		self.assertEqual(1, len(test_output[self.first_convo_idx]))
		self.assertEqual(0, len(test_output[self.second_convo_idx]))
		first_timediff = \
			(calendar.timegm(self.first_convo_second_time.timetuple()) -
			calendar.timegm(self.first_convo_first_time.timetuple()))
		self.assertEqual(first_timediff, test_output[self.first_convo_idx][0])

if __name__ == '__main__':
	unittest.main()
