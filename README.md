# pfSense-FauxAPI
A custom component for Home Assistant that interfaces with FauxAPI installed on a pfSense firewall.
This isn't in any way intended to be an official or supported release, so continue at your own risk. 


I owe credit to mainly this Home Assistant community post: https://community.home-assistant.io/t/pfsense-stat-monitor/61070
Also: https://community.home-assistant.io/t/pfsense-rule-switch/109424 / https://github.com/dgshue/home-assistant-custom-components

### Prerequisites
 - FauxAPI installed and configured with an API key and access token
 - Home Assistant - I am running on Home Assistant OS / Hassio 
 - Patience and understanding 
 - Python3?
 

# Install instructions

## Install the components
1. Copy the folder in custom_components/ called "pfsense_fauxapi" to your custom components directory in Home Assistant
2. To switch firewall rules on or off you need this: https://github.com/dgshue/home-assistant-custom-components

## Configure your secrets.yaml with the appropriate python commands
```yaml
# Example secrets.yaml entries - you will need to change your host IP, apikey, and accesstoken in each command below
pf_api_stats: "python3 /config/custom_components/pfsense_fauxapi/function-stats.py 192.168.1.1 PFFAyourapikey youraccesstoken"
pf_api_info: "python3 /config/custom_components/pfsense_fauxapi/function-info.py 192.168.1.1 PFFAyourapikey youraccesstoken"
pf_api_gw: "python3 /config/custom_components/pfsense_fauxapi/function-gateway.py 192.168.1.1 PFFAyourapikey youraccesstoken"
pf_api_restart: "python3 /config/custom_components/pfsense_fauxapi/function-reboot.py 192.168.1.1 PFFAyourapikey youraccesstoken"
```

## Configure your reboot command
```yaml
# Example configuration.yaml entries
shell_command:
  pfsense_restart: !secret pf_api_restart

```

## Configure your sensors
```yaml
# Example configuration.yaml entry
sensor:
# Version
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
# Hardware
  - platform: command_line
    command: !secret pf_api_info
    name: pfSense_CPU_temp
    value_template: '{{ value_json["data"]["stats"]["temp"] }}'
    unit_of_measurement : 'C'
    scan_interval: 30

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
    scan_interval: 15

  - platform: command_line
    command: !secret pf_api_stats
    name: pfSense CPU load avg
    value_template: '{{ ((value_json["data"]["stats"]["load_average"][0] | float) * 100.0 / 2.0 ) | round(0) }}'
    unit_of_measurement : '%'
    scan_interval: 15

  - platform: command_line
    command: !secret pf_api_stats
    name: pfSense CPU usage
    value_template: '{{ ( ( ((value_json["data"]["stats"]["cpu"].split("|")[0] | float) / (value_json["data"]["stats"]["cpu"].split("|")[1] | float)) - 1.0 ) * 100.0 ) | round(1) }}'
    unit_of_measurement : '%'
    scan_interval: 15
```

  
