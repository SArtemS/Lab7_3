import aiohttp
import asyncio
import asyncpg
import json

WEB_SERVER_URL = "https://rnacentral.org/api/v1/rna/"
DB_CONNECTION_STRING = "postgres://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"


async def requestPublicWebServer():
    async with aiohttp.ClientSession() as session:
        async with session.get(WEB_SERVER_URL) as response:

            httpData = await response.json()
            httpJsonData = json.dumps(httpData, indent=4)

            return httpJsonData


async def requestPublicDB():
    conn = await asyncpg.connect(DB_CONNECTION_STRING)
    first_row = await conn.fetchrow("SELECT upi, taxid, ac FROM xref")
    print(first_row)
    await conn.close()
    return f'\nPart of the first row of the DB is:\n{first_row}'


async def tasksTogether():
    for res in await asyncio.gather(requestPublicWebServer(),
                                    requestPublicDB()):
        print(res)


asyncio.run(tasksTogether())
