import asyncio
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen

from ping3 import ping

pattern = re.compile(
    r'<th>IP Addresse?s?</th><td><ul class="comma-separated"><li>(.+?)</li>'
)
pattern2 = re.compile(r"addresses:<ul>(.+?)</ul>")
pattern3 = re.compile(r"<strong>(.+?)</strong>")


def lowest_delay_ip(ip_lst):
    lst = []
    for i in ip_lst:
        ip = ping(i)
        if isinstance(ip, float):
            lst.append(ip)
    return ip_lst[lst.index(min(lst))]


def url_lookup_transform(url: str):
    return f"https://ipaddress.com/website/{url}"


def ip_lookup(url):
    lookup_url = url_lookup_transform(url)
    req = urlopen(lookup_url).read().decode()
    ip = re.findall(pattern, req)
    if ip:
        return {url: ip[0]}
    # if multi ip address is acquared, ping each ip and select ip with best latency.
    try:
        test = re.findall(pattern2, req)[0]
        ip = re.findall(pattern3, test)
        ips = lowest_delay_ip(ip)
        return {url: ips}
    except:
        print(url)
        return


domains = [
    "collector.github.com",
    "alive.github.com",
    "live.github.com",
    "github.githubassets.com",
    "central.github.com",
    "desktop.githubusercontent.com",
    "assets-cdn.github.com",
    "camo.githubusercontent.com",
    "github.map.fastly.net",
    "github.global.ssl.fastly.net",
    "gist.github.com",
    "github.io",
    "github.com",
    "github.blog",
    "api.github.com",
    "raw.githubusercontent.com",
    "user-images.githubusercontent.com",
    "favicons.githubusercontent.com",
    "avatars5.githubusercontent.com",
    "avatars4.githubusercontent.com",
    "avatars3.githubusercontent.com",
    "avatars2.githubusercontent.com",
    "avatars1.githubusercontent.com",
    "avatars0.githubusercontent.com",
    "avatars.githubusercontent.com",
    "codeload.github.com",
    "github-cloud.s3.amazonaws.com",
    "github-com.s3.amazonaws.com",
    "github-production-release-asset-2e65be.s3.amazonaws.com",
    "github-production-user-asset-6210df.s3.amazonaws.com",
    "github-production-repository-file-5c1aeb.s3.amazonaws.com",
    "githubstatus.com",
    "github.community",
    "github.dev",
    "media.githubusercontent.com",
    "cloud.githubusercontent.com",
    "objects.githubusercontent.com",
]


async def start():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        futures = [loop.run_in_executor(pool, ip_lookup, url) for url in domains]
        reqs = await asyncio.gather(*futures)
    dist = {}
    for s in reqs:
        dist.update(s)

    hosts = ""

    for domain, ip in dist.items():
        hosts += f"{ip} {domain}\n"

    with open("/etc/hosts", "w") as host_file:
        host_file.write(hosts)

    print("Hosts file updated")
    os.system("systemctl restart nscd.service")
    print("Name service cache daemon is restarted")


def main():
    try:
        asyncio.run(start())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())
