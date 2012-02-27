#!/usr/bin/python2
import pybing, argparse

parser = argparse.ArgumentParser(description="List domains pointing to given ips")
parser.add_argument('ip', metavar='xxx.xxx.xxx.xxx', type=str, help="IP to check")

if __name__ == '__main__':
    with open(".apikey") as keyfile:
        API_KEY = keyfile.readline().strip()
    assert API_KEY not in [None, ""]
    args = parser.parse_args()
    bing = pybing.Bing(API_KEY)
    ip_addr = args.ip
    bing_results = bing.search_web("ip:%s" % ip_addr)
    results = set()
    for r in bing_results['SearchResponse']['Web']['Results']:
        results.add(r['Url'])

    for r in results:
        print r
