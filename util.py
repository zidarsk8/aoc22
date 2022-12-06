
# curl  \
#   -H 'authority: adventofcode.com' \
#   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
#   -H 'accept-language: en-GB,en-US;q=0.9,en;q=0.8' \
#   -H 'cache-control: max-age=0' \
#   -H 'cookie: session=53616c7465645f5f5bf51eb1a7a36aee437911df0ae3358cb5a43eda46d184736e0d039ba8a63f4273ec52e7cf1a600d1338b570a35c5ab1d71d1b5965e12cbe' \
#   -H 'referer: https://adventofcode.com/2022/day/2' \
#   -H 'sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   -H 'sec-fetch-dest: document' \
#   -H 'sec-fetch-mode: navigate' \
#   -H 'sec-fetch-site: same-origin' \
#   -H 'sec-fetch-user: ?1' \
#   -H 'sec-gpc: 1' \
#   -H 'upgrade-insecure-requests: 1' \
#   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' \
#   --compressed ;

import requests
import json
import os
import pickle
 
 
headers = {
    'authority': 'adventofcode.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'cookie': 'session=53616c7465645f5f5bf51eb1a7a36aee437911df0ae3358cb5a43eda46d184736e0d039ba8a63f4273ec52e7cf1a600d1338b570a35c5ab1d71d1b5965e12cbe',
    'referer': 'https://adventofcode.com/2022/day/2',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

def read_data(day:int)->str:
    file = f"data/aoc_{day}_input.txt"
    
    url = f"https://adventofcode.com/2022/day/{day}/input"
    response = requests.get(url, headers=headers)
    return response.text
