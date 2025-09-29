from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    try:
        conn = psycopg2.connect(
            host='db',
            database='mydb',
            user='myuser',
            password='mypassword'
        )
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return f'Connected to PostgreSQL: {db_version}'
    except Exception as e:
        return f'Failed to connect to PostgreSQL: {e}'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

#docker-compose.yml
"""version: '3.8'
services:
  web:
    build: .
    ports:
      - "5001:5000"
    depends_on:
      - db
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:"""
#D
"""
FROM python:3.9-slim

WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY app/ .
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

CMD ["/wait-for-postgres.sh", "db", "python", "app.py"]
"""
#wait-for-postgres.sh
"""#!/bin/bash
set -e
host="$1"
shift
cmd="$@"
until PGPASSWORD=mypassword psql -h "$host" -U "myuser" -d "mydb" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - executing command"
exec $cmd"""
