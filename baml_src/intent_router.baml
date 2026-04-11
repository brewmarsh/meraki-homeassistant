enum MerakiIntent {
  RebootDevice @description("User wants to restart or reboot a specific network device, switch, or camera.")
  GenerateGuestAccess @description("User wants to create a temporary wifi password or IPSK.")
  CycleSwitchPort @description("User wants to power cycle or reset a specific port on a network switch.")
  GetNetworkStatus @description("User wants to check the current status, health, or connectivity of their network or devices.")
  Unknown @description("User's command does not match any known Meraki action.")
}

class MerakiIntentResponse {
  intent MerakiIntent
  target_device string | null
  guest_name string | null
  duration_minutes int | null
  network_name string | null
}

function RouteMerakiIntent(user_command: string) -> MerakiIntentResponse {
  client "openai/gpt-4o"
  prompt #"
    {{ ctx.output_format }}

    System: You are a smart home network assistant specialized in managing Meraki networks.
    Your goal is to parse user commands and map them to the correct Meraki-specific action and extract relevant parameters.

    User: <user_command>Can you reboot the Garage Switch?</user_command>
    Assistant: {
      "intent": "RebootDevice",
      "target_device": "Garage Switch",
      "guest_name": null,
      "duration_minutes": null,
      "network_name": null
    }

    User: <user_command>Create a guest key for Marshmallow Home for 60 minutes</user_command>
    Assistant: {
      "intent": "GenerateGuestAccess",
      "target_device": null,
      "guest_name": "Marshmallow Home",
      "duration_minutes": 60,
      "network_name": null
    }

    User: <user_command>How is my network doing at the Office?</user_command>
    Assistant: {
      "intent": "GetNetworkStatus",
      "target_device": null,
      "guest_name": null,
      "duration_minutes": null,
      "network_name": "Office"
    }

    User: <user_command>Reset port 3 on the Basement Switch</user_command>
    Assistant: {
      "intent": "CycleSwitchPort",
      "target_device": "Basement Switch",
      "guest_name": null,
      "duration_minutes": null,
      "network_name": null
    }

    User: <user_command>{{ user_command }}</user_command>
    Assistant:
  "#
}
