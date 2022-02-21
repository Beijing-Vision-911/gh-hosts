import asyncio
import os
import re
import sys

import aiohttp
from ping3 import ping

single_ip_text = re.compile(
    r'<th>IP Addresse?s?</th><td><ul class="comma-separated"><li>(.+?)</li>'
)
multiple_ip_text1 = re.compile(r"addresses:<ul>(.+?)</ul>")
multiple_ip_text2 = re.compile(r"<strong>(.+?)</strong>")


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


async def lowest_delay_ip(ip):
    lowest_delay = ping(ip)
    if type(lowest_delay) == float:
        return lowest_delay
    return 99


async def url_lookup_transform(session, url):
    async with session.get(url) as response:
        r = await response.text()
        ip = re.findall(single_ip_text, str(r))
        url = url.split("/")[-1]
        if ip:
            return {url: ip[0]}
        # if multi ip address is acquared, ping each ip and select ip with best latency.
        try:
            html = re.findall(multiple_ip_text1, str(r))[0]
            ips = re.findall(multiple_ip_text2, html)
            lowest_delay = await asyncio.gather(*[lowest_delay_ip(ip) for ip in ips])
            ip = ips[lowest_delay.index(min(lowest_delay))]
            return {url: ip}
        except:
            return


async def ip_lookup():
    dist = {}
    async with aiohttp.ClientSession() as session:
        r = await asyncio.gather(
            *[
                url_lookup_transform(session, f"https://ipaddress.com/website/{url}")
                for url in domains
            ]
        )
    for vlaue in r:
        dist.update(vlaue)

    hosts = ""

    for domain, ip in dist.items():
        hosts += f"{ip} {domain}\n"

    with open("/etc/hosts", "w") as host_file:
        host_file.write(hosts)

    print("Hosts file updated")
    os.system("systemctl restart nscd.service")
    print("Name service cache daemon is restarted")


def main():
    asyncio.run(ip_lookup())


if __name__ == "__main__":
    sys.exit(main())
