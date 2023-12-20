import aiohttp
import asyncio
import json


class WebScraper():
    def __init__(self, urls_list_file):
        with open(urls_list_file, 'r') as file:
            self._urls_list = [row.strip() for row in file]
    
    async def __aenter__(self):
        print('Entering the context manager\n')
        self._session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc, tb):
        print('Exiting the context manager')
        await self._session.close()
    
    async def takeJsonFromWebPage(self, url):
        async with self._session.get(url) as response:
            return await response.text()
    
    async def scrape(self):
        task_list = []
        for url in self._urls_list:
            task_list.append(self.takeJsonFromWebPage(url))
        for res in await asyncio.gather(*task_list):
            print(f'{res[:200]}\n\n')
            

async def main():
    async with WebScraper("urls_list.txt") as manager:
        await manager.scrape()
        

asyncio.run(main())