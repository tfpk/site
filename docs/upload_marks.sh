#!/bin/bash

pip install requests

python <(cat <<EoF
import getpass
import pathlib
import requests
import re


SUBMIT_URL = "https://cgi.cse.unsw.edu.au/~cs2041/19T2/peer_assess/ass2_seddit/{zid}/Q{qid:02}/{grade}"

print("""
===========================================================
2041 Ass2 Peer Marking Workaround Script (~tfpk)
===========================================================

Hopefully this helps, if it doesn't contact t.kunc@unsw.edu.au
(This is not an official course tool, don't blame the course if this doesn't work)

HOWTO: Run this script in a directory with files called mark_<zid> (i.e. mark_5555555)
Follow the instructions, and it should mark everything for you...
""")

while True:
    zid = input(f"zid: ")
    zpass = getpass.getpass(prompt="zpass (will not display): ")
    if not all([zid, zpass]):
        print("zid or zpass not given! Try again?")
        continue

    req = requests.post(
        "https://cgi.cse.unsw.edu.au/~cs2041/19T2/flask.cgi/peer_assess/ass2_seddit/",
        data={'zid': zid, 'zpass': zpass}
    )

    SESSION_TOKEN = req.cookies.get('session')
    if SESSION_TOKEN:
        print("Session Token: "+ SESSION_TOKEN)
        break
    else:
        print("zid and zpass incorrect!")


for path in pathlib.Path('.').glob('mark_*'):
    zid = str(path).split('mark_')[-1]
    offset = 1
    with open(path, 'r') as f:
        for i, line in enumerate(f):
            line = line.replace('\n', '')
            line = line.strip()
            grade = re.search(r'\| +([a-zA-Z])$', line)
            if grade:
                grade = grade.group(1).upper()
                url = SUBMIT_URL.format( zid=zid, qid=i+offset, grade=grade)
                print(url)

                requests.put(url, cookies={'session': SESSION_TOKEN})
            else:
                offset -= 1

EoF
)
