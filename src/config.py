# Python
from datetime import timedelta
from struct import unpack

# Pip
from yaml import safe_load

# Local
from call_data import CallType


def colourify(rgb: int):
    return unpack('BBB', rgb.to_bytes(3, 'big'))


class Config:
    def __init__(self, cfgfile):
        config = safe_load(cfgfile)
        cfgfile.close()

        self.types = {CallType[t]: colourify(c) for t, c in config['types'].items()}

        self.colour_background = colourify(config['background'])
        self.colour_grid = colourify(config['grid'])
        self.colour_text = colourify(config['text'])

        self.colour_rollover = colourify(config['rollover'])
        self.colour_expired = colourify(config['expired'])

        self.sh = config['size']['sh']
        self.day_width = config['size']['day-width']
        self.legend_width = config['size']['legend-width']

        self.top_callers = config['top-callers']
        self.max_call_length = timedelta(seconds=config['max-call-length'])
        self.start_hour = config['start-hour']

        self.start = config['start'] if 'start' in config else None
        self.end = config['end'] if 'end' in config else None
        self.show = config['show']
        self.numbers = {n: colourify(c) for n, c in config['numbers'].items()}
