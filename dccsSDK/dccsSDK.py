import os, sys, time
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

import ctypes
import random
import json

from urllib.request import urlopen
# MQTTError
ERROR_ServiceKeyNotCorrect 	= -1
ERROR_BadProtocol 			= -2
ERROR_ClientError			= -3
ERROR_ServiceUnavailable 	= -4
ERROR_BadUsernamePassword   = -5
ERROR_NotAuthorized 		= -6
ERROR_CredentialNotFound 	= -7
ERROR_ConnectError			= -8
# JsonError
ERROR_LoadJsonError			= -10
ERROR_HostValueNull			= -11
ERROR_UsernameValueNull 	= -12
ERROR_PortValueNull 		= -13
ERROR_PasswordValueNull		= -14

Rand_MAX = 32767
count = 0
pub_count = 0
sub_count = 0

class dccsSDKStart:
	def __init__(self, ServiceKey):
		self.ServiceKey = ServiceKey;

		self.dccsSDK_Username 			= None
		self.dccsSDK_Password 			= None
		self.dccsSDK_BrokeHost 			= None
		self.dccsSDK_Port 				= None
		self.dccsSDK_ServiceKey 		= None
		self.dccsSDK_TopicSubscribe 	= None
		self.dccsSDK_TopicPublish 		= None

		self.dccsInfo_Topic 			= None
		self.dccsInfo_Qos				= None
		self.dccsInfo_Payload			= None
		
		self.message_payload			= None
		self.CB_Func 					= None
		# 執行parser
		self.dccs_parseCredential()

	def mosquitto_getRandomId(self):
		szID = ''
		r1 = random.randrange(0, Rand_MAX, 1);
		r2 = random.randrange(0, Rand_MAX, 1);
		r3 = random.randrange(0, Rand_MAX, 1);
		ctypes.memset(szID, 0, 256)

		szID = ("%04d%04d%04d") % (r1,r2,r3)
		return szID

	def on_connect(self, client, userdata, flags, rc):
		global sub_count;
		if rc == 0:
			print("Connected to broker")
			client.subscribe(self.dccsInfo_Topic)
			Connected = True
		
		elif rc == 1:
			if sub_count == 0:
				sub_count -= 1
				self.dccs_parseCredential()
				self.dccsSDK_lib_subscribe(self.dccsInfo_Topic, self.dccsInfo_Payload, self.dccsInfo_Qos)
			else:
				print("ERROR: connection refused, bad protocol ")
				return ERROR_BadProtocol
		
		elif rc == 2:
			if sub_count == 0:
				sub_count -= 1
				self.dccs_parseCredential()
				self.dccsSDK_lib_subscribe(self.dccsInfo_Topic, self.dccsInfo_Payload, self.dccsInfo_Qos)
			else:
				print("ERROR: connection refused, client-id error")
				return ERROR_ClientError				
		
		elif rc == 3:
			if sub_count == 0:
				sub_count -= 1
				self.dccs_parseCredential()
				self.dccsSDK_lib_subscribe(self.dccsInfo_Topic, self.dccsInfo_Payload, self.dccsInfo_Qos)
			else:
				print("ERROR: connection refused, service unavailable")
				return ERROR_ServiceUnavailable					
		
		elif rc == 4:
			if sub_count == 0:
				sub_count -= 1
				self.dccs_parseCredential()
				self.dccsSDK_lib_subscribe(self.dccsInfo_Topic, self.dccsInfo_Payload, self.dccsInfo_Qos)
			else:
				print("ERROR: connection refused, bad username or password")
				return ERROR_BadUsernamePassword
		
		elif rc == 5:
			if sub_count == 0:
				sub_count -= 1
				self.dccs_parseCredential()
				self.dccsSDK_lib_subscribe(self.dccsInfo_Topic, self.dccsInfo_Payload, self.dccsInfo_Qos)
			else:
				print("ERROR: refused, not authorized")
				return ERROR_NotAuthorized

	def on_message(self, mq, userdata, msg):
		message = str(msg.payload, 'utf-8')
		self.CB_Func(message)

	def dccs_parseCredential(self):
		flag = 0

		if self.ServiceKey.find("http") == 0:
			flag = 0
		else:
			flag = -1

		if flag == 0:
			try:
				dccsData = urlopen(self.ServiceKey)
			except:
				print("ERROR: URL not correct or Internet not connect")
				return ERROR_ServiceKeyNotCorrect
				sys.exit(0)
		else:
			try:
				dccsData = urlopen("https://api-dccs.wise-paas.com/v1/serviceCredentials/"+self.ServiceKey)
			except:
				print("ERROR: ServiceKey not correct or Internet not connect")
				return ERROR_ServiceKeyNotCorrect
				sys.exit(0)			

		try:
			data = json.loads(dccsData.read().decode('utf-8'))
		except:
			print("ERROR: load json error")
			return ERROR_LoadJsonError
			sys.exit(0)			

		self.dccsSDK_BrokeHost		= data['serviceHost']
		self.dccsSDK_TopicSubscribe	= data['serviceParameter']['rmqTopicRead']
		self.dccsSDK_TopicPublish 	= data['serviceParameter']['rmqTopicWrite']
		
		self.dccsSDK_Username		= data['credential']['protocols']['mqtt']['username']
		self.dccsSDK_Password 		= data['credential']['protocols']['mqtt']['password']
		self.dccsSDK_Port 			= data['credential']['protocols']['mqtt']['port']

		if self.dccsSDK_BrokeHost == None:
			print("ERROR: json value(Host) is Null")
			return ERROR_HostValueNull	
			sys.exit(0)	
			
		elif self.dccsSDK_Username == None:
			print("ERROR: json value(Username) is Null")
			return ERROR_UsernameValueNull
			sys.exit(0)

		elif self.dccsSDK_Password == None:
			print("ERROR: json value(Username) is Null")
			return ERROR_PasswordValueNull
			sys.exit(0)	
		elif self.dccsSDK_Port == None:
			print("ERROR: json value(Port) is Null")
			return ERROR_PortValueNull 
			sys.exit(0)	

	def dccsSDK_lib_publish(self, topic, payload, Qos):
		global count

		self.dccsInfo_Topic = topic
		self.dccsInfo_Qos = Qos;
		self.dccsInfo_Payload = payload
		clientId = self.mosquitto_getRandomId()
		auth = {'username': self.dccsSDK_Username, 'password': self.dccsSDK_Password}

		if count == 0:
			try:
				publish.single(self.dccsInfo_Topic, self.dccsInfo_Payload, port=self.dccsSDK_Port, qos=self.dccsInfo_Qos, hostname=self.dccsSDK_BrokeHost, auth=auth, client_id=clientId)
			except:
				count -= 1
				print("ERROR: Credential not found")
				self.dccs_parseCredential()
				self.dccsSDK_lib_publish(self.dccsInfo_Topic, self.dccsInfo_Payload, self.dccsInfo_Qos)
		else:
			try:
				publish.single(self.dccsInfo_Topic, self.dccsInfo_Payload, port=self.dccsSDK_Port, qos=self.dccsInfo_Qos, hostname=self.dccsSDK_BrokeHost, auth=auth, client_id=clientId)
			except:
				print("ERROR: Credential not found")
				return ERROR_CredentialNotFound
				sys.exit(0)

	def dccsSDK_lib_subscribe(self, Topic, Qos, CB_Func):
		self.dccsInfo_Topic = Topic
		self.dccsInfo_Qos = Qos
		self.CB_Func = CB_Func
		clientId = self.mosquitto_getRandomId()	
		
		client = mqtt.Client(clientId)
		
		try:
			client.username_pw_set(self.dccsSDK_Username, self.dccsSDK_Password)
		except:
			print("'NoneType' object has no attribute 'encode'")
			return ERROR_ConnectError
			sys.exit(0)		

		client.loop_start()
		client.on_connect = self.on_connect
		client.on_message = self.on_message
	
		try:
			client.connect(self.dccsSDK_BrokeHost, self.dccsSDK_Port, 30)
		except:
			print("ERROR: Can't connect to broker")
			return ERROR_ConnectError
			sys.exit(0)
	
		try:
			while True:
				time.sleep(1)
		except (KeyboardInterrupt):
			print("exiting")
			client.disconnect()

		
		print("exit program")
		sys.exit(0)