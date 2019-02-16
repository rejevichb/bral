import unittest


def pick_smaller_ip(a, b):
	a_split = a.split(".")
	b_split = b.split(".")
	for index, octet in enumerate(a_split):
		if octet > b_split[index]:
			return b
		elif octet < b_split[index]:
			return a


# DECIMALIPSTR -> BINIPSTR
def addr_to_binary(address):
	nw_split = address.split(".")
	temp = []
	for each in nw_split:
		temp.append(bin(int(each))[2:].zfill(8))
	out = [x for y in temp for x in y]
	return ''.join(map(str, out))

def get_nw_prefix_binary(entry):
	"""get the network prefix in a list of 4 chunks of 8 bytes"""
	return addr_to_binary(entry)

def get_nm_length(address):
	return addr_to_binary(address).count("1")

def nw_prefix_coalesce(binary_addr1, binary_addr2, nm_len):
	""" can the entry be aggregated based on length of prefix"""
	matching = 0
	for i in range(nm_len - 1):
		if binary_addr1[i] == binary_addr2[i]:
			matching += 1
		else:
			return False
	return True


# Int -> DDNetmaskString
def mask(i):
	"generate a netmast strink from a prefix length"
	if i <= 8:
		out = str(int(("1" * i) + ("0" * (8 - i)), 2)) + ".0.0.0"
		return out
	elif i <= 16:
		out = "255." + str(int(("1" * (i - 8)) + ("0" * (8 - (i - 8))), 2)) + ".0.0"
		return out
	elif i <= 24:
		out = "255.255." + str(int(("1" * (i - 16)) + ("0" * (8 - (i - 16))), 2)) + ".0"
		return out
	else:
		out = "255.255.255." + str(int(("1" * (i - 24)) + ("0" * (8 - (i - 24))), 2))
		return out


class MyTest(unittest.TestCase):

	def test_smaller_ip(self):
		self.assertEqual("162.32.0.5", pick_smaller_ip("192.32.0.6","162.32.0.5"))
		self.assertEqual("127.0.0.0", pick_smaller_ip("127.0.0.1", "127.0.0.0"))
		self.assertEqual("128.42.5.4", pick_smaller_ip("128.42.5.4", "207.0.0.0"))
		self.assertEqual("207.46.128.0", pick_smaller_ip("207.46.128.0", "207.46.192.0"))

	def test_addr_to_binary(self):
		self.assertEqual(str("10000000001010100000010100000100"), addr_to_binary("128.42.5.4"))
		self.assertEqual(str("11111111111111111111111111111111"), addr_to_binary("255.255.255.255"))
		self.assertEqual(str("11111111111111111111111100000000"), addr_to_binary("255.255.255.0"))
		self.assertEqual(str("11000000101010000000000000000001"), addr_to_binary("192.168.0.1"))
		self.assertEqual(str("10000000001010100000010100000100"), addr_to_binary("128.42.5.4"))
		self.assertEqual(str("00010100000101001010010000000001"), addr_to_binary("20.20.164.1"))

	def test_prefix_binary(self):
		self.assertEqual(str("11111111111111111111111100000000"), get_nw_prefix_binary("255.255.255.0"))
		self.assertEqual(str("11111111111000000000000000000000"), get_nw_prefix_binary("255.224.0.0"))
		self.assertEqual(str("11111111111111111111000000000000"), get_nw_prefix_binary("255.255.240.0"))

	def test_nm_length(self):
		self.assertEqual(24, get_nm_length("255.255.255.0"))
		self.assertEqual(11, get_nm_length("255.224.0.0"))
		self.assertEqual(21, get_nm_length("255.255.248.0"))
		self.assertEqual(27, get_nm_length("255.255.255.224"))


	def test_mask(self):
		self.assertEqual("255.255.255.0", mask(24))
		self.assertEqual("255.224.0.0", mask(11))
		self.assertEqual("255.255.248.0", mask(21))
		self.assertEqual("255.255.255.224", mask(27))


	def test_coalesce_rule(self):
		# False (/18) - (they differ before the 18th bit)
		a1 = "11000000101010000000000000000001"
		a2 = "11000000101010001000000000000001"
		self.assertEqual(False, nw_prefix_coalesce(a1, a2, 18))

		# True (/17) - (they difffer on the 17th string)
		self.assertEqual(True, nw_prefix_coalesce(a1, a2, 17))







