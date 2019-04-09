

###Passing:
**(70% of all tests)**

##### Simple 1 (all)
- Simple-1 &nbsp; `(+ bonus x2)`
- Simple-2 &nbsp; `(+ bonus)`

#####Crash 
- Crash-1 &nbsp; `(+ bonus)`
- Crash-2 &nbsp; `(+ bonus)`

#####Partition
- partition-1
- partition-2 &nbsp; `(+ bonus)`
- partition-3 

#####Unreliable 
- unreliable-1 &nbsp; `(+ bonus)`
- unreliable-2 &nbsp; `(+ bonus)`
- unreliable-3 &nbsp; `(+ bonus)`


#####Advanced 
- advanced-1 
    -   Total Failures and Unanswered Requests: 58 < 100, `Partial credit, needs improvement`
- advanced-4 &nbsp; `(+ bonus)`



###Failing
**(30% of all tests)**
- Crash-3
    - 	insufficient get() requests answered (51 > 81 * 0.50)
	-   insufficient put() requests answered (195 > 319 * 0.50)
- Crash-4
    -   insufficient get() requests answered (50 > 77 * 0.50)
	-   insufficient put() requests answered (158 > 223 * 0.50)
	-   too few messages between the replicas

- Partition-4
    -  insufficient get() requests were generated because insufficient put()s were accepted (7 > 53 * 0.10)
    
- Advanced-2
    - insufficient get() requests answered (37 > 59 * 0.50)
    
- Advanced-3 
    - insufficient get() requests answered (31 > 38 * 0.50)
	- insufficient put() requests answered (113 > 162 * 0.50)
	- too few messages between the replicas

