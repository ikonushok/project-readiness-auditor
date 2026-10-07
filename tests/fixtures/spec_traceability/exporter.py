import argparse
import csv
import sys


def normalize(names):
    return [" ".join(name.split()) for name in names if name.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="*")
    args = parser.parse_args()
    writer = csv.writer(sys.stdout)
    for name in normalize(args.names):
        writer.writerow([name])


if __name__ == "__main__":
    main()
