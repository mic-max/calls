# Python
import argparse
import collections
from datetime import datetime, timedelta
import enum
import xml.etree.ElementTree as ET

# Pip
from PIL import Image, ImageDraw

class LogType(enum.Enum):
	Inc = 1
	Out = 2
	Miss = 3
	Rej = 5

type_colours = {
	LogType.Inc: (46, 204, 113, 255),
	LogType.Out: (52, 152, 219, 255),
	LogType.Miss: (243, 156, 18, 255),
	LogType.Rej: (231, 76, 60, 255)
}

NDC = (155, 89, 182, 255)
DW = 40
MH = 0.5
HH = MH * 60
SH = 4
BG = (44, 62, 80, 255)
GRID = (22, 31, 40, 255)

def parse_xml(xml_file):
	root = ET.parse(xml_file).getroot()
	result = []

	for child in root:
		if child[0].text is None:
			continue
		result.append({
			'number': child[0].text,
			'datetime': datetime.fromtimestamp(int(child[1].text) / 1000),
			'duration': timedelta(0, int(child[2].text)),
			'type': LogType(int(child[3].text)),
		})

	return result

def strfdelta(tdelta, fmt):
	d = {"days": tdelta.days}
	d["hours"], rem = divmod(tdelta.seconds, 3600)
	d["minutes"], d["seconds"] = divmod(rem, 60)
	return fmt.format(**d)

def draw_line(draw, x, y1, y2, colour):
	draw.rectangle((x, y1, x + DW, y2), fill=colour)

def main(args):
	number = args.number
	data = parse_xml(args.xml_file)

	# Create a chronological order calls logs from the given number
	calls = [x for x in data if number in x['number']]
	calls.sort(key=lambda x: x['datetime'])

	# Add 1 day of padding to start and stop date range
	min_date = calls[0]['datetime'] - timedelta(1)
	max_date = calls[-1]['datetime'] + timedelta(2)

	image_width = (max_date - min_date).days * DW
	image_height = int(24 * 60 * MH)

	img = Image.new('RGBA', (image_width, image_height), BG)
	draw = ImageDraw.Draw(img)

	# Horizontal lines
	for i in range(24):
		draw.text((4, i * HH + 4), f'{i}:00')
		draw.line((0, i * HH, image_width, i * HH), GRID)

	for call in sorted(calls, key=lambda x: x.get('duration')):
		dt_start = call['datetime']
		dt_end = dt_start + call['duration']
		colour = type_colours[call['type']]

		minute_start = dt_start.hour * 60 + dt_start.minute
		minute_end = dt_end.hour * 60 + dt_end.minute

		# Make all call events at least 2 minutes
		if minute_end == minute_start:
			minute_end += SH

		y_start = int(minute_start * MH)
		y_end = int(minute_end * MH)

		x = (dt_start - min_date).days * DW

		# This means the call went past midnight
		if minute_end < minute_start:
			# Draw line indicating the call extended to the next day
			draw_line(draw, x, y_start, image_height, colour)
			draw_line(draw, x + DW, 0, y_end, colour)
			draw_line(draw, x, image_height - SH, image_height, NDC)
			draw_line(draw, x + DW, 0, SH, NDC)
		else:
			draw_line(draw, x, y_start, y_end, colour)

	# Vertical lines
	last_month = (min_date - timedelta(31)).strftime('%b')
	for i in range((max_date - min_date).days):
		# Don't print month overlapping the time in the first column
		if i == 0: continue
		day = (min_date + timedelta(i))
		month = day.strftime('%b')

		draw.line((i * DW, 0, i * DW, image_height), GRID)
		if month != last_month:
			draw.text(((SH + i * DW, image_height - 28)), month)
		draw.text((SH + i * DW, image_height - 14), day.strftime('%d'))
		last_month = month

	# Colour Legend
	types = [x['type'] for x in calls]
	frequency = dict(collections.Counter(types))
	LEGW = 60
	for i, t in enumerate(LogType):
		draw.rectangle((DW + i * LEGW + SH, SH, DW + (i + 1) * LEGW - SH, 16), fill=type_colours[t])
		draw.text((DW + i * LEGW + 2 * SH, SH), f'{t.name}: {frequency[t]}')

	# Total Duration
	durations = [x['duration'] for x in calls]
	total_duration = timedelta(0, sum([x.seconds for x in durations]))
	total_text = strfdelta(total_duration, '{days} days {hours}:{minutes}:{seconds}')
	draw.text((SH * 2 + DW, HH + 4), total_text)

	img.save(args.image_file)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Create image from phone logs XML')
	parser.add_argument('number', type=str)
	parser.add_argument('xml_file', type=str)
	parser.add_argument('image_file', type=str)
	args = parser.parse_args()
	main(args)
