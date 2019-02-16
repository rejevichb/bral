import unittest


def pick_smaller_ip(a, b):
	a_split = a.split(".")
	b_split = b.split(".")
	for index, octet in enumerate(a_split):
		if octet > b_split[index]:
			return b
		elif octet < b_split[index]:
			return a


class MyTest(unittest.TestCase):
	def test(self):
		self.assertEqual(pick_smaller_ip("",""), "")