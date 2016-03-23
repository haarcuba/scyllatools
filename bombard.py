#!/usr/bin/env python
import cassandra.cluster
import threading
import sys
import argparse
import uuid
import time
import random

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bootstrap', action='store_true', help="setup keyspace and table")
parser.add_argument('threads', type=int, help="number of simultanious sessions")
arguments = parser.parse_args()

cluster = cassandra.cluster.Cluster()
if arguments.bootstrap:
    session = cluster.connect()
    session.execute("DROP KEYSPACE IF EXISTS bombard")
    session.execute("CREATE KEYSPACE bombard WITH REPLICATION = {'class':'SimpleStrategy','replication_factor':1}")
    session.execute('USE bombard')
    session.execute("CREATE TABLE tokens (id uuid PRIMARY KEY, thing uuid)")
    quit()


class Bomber(object):
    count = 0

    def __init__(self, cluster):
        self._session = cluster.connect('bombard')
        self._thread = threading.Thread(target=self._go)
        self._thread.daemon = True
        self._thread.start()
        self._symbol = Bomber.count
        Bomber.count += 1

    def _go(self):
        while True:
            self._session.execute('INSERT INTO tokens (id, thing) VALUES ({0},{1})'.format(uuid.uuid4(), uuid.uuid4()))
            time.sleep(random.random())
            self._session.execute('SELECT * FROM tokens')
            sys.stderr.write(' {0} '.format(self._symbol))

for _ in range(arguments.threads):
    Bomber(cluster)

while True:
    time.sleep(1000)
