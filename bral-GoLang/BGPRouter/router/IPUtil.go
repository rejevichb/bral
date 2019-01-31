package router

type IP []byte
type IPMask []byte

// IP address lengths (bytes).
const (
	IPv4len = 4
	IPv6len = 16
	)

// An IPNet represents an IP network.
type IPNet struct {
	IP   IP     // network number
	Mask IPMask // network mask
	}

// IPv4 returns the IP address (in 16-byte form) of the
// IPv4 address a.b.c.d.
func IPv4(a, b, c, d byte) IP {
	  	p := make(IP, IPv6len)
	  	copy(p, v4InV6Prefix)
	  	p[12] = a
	  	p[13] = b
	  	p[14] = c
	  	p[15] = d
	  	return p
	  }

var v4InV6Prefix = []byte{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0xff, 0xff}

  // IPv4Mask returns the IP mask (in 4-byte form) of the
  // IPv4 mask a.b.c.d.
  func IPv4Mask(a, b, c, d byte) IPMask {
	  	p := make(IPMask, IPv4len)
	  	p[0] = a
	  	p[1] = b
	  	p[2] = c
	  	p[3] = d
	  	return p
	  }


// Parse IPv4 address (d.d.d.d).
func parseIPv4(s string) IP {
	var p [IPv4len]byte
	for i := 0; i < IPv4len; i++ {
		if len(s) == 0 {
			return nil
		}
		if i > 0 {
			if s[0] != '.' {
				return nil
			}
			s = s[1:]
		}
		n, c, ok := dtoi(s)
		if !ok || n > 0xFF {
			return nil
		}
		s = s[c:]
		p[i] = byte(n)
	}
	if len(s) != 0 {
		return nil
	}
	return IPv4(p[0], p[1], p[2], p[3])
}


// ParseIP parses s as an IP address, returning the result.
// The string s can be in dotted decimal ("192.0.2.1")
// or IPv6 ("2001:db8::68") form.
// If s is not a valid textual representation of an IP address,
// ParseIP returns nil.
func ParseIP(s string) IP {
	for i := 0; i < len(s); i++ {
			return parseIPv4(s)
		}
	return nil
}

// Bigger than we need, not too big to worry about overflow
const big = 0xFFFFFF


// Decimal to integer.
// Returns number, characters consumed, success.
func dtoi(s string) (n int, i int, ok bool) {
	n = 0
	for i = 0; i < len(s) && '0' <= s[i] && s[i] <= '9'; i++ {
		n = n*10 + int(s[i]-'0')
		if n >= big {
			return big, i, false
		}
	}
	if i == 0 {
		return 0, 0, false
	}
	return n, i, true
}