import sys
from PIL import Image

sys.path.append("..")
from dccsSDK import dccsSDK

def main():
	# TypeError: payload must be a string, bytearray, int, float or None.
	dccsContent = dccsSDK.dccsSDKStart("8e4297f56de1ec333557d5778ac496b5")
	dccsContent.dccsSDK_lib_publish("testtopic/1", "123", 0)

main()