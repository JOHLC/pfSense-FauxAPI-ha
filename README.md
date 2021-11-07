# pfSense FauxAPI for Home Assistant - DEPRECIATED
<img src="https://raw.githubusercontent.com/home-assistant/brands/master/custom_integrations/pfsense_gateways/logo.png" alt="pfSense" width="275">  

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
<img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/johlc/pfSense-FauxAPI-ha"> ![GitHub release (latest by date)](https://img.shields.io/github/v/release/johlc/pfSense-FauxAPI-ha?label=Version&style=flat-square&labelColor=2ea9f4&color=1473ae)
![GitHub All Releases](https://img.shields.io/github/downloads/johlc/pfSense-FauxAPI-ha/total?&label=Total%20Downloads&style=flat-square&labelColor=2ea9f4&color=1473ae) 

A custom component for Home Assistant that interfaces with FauxAPI installed on a pfSense firewall.

**Attention:** This isn't in any way intended to be an official or supported release, it is intended mainly for my own personal use. Continue at your own risk.  
If anyone with a better understanding of Python would like to help improve this, that would be cool. 

I owe credit mainly to the incredibly intellegent folks in this Home Assistant community post: [pfSense stat monitor](https://community.home-assistant.io/t/pfsense-stat-monitor/61070)  
and @dgshue for the [pfSense Rule Switch Component](https://github.com/dgshue/home-assistant-custom-components#pfsense_rule)

### Prerequisites
 - A device with [pfSense](https://www.pfsense.org/) installed - tested with v2.5 CE
   - Web access should be configured with ssl/https encryption and a certificate
 - [FauxAPI](https://github.com/ndejong/pfsense_fauxapi) installed on your pfSense instance, configured with an API key and access token - tested using the latest version as of 3/7/21
 - [Home Assistant](https://www.home-assistant.io/) - tested with core version 2021.3.3 on Home Assistant OS 5.12
 - The ability to run Python3 commands in your Home Assistant environmet - see [#8](https://github.com/JOHLC/pfSense-FauxAPI-ha/issues/8)
 - Patience and understanding 
 
### Screenshot
<img src="https://raw.githubusercontent.com/JOHLC/pfSense-FauxAPI-ha/main/images/sclatest.jpg" alt="Screenshot 1" >
# Install instructions

## 1. HACS installation - recommended<br /> 
1. Open HACS
2. Select "Frontend"
3. Select the ... menu button at the top right
4. Select "Custom repositories"
5. At the bottom left of the menu where it says "Add custom repository URL" add this repository: https://github.com/JOHLC/pfSense-FauxAPI-ha
6. Select the "Integration" category
7. Select "ADD"
8. Close this menu
9. This should now show up as a new repository
10. Click "INSTALL" then install again on the pop-up
11. Restart Home Assistant

### 1.1 Manual Installation - not recommended<br /> 
1. Download the files in custom components folder
2. Upload the downloadeded files to your custom components directory
3. Restart Home Assistant

## 2. Configure your sensors and commands<br /> 

#### Configure your secrets.yaml with the appropriate python commands
Important: You need to change a few things below with your setup information 
```yaml
# Example secrets.yaml entries - you will need to change your host IP, apikey, and accesstoken in each command below
pf_api_restart: "python3 /config/custom_components/pfsense_fauxapi/function-reboot.py 192.168.1.1 PFFAyourapikey youraccesstoken"
pf_api_command: "python3 /config/custom_components/pfsense_fauxapi/function-iterate.py 192.168.1.1 PFFAyourapikey youraccesstoken"
# Note: In order to fetch wan information you may need to do at least the following:
#   - Add `interface_*` to the `permit` line in `/etc/fauxapi/credentials.ini` in your pfSense instance
#   - Change the interface name in `config/custom_components/pfsense_fauxapi/function-iterate.py` if your pfSense wan interface is not `igb0` #e.g. interface = 'igb1' 

pf_key: PFFAyourpfsensekey
pf_token: yourpfsensetoken
```

#### Configure your rule switches
For more information on rule switches, see the creator's [repo](https://github.com/nagyrobi/home-assistant-custom-components-pfsense-ruleswitch)
```yaml
# Example configuration.yaml entries
switch:
  - platform: pfsense_fauxapi
    host: 192.168.1.1
    api_key: !secret pf_key
    access_token: !secret pf_token
    rule_filter: ha
```

#### Configure your reboot command
```yaml
# Example configuration.yaml entries
shell_command:
  pfsense_restart: !secret pf_api_restart
```

#### Configure your sensors
Note: You will need to change your.gw.ip.address under WAN section below to the IP address of your upstream gateway. 
```yaml
# Example configuration.yaml entry
sensor:
#######################################
#              FauxAPI                #
#######################################
###Version
  - platform: command_line
    command: !secret pf_api_command
    name: pfSense version
    value_template: '{{ value_json["info"]["data"]["info"]["pfsense_remote_version"]["installed_version"] }}'
    scan_interval: 43200

  - platform: command_line
    command: !secret pf_api_command
    name: pfSense latest
    value_template: '{{ value_json["info"]["data"]["info"]["pfsense_remote_version"]["version"] }}'
    scan_interval: 43200
    
###Hardware
  - platform: command_line
    command: !secret pf_api_command
    name: pfSense CPU temp
    value_template: '{{ value_json["stat"]["data"]["stats"]["temp"] }}'
    unit_of_measurement : '°C'
    scan_interval: 60

  - platform: command_line
    command: !secret pf_api_command
    name: pfSense uptime
    value_template: '{{ value_json["stat"]["data"]["stats"]["uptime"] | regex_replace(find=" days ",replace=":",ignorecase=True) | regex_replace(find=" day ",replace=":",ignorecase=True) | regex_replace(find=" hours ",replace=":",ignorecase=True) | regex_replace(find=" hour ",replace=":",ignorecase=True)| regex_replace(find=" Minutes ",replace=":",ignorecase=True) | regex_replace(find=" Minute ",replace=":",ignorecase=True) | regex_replace(find=" Seconds",replace="",ignorecase=True) | regex_replace(find=" Second",replace="",ignorecase=True) }}'
    scan_interval: 300

  - platform: command_line
    command: !secret pf_api_command
    name: pfSense memory use
    value_template: '{{ value_json["stat"]["data"]["stats"]["mem"] }}'
    unit_of_measurement : '%'
    scan_interval: 30

  - platform: command_line
    command: !secret pf_api_command
    name: pfSense CPU load avg
    value_template: '{{ ((value_json["stat"]["data"]["stats"]["load_average"][0] | float) * 100.0 / 2.0 ) | round(0) }}'
    unit_of_measurement : '%'
    scan_interval: 30

  - platform: command_line
    command: !secret pf_api_command
    name: pfSense CPU usage
    value_template: '{{ ( ( ((value_json["stat"]["data"]["stats"]["cpu"].split("|")[0] | float) / (value_json["stat"]["data"]["stats"]["cpu"].split("|")[1] | float)) - 1.0 ) * 100.0 ) | round(1) }}'
    unit_of_measurement : '%'
    scan_interval: 30

###WAN stats - change your.gw.ip.address to the correct IP address
  - platform: command_line
    command: !secret pf_api_command
    name: pfSense WAN IP
    value_template: '{{ value_json["gw_status"]["data"]["gateway_status"]["your.gw.ip.address"]["srcip"] }}'
    scan_interval: 300
    
  - platform: command_line
    command: !secret pf_api_command
    name: pfSense WAN packetloss
    value_template: '{{ (value_json["gw_status"]["data"]["gateway_status"]["your.gw.ip.address"]["loss"]) | regex_replace(find="%",replace="",ignorecase=True) }}'
    unit_of_measurement: "%"
    scan_interval: 30

  - platform: command_line
    command: !secret pf_api_command
    name: pfSense WAN status
    value_template: '{{ (value_json["gw_status"]["data"]["gateway_status"]["your.gw.ip.address"]["status"]) }}'
    scan_interval: 30

  - platform: command_line
    command: !secret pf_api_command
    name: pfSense WAN latency
    value_template: '{{ (value_json["gw_status"]["data"]["gateway_status"]["your.gw.ip.address"]["delay"]) | regex_replace(find="ms",replace="",ignorecase=True) }}' 
    unit_of_measurement: "ms"
    scan_interval: 60
    
  - platform: command_line
    command: !secret pf_api_command
    name: pfSense WAN GB in
    value_template: '{{ (value_json["int_status"]["data"]["stats"]["inbytes"] | float / 1000 / 1000 / 1000) | round(2)}}'
    scan_interval: 60
    unit_of_measurement: GB

  - platform: command_line
    command: !secret pf_api_command
    name: pfSense WAN GB out
    value_template: '{{ (value_json["int_status"]["data"]["stats"]["outbytes"] | float / 1000 / 1000 / 1000) | round(2)}}'
    scan_interval: 60
    unit_of_measurement: GB
