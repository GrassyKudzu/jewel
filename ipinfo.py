import requests
import json
import argparse
import curses

VIRUSTOTAL_API_KEY = "YOUR_VIRUSTOTAL_API_KEY"
SHODAN_API_KEY = "YOUR_SHODAN_API_KEY"

def get_virustotal_info(query):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{query}"
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return json.dumps(result, indent=4)
    else:
        return f"VirusTotal API Error: {response.status_code}"

def get_shodan_info(query):
    url = f"https://api.shodan.io/shodan/host/{query}?key={SHODAN_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        return json.dumps(result, indent=4)
    else:
        return f"Shodan API Error: {response.status_code}"

def display_tui(virustotal_result, shodan_result):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    max_rows, max_cols = stdscr.getmaxyx()

    stdscr.addstr(0, 0, "=== VirusTotal Results ===")

    # Split the VirusTotal result into smaller chunks to fit the window
    virus_rows = virustotal_result.split("\n")
    for i, row in enumerate(virus_rows):
        if i < max_rows - 1:
            stdscr.addstr(i + 1, 0, row[:max_cols // 2 - 1])
        else:
            break
    
    stdscr.addstr(0, max_cols // 2, "=== Shodan Results ===")

    # Split the Shodan result into smaller chunks to fit the window
    shodan_rows = shodan_result.split("\n")
    for i, row in enumerate(shodan_rows):
        if i < max_rows - 1:
            stdscr.addstr(i + 1, max_cols // 2, row[:max_cols // 2 - 1])
        else:
            break

    stdscr.refresh()
    stdscr.getch()

    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.endwin()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IP/DNS information lookup")
    parser.add_argument("query", help="IP address or domain name to lookup")
    args = parser.parse_args()

    virustotal_result = get_virustotal_info(args.query)
    shodan_result = get_shodan_info(args.query)

    display_tui(virustotal_result, shodan_result)
