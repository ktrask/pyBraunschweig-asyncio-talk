from sanic import Sanic
from sanic.response import json
import aiopg
from threading import get_ident

app = Sanic(__name__)

@app.route('/')
async def test(request):
    return json({
        'hello': 'world',
        'thread': get_ident(),
        })

pool = None

async def runQuery(query,params=None):
    global pool
    if not pool:
        pool = await aiopg.create_pool(
                "dbname=dbuser user=dbuser password=YeiCoo0dujih host=127.0.0.1 port=15432",
                maxsize=3,
                )
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query,params)
            return await cur.fetchall()
    return None



@app.route('/rundb')
async def dbtest(request):
    await runQuery("""SELECT pg_sleep(%(sleepTime)s);""", {'sleepTime':5})
    return json({
        'state': 'done',
        'thread': get_ident(),
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8765, debug=True)
