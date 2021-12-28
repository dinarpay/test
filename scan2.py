#!/usr/bin/env python3
# encoding:utf8
import sys
import argparse
from socket import gethostbyname
from netaddr import IPNetwork
import requests
from time import time
import asyncio
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

__author__ = "nul1"
__update__ = "2021/07/02"
__version__ = "v2.2.0"
"""
??? HTTP ? 
?????? ???? ????? ????? ??? ????? ? ??????? ??
? ??????? ???????? ??????? ???????.
"""

Ports_web = [80, 443]
Ports_other = [21, 22]

ScanedURL = []
COUNT = 0
TIMEOUT_HTTP = 15
TIMEOUT_SOCK = 3
PATH = ''

user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"

purp = ''
blue = ''
red = ''
yellow = ''
green = ''
end = ''


def save(save_file, content):
    with open(save_file, 'a') as f:
        try:
            f.writelines(content + '\n')
        except Exception as e:
            pass

def tag(info):
    return "||" + info + "||"

# ????? ??? ?????? ??? IP
def url_to_ip(url):
    domain = url.split('/')[0] if '://' not in url else url.split('//')[1].split('/')[0]
    domain = domain.split(':')[0] if ':' in domain else domain  # fix domain

    try:
        ip = gethostbyname(domain)
        return ip
    except Exception as e:
        return ""

def get_info(url, keyword):
    try:
        r = requests.get(url, headers={'UserAgent': user_agent}, timeout=TIMEOUT_HTTP, verify=False,allow_redirects=True)
        soup = BeautifulSoup(r.content, "html.parser")
        # ????? ??????? ??? HTTP
        info_code = tag(red + str(r.status_code) + end)
        info_title = tag(blue + soup.title.string.replace('\n', '').replace('\r', '').replace('\t','') + end) if soup.title else tag("")
        info_len = tag(purp + str(len(r.content)) + end)
        if 'Server' in r.headers:
            info_server = " [" + yellow + r.headers['Server']
            info_server += " " + r.headers['X-Powered-By'] + end + "]" if 'X-Powered-By' in r.headers else "]"
        else:
            info_server = tag("")
        result = info_code + info_title + info_server + info_len

        # ????? HTTP ? ?????? ??????? ????????
        key = tag(red + "Keyword!!!" + end) if keyword and keyword in r.text else ""
        
        return result + key
    except Exception as e:
        # print(e)
        return tag(green + "open" + end)

async def connet(host, sem, keyword, ip):
    """
    ?????? ????? ??? ?????? ??? ???????? ?????? ?? ??? ??? ?????? ??????? ? ?? ??? ? ?? ?? ?????? ????????? ??? ???? ?????
    :param host thread keyword ip
    :param sem: ????? ???????
    :param keyword: ?????? ??????? ???????? ?????? ?????
    :param ip: ???? ??? IP ????? ??????? ????????
    :return info
    """
    global COUNT
    async with sem:
        # ???? ?????? IP ?????
        h_ip = host.split(':')[0]

        port = host.split(':')[1]

        host = h_ip
        output_ip = url_to_ip(host) if ip else ""
        fut = asyncio.open_connection(host=host, port=port)
        try:
            reader, writer = await asyncio.wait_for(fut, timeout=TIMEOUT_SOCK)
            if writer:
                # ?????? ?????? ??? ??????? ??? ?????
                if port in Ports_other:
                    url = str(host) + ":" + str(port)
                    info = tag(green + "open" + end)

                # ??????? get_info () ?????? ??? ???? ?????
                else:
                    protocol = "http" if int(port) not in [443] else "https"
                    url = "{0}://{1}:{2}{3}".format(protocol, host, port, PATH)
                    info = get_info(url, keyword)
                if(url not in ScanedURL):
                    print("%-28s %-28s %-30s\n" % (url, info, output_ip))
                    ScanedURL.append(url)
                COUNT += 1

        except Exception as e:
            # print(e)
            pass

async def scan(mode, x, t, keyword, myip):
    time_start = time()

    # ????? ????? ???? ?? ??? ?????????
    sem = asyncio.Semaphore(t)
    tasks = []

    # ??? IP:10.1.1.1/24
    if mode == 'ips':
        ips = [str(ip) for ip in IPNetwork(x)]
        for host in ips:
            tasks.append(asyncio.create_task(connet(host, sem, keyword, myip)))

    # ??? ?????: ????? ????? ???? IP ???? ??????
    if mode == 'file':
        with open(x, 'r') as f:
            for line in f.readlines():
                line = line.rstrip()
                if len(line) != 0:
                    host = line if '://' not in line else line.split('//')[1]
                    tasks.append(asyncio.create_task(connet(host, sem, keyword, myip)))

    # print(tasks)
    await asyncio.wait(tasks)


def main():
    global Ports, PATH

    parser = argparse.ArgumentParser(usage='\ncscan -i 192.168.0.1/24 -t 100\ncscan -f url.txt -t 100\ncscan -i 192.168.0.1/24 -t 100 -q -port 80,8080 -path /actuator',description="CScan Tookit V2",)

    basic = parser.add_argument_group('Basic')
    basic.add_argument("-i", dest="ips", help="Use ip segment (192.168.0.1/24)")
    basic.add_argument("-f", dest="file",help="Use ip or domain file")
    basic.add_argument("-t", dest="threads", type=int, default=200,help="Set thread (default 200)")
   #basic.add_argument("-o", dest="output",help="Specify output file default output.txt")
    basic.add_argument("-q", dest="silent", action="store_true",help="Silent mode")

    god = parser.add_argument_group('God')
    god.add_argument("-port", dest="port", help="Specify port")
    god.add_argument("-path", dest="path", help="Request path (example '/phpinfo.php')")
    god.add_argument("-key", dest="keyword", help="Specify keyword")
    god.add_argument("-web", dest="web", action="store_true", help="Only scan web ports")
    god.add_argument("-ip", dest="ip", action="store_true", help="Output target ip")

    args = parser.parse_args()

    # ????? ??? ????? ??????? -web
    Ports = Ports_web if args.web else Ports_web + Ports_other

    # ????? ????
    if args.port:
        Ports = args.port.split(',')
    
    if args.ips is None and args.file is None:
        sys.exit(0)
    if args.path:
        PATH = args.path
    if args.ips:
        try:
            asyncio.run(scan('ips', args.ips, args.threads, args.keyword, args.ip))
        except KeyboardInterrupt:
            t=0

    if args.file:
        try:
            asyncio.run(scan('file', args.file, args.threads, args.keyword, args.ip))
        except KeyboardInterrupt:
            t=0

if __name__ == '__main__':
    main()