import sys

def defang_url(url):
    first_period_index = url.find('.')
    if first_period_index != -1:
        url = url[:first_period_index] + '[.' + url[first_period_index + 1:]

        second_period_index = url.find('.', first_period_index + 2)
        if second_period_index != -1:
            url = url[:second_period_index] + '.]' + url[second_period_index + 1:]

    return url

def modify_protocol(url):
    if url.startswith("http://"):
        url = url.replace("http://", "hxxp://", 1)
    elif url.startswith("https://"):
        url = url.replace("https://", "hxxps://", 1)
    elif url.startswith("ftp://"):
        url = url.replace("ftp://", "fxp://", 1)
    elif url.startswith("file://"):
        url = url.replace("file://", "fxxe://", 1)

    return url

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    normal_url = sys.argv[1]
    safe_url = modify_protocol(normal_url)
    defanged_url = defang_url(safe_url)
    print("SAFE DEFANGED URL:", defanged_url)
