#!/usr/bin/env python3
import requests
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--translate", action="store_true")
    parser.add_argument("--index", action="store_true")
    args = parser.parse_args()

    url = "http://localhost:8771/api/trend/crawl-latest"
    payload = {
        "limit": args.limit,
        "translate": args.translate,
        "summarize": True,
        "index": args.index
    }
    
    print(f"Running crawl-latest with limit {args.limit}...")
    res = requests.post(url, json=payload)
    if res.ok:
        print(res.json())
    else:
        print(f"Error: {res.text}")

if __name__ == "__main__":
    main()
