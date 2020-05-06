#!/usr/bin/env python3
import csv
import json
from pathlib import Path

DEST_PATH = Path('data', 'compiled', 'npr-stations.csv')
SRC_DIR = Path('data', 'collected', 'npr-stations')


def glob_files():
    return SRC_DIR.glob('*.json')



def main():
    DEST_PATH.parent.mkdir(exist_ok=True, parents=True)
    stations = []
    for src in glob_files():
        data = json.loads(src.read_text())
        for item in data['items']:
            s = {}
            atts = item['attributes']
            s['org_id'] = atts['orgId']

            net = atts['network']
            s['network_name'] = net.get('name')
            # s['tier1_name'] = net['tier1']['name']

            el = atts['eligibility']
            s['eformat'] = el['format']
            s['estatus'] = el['status']
            s['music_only'] = el['musicOnly']

            brand = atts['brand']
            s['name'] = brand['name']
            s['band'] = brand['band']
            s['callsign'] = brand['call']
            s['tagline'] = brand['tagline']
            stations.append(s)

    with open(DEST_PATH, 'w') as dest:
        outs = csv.DictWriter(dest, fieldnames=stations[0].keys())
        outs.writeheader()
        outs.writerows(stations)


if __name__ == '__main__':
    main()
