package client

import (
	"errors"
	"fmt"
	"io"
	"net"
	"strconv"
	"strings"
)

const NETWORK_PORT = ":27993"


//Main run method that handles communication with server over TCP. The client program sends an initial "HELLO" message,
//recieves output, and continues to loop back and forth with the server sending COUNT based on each FIND recieved
//until the BYE message is recieved, at which point the client will disconnect from the server
func Run(server string) {
	// Establish TCP connection to server
	r, w, err := connectTCP(server)

	if err != nil {
		panic(err)
	}

	//sends hello
	sendHello("001667932", w)
	
	resp := retrieveResp(r)

	//get secret string to search
	var s string
	err = sendCount(specialCount(s), r, w)
	if err != nil {
		panic(err)
	}

	//continue until server sends BYE message with flag -- handle error vs valid flag
	//for {
	//
	//}
	var byeMsg string

	//ends by printing bye secret flag
	fmt.Printf(byeMsg)
}




//check if the message recieved conforms to protocol
func isValidMessage() bool {
	return false
}



func connectTCP(server string) (io.Reader, io.Writer, error) {
	conn, err := net.Dial("tcp", server+NETWORK_PORT)
	if err != nil {
		return nil, nil, errors.New("Dialing " + server + " failed: " + err.Error())
	}
	return conn, conn, nil
}

func sendHello(nuid string, w io.Writer) error {
	//marshall/endcode nuid string
	_, err := w.Write([]byte(nuid))

	if err != nil {
		panic(err)
	}

	return nil
}

func retrieveResp(r io.Reader) ([]byte, error) {
	var out []byte
	_, e := r.Read(out)
	if e != nil {
		return nil, e
	}
	return out, nil
}

func sendCount(count int, r io.Reader, w io.Writer) error {
	_, e := w.Write("c")
	_, e := w.Write([]byte(strconv.Itoa(count)))
	if e != nil {
		return e
	}
	return nil
}

func specialCount(s string) int {

	return 0
}

func isValidFindRequest(in []byte) bool {
	split := getSplitString(in)
	switch split[1] {
	case "FIND" :
		if len(split) != 4 || split[2] == "" { return false }
	}
}

func requestType(in []byte) string {
	split := getSplitString(in)
	if split[1] == "BYE" { return "BYE" }
	if split[1] == "FIND" {return "FIND" }
	return "INVALID"
}

func getSplitString(in []byte) []string {
	st := string(in)
	split := strings.Split(st, " ")
	return split
}
