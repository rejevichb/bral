package project1

//Constants for message types
type MSGType int
const (
	update    MSGType = 0
	revoke    MSGType = 1
	data      MSGType = 2
	noRoute   MSGType = 3
	dump      MSGType = 4
	table     MSGType = 5
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


/*
This data type represents a single message
 */
type BGPMessage struct {
	src string `json:"src"`
	dst string `json:"dst"`
	typ MSGType `json:"type"`
	msg []byte `json:"msg"`
}


func main() {
	StartUp()
}


func StartUp() {

}

//todo 1 translate starter code from python to GoLang (Brendan by wed)
//todo 2 get JSON encoding/decoding working (B&A by wed)
//todo 3 start implementing step by step 

