import sqlite3
import time

# Connect to SQLite database (or create it)

def init_db():
    conn = sqlite3.connect('discord_messages.db')
    c = conn.cursor()

    # Create a table to store user messages and timestamps
    c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        user_id TEXT,
        message TEXT,
        role TEXT,
        timestamp INTEGER
    )
    ''')

    return conn, c


def log_message(conn, c, user_id, message, role):
    timestamp = int(time.time())  # Get current epoch time
    c.execute('INSERT INTO messages (user_id, message, role, timestamp) VALUES (?, ?, ?, ?)', 
              (user_id, message, role, timestamp))
    conn.commit()


def get_conversations(c, user_id: str, time_window: int = 1800) -> list:
    """
    Fetch conversation history for a specific user within a time window (e.g., last 30 minutes).
    
    :param user_id: ID of the user to fetch the conversation for.
    :param time_window: Time window in seconds (default is 1800 seconds or 30 minutes).
    :return: List of messages formatted as a conversation with 'role' and 'parts'.
    """
    current_time = int(time.time())
    time_threshold = current_time - time_window

    # Fetch messages for the given user within the time window
    c.execute('''
    SELECT role, message 
    FROM messages 
    WHERE user_id = ? AND timestamp >= ?
    ORDER BY timestamp ASC
    ''', (user_id, time_threshold))

    rows = c.fetchall()

    if not rows:
        return []  # No messages found

    conversation = [
        {"role": row[0], "parts": [row[1]]}
        for row in rows
    ]
    return conversation



