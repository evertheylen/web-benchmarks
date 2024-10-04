import subprocess
import time
from datetime import datetime
from pathlib import Path


root = Path(__file__).parent


env = {
    'PG_VERSION': '16.3',
    'PG_USER': 'postgres',
    'PG_PASS': 'bench',
    'PG_PORT': '55432',
    'PG_DB': 'postgres',
    'NODE_ENV': 'production',
}


class Server:
    def __init__(self, id, *, script: Path, threads = 1, extra_env = None):
        self.id = id
        self.script = script
        self.threads = threads
        self.extra_env = {'SERVER_THREADS': str(threads), **(extra_env or {})}

class NodeServer(Server):
    @property
    def name(self):
        return f'node-{self.id}'

    def run(self):
        return subprocess.Popen(['node', str(self.script)], env={**env, **self.extra_env})


# class Pm2NodeServer(NodeServer):
#     def run(self):
#         return subprocess.Popen(['node', str(script)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)


class BunServer(Server):
    @property
    def name(self):
        return f'bun-{self.id}'

    def run(self):
        return subprocess.Popen(['bun', 'run', str(self.script)], env={**env, **self.extra_env})



servers = [
    # NodeServer('express', root / 'nodejs' / 'cluster-express.js'),
    # NodeServer('fastify', root / 'nodejs' / 'cluster-fastify.js'),
    # NodeServer('hapi', root / 'nodejs' / 'cluster-hapi.js'),
    NodeServer('1', script = root / 'nodejs' / 'cluster-http.js', threads=1),
    NodeServer('2', script = root / 'nodejs' / 'cluster-http.js', threads=2),
    NodeServer('4', script = root / 'nodejs' / 'cluster-http.js', threads=4),
    NodeServer('8', script = root / 'nodejs' / 'cluster-http.js', threads=8),
    NodeServer('12', script = root / 'nodejs' / 'cluster-http.js', threads=12),
    NodeServer('16', script = root / 'nodejs' / 'cluster-http.js', threads=16),
    NodeServer('20', script = root / 'nodejs' / 'cluster-http.js', threads=20),
    # NodeServer('koa', root / 'nodejs' / 'cluster-koa.js'),
    BunServer('1', script = root / 'bun' / 'bun-single.js', threads=1),
    BunServer('2', script = root / 'bun' / 'bun-multi.js', threads=2),
    BunServer('4', script = root / 'bun' / 'bun-multi.js', threads=4),
    BunServer('8', script = root / 'bun' / 'bun-multi.js', threads=8),
    BunServer('12', script = root / 'bun' / 'bun-multi.js', threads=12),
    BunServer('16', script = root / 'bun' / 'bun-multi.js', threads=16),
    BunServer('20', script = root / 'bun' / 'bun-multi.js', threads=20),
]


def main():
    results = root / 'results_nopg'

    for connections in [50, 100, 200, 400, 600, 800]:
        for server in servers:
            print(f"\n------------------- {connections} - {server.name} -------------------")
            timestamp = datetime.now().isoformat()
            proc = server.run()
            time.sleep(1)

            result_dir = results / str(connections) / server.name
            result_dir.mkdir(parents=True, exist_ok=True)

            result_file = result_dir / f'{timestamp}.csv'
            with open(result_file, 'w') as f:
                # too high -c (e.g. 32 * threads) => makes higher threads actually give slower response times!
                subprocess.run(['hey', '-n', '50000', '-c', str(connections), '-o', 'csv', 'http://127.0.0.1:8000'], stdout=f)

            # Stop the server
            proc.send_signal(subprocess.signal.SIGINT)
            retcode = proc.wait()

if __name__ == '__main__':
    main()
