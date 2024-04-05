import requests
#requests to be used later
import socket
import threading

usrUrl = input("Enter Url of site")
serverPorts = []

def getIp(url):
	try:
		#Perform DNS lookup to get ip address
		ipAddress = socket.getaddrinfo(url, None)[0][4][0]
		return ipAddress

	except Exception as e:
		print('Unable to retrieve Ip Address')

def checkPorts(ipAddress,port):
	#Init the socket not actually connecting yet just initialising
	#AF_INET is just tcp over ip4 there are others udp and tcp over ip6 etc
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#Code runs really slow without setting a timeout maybe awaiting tcp handshake
	#sock.settimeout()
	try:
		#Connect if server is looking for client but iterate through ports, cant just assume port 80 
		print(f"trying port: {port}")
		sock.connect((ipAddress,port))
		print((f"socket was successful on port: {port}"))
		sock.close()
		serverPorts.append(port)

	except Exception as e:
		print('Unable to connect socket')
		sock.close()


ipAddress = getIp(usrUrl)
print(ipAddress)
threads=[]

# Create threads for each port connection attempt
for i in range(1, 65535):
	thread = threading.Thread(target=checkPorts, args=(ipAddress, i))
	threads.append(thread)
	thread.start()

# Wait for all threads to finish
for thread in threads:
	thread.join()
	print("All threads finished")

print(serverPorts)
