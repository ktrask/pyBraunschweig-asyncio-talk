from flask import Flask, jsonify
import psycopg2
from psycopg2 import pool as pgpool
from threading import get_ident

app = Flask(__name__)

@app.route('/')
def test():
    return jsonify({
        'hello': 'world',
        'thread': get_ident(),
        })

pool = None

def runQuery(query,params=None):
    global pool
    if not pool:
        pool = pgpool.ThreadedConnectionPool(
                1,
                3,
                "dbname=dbuser user=dbuser password=YeiCoo0dujih host=127.0.0.1 port=15432",
                )
    conn = pool.getconn()
    cur = conn.cursor()
    cur.execute(query,params)
    result = cur.fetchall()
    pool.putconn(conn)
    return result

@app.route('/rundb')
def dbtest():
    runQuery("""SELECT pg_sleep(%(sleepTime)s);""", {'sleepTime':5})
    return jsonify({
        'state': 'done',
        'thread': get_ident(),
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8766, debug=True)
