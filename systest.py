#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser(prog="TreeDoc", description="Create lovely pictures of your project's file tree!", epilog="All rights reserved blah blah blah.")
parser.add_argument("path", default=".")
parser.add_argument("-c", "--count", default=9999)
args = parser.parse_args()
print(args.count)
print(args.path)