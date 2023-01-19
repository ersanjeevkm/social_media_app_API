from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


@app.route('/messages', methods=['POST'])
def create_message():
    text = request.json.get('text')

    conn = psycopg2.connect(dbname="social_media_app",
                            user="postgres", password="admin")

    cur = conn.cursor()

    cur.execute('INSERT INTO messages (message) VALUES (%s)', (text,))
    conn.commit()

    cur.execute('SELECT * FROM messages ORDER BY timestamp DESC')
    messages = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(messages)


@app.route('/messages', methods=['GET'])
def get_messages():
    conn = psycopg2.connect(dbname="social_media_app",
                            user="postgres", password="admin")
    cur = conn.cursor()

    cur.execute('SELECT * FROM messages ORDER BY timestamp DESC')
    messages = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(messages)


@app.route('/likes/<message_id>', methods=['POST'])
def create_like(message_id):
    conn = psycopg2.connect(dbname="social_media_app",
                            user="postgres", password="admin")
    cur = conn.cursor()

    cur.execute('INSERT INTO likes (message_id) VALUES (%s)', (message_id,))
    conn.commit()

    cur.execute('SELECT COUNT(*) FROM likes WHERE message_id = %s',
                (message_id,))
    likes = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({'likes': likes})
