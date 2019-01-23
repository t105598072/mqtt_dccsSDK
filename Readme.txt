# �e�m�@�~ #
=================================================================================================
- �ظm���� 
	- pyhon3.x.x
	   
- �ۨ�library
	- paho-mqtt (MQTT Client)
		- https://pypi.python.org/pypi/paho-mqtt/

# �ϥλ���#
=================================================================================================
	1. Build paho-mqtt 
		pip install paho-mqtt
		�w�� paho-mqtt
	
	2. �ϥ�dccsSample_sub (..\dccs\dccsSample)
		python dccsSample_sub.py
	
	3. �ϥ�dccsSample_pub (..\dccs\dccsSample)
		python dccsSample_pub.py	

# Python Code API����#
=================================================================================================
- Class dccsSDKStart(ServiceKey)
	- Initial dccsSDK. Auto Get DCCS Credential. 
	- @param ServiceKey (in) String of the ServiceKey or URL to get DCCS Credential.

- dccsSDK_lib_subscribe(Topic, Qos, RecvMsgCB)
	- Subscribe to a topic.
	- @param TOPIC (in) String of the topic to publish to.
	- @param Qos (in) Boolean vlaue True(1) or False(0). Quality of Service
	- @param RecvMsgCB (in) Recv message callback function.
	- @returns DCCS_SUCCESS: Success, else: Fail. Reference Error Code

- dccsSDK_lib_publish(Topic, payloadlen, Qos)
	- Publish a message on a given topic.
	- @param TOPIC (in) String of the topic to publish to.
	- @param Payloadlen (in) The size of the payload (bytes).
	- @param Qos (in) Boolean vlaue True(1) or False(0). Quality of Service
	- @returns DCCS_SUCCESS: Success, else: Fail. Reference Error Code

# Error Code �N�X#
=================================================================================================
- ERROR_ServiceKeyNotCorrect -1
Return code: URL not correct or Internet not connect

- ERROR_BadProtocol -2
Return code: Connection refused, bad protocol

- ERROR_ClientError -3
Return code: Connection refused, client-id error

- ERROR_ServiceUnavailable -4
Return code: Connection refused, service unavailable

- ERROR_BadUsernamePassword -5
Return code: Connection refused, bad username or password

- ERROR_NotAuthorized -6
Retrun code: Connection refused, not authorized

- ERROR_CredentialNotFound -7
Return code: Credential not found in dccsSDK_lib_subscribe()

- ERROR_ConnectError -8
Return code: 'NoneType' object has no attribute 'encode'

- ERROR_LoadJsonError -10
Return code: An invalid UTF-8 string has been detected.

- ERROR_HostValueNull -11
Return code: The value(Host) json get is Null

- ERROR_UsernameValueNull -12
Return code: The value(Username) json get is Null

- ERROR_PortValueNull -13
Return code: The value(Port) json get is Null

- ERROR_PasswordValueNull -14
Return code: The value(Password) json get is Null
