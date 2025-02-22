#!/bin/bash

echo "Starting Meraki integration for Home Assistant"
# Read the secret key and Meraki API key from the configuration
API_KEY=$(jq --raw-output '.api_key' /data/options.json)
ORGANIZATION_ID=$(jq --raw-output '.organization_id' /data/options.json)

# Define the Home Assistant API URL
HA_API_URL="http://homeassistant.local:8123/api/states/sensor.meraki_mx_status"

if [ -z "$API_KEY" ]; then
  echo "Error: API key not provided. Please obtain your secret key from the Meraki dashboard."
  echo "To obtain your API key, navigate to the Meraki dashboard, go to Organization -> API & Webhooks -> API keys and access and generate an API key."
  exit 1
fi

echo "Your secret key is: $API_KEY"

python /merakisync.py --api_key $API_KEY --organization_id $ORGANIZATION_ID

# Post the Meraki MX status to Home Assistant
#curl -X POST "$HA_API_URL" -H "Authorization: Bearer $SECRET_KEY" -H "Content-Type: application/json" -d "{\"state\": \"$MX_STATUS\"}"

#echo "Meraki MX Status posted to Home Assistant"