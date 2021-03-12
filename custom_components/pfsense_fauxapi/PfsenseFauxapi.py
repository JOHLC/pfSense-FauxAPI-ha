#
# Copyright 2020 Nicholas de Jong  <contact[at]nicholasdejong.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

import os
import json
import base64
import urllib
import requests
import datetime
import hashlib


class PfsenseFauxapiException(Exception):
    pass


class PfsenseFauxapi:

    host = None
    proto = None
    debug = None
    version = None
    apikey = None
    apisecret = None
    use_verified_https = None

    def __init__(self, host, apikey, apisecret, use_verified_https=False, debug=False):
        self.proto = 'https'
        self.base_url = 'fauxapi/v1'
        self.host = host
        self.apikey = apikey
        self.apisecret = apisecret
        self.use_verified_https = use_verified_https
        self.debug = debug
        if self.use_verified_https is False:
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    def config_get(self, section=None):
        config = self._api_request('GET', 'config_get')
        if section is None:
            return config['data']['config']
        elif section in config['data']['config']:
            return config['data']['config'][section]
        raise PfsenseFauxapiException('Unable to complete config_get request, section is unknown', section)

    def config_set(self, config, section=None):
        if section is None:
            config_new = config
        else:
            config_new = self.config_get(section=None)
            config_new[section] = config
        return self._api_request('POST', 'config_set', data=config_new)

    def config_patch(self, config):
        return self._api_request('POST', 'config_patch', data=config)

    def config_reload(self):
        return self._api_request('GET', 'config_reload')

    def config_backup(self):
        return self._api_request('GET', 'config_backup')

    def config_backup_list(self):
        return self._api_request('GET', 'config_backup_list')

    def config_restore(self, config_file):
        return self._api_request('GET', 'config_restore', params={'config_file': config_file})

    def send_event(self, command):
        return self._api_request('POST', 'send_event', data=[command])

    def system_reboot(self):
        return self._api_request('GET', 'system_reboot')

    def system_stats(self):
        return self._api_request('GET', 'system_stats')

    def interface_stats(self, interface):
        return self._api_request('GET', 'interface_stats', params={'interface': interface})

    def gateway_status(self):
        return self._api_request('GET', 'gateway_status')

    def rule_get(self, rule_number=None):
        return self._api_request('GET', 'rule_get', params={'rule_number': rule_number})

    def alias_update_urltables(self, table=None):
        if table is not None:
            return self._api_request('GET', 'alias_update_urltables', params={'table': table})
        return self._api_request('GET', 'alias_update_urltables')

    def function_call(self, data):
        return self._api_request('POST', 'function_call', data=data)

    def system_info(self):
        return self._api_request('GET', 'system_info')

    def _api_request(self, method, action, params=None, data=None):

        if params is None:
            params = {}

        if self.debug:
            params['__debug'] = 'true'

        url = '{proto}://{host}/{base_url}/?action={action}&{params}'.format(
            proto=self.proto, host=self.host, base_url=self.base_url, action=action, params=urllib.parse.urlencode(params))

        if method.upper() == 'GET':
            res = requests.get(
                url,
                headers={'fauxapi-auth': self._generate_auth()},
                verify=self.use_verified_https
            )
        elif method.upper() == 'POST':
            res = requests.post(
                url,
                headers={'fauxapi-auth': self._generate_auth()},
                verify=self.use_verified_https,
                data=json.dumps(data)
            )
        else:
            raise PfsenseFauxapiException('Request method not supported!', method)

        if res.status_code == 404:
            raise PfsenseFauxapiException('Unable to find FauxAPI on target host, is it installed?')
        elif res.status_code != 200:
            raise PfsenseFauxapiException('Unable to complete {}() request'.format(action), json.loads(res.text))

        return self._json_parse(res.text)

    def _generate_auth(self):
        # auth = apikey:timestamp:nonce:HASH(apisecret:timestamp:nonce)
        nonce = base64.b64encode(os.urandom(40)).decode('utf-8').replace('=', '').replace('/', '').replace('+', '')[0:8]
        timestamp = datetime.datetime.utcnow().strftime('%Y%m%dZ%H%M%S')
        hash = hashlib.sha256('{}{}{}'.format(self.apisecret, timestamp, nonce).encode('utf-8')).hexdigest()
        return '{}:{}:{}:{}'.format(self.apikey, timestamp, nonce, hash)

    def _json_parse(self, data):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            pass
        raise PfsenseFauxapiException('Unable to parse response data!', data)