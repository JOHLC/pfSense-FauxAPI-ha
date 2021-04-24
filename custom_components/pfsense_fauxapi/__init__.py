"""pfSense FauxAPI for Home Assistant"""

DOMAIN = "pfsense_fauxapi"

def setup(hass, config):
    import PfsenseFauxapi
    #from funkapi import FunkAPI
    # Return boolean to indicate that initialization was successful.
    return True
