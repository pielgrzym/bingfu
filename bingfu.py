#!/usr/bin/python2
import pybing, argparse

parser = argparse.ArgumentParser(prog="bingfu",
        description="List domains pointing to given ips")
parser.add_argument('ip', metavar='xxx.xxx.xxx.xxx', type=str, help="IP to check")

if __name__ == '__main__':
    with open(".apikey") as keyfile:
        API_KEY = keyfile.readline().strip()
    assert API_KEY not in [None, ""]
    args = parser.parse_args()
    bing = pybing.Bing(API_KEY)
    ip_addr = args.ip
    bing_response = bing.search_web("ip:%s" % ip_addr)
    results = set()
    try:
        search_results = bing_response['SearchResponse']['Web']['Results']
    except KeyError:
        print "No results"
        exit(1)
    if len(search_results) == 0:
        print "No results"
        exit(1)

    for r in search_results:
        results.add(r['Url'])

    for r in results:
        print r
