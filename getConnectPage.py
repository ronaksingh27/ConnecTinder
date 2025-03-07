import requests
import json
import os
import re
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Constants
OUTPUT_FILE = "rehydration.json"
LINKEDIN_URL = "https://www.linkedin.com/flagship-web/rsc-action/actions/server-request?sduiid=com.linkedin.sdui.requests.mynetwork.addaAddConnection"

# Load environment variables
load_dotenv()

# Setup session with headers and cookies
session = requests.Session()
session.headers.update({
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
})

cookies = {
    "JSESSIONID": os.getenv("JSESSIONID"),
    "li_at": os.getenv("LI_AT"),
    "bscookie": os.getenv("BSCOOKIE"),
    "bcookie": os.getenv("BCOOKIE"),
    "lidc": os.getenv("LIDC"),
    "timezone": os.getenv("TIMEZONE"),
    "liap": os.getenv("LIAP"),
}
session.cookies.update(cookies)

csrf_token = cookies.get("JSESSIONID", "").strip('"').replace('ajax:', '')
session.headers.update({"csrf-token": f"ajax:{csrf_token}"})


def fetch_rehydration_data():
    url = "https://www.linkedin.com/mynetwork/"
    response = session.get(url, timeout=10)

    tries = 10
    while len(response.text) < 400000 and tries > 0:
        response = session.get(url, timeout=10)
        tries = tries - 1

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", {"id": "rehydrate-data"})

    if not script_tag or not script_tag.string:
        print("❌ Could not find rehydrate-data script.")
        return None

    match = re.search(r'window\.__como_rehydration__\s*=\s*(\[[^\n]+)', script_tag.string)
    if not match:
        print("❌ Could not locate window.__como_rehydration__ data.")
        return None

    raw_json = match.group(1).strip().rstrip(';')
    raw_json = raw_json.replace(r'\u0026', '&').replace(r'\\"', '"')

    return raw_json


def get_unique_payloads():
    data = fetch_rehydration_data()
    if not data:
        return set()

    payloads = re.findall(r'"payload\\"\s*:\s*({.*?{.*?}.*?}.*?}.*?})', data)
    print(f"🔎 Found {len(payloads)} payload candidates.")

    required_fields = {
        "inviteeUrn", "nonIterableProfileId", "renderMode",
        "firstName", "lastName", "isDisabled", "connectionState"
    }

    unique_payloads = set()

    for payload_str in payloads:
        try:
            decoded_payload = payload_str.encode('utf-8').decode('unicode_escape')
            payload_json = json.loads(decoded_payload)

            if required_fields.issubset(payload_json):
                unique_payloads.add(json.dumps(payload_json, sort_keys=True))

        except json.JSONDecodeError:
            continue

    print(f"✅ {len(unique_payloads)} unique valid payloads found.")
    return unique_payloads


def create_payload(profile):
    return {
        "requestId": "com.linkedin.sdui.requests.mynetwork.addaAddConnection",
        "serverRequest": {
            "$type": "proto.sdui.actions.core.ServerRequest",
            "requestId": "com.linkedin.sdui.requests.mynetwork.addaAddConnection",
            "payload": profile,
            "requestedStates": [],
            "requestedArguments": {
                "$type": "proto.sdui.actions.requests.RequestedArguments",
                "payload": profile,
                "requestedStateKeys": []
            },
            "onClientRequestFailureAction": {
                "actions": [
                    {
                        "$type": "proto.sdui.actions.core.SetState",
                        "value": {
                            "$type": "proto.sdui.actions.core.SetState",
                            "stateKey": "",
                            "stateValue": "",
                            "state": {
                                "$type": "proto.sdui.State",
                                "stateKey": "",
                                "key": {
                                    "$type": "proto.sdui.Key",
                                    "value": {
                                        "$case": "id",
                                        "id": profile["connectionState"]
                                    }
                                },
                                "namespace": ""
                            },
                            "value": {
                                "$case": "stringValue",
                                "stringValue": "Connect"
                            },
                            "isOptimistic": False
                        }
                    },
                    {
                        "$type": "proto.sdui.actions.core.SetState",
                        "value": {
                            "$type": "proto.sdui.actions.core.SetState",
                            "stateKey": "",
                            "stateValue": "",
                            "state": {
                                "$type": "proto.sdui.State",
                                "stateKey": "",
                                "key": {
                                    "$type": "proto.sdui.Key",
                                    "value": {
                                        "$case": "id",
                                        "id": profile["isDisabled"]
                                    }
                                },
                                "namespace": ""
                            },
                            "value": {
                                "$case": "booleanValue",
                                "booleanValue": False
                            },
                            "isOptimistic": False
                        }
                    }
                ]
            },
            "isStreaming": False,
            "rumPageKey": ""
        },
        "states": [],
        "requestedArguments": {
            "$type": "proto.sdui.actions.requests.RequestedArguments",
            "payload": profile,
            "requestedStateKeys": [],
            "states": []
        }
    }


def generate_payloads():
    unique_payloads = get_unique_payloads()
    profiles = [json.loads(payload) for payload in unique_payloads]

    payloads = [create_payload(profile) for profile in profiles]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payloads, f, indent=4)

    print(f"✅ Saved {len(payloads)} payloads to {OUTPUT_FILE}")
    return payloads


def send_connection_requests():
    payloads = generate_payloads()
    sent_names = set()

    for payload in payloads:
        first_name = payload['serverRequest']['requestedArguments']['payload'].get('firstName', 'Unknown')
        response = session.post(LINKEDIN_URL, json=payload)

        print(f"📨 Sent request for: {first_name}")
        print(f"Response Code: {response.status_code}")
        print(f"Response: {response.text}\n{'-'*50}")

        if response.status_code == 400:
            print("⚠️ Retrying failed request...")
            response = session.post(LINKEDIN_URL, json=payload)
            print(f"Retry Response Code: {response.status_code}")
            print(f"Retry Response: {response.text}\n{'-'*50}")

        if '"message":"Failed to create connection"}]},"states":[]}' not in response.text:
            sent_names.add(payload.get('serverRequest', {}).get('requestedArguments', {}).get('payload', {}).get('firstName', 'Unknown'))


    return sent_names


if __name__ == "__main__":
    all_names = set()

    for i in range(10):
        print(f"🔄 Starting round {i+1}")
        time.sleep(2)
        all_names.update(send_connection_requests())

    print(f"✅ Total unique names processed: {len(all_names)}")
    print(f"Request sent to : {all_names}")
