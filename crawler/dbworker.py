import os
import sqlite3
from threading import Thread
from queue import Queue

class DBWorker(Thread):
    def __init__(self, db_path, logger):
        super().__init__(daemon=True)
        self.db_path = db_path
        self.requests = Queue()
        self.logger = logger
        self.db_exists = os.path.exists(self.db_path)

    def run(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.setup_database()

        while True:
            operation, args, response_queue = self.requests.get()
            if operation == "stop":
                break
            result = getattr(self, operation)(*args)
            response_queue.put(result)

        self.conn.close()

    def setup_database(self):
        """Sets up the database tables if they don't exist."""
        if not self.db_exists:
            self.logger.info("No existing database found. Creating a new database.")
        else:
            self.logger.info("Existing database found. Using existing database.")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                urlhash TEXT PRIMARY KEY,
                url TEXT,
                completed BOOLEAN NOT NULL CHECK (completed IN (0, 1))
            )
        ''')
        self.conn.commit()

    def clear_database(self):
        self.cursor.execute('DELETE FROM urls')
        self.conn.commit()

    def add_url(self, url, urlhash, completed=False):
        self.cursor.execute('INSERT OR IGNORE INTO urls (urlhash, url, completed) VALUES (?, ?, ?)', (urlhash, url, int(completed)))
        self.conn.commit()

    def mark_url_complete(self, urlhash):
        self.cursor.execute('UPDATE urls SET completed = 1 WHERE urlhash = ?', (urlhash,))
        self.conn.commit()

    def get_all_urls(self):
        self.cursor.execute('SELECT urlhash, url, completed FROM urls')
        return {row[0]: (row[1], bool(row[2])) for row in self.cursor.fetchall()}

    def request(self, operation, *args):
        response_queue = Queue()
        self.requests.put((operation, args, response_queue))
        return response_queue.get()  # This blocks until the response is available

    def stop_worker(self):
        self.requests.put(("stop", [], None))