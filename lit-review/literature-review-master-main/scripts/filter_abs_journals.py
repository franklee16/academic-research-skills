#!/usr/bin/env python3
"""Filter the embedded ABS AJG 2024 database.

Examples
python scripts/filter_abs_journals.py --rating '4*' --field MKT
python scripts/filter_abs_journals.py --query retail --min-rating 3
"""
import argparse
import csv
from pathlib import Path

ORDER = {'4*': 0, '4': 1, '3': 2}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default=str(Path(__file__).resolve().parents[1] / 'database' / 'abs_2024_3_4_4star_database.csv'))
    parser.add_argument('--rating', action='append', help='Filter by exact rating. Can be repeated.')
    parser.add_argument('--field', action='append', help='Filter by exact field code. Can be repeated.')
    parser.add_argument('--query', help='Case-insensitive substring search in title or field.')
    parser.add_argument('--limit', type=int, default=200)
    args = parser.parse_args()

    rows = []
    with open(args.db, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if args.rating and row['ajg_2024'] not in args.rating:
                continue
            if args.field and row['field'] not in args.field:
                continue
            if args.query:
                q = args.query.lower()
                if q not in row['title'].lower() and q not in row['field'].lower():
                    continue
            rows.append(row)
    rows.sort(key=lambda r: (ORDER.get(r['ajg_2024'], 99), r['field'], r['title']))
    for row in rows[:args.limit]:
        print(f"{row['ajg_2024']}\t{row['field']}\t{row['title']}")
    if len(rows) > args.limit:
        print(f"... {len(rows) - args.limit} more")

if __name__ == '__main__':
    main()
