import requests


def main():
    r = requests.get("https://www.bilibili.com/video/BV1kK4y1Y7Zq?from=articleDetail")
    print(r.text)
    

if __name__ == '__main__':
    main()