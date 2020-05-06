#!/usr/bin/env python3
import csv
import json
from pathlib import Path
import requests
from urllib.parse import urlencode

# example for California: https://www.npr.org/proxy/stationfinder/v3/stations?q=CA
BASE_API_ENDPOINT = 'https://www.npr.org/proxy/stationfinder/v3/stations'
DEST_DIR = Path('data', 'collected', 'npr-stations')

SRC_PATH = Path('data', 'archived', 'lookups', 'state-codes.csv')


def api_url(code):
    return f"{BASE_API_ENDPOINT}?{urlencode({'q': code})}"

def dest_path(code):
    return DEST_DIR.joinpath(f'{code}.json')

def fetch_api(url):
    resp = requests.get(url)
    return (True, resp.text) if resp.status_code == 200 else (False, resp.status_code)

def load_state_codes():
    return [row['usps'] for row in csv.DictReader(SRC_PATH.open()) if row['is_state'] == 'TRUE' or row['usps'] == 'DC' ]


def loge(txt):
    print(txt)


def main():
    DEST_DIR.mkdir(exist_ok=True, parents=True)
    for state in load_state_codes():
        url = api_url(state)
        loge(f"Fetching {url}")
        is_success, txt = fetch_api(url)

        if not is_success:
            loge(f"ERROR: got status code of {txt}")
        else:
            loge(f"Success: {len(txt)} chars")
            jdata = json.loads(txt)
            jtext = json.dumps(jdata, indent=2)
            dest = dest_path(state)
            dest.write_text(jtext)
            loge(f"Wrote {len(jdata['items'])} stations to {dest}")


if __name__ == '__main__':
    main()
