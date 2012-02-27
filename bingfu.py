#!/usr/bin/python2
import pybing, argparse

parser = argparse.ArgumentParser(prog="bingfu",
        description="List domains pointing to given ips")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', '--ip', metavar='xxx.xxx.xxx.xxx', type=str, help="IP to check")
group.add_argument('-f', '--file', metavar='filename', type=file, help="File with ips")

def get_bing_shite(ip_addr):
    bing_response = bing.search_web("ip:%s" % ip_addr)
    results = set()
    try:
        search_results = bing_response['SearchResponse']['Web']['Results']
    except KeyError:
        return []
    if len(search_results) == 0:
        return []

    for r in search_results:
        results.add(r['Url'])
    return results


if __name__ == '__main__':
    with open(".apikey") as keyfile:
        API_KEY = keyfile.readline().strip()
    assert API_KEY not in [None, ""]
    args = parser.parse_args()
    bing = pybing.Bing(API_KEY)
    if args.ip:
        results = get_bing_shite(args.ip)
    if args.file:
        results = []
        for ip_addr in args.file.readlines():
            ip_addr = ip_addr.strip()
            results.append("\n# %s" % ip_addr)
            results += get_bing_shite(ip_addr)

    for r in results:
        print r
