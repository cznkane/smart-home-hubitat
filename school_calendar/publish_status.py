"""Produce validated, date-stamped school status JSON; never write to WebCoRE."""
import argparse
import json
from datetime import datetime
from pathlib import Path
from school_calendar.calendar import status_pair
from school_calendar.intake import validate_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('calendar', type=Path)
    args = parser.parse_args()
    validate_file(args.calendar)
    result = status_pair(args.calendar, datetime.now().astimezone())
    print(json.dumps(result, sort_keys=True))

if __name__ == '__main__':
    main()
