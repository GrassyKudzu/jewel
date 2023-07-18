import argparse
import pyperclip

def defang_url(url):
    defanged_url = url.replace(":", "x").replace(".", "[.]")
    return "h" + defanged_url

def get_input_url():
    parser = argparse.ArgumentParser(description="DEFANG a URL or read from the clipboard.")
    parser.add_argument("url", nargs="?", help="URL to DEFANG (optional, will use clipboard if not provided)")
    args = parser.parse_args()

    if args.url:
        return args.url.strip()
    else:
        clipboard_content = pyperclip.paste()
        if clipboard_content:
            return clipboard_content.strip()
        else:
            print("No URL provided and clipboard is empty.")
            exit(1)

if __name__ == "__main__":
    normal_url = get_input_url()
    defanged_url = defang_url(normal_url)
    print("DEFANGED URL:", defanged_url)
