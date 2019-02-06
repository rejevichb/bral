package router

import (
	"errors"
	"net"
	"strings"
)

type MSGType int
type FTableEntry struct {
	Network IP
	Netmask IP
	conn net.Conn
}
type ForwardingTable []FTableEntry

const (
	// Message Types
	update    MSGType = 0
	revoke    MSGType = 1
	data      MSGType = 2
	noRoute   MSGType = 3
	dump      MSGType = 4
	table     MSGType = 5


	//Update Message Fields
	NTWK = "network"
	NMSK = "netmask"
	ORIG = "origin"
	LPRF = "localpref"
	APTH = "ASPath"
	SORG = "selfOrigin"

	//internal route info
	CUST = "cust"
	PEER = "peer"
	PROV = "prov"

)

//returns the string representation from a MSG type
func (t MSGType) String() string {
	names := [...]string{
		"update",
		"revoke",
		"data",
		"no route",
		"dump",
		"table"}

	if t < update || t > table {
		panic("bad message type")
	}
	return names[t]
}

func StringToMSGType(s string) (MSGType, error) {
	s = strings.ToLower(s)
	switch s {
	case "update" :
		return update, nil
	case "revoke" :
		return revoke, nil
	case "data" :
		return data, nil
	case "no route":
		return noRoute, nil
	case "dump":
		return dump, nil
	case "table":
		return table, nil
	default:
		return -999, errors.New("invalid message type to parse")
	}
}


/*
This data type represents a single message
 */
type Packet struct {
	Src IP                  `json:"src"`
	Dst IP                  `json:"dst"`
	Typ MSGType             `json:"type"`
	Msg []byte              `json:"msg"`
	Table ForwardingTable   `json:"table"`
}










