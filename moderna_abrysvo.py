#!/usr/bin/env python3
"""Fetch pharmacy data from Moderna and Abrysvo websites.

This script is a simple example using ``requests`` and ``BeautifulSoup``.
Check each website's Terms of Service before scraping and ensure your usage
complies with those terms.
"""

import argparse
import requests
from bs4 import BeautifulSoup

MODERNA_URL = "https://www.modernatx.com/vaccine-locator"
ABRYSVO_URL = "https://www.abrysvo.com/locator"


def fetch_moderna_pharmacies():
    """Return a list of pharmacy names from Moderna's RSV locator."""
    response = requests.get(MODERNA_URL, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    pharmacies = [tag.get_text(strip=True) for tag in soup.select(".pharmacy-name")]
    return pharmacies


def fetch_abrysvo_pharmacies():
    """Return a list of pharmacy names from Abrysvo's RSV locator."""
    response = requests.get(ABRYSVO_URL, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    pharmacies = [tag.get_text(strip=True) for tag in soup.select(".pharmacy-name")]
    return pharmacies


def main():
    parser = argparse.ArgumentParser(description="Count pharmacies offering RSV products.")
    parser.add_argument(
        "--source",
        choices=["moderna", "abrysvo", "all"],
        default="all",
        help="Which source to query (default: all)",
    )
    args = parser.parse_args()

    total = 0
    if args.source in ("moderna", "all"):
        try:
            mod = fetch_moderna_pharmacies()
            print(f"Found {len(mod)} Moderna pharmacies")
            total += len(mod)
        except Exception as exc:
            print(f"Failed to fetch Moderna data: {exc}")

    if args.source in ("abrysvo", "all"):
        try:
            abr = fetch_abrysvo_pharmacies()
            print(f"Found {len(abr)} Abrysvo pharmacies")
            total += len(abr)
        except Exception as exc:
            print(f"Failed to fetch Abrysvo data: {exc}")

    print(f"Total RSV pharmacies: {total}")


if __name__ == "__main__":
    main()
