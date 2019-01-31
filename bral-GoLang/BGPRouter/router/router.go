package router

import (
	"encoding/json"
	"net"
)

type IRouter interface {
	Run()
	//TODO finalize what we want in the interface
}

//left types as string for now
type Router struct {
	FwdTable ForwardingTable
	Routes [][]net.IPAddr
	updates [] Packet
	relations string //FIXME type
	sockets []net.Conn
}

// Lookup all valid routes for an address
func (r Router) lookupRoutes(destaddr IP) [][]IP {
	return make([][]IP, 0)
	//bitwise-OR using subnet mask
	//TODO
}

//select the route with the shortest AS path
func (r Router) shortestASPath(routes [][]IP ) [][]IP {
	//TODO multiple return types or just 1?
}

//select the route with the shortest AS Path """
func (r Router) highestPreference(routes [][]IP) [][]IP {
	//TODO
}

//select self originating routes
func (r Router) selfOrigin(routes [][]IP) [][]IP {
	//TODO
}

//select origin routes: EGP > IGP > UNK
func (r Router) originRoutes(routes [][]IP) [][]IP {
	//TODO
}

// Don't allow Peer->Peer, Peer->Prov, or Prov->Peer forwards
func (r Router) filterRelationships(srcif string, routes [][]IP) [][]IP {
	//TODO
}

//Select the best route for a given address
func (r Router) BestRoute(srcif string, daddr [][]IP) {
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
func (r Router) forward(srcif string, p Packet) {

}

//coalesce any routes directly next to each other
func (r Router) coalesce() {

}

//handle update packets
func (r Router) update(srcif string, p Packet) {
	if srcif == CUST {
		//update all neighbors
	} else {
		//update only customers
	}
}

//handles revoke packets
func (r Router) revoke(p Packet) {
	revMsg := string(p.Msg)

	//for each in self.networks:
	//TODO should networks be in
}

//handles dump table requests
func (r Router) dump(p Packet) {

}

//dispatches a packet
func (r Router) handlePacket(srcif string, p Packet) {

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
			a, x := net.Dial("unix", "filepath")
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
					var msg Packet
					json.Unmarshal(data, &msg)
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

