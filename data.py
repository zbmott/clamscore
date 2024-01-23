import asyncio, json, pprint, sys

import wcl, settings


async def main(args):
    server_slug = args[0]
    region = args[1]
    starting_page = int(args[2])

    mode = 'w' if starting_page == 1 else 'a'

    with open('ClamScore/data/ChaosBolt.lua', mode, encoding='utf-8') as outfile:
        if starting_page == 1:
            outfile.write("ClamScore['data']['ChaosBolt'] = {\n\n")

        async with wcl.WCL(settings.WCL_CLIENT_ID, settings.WCL_CLIENT_SECRET) as client:
            page = starting_page
            has_more_pages = True
            while has_more_pages:
                try:
                    data = await client.allCharacters(server_slug, region, 2007, page=page, limit=100)
                except wcl.WCLException as wcle:
                    print(f"Error {wcle.status}\n")
                    pprint.pprint(wcle.details)
                    return

                #has_more_pages = data['data']['worldData']['server']['characters']['has_more_pages']
                has_more_pages = False
                for char in data['data']['worldData']['server']['characters']['data']:
                    name = char['name']
                    best = char.get('zoneRankings', {}).get('bestPerformanceAverage', None)
                    median = char.get('zoneRankings', {}).get('medianPerformanceAverage', None)
                    outfile.write(f"[\"{name}\"]={{{format_ranking(best)},{format_ranking(median)}}},\n")

                page += 1

        #outfile.write('\n}\n')


def format_ranking(r):
    if r is None:
        return '"--"'
    return f"{r:.1f}"


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(sys.argv[1:]))
