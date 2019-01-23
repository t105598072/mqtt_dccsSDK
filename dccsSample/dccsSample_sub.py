import sys
sys.path.append("..")
from dccsSDK import dccsSDK

def RecvMsgCB(Msg):
	print("Message received: " + Msg);
	return Msg;

def main():
	dccsContent = dccsSDK.dccsSDKStart("https://api-dccs.wise-paas.com/v1/serviceCredentials/8e4297f56de1ec333557d5778ac496b5")
	dccsContent.dccsSDK_lib_subscribe("testtopic/1", 0, RecvMsgCB)

main()