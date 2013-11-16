"""
Tests for parsers.py

@author Kevin Wilson <khwilson@gmail.com>
"""
import crisis.parsers as undertest

import datetime
import unittest

class TestParsers(unittest.TestCase):
	def test_parse_date(self):
		date = '8/5/2013 16:14'
		self.assertEqual(datetime.datetime(2013, 8, 5, 16, 14),
						undertest.parse_date(date))

	def test_part_date_short(self):
		date  = '8/5/13 16:14'
		self.assertEqual(datetime.datetime(2013, 8, 5, 16, 14),
						undertest.parse_date_short(date))

	def test_parse_line(self):
		line = "1,2,3"
		actual = undertest.parse_line(line)
		expected = [1,2,3]
		self.assertTrue(all(x == y for x, y in zip(expected, actual)))

if __name__ == '__main__':
	unittest.main()
