import aiohttp, datetime, json


class WCLException(Exception):
    def __init__(self, details):
        self.details = details


class WCL:
    def __init__(self, client_id, client_secret):
        self.session = aiohttp.ClientSession()
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://vanilla.warcraftlogs.com/api/v2/client'
        self.expires_at = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            print(exc_type, exc_value, exc_tb, sep='\n')

        await self.session.close()

    async def authenticate(self):
        url = 'https://www.warcraftlogs.com/oauth/token'
        auth = aiohttp.BasicAuth(self.client_id, self.client_secret)
        async with self.session.post(url, data={'grant_type': 'client_credentials'}, auth=auth) as resp:
            data = await resp.json()

            self.session._default_headers['Authorization'] = f"Bearer {data['access_token']}"
            self.expires_at = datetime.datetime.now() + datetime.timedelta(seconds=data['expires_in'])

    async def query(self, query, vars):
        if self.expires_at is None or self.expires_at <= datetime.datetime.now():
            await self.authenticate()

        async with self.session.post(self.base_url, json={'query': query, 'variables': vars}) as resp:
            data = await resp.json()

            if 'error' in data:
                raise WCLException(data)

            return data

    async def characterInfo(self, name, serverSlug, serverRegion, role, zoneID):
        query = '''
        query($name: String, $serverSlug: String, $serverRegion: String, $role: RoleType!, $zoneID: Int) {
            characterData {
                character(name: $name, serverSlug: $serverSlug, serverRegion: $serverRegion) {
                    name
                    zoneRankings(role: $role, zoneID: $zoneID)
                }
            }
        }
        '''

        return await self.query(query, {'name': name, 'serverSlug': serverSlug, 'serverRegion': serverRegion, 'role': role, 'zoneID': zoneID})

    async def allCharacters(self, serverSlug, serverRegion, zoneID, page=1, limit=100):
        query = '''
        query($serverSlug: String, $serverRegion: String, $zoneID: Int, $page: Int, $limit: Int) {
            worldData {
                server(region: $serverRegion, slug: $serverSlug) {
                    name
                    characters(page: $page, limit: $limit) {
                        data {
                            name
                            zoneRankings(role: Any, zoneID: $zoneID)
                        }
                        from
                        to
                        has_more_pages
                    }
                }
            }
        }
        '''

        return await self.query(query, {'serverSlug': serverSlug, 'serverRegion': serverRegion, 'zoneID': zoneID, 'page': page, 'limit': limit})