package router

import (
	"encoding/json"
	"github.com/CS3700-S19/bral/bral-GoLang/BGPRouter/router/data"
	"net"
)

type IRouter interface {
	Run()
	//TODO finalize what we want in the interface
}


//left types as string for now
type Router struct {
	FwdTable [4][]string
	Routes [][]net.IPAddr
	updates string
	relations string
	sockets []net.Conn
}


// Lookup all valid routes for an address
func (r Router) lookupRoutes(destaddr net.IPAddr) [][]net.IPAddr {
	return make([][]net.IPAddr, 0)
	//bitwise-OR using subnet mask
	//TODO
}

//select the route with the shortest AS path
func (r Router) shortestASPath(routes [][]net.IPAddr ) net.IPAddr {
	//TODO
}

//select the route with the shortest AS Path """
func (r Router) highestPreference(routes [][]net.IPAddr) net.IPAddr {
	//TODO
}

//select self originating routes
func (r Router) selfOrigin(routes [][]net.IPAddr) [][]net.IPAddr {
	//TODO
}

//select origin routes: EGP > IGP > UNK
func (r Router) originRoutes(routes [][]net.IPAddr) [][]net.IPAddr {
	//TODO
}

// Don't allow Peer->Peer, Peer->Prov, or Prov->Peer forwards
func (r Router) filterRelationships(srcif string, routes [][]net.IPAddr) [][]net.IPAddr {
	//TODO
}

//Select the best route for a given address
func (r Router) BestRoute(srcif string, daddr net.IPAddr) {
	peer := "none" //edit for type
	routes := r.lookupRoutes(daddr)

	//filter the routes in the sequence stipulated by requirements.
	if routes != nil && len(routes) > 0 {
		routes = r.highestPreference(routes) //1 Highest Preference
		routes = r.selfOrigin(routes)        //2 Self Origin
		routes = r.shortestASPath(routes)    //3 Shortest ASPath
		routes = r.originRoutes(routes)      //4 EGP > IGP > UNK
		routes = lowestIP(routes)

	}
}

//return the lowest IP address of the given connections
func lowestIP(routes [][]net.IPAddr) net.IPAddr {
//TODO
}

//forward the given data packet
func (r Router) forward(srcif string, p data.Packet) {

}

//coalesce any routes directly next to each other
func (r Router) coalesce() {

}

//handle update packets
func (r Router) update(srcif string, p data.Packet) {
	if srcif == data.CUST {
		//update all neighbors
	} else {
		//update only customers
	}
}

//handles revoke packets
func (r Router) revoke(p data.Packet) {
	revMsg := string(p.Msg)

	//for each in self.networks:
	//TODO should networks be in
}

//handles dump table requests
func (r Router) dump(p data.Packet) {

}

//dispatches a packet
func (r Router) handlePacket(srcif string, p data.Packet) {

}

//todo what is MSG
//def send_error(self, conn, msg):
//send a no_route error message
func (r Router) sendError(net.Conn, ...string) {

}

func (r Router) Run() {

	for {
		sockets := r.sockets //FIXME (select (0.1))[0]
		for i, conn := range sockets {
			var data []byte
			_, e := conn.Read(data)
			//FIXME UNMARSHALL/READ
			if e != nil {
				panic("cannot read from socket")
			}
			if data != nil {
				srcif := ""
				for i, s := range r.sockets {
					if r.sockets(i) == conn {
						srcif = s
					}
					var msg data.Packet
					  json.Unmarshal(data, msg)
					//FIXME UNMARSHALL/READ
					//if r.handlePacket(srcif, msg) { }
				}
			}
		}
	}
}








//todo 1 translate starter code from python to GoLang (Brendan by wed)
//todo 2 get JSON encoding/decoding working (B&A by wed)
//todo 3 start implementing step by step

