#!/usr/bin/env python3
# Copyright 2017 Nicholas de Jong  <contact[at]nicholasdejong.com>
# Licensed under the Apache License, Version 2.0 

#############################################################################################
# Modified by JOHLC for use in Home Assistant                                               #
#############################################################################################
#Enter your interface for monitoring below:
interface = 'igb0'
# e.g. interface = 'igb1' 

########DO NOT EDIT ANYTHING BELOW THIS LINE############
import os,sys,json
sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '../client-libs/python')))     # hack to make this work in-place

try:
    from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi
except:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from PfsenseFauxapi import PfsenseFauxapi

# config
host=sys.argv[1]
apikey=sys.argv[2]
apisecret=sys.argv[3]

FauxapiLib = PfsenseFauxapi(host, apikey, apisecret, debug=False)

stat = FauxapiLib.system_stats()
info = FauxapiLib.system_info()
gw_status = FauxapiLib.gateway_status()
int_status = FauxapiLib.interface_stats(interface)

print('{"stat": ' + (json.dumps(stat)) + ',"info": ' + (json.dumps(info)) + ',"gw_status": ' + (json.dumps(gw_status)) + ',"int_status": ' + (json.dumps(int_status)) + '}')