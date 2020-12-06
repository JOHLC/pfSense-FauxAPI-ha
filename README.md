# pfSense FauxAPI for Home Assistant
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
![GitHub All Releases](https://img.shields.io/github/downloads/johlc/pfSense-FauxAPI-ha/total?&label=Total%20Downloads&style=flat-square&labelColor=2ea9f4&color=1473ae) 

A custom component for Home Assistant that interfaces with FauxAPI installed on a pfSense firewall.
This isn't in any way intended to be an official or supported release, so continue at your own risk. I'm not even sure it's even a "component."
If anyone with a better understanding of Python would like to help improve this, that would be cool. 

I owe credit to mainly this Home Assistant community post: https://community.home-assistant.io/t/pfsense-stat-monitor/61070
Also: https://community.home-assistant.io/t/pfsense-rule-switch/109424 / https://github.com/dgshue/home-assistant-custom-components

### Prerequisites
 - [FauxAPI](https://github.com/ndejong/pfsense_fauxapi) installed and configured with an API key and access token
 - [Home Assistant](https://www.home-assistant.io/) - I am running on Home Assistant OS / Hassio 
 - The ability to run Python3 commands in your Home Assistant environmet
 - To switch firewall rules on or off you need this component: https://github.com/dgshue/home-assistant-custom-components
 - Patience and understanding 
 
### Screenshot

<img src="https://raw.githubusercontent.com/JOHLC/pfSense-FauxAPI-ha/main/images/screen1.png" alt="Screenshot 1" >



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
```yaml
# Example secrets.yaml entries - you will need to change your host IP, apikey, and accesstoken in each command below
pf_api_stats: "python3 /config/custom_components/pfsense_fauxapi/function-stats.py 192.168.1.1 PFFAyourapikey youraccesstoken"
pf_api_info: "python3 /config/custom_components/pfsense_fauxapi/function-info.py 192.168.1.1 PFFAyourapikey youraccesstoken"
pf_api_restart: "python3 /config/custom_components/pfsense_fauxapi/function-reboot.py 192.168.1.1 PFFAyourapikey youraccesstoken"
pf_api_gw: "python3 /config/custom_components/pfsense_fauxapi/function-gateway.py 192.168.1.1 PFFAyourapikey youraccesstoken"
# Note: In order to fetch wan information you may need to do the following:
#   - Add `interface_*` to the `permit` line in `/etc/fauxapi/credentials.ini` in your pfSense instance
#   - Change the interface name in `config/custom_components/pfsense_fauxapi/function-int-wan.py` if your pfSense wan interface is not `igb0`
pf_api_int_wan: "python3 /config/custom_components/pfsense_fauxapi/function-int-wan.py 192.168.1.1 PFFAyourapikey youraccesstoken"
```

#### Configure your reboot command
```yaml
# Example configuration.yaml entries
shell_command:
  pfsense_restart: !secret pf_api_restart
```

#### Configure your sensors
```yaml
# Example configuration.yaml entry
sensor:
#######################################
#              FauxAPI                #
#######################################
###Version
  - platform: command_line
    command: !secret pf_api_info
    name: pfSense version
    value_template: '{{ value_json["data"]["info"]["pfsense_remote_version"]["installed_version"] }}'
    scan_interval: 3600

  - platform: command_line
    command: !secret pf_api_info
    name: pfSense latest
    value_template: '{{ value_json["data"]["info"]["pfsense_remote_version"]["version"] }}'
    scan_interval: 3600
###Hardware
  - platform: command_line
    command: !secret pf_api_stats
    name: pfSense_CPU_temp
    value_template: '{{ value_json["data"]["stats"]["temp"] }}'
    unit_of_measurement : 'C'
    scan_interval: 60

  - platform: command_line
    command: !secret pf_api_stats
    name: pfSense_uptime
    value_template: '{{ value_json["data"]["stats"]["uptime"] }}'
    scan_interval: 60

  - platform: command_line
    command: !secret pf_api_stats
    name: pfSense memory use
    value_template: '{{ value_json["data"]["stats"]["mem"] }}'
    unit_of_measurement : '%'
    scan_interval: 60

  - platform: command_line
    command: !secret pf_api_stats
    name: pfSense CPU load avg
    value_template: '{{ ((value_json["data"]["stats"]["load_average"][0] | float) * 100.0 / 2.0 ) | round(0) }}'
    unit_of_measurement : '%'
    scan_interval: 60

  - platform: command_line
    command: !secret pf_api_stats
    name: pfSense CPU usage
    value_template: '{{ ( ( ((value_json["data"]["stats"]["cpu"].split("|")[0] | float) / (value_json["data"]["stats"]["cpu"].split("|")[1] | float)) - 1.0 ) * 100.0 ) | round(1) }}'
    unit_of_measurement : '%'
    scan_interval: 60
    
###WAN stats
  - platform: command_line
    command: !secret pf_api_gw
    name: pfSense WAN IP
    value_template: '{{ value_json["data"]["gateway_status"]["ip.address.of.yourgw"]["srcip"] }}'
    scan_interval: 1800
    
  - platform: command_line
    command: !secret pf_api_gw
    name: pfSense WAN packetloss
    value_template: '{{ value_json["data"]["gateway_status"]["ip.address.of.yourgw"]["loss"] }}'
    scan_interval: 15

  - platform: command_line
    command: !secret pf_api_gw
    name: pfSense WAN status
    value_template: '{{ value_json["data"]["gateway_status"]["ip.address.of.yourgw"]["status"] }}'
    scan_interval: 15

  - platform: command_line
    command: !secret pf_api_gw
    name: pfSense WAN latency
    value_template: '{{ value_json["data"]["gateway_status"]["ip.address.of.yourgw"]["delay"] }}'
    scan_interval: 60

  - platform: command_line
    command: !secret pf_api_int_wan
    name: pfSense WAN GB in
    value_template: '{{ (value_json["data"]["stats"]["inbytes"] | float / 1000 / 1000 / 1000) | round(2)}}'
    scan_interval: 60
    unit_of_measurement: GB

  - platform: command_line
    command: !secret pf_api_int_wan
    name: pfSense WAN GB out
    value_template: '{{ (value_json["data"]["stats"]["outbytes"] | float / 1000 / 1000 / 1000) | round(2)}}'
    scan_interval: 60
    unit_of_measurement: GB
  
