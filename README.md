# Call Visualization

Given an XML call log backup file and a phone number
an image will be generated showing all calls with
this number (or any number it is a substring of, e.g. use just first 3 digits to show all one area code) with their time, duration and type (incoming, outgoing, etc.)
Not as good as regex since the area code could appear somewhere else in the phone number, not necessarily at the beginning

## Notes

- XML is generated from the Android app: `Call Log Backup & Restore`
- Supply a phone number without the +1 or any hyphens <!-- TODO: Just strip +1 and hypens? -->
- To combine multiple call history files simply concatenate them <!-- TODO: Test that this works and provide windows and linux CLI example commands -->
- TODO add commands to concatenate multiple XML files

<https://github.com/search?q=history+call+phone>
<https://sqlitebrowser.org/>
<https://forum.xda-developers.com/t/guide-root-pixel-4a-5g-android-12.4221133/>
<https://www.youtube.com/watch?v=0czbUAJ39qI&t=1s&ab_channel=stayshubh>
<https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html?highlight=text#PIL.ImageDraw.ImageDraw.text>
<https://www.androidauthority.com/android-app-development-1128595/>
<https://www.androidauthority.com/kotlin-tutorial-1134289/>
<https://developers.google.com/protocol-buffers/docs/kotlintutorial>

## Build

1. `pip install -r requirements.txt`
1. Download [protoc](https://github.com/protocolbuffers/protobuf/releases)
1. `protoc -I=C:\Git\calls --python_out=src calls.proto`
1. `protoc -I=C:\Git\calls --java_out=kotlin --kotlin_out=kotlin calls.proto`
1. `python .\src\call_log.py .\input\history_simple.xml .\calls.png`

## To do

- hash number to use as colour, if one is specified in the config file
- outline the call with colour info indicating call type enum
- write year number for first month rendered and every january.
- re-export XML file from oneplus 5, also export from pixel and combine them.
