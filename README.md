# calls

Given an XML call log backup file and a phone number
an image will be generated showing all calls with
this number with their time, duration and type (incoming, outgoing, etc.)

Notes:

- XML is generated from the Android app: `Call Log Backup & Restore`
- Supply a phone number without the +1 or any hyphens

`pip install PIL`

Usage: `python call_log.py 206555xxxx calls.xml calls.png`
