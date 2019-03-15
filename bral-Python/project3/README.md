Protocol 

We implement a simple transport protocol as follows:

We allow for continuous sending from the sender. After the sender has sent all the packets, 
it waits for a list of acks from the reciever. Then, it compares this list of acks to the messsages
it sent and resends any that were not recieved. 

The burden of dealing with ordering is on the reciever. The reciever waits until all the packets 
have arrived, the sorts packets before printing to standard out. 

The ack contains a sequence number, which is incremented ONLY by the sender. The reciever acks 
the sequence numbers of packets it has recieved. 


