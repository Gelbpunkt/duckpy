import re
import secrets

import aiohttp

ddg_url = "https://duckduckgo.com/html"

user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SM-S767VL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36",
]


class Client:
    def __init__(self, session: aiohttp.ClientSession = None):
        self.session = session or aiohttp.ClientSession()

    async def search(self, query, exact_match=False):
        if exact_match:
            query = f'"{query}"'
        headers = {"User-Agent": secrets.choice(user_agents)}

        async with self.session.get(ddg_url, params={"q": query}, headers=headers) as r:
            data = await r.text()

        return parse_page(data)

    async def close(self):
        await self.session.close()

def strip_html(text):
    return re.sub("<[^<]+?>", "", text)


def parse_page(html):
    regex1 = r'<a rel="nofollow" class="result__a" href="(.*)">(.*)</a>'
    results = []
    for match in re.finditer(regex1, html, re.MULTILINE):
        link = match.group(1)
        text = match.group(2)
        results.append({"link": link, "title": strip_html(text)})
    regex2 = r"<img class=\"result__icon__img\" width=\"16\" height=\"16\" alt=\"\"\s+src=\"(.*)\" name=\"(.*)\" />"
    for idx, match in enumerate(re.finditer(regex2, html, re.MULTILINE)):
        link = match.group(1)
        results[idx]["image"] = link
    regex3 = r"<a class=\"result__snippet\" href=\"(.*)\">(.*)</a>"
    for idx, match in enumerate(re.finditer(regex3, html, re.MULTILINE)):
        summary = match.group(2)
        results[idx]["summary"] = strip_html(summary)
    return results
