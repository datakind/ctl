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

if __name__ == '__main__':
	unittest.main()
