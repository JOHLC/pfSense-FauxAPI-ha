import os, sys, json

sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '../client-libs/python')))     # hack to make this work in-place
from PfsenseFauxapi import PfsenseFauxapi


# check args exist
if(len(sys.argv) < 4):
    print()
    print('usage: ' + sys.argv[0] + ' <host> <apikey> <apisecret>')
    print()
    print('pipe JSON output through jq for easy pretty print output:-')
    print(' $ ' + sys.argv[0] + ' <host> <apikey> <apisecret> | jq .')
    print()
    sys.exit(1)

# config
fauxapi_host=sys.argv[1]
fauxapi_apikey=sys.argv[2]
fauxapi_apisecret=sys.argv[3]

PfsenseFauxapi= PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=False)


# system_stats
# =============================================================================
print(json.dumps(
    PfsenseFauxapi.system_stats())
)
