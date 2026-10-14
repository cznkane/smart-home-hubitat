"""Validate a proposed academic calendar submission."""
import argparse
from school_calendar.intake import validate_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    data = validate_file(args.path)
    print('VALID:', data['first_day'], 'to', data['last_day'])

if __name__ == '__main__':
    main()

