# WhsappCS

it's a linux application to send whatsapp messages. 
It consists of a socket gateway process (whg.py) and a command line client (whc.py).

OS/Python system requirements:

- CPython 2.7 (not tested with > 2.7)
- Any graphical environment that supports graphical internet browsing 
- selenium module >= 3.4.3
- chrome webdriver >= 2.30.477691 for chrome browser
- tested with chrome browser version >= 59
- copy chrome webdriver under folder named 'driver' where whs.py and whc.py files reside


Gateway start:

	- open graphical terminal , then start whg.py and follow instructions to authenticate via QR code using phone.
	  This process starts using port 5000 as default listening port; press CTRL+C to stop

Client use (to send message):

	- start whc.py with arguments: <ip_gateway> <port_gateway> <whatsapp contact/group name> <message>
