import re

from click import secho
import requests


URL = 'https://www.bikeseoul.com/app/station/getStationRealtimeStatus.do'

DISTRICTS = [
    {  # Songpa-gu
        'code': 23,
        'interested': set([
            '1210. 롯데월드타워(잠실역2번출구 쪽)',
            '1231. 잠실역 6번출구',
        ])
    },
    {  # Gangnam-gu
        'code': 33,
        'interested': set([
            '2316. 삼성역 8번출구',
            '2322. 삼성역 3번 출구',
            '2348. 포스코사거리(기업은행)',
            '2355. 삼성역 5~6번 출구 사이',
        ])
    },
]

def command():
    for name, count in query(DISTRICTS):
        color = ('red' if count == 0 else 'green')
        secho(f'({count})', fg=color, nl=False)
        secho(f'- {name}')


def query(districts):
    for d in districts:
        payload = {'stationGrpSeq': d['code']}
        response = requests.post(URL, data=payload)
        rows = response.json()['realtimeList']
        for row in rows:
            name = row['stationName'].strip()
            if name in d['interested']:
                count = int(row['parkingBikeTotCnt'])
                yield (name, count)
