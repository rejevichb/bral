Protocol 

We implement a simple transport protocol as follows:

All data is read in bulk by the send and stored in JSON packets in the TO_SEND dict. Sequence numbers are zero-indexed and only incremented by 1. There is also an "EOF" flag in the packet that denotes that final packet to be added.

We allow for continuous sending from the sender. After the sender has sent all the packets, 
it waits for a list of acks from the receiver. Then, it compares this list of acks to the messsages
it sent and resends any that were not received. 

The burden of dealing with ordering is on the receiver. The receiver waits until all the packets 
have arrived, then sorts packets before printing to stdout. We use a dict structure for holding the actual packets and a set to hold the list of ACKs to be sent back to the sender. In this way, duplicates are handled on the receiver side. 





