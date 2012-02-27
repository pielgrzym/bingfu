#!/usr/bin/python2
import pybing, argparse

parser = argparse.ArgumentParser(prog="bingfu",
        description="List domains pointing to given ips")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', '--ip', metavar='xxx.xxx.xxx.xxx', type=str, help="IP to check")
group.add_argument('-f', '--file', metavar='filename', type=file, help="File with ips")
parser.add_argument('-o', '--output', metavar='outfile', type=str, help="Output file")
parser.add_argument('-a', '--append-output', action='store_true', help="Append to output file instead of overwriting")

def get_bing_shite(ip_addr):
    bing_response = bing.search("ip:%s" % ip_addr, extra_params={"web.count":50})
    results = set()
    try:
        search_results = bing_response['SearchResponse']['Web']['Results']
    except KeyError:
        return []
    if len(search_results) == 0:
        return []
    total_count = bing_response['SearchResponse']['Web']['Total']
    for r in search_results:
        results.add(r['Url'])
    if total_count > 50: # fuck default 50 results boundary for fun and profit
        page = 1
        while total_count > 0:
            bing_response = bing.search("ip:%s" % ip_addr,
                    extra_params={"web.count":50, "web.offset":50*page})
            search_results = bing_response['SearchResponse']['Web']['Results']
            for r in search_results:
                results.add(r['Url'])
            page += 1
            total_count -= 50
    return results

if __name__ == '__main__':
    with open(".apikey") as keyfile:
        API_KEY = keyfile.readline().strip()
    assert API_KEY not in [None, ""]
    args = parser.parse_args()
    bing = pybing.Bing(API_KEY)
    if args.ip:
        final_results = get_bing_shite(args.ip)
    if args.file:
        final_results = []
        for ip_address in args.file.readlines():
            ip_address = ip_address.strip()
            final_results.append("\n# %s" % ip_address)
            final_results += get_bing_shite(ip_address)

    results_string = "\n".join(final_results)
    if args.output:
        if args.append_output:
            flag = 'a'
        else:
            flag = 'w'
        with open(args.output, flag) as outfile:
            outfile.write(results_string + "\n")
    else:
        print results_string
