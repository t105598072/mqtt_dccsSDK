import sys
sys.path.append("..")
from dccsSDK import dccsSDK

def RecvMsgCB(Msg):
	print("Message received: " + Msg);
	return Msg;

def main():
	dccsContent = dccsSDK.dccsSDKStart("")
	dccsContent.dccsSDK_lib_subscribe("Topic", 0, RecvMsgCB)

main()
