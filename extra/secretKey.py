import os
from base64 import b64encode

def main():
	print b64encode(os.urandom(24))

main()