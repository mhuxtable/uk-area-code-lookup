#!/usr/bin/env python3

import argparse
import csv


class AreacodeClashException(Exception):
    pass


class NoMatchException(Exception):
    pass


def load_area_codes(filepath):
    dict = {}
    with open(filepath, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            code, name = row
            if not dict.get(code):
                dict[code] = name
            else:
                raise AreacodeClashException()
    return dict


def lookup(number, areacodes):
    if number[0] == '0':
        number = number[1::]
    for prefix_length in range(len(number), 0, -1):
        prefix = number[:prefix_length:]
        area = areacodes.get(prefix)
        if not area:
            continue
        return ('0{}'.format(prefix), area)
    raise NoMatchException()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Look up area codes from UK telephone numbers'
    )
    parser.add_argument('number',
                        help='A UK telephone number (full/partial) to lookup'
                        )
    parser.add_argument('--areacodes', metavar='CSV',
                        help=('Path to CSV containing area code prefixes. '
                              'Defaults to uk-area-codes.csv if omitted.'),
                        default='uk-area-codes.csv')
    output_format = parser.add_mutually_exclusive_group(required=False)
    output_format.add_argument('--json', action='store_true',
                               help=('Print output in machine-interchangeable '
                                     'JSON format.')
                               )
    output_format.add_argument('--name', action='store_true',
                               help=('Only print the area name if a match is '
                                     'found. Otherwise, print nothing'),
                               )
    args = parser.parse_args()

    areacodes = load_area_codes(args.areacodes)
    try:
        prefix, area = lookup(args.number, areacodes)
    except NoMatchException:
        prefix, area = None, None

    if args.json:
        print({
            'code': prefix,
            'area': area,
        })
    elif args.name:
        if area is not None:
            print(area, end="")
    else:
        print("Prefix {} is the area code for {}.".format(prefix, area))
