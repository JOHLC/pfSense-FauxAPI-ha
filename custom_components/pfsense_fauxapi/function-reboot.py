import os, sys, json

sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '../client-libs/python')))     # hack to make this work in-place
from PfsenseFauxapi import PfsenseFauxapi


# check args exist
if(len(sys.argv) < 4):
    print()
    print('usage: ' + sys.argv[0] + ' <host> <apikey> <apisecret>')
    print()
    print(' $ ' + sys.argv[0] + ' <host> <apikey> <apisecret> | jq .')
    print()
    sys.exit(1)

#config
host=sys.argv[1]
port=sys.argv[2]
apikey=sys.argv[3]
apisecret=sys.argv[4]

fauxapi_host = '{}:{}'.format(host, port)

FauxapiLib = PfsenseFauxapi(fauxapi_host, apikey, apisecret, debug=False)

# reboot
# =============================================================================
print(json.dumps(
    PfsenseFauxapi.system_reboot())
)
