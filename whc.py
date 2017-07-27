
import socket
import sys,time

#
def checkArgs():

	if len(sys.argv) != 5:
	 	check_arg = False
		ip_gateway = ''
		port_gateway = ''
		wh_contact = ''
		wh_msg = ''
        else:
		ip_gateway = sys.argv[1]
		port_gateway = sys.argv[2]
		wh_contact = sys.argv[3]
		wh_msg = sys.argv[4]

		check_arg = True

	return (check_arg,ip_gateway,port_gateway,wh_contact,wh_msg)

#
def sockConnect(ip_gateway,port_gateway,wh_contact,wh_msg):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		gateway_address = (ip_gateway,int(port_gateway))
		print 'Connecting to '+ip_gateway+':'+port_gateway
		sock.connect(gateway_address)
		print 'Gateway connection established'
		sock_status = True
	except socket.error as e:
		print e
		sock_status = False

	return (sock_status,sock)

#
def SendMsg(sock,wh_contact,wh_msg):
	try:
		contact_with_msg = str(wh_contact) + ':' + str(wh_msg)
		print 'Sending message..'
		sock.sendall(contact_with_msg)
		gateway_reply = sock.recv(4096)
		send_msg_status = True
	except socket.error as e:
		print e
		send_msg_status = False
		gateway_reply = ''

	return (send_msg_status,gateway_reply)

#
def ShowCBanner():
	print 'WhsappCS - whatsapp web client - v0.11'
	print "args: <gateway ip> <gateway port> <contact/group name> <message>\n"

##################################################################################
##################################   MAIN   ######################################
##################################################################################

if __name__ == '__main__':

	ShowCBanner()
	
	(checkArgs_status,ip_gateway,port_gateway,wh_contact,wh_msg) = checkArgs()
	if checkArgs_status:
		(sock_status,sock) = sockConnect(ip_gateway,port_gateway,wh_contact,wh_msg)
		if sock_status:
			(send_msg_status,gateway_reply) = SendMsg(sock,wh_contact,wh_msg)
			if send_msg_status:
				print 'Gateway reply : '+gateway_reply
			else:
				print 'Errror sending message\n'
			print 'Closing socket..'
			sock.close()
	 	else:
			print 'No gateway running at '+ip_gateway+':'+port_gateway+'\n'	
	else:
		print 'Arg errors\n'

