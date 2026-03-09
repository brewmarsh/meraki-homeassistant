import os
from baml_client import b
from baml_client.types import MerakiIntent

def test_intent_router():
    # Test cases: (input_command, expected_intent)
    test_cases = [
        ("Reboot my Living Room AP", MerakiIntent.RebootDevice),
        ("Give me a guest password for my friend John for 2 hours", MerakiIntent.GenerateGuestAccess),
        ("Can you cycle port 5 on the core switch?", MerakiIntent.CycleSwitchPort),
        ("Is the network okay in the Kitchen?", MerakiIntent.GetNetworkStatus),
        ("What's for dinner?", MerakiIntent.Unknown),
    ]

    print(f"Running {len(test_cases)} test cases...")

    for command, expected_intent in test_cases:
        print(f"\nTesting: \"{command}\"")
        try:
            response = b.RouteMerakiIntent(user_command=command)
            print(f"Extracted Intent: {response.intent}")
            print(f"Response: {response}")

            if response.intent == expected_intent:
                print("✅ PASS")
            else:
                print(f"❌ FAIL: Expected {expected_intent}, got {response.intent}")
        except Exception as e:
            print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        print("Skipping LLM-based verification: OPENAI_API_KEY not set.")
    else:
        test_intent_router()
