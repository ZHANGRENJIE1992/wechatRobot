# agrv is string, can't be used now, need convert to right format
import json
import re
from datetime import datetime,timedelta

def convert(argv):
	keyinfo = []
	host = argv[1] # string ->string
	keyinfo.append(host)
	
	port = argv[2] # string -> string
	keyinfo.append(port)
	
	user = argv[3]	 #string -> string
	keyinfo.append(user)
	
	password = argv[4] #string -> string
	keyinfo.append(password)
	
	database = argv[5] #string -> string
	keyinfo.append(database)
	
	return keyinfo