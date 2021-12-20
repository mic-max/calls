# Python
from argparse import ArgumentParser, FileType
from collections import Counter, OrderedDict
from datetime import timedelta

# Pip
from PIL import Image, ImageDraw

# Local
from config import Config
from history_parser import HistoryParser


def should_include(call):
    # Within the configured time window
    if config.start != None and call.end < config.start:
        return False

    if config.end != None and call.start > config.end:
        return False

    # An empty whitelist / blacklist should include all calls
    if (config.show is None or not config.numbers):
        return True

    return (call.number in list(config.numbers.keys())) == config.show


def draw_call_block(x, y1, y2, fill, side, top, bottom):
    dw = config.day_width
    draw.rectangle((x, y1, x + dw, y2), fill)
    if side is not None:
        draw.line((x + 1, y1, x + 1, y2), side)
        draw.line((x + dw - 1, y1, x + dw - 1, y2), side)
    if top is not None:
        draw.line((x, y1, x + dw - 1, y1), top)
    if bottom is not None:
        draw.line((x, y2, x + dw - 1, y2), bottom)


def draw_text(x, y, text):
    draw.text((x, y), text, config.colour_text)


def call_durations_by_number(calls):
    result = {}
    for call in calls:
        if call.number not in result:
            result[call.number] = timedelta(0)
        result[call.number] += call.duration
    return OrderedDict(sorted(result.items(), key=lambda kv: kv[1], reverse=True))


def render_image(calls):
    # Add 2 days of padding to the date range
    min_date = min([x.start for x in calls]) - timedelta(1)
    max_date = max([x.end for x in calls]) + timedelta(2)

    NDC = config.colour_rollover
    dw = config.day_width
    width = (max_date - min_date).days * dw
    height = 60 * 24  # 1 vertical pixel per minute

    image = Image.new('RGB', (width, height), config.colour_background)
    global draw
    draw = ImageDraw.Draw(image)

    # Horizontal Lines + Hours
    for i in range(24):
        draw.line((0, i * 60, width, i * 60), config.colour_grid)
        draw_text(2, i * 60, f'{i}:00')

    # Sorted in descending order by duration
    # Note: This will help short calls from being covered, e.g. missed, rejected
    for call in sorted(calls, key=lambda x: x.duration, reverse=True):
        fill = config.types[call.call_type]
        side = config.numbers[call.number] if config.numbers and call.number in config.numbers else config.colour_default

        minute_start = call.start.hour * 60 + call.start.minute
        minute_end = call.end.hour * 60 + call.end.minute

        y1 = int(minute_start)
        y2 = int(minute_end)
        x = (call.start - min_date).days * dw

        past_midnight = call.start.day != call.end.day
        y2_real = height if past_midnight else y2
        bottom = NDC if past_midnight else None
        draw_call_block(x, y1, y2_real, fill, side, None, bottom)
        if past_midnight:
            bottom = config.colour_expired if call.duration >= config.max_call_length else None
            draw_call_block(x + dw, 0, y2, fill, side, NDC, bottom)

    # Vertical Lines + Days
    last_time = None
    cur_time = min_date
    i = 0
    while cur_time <= max_date:
        draw.line((i * dw, 0, i * dw, height), config.colour_grid)
        if i == 0 or cur_time.month != last_time.month:
            draw_text(2 + i * dw, height - 22, cur_time.strftime('%b'))
        draw_text(2 + i * dw, height - 12, cur_time.strftime('%d'))

        i += 1
        last_time = cur_time
        cur_time += timedelta(days=1)

    # Colour Legend
    frequency = dict(Counter([x.call_type for x in calls]))
    for i, (c, n) in enumerate(frequency.items()):
        lw = config.legend_width
        start = (i * 2 + 2) * dw - (lw / 2)
        draw.rectangle((start, 2, start + lw, 12), config.types[c])
        draw_text(start + 1, 1, f'{c.name[:3]}:{n}')

    # Total Duration
    total_duration = sum([x.duration for x in calls], timedelta())
    draw_text(2 + config.day_width, 60, str(total_duration))

    return image


def main(args):
    # Load Config
    global config
    config = Config(args.cfgfile)

    # Parse Call History File
    history_parser = HistoryParser(args.infile)
    calls = history_parser.parse()
    print(f'Found Calls: {len(calls)}')

    # Filter Call History
    calls = list(filter(lambda x: should_include(x), calls))
    print(f'Calls After Filtering: {len(calls)}')
    if not calls:
        return

    # Print Statistics
    durations = call_durations_by_number(calls)
    for i, (number, duration) in enumerate(durations.items()):
        print(f'{i}. {number} = {duration}')
        if i >= config.top_callers:
            break

    # Save Rendered Image to File
    image = render_image(calls)
    image.save(args.outfile)
    print(f'Generated Image: {args.outfile.name}')


if __name__ == '__main__':
    parser = ArgumentParser(description='Visualization of Call History')
    parser.add_argument('cfgfile', type=FileType('r'))
    parser.add_argument('infile', type=FileType('rb'))
    parser.add_argument('outfile', type=FileType('wb'))
    main(parser.parse_args())
