import sys

def defang_url(url):
    first_period_index = url.find('.')
    if first_period_index != -1:
        url = url[:first_period_index] + '[.' + url[first_period_index + 1:]

        second_period_index = url.find('.', first_period_index + 2)
        if second_period_index != -1:
            url = url[:second_period_index] + '.]' + url[second_period_index + 1:]

    return url

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    normal_url = sys.argv[1]
    defanged_url = defang_url(normal_url)
    print("DEFANGED URL:", defanged_url)
