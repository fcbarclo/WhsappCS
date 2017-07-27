
import socket
import sys,time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException as WebDriverException


#
def WhBrStart():
	try:
		print '     starting browser..'
		# setting up Chrome with selenium
           	WHdriver = webdriver.Chrome('./driver/chromedriver')
		# open WA in browser
            	WHdriver.get('https://web.whatsapp.com/')

		#print WHdriver.current_window_handle 

		try:
        		assert "WhatsApp" in WHdriver.title	
			br_start_is_ok = True
		except: 
			print "     Browser title 'WhatsApp' not found.Exiting...\n"
			br_start_is_ok = False
			WHdriver=''
		
	except:
		br_start_is_ok = False
		WHdriver=''

	return (br_start_is_ok,WHdriver)
#
def WhTestScanMe(WHdriver, tmsecs):
	try:
		# poll the DOM waiting element max for tmsecs secs
		try:
			elem_qrcode = WebDriverWait(WHdriver,tmsecs).until(EC.presence_of_element_located((By.CLASS_NAME, "qrcode")) )
			scan_me = WHdriver.find_element_by_class_name('qrcode')

			#print scan_me

			if scan_me == []:
				scan_me_request = False
			else:
				scan_me_request = True
		except: 
			scan_me_request = False

	except:
		scan_me_request = False
	
	return scan_me_request

#
def WhappWEBConnect(WHdriver):
	try:
		QR_read_code_retry = 0
		QR_read_code_max_retry = 30

		scan_request = WhTestScanMe(WHdriver,2)

		if scan_request:
			print '        waiting for QR Code auth..'
			while 1:
				try:
					intro_request_qr = WhTestScanMe(WHdriver,1)

					if not intro_request_qr:
						#QR code match
						qr_code_status = 1
						break
					else:
						QR_read_code_retry += 1
						if QR_read_code_retry < QR_read_code_max_retry:
							if QR_read_code_retry == 1:
								print '          QR waiting..'
							time.sleep(1)
						else:
							#max retry reached
							qr_code_status = 0
							break
				except KeyboardInterrupt:
        				print '      CTRL-C pressed. Exiting..\n'
					whs_auth = False
					qr_code_status = -1
					#whdrv.close()
					break

			if qr_code_status == 1:
				try:
		        		assert "WhatsApp" in WHdriver.title	
					whs_auth = True
					print '        QR code passed\n'
				except: 
					print "     Browser title 'WhatsApp' not found.Exiting...\n"
					whs_auth = False
			else:
				whs_auth = 0
				if qr_code_status == 0:
					print '     Bad QR or timeout. Aborting..\n'
		else:
			whs_auth = True

	except:
		whs_auth = False


	return whs_auth

#
def WHchooseReceiver(wdriver, receiver, tmsecs):
	try:
        	# search name of friend/group
        	friend_name = receiver
        	input_box = wdriver.find_element(By.XPATH, '//*[@id="side"]//input')
        	input_box.clear()
        	input_box.click()
        	input_box.send_keys(friend_name)
        	input_box.send_keys(Keys.RETURN)

		try:
			elem_emp_list = WebDriverWait(wdriver,tmsecs).until(EC.presence_of_element_located((By.CLASS_NAME, "empty-text")) )
        		no_chat_or_contact = wdriver.find_element_by_class_name('empty-text')

			#print no_chat_or_contact

        		if  no_chat_or_contact == []:
				#friend's list niot empty
                		chat_list_is_ok = True
        		else:
				#friend's list is empty
                		chat_list_is_ok = False
        			input_box.clear()

		except:
			#exception on "find by class", no class 'empty-list' found. Assume friend list is not empty
               		chat_list_is_ok = True

	except Exception as e:
		print e
		chat_list_is_ok = False

        return chat_list_is_ok

#
def WHsendMsg(wdriver, msg):
	try:
        	# select correct input box to type msg
        	input_box = wdriver.find_element(By.XPATH, '//*[@id="main"]//footer//div[contains(@class, "input")]')
        	# input_box.clear()
        	input_box.click()
        	action = ActionChains(wdriver)
        	action.send_keys(msg)
        	action.send_keys(Keys.RETURN)
        	action.perform()

		send_msg_result = True
	except:
		send_msg_result = False

	return send_msg_result

#
def StartServer(WHdriver):
 
	HOST = ''  # any interface 
	PORT = 5000 

	print '  Starting gateway..'
	sock_ptr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print '     Socket created'
 
	try:
    		sock_ptr.bind((HOST, PORT))
	except socket.error , msg:
    		print '  Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    		sys.exit()

	print '     Socket bind complete'
 
	sock_ptr.listen(1)
	print '     Listening\n'

	client_conn_sock_is_open = 0

	while 1:
		try:
    			conn_ptr, addr = sock_ptr.accept()
			client_conn_sock_is_open = 1
  
 			print '  Connected with ' + addr[0] + ':' + str(addr[1])
		
    			while 2:
    				data = conn_ptr.recv(4096)

				#process string (format group:msg or contact:msg)
				if len(data) > 0:
					pos_separator = data.index(':')
					if pos_separator > 0:
						contact_name = data[:pos_separator]
						#message = data[pos_separator+1:len(data)-1]
						message = data[pos_separator+1:]
						if len(contact_name) > 0 :
							#WHdriver.refresh()
							#time.sleep(2)
							# check auth
							is_auth_ok = WhappWEBConnect(WHdriver)
							if is_auth_ok:
								check_WHcontact = WHchooseReceiver(WHdriver, contact_name, 2)
								if check_WHcontact:
									sendWhappMsgStatus = WHsendMsg(WHdriver,message)
									if sendWhappMsgStatus:
										reply = 'CONTACT='+contact_name+'  MSG='+message+' sent status = OK'
									else:
										reply = 'CONTACT='+contact_name+'  MSG='+message+' sent status = KO!'
								else:
									reply = 'CONTACT='+contact_name+' not found'
							else:
								reply = 'Not qrcode-authenticated.Restart server.'
						else:
							reply = 'no contact or group'
	 				else:
						reply = 'bad message format'
    				if not data: 
        				break

    				conn_ptr.sendall(reply)

    			conn_ptr.close()
			client_conn_sock_is_open = 0
    			print '  Connection with ' + addr[0] + ' closed'

		except KeyboardInterrupt:
			print '\nCTRL-C pressed. Exiting..\n'
			if client_conn_sock_is_open == 1:
				print '  Closing client connection..'
    				conn_ptr.close()
			print '  Closing listener..'
			sock_ptr.close()
			#WHdriver.close()
			break

#
def ShowBanner():
	print 'WhsappCS - whatsapp web connector gateway - v0.10\n'

##################################################################################
##################################   MAIN   ######################################
##################################################################################

if __name__ == '__main__':

	ShowBanner()
	
	print '  Starting WhsappCS gateway'

	(br_start_status,whdrv) = WhBrStart()

	if br_start_status:
		print '     browser started'
	else:
		print '     ERROR starting browser'
    		sys.exit()
	
	wh_conn_status = WhappWEBConnect(whdrv)

	if wh_conn_status: 
		StartServer(whdrv)
		whdrv.quit()
	else:
		print '  Error connecting to WhatsApp Web\n'
		if br_start_status:
			whdrv.quit()

