import meraki
import argparse
import re
import time
import json

DOMAIN = "meraki_ha"

def setup(hass, config):
    hass.states.set("meraki_ha.world", "Started")
    
    return True;

def validate_api_key(api_key):
    # Example validation: API_KEY should be a non-empty string
    if not api_key or not isinstance(api_key, str):
        raise argparse.ArgumentTypeError("API_KEY must be a non-empty string.")
    return api_key

def validate_organization_id(organization_id):
    # Example validation: ORGANIZATION_ID should be a non-empty string of digits
    if not organization_id or not re.match(r'^\d+$', organization_id):
        raise argparse.ArgumentTypeError("ORGANIZATION_ID must be a non-empty string of digits.")
    return organization_id

def main():
    parser = argparse.ArgumentParser(description="Pass API_KEY and ORGANIZATION_ID as parameters.")
    parser.add_argument("--api_key", type=validate_api_key, required=True, help="API key for Meraki API.")
    parser.add_argument("--organization_id", type=validate_organization_id, required=True, help="Organization ID for Meraki API.")
    
    args = parser.parse_args()
    
    api_key = args.api_key
    org_id = args.organization_id
    
    print(f"API_KEY: {args.api_key}")
    print(f"ORGANIZATION_ID: {args.organization_id}")
    
    dashboard = meraki.DashboardAPI(api_key)

    devices_json = dashboard.organizations.getOrganizationDevices(org_id, total_pages='all')
    #devices = json.load(devices_json)
    
    #print (devices)

    serial_numbers = [item['serial'] for item in devices_json]

    # Print the serial numbers
    for serial in serial_numbers:
        print(serial)
    
    while True:
        time.sleep(60)
    
if __name__ == "__main__":
    main()


