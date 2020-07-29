# remote-sploit 
**Automated exploitation tool for SSH and RDP**

## Starting
	$ ./remotesploit.py
	 ______                        __          _______         __         __ __   
	|   __ \.-----.--------.-----.|  |_.-----.|     __|.-----.|  |.-----.|__|  |_ 
	|      <|  -__|        |  _  ||   _|  -__||__     ||  _  ||  ||  _  ||  |   _|
	|___|__||_____|__|__|__|_____||____|_____||_______||   __||__||_____||__|____|
		                                               |__|                        v2.4.7

	Checking internet connection ... DONE!
	Loading wordlists ... DONE!
	Loading countries ... DONE!

	Welcome to RemoteSploit. Type help or ? to list available commands.

	RemoteSplit [unnamed]>

## Creating a project
	RemoteSplit [unnamed]>create test2
	Project "test2" created

## Switching projects
	RemoteSplit [test2]>use test
	Loading scan-counter:      1 scanned, 0 cracked
	Setting password list:     
	Setting username list:     
	Setting comined loginlist: 

## Adding IP-ranges
	RemoteSplit [test]>add 192.168.1.1-10
	1 network(s) added

	RemoteSplit [test]>list countries
	  1) AFGHANISTAN
	  2) ALAND+ISLANDS
	  3) ALBANIA
	  4) ALGERIA
	     ...
	240) ZIMBABWE

	RemoteSplit [test]>add 3
	1620 network(s) added

## Deleting IP-ranges
RemoteSplit [test]>list ranges
      1) 192.168.1.1-10
      2) 5.206.232.1-254
      3) 5.206.233.1-254
         ...
   1621) 217.73.143.1-254

RemoteSplit [test]>del 2
5.206.232.1-254 removed from list and list new arranged!

RemoteSplit [test]>del all
All IP-ranges deleted ... 

## Scanning
	RemoteSplit [test]>run scan
	Scanning 192.168.1.1-10 [1 / 3]
	192.168.1.2:22
	192.168.1.3:22
	192.168.1.7:22
	3 host(s) added
	Scanning 192.168.1.100-110 [2 / 3]
	Scanning 192.168.1.111-120 [3 / 3]

## Listing ranges / hosts / wordlists / ...

	RemoteSplit [test]>list ranges
		  1) 192.168.1.1-10
		  2) 192.168.1.100-110
		  3) 192.168.1.111-120

	RemoteSplit [test]>list hosts
		  1) 192.168.1.2:22
		  2) 192.168.1.3:22
		  3) 192.168.1.7:22

	RemoteSplit [test]>list wordlists
	  1) top_100_bad_passwords.lst
	  2) top_500_bad_passwords.lst
	  3) standard_logins_iot.lst
	  4) testlogins_en_short.lst
	  5) standard_logins_mix.lst
	  6) testlogins_de_short.lst
	  7) rdp_users.lst
	  8) ssh_users.lst

## Setting wordlist
	RemoteSplit [test]>set loginlist 4
	Setting combined login-list: /home/markb/Projects/remote_sploit/wordlists/testlogins_en_short.lst

## Run cracker
	RemoteSplit [test]>run logintest
	Cracking 192.168.1.2:22 [1 / 3]

## Getting help
	RemoteSplit [test]>?

	Documented commands (type help <topic>):
	----------------------------------------
	add  create  del  help  list  quit  reset  run  set  shell  use

	Undocumented commands:
	----------------------
	cmd

	RemoteSplit [test]>?set
	set [wordlist-type] [file-ID] ... set a wordlist

	Valid wardlist-types are:
	pwlist ...... password list 
	userlist .... user list 
	loginlist ... compined list login:password 

## Exit remote-sploit
	RemoteSplit [test]>quit
	Bye!
