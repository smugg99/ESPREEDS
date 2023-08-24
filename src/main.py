import re
import time
from typing import Any, Dict, List, Optional

import requests
from plyer import notification

# Add more IP addresses here
IP_ADDRESSES: List[str] = [
    "http://192.168.1.48",
]

global previous_pin_states
previous_pin_states: Dict[str, Optional[bool]] = {}


def remove_http(url: str) -> str:
    cleaned_url = re.sub(r'^http://', '', url)
    return cleaned_url


def send_notification(title: str, message: str):
    notification.notify(
        title=title,
        message=message,
        app_name='ESPREEDS',
        timeout=2,
        app_icon='/data/icon.png'
    )


def check_pin_states():
    while True:
        try:
            for ip_address in IP_ADDRESSES:
                response: requests.Response = requests.get(ip_address)
                data: Dict[str, Any] = response.json()
                pin_state: bool = data.get("pinState", False)

                global previous_pin_states

                if ip_address not in previous_pin_states:
                    previous_pin_states[ip_address] = pin_state

                if pin_state != previous_pin_states[ip_address]:
                    send_notification("ESPREED", remove_http(ip_address) + " changes its state to: " +
                                      ("OPEN" if pin_state == False else "CLOSED"))
                    previous_pin_states[ip_address] = pin_state

        except requests.exceptions.ConnectionError:
            print("Couldn't connect to some ESPREED's IP, shieeeeeet!")
        except Exception as e:
            print("An error occurred: ", e)

        # Adjust as needed
        time.sleep(0.2)


if __name__ == "__main__":
    check_pin_states()
