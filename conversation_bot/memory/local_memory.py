import sqlite3
from datetime import datetime

# Initialize DB and create table if not exists
def init_db():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Save a message
def save_message(user_id, role, message):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cursor.execute("""
        INSERT INTO messages (user_id, role, message, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, role, message, timestamp))
    conn.commit()
    conn.close()

# Retrieve all messages for a user
def retrieve_last_5_pairs(user_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    # Fetch last 10 messages
    cursor.execute("""
        SELECT role, message FROM messages
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 10
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    # Reverse to get chronological order
    rows.reverse()

    # Convert to LangChain-compatible message dicts
    formatted_messages = [{"role": role, "content": message} for role, message in rows]

    return formatted_messages



# # Example usage
# if __name__ == "__main__":
#     init_db()

#     # Save some messages
#     save_message("user_123", "user", "What are the symptoms of flu?")
#     save_message("user_123", "assistant", "Fever, cough, sore throat, and fatigue are common symptoms.")

#     # Retrieve chat history
#     history = retrieve_messages("user_123")
#     for role, msg, ts in history:
#         print(f"[{ts}] {role.upper()}: {msg}")
