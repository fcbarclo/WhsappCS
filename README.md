# WhsappCS

it's a linux application to send whatsapp messages. 
It consists of a socket server process (whs.py) and a command line client (whc.py).

OS/Python system requirements:

- CPython 2.7 (not tested with > 2.7)
- Any graphical environment that supports graphical internet browsing 
- selenium module >= 3.4.3
- chrome webdriver >= 2.30.477691 for chrome browser
- tested with chrome browser version >= 59
- copy chrome webdriver under folder named 'driver' where whs.py and whc.py files reside


Server start:

	- open graphical terminal , then start whs.py and follow instructions.
	  This process starts using port 5000 as default listening port. 

Client use (to send message):

	- start whc.py with arguments: ip_server port_server whatsapp_contact_name whatspp_message
