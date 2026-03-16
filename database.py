import sqlite3
import os

DB_PATH = os.path.join("data", "database.db")

def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Resumes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        filename TEXT NOT NULL,
        content TEXT NOT NULL,
        skills TEXT,
        education TEXT,
        projects TEXT,
        experience TEXT,
        certifications TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Opportunities table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT,
        description TEXT NOT NULL,
        type TEXT,
        link TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Analysis results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        resume_id INTEGER NOT NULL,
        opportunity_id INTEGER NOT NULL,
        score INTEGER,
        matched_skills TEXT,
        missing_skills TEXT,
        suggestions TEXT,
        analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (resume_id) REFERENCES resumes (id),
        FOREIGN KEY (opportunity_id) REFERENCES opportunities (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def execute_query(query, params=(), commit=False):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return cursor.lastrowid
        return cursor.fetchall()
    finally:
        conn.close()

def fetch_one(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    finally:
        conn.close()

def delete_analysis(analysis_id: int, user_id: int):
    """Delete a single analysis result (and its linked opportunity if no other results use it)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get the opportunity_id first
        cursor.execute("SELECT opportunity_id FROM analysis_results WHERE id=? AND user_id=?",
                       (analysis_id, user_id))
        row = cursor.fetchone()
        if row:
            opp_id = row['opportunity_id']
            # Delete the analysis result
            cursor.execute("DELETE FROM analysis_results WHERE id=? AND user_id=?",
                           (analysis_id, user_id))
            # Delete opportunity only if no other analyses reference it
            cursor.execute("SELECT COUNT(*) c FROM analysis_results WHERE opportunity_id=?", (opp_id,))
            if cursor.fetchone()['c'] == 0:
                cursor.execute("DELETE FROM opportunities WHERE id=?", (opp_id,))
        conn.commit()
    finally:
        conn.close()

def delete_all_history(user_id: int):
    """Delete all analysis results for a user (keeps resumes intact)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Collect orphaned opportunity IDs before deleting
        cursor.execute("SELECT opportunity_id FROM analysis_results WHERE user_id=?", (user_id,))
        opp_ids = [r['opportunity_id'] for r in cursor.fetchall()]
        cursor.execute("DELETE FROM analysis_results WHERE user_id=?", (user_id,))
        # Delete opportunities that are now orphaned
        for oid in opp_ids:
            cursor.execute("SELECT COUNT(*) c FROM analysis_results WHERE opportunity_id=?", (oid,))
            if cursor.fetchone()['c'] == 0:
                cursor.execute("DELETE FROM opportunities WHERE id=?", (oid,))
        conn.commit()
    finally:
        conn.close()

def delete_resume(resume_id: int, user_id: int):
    """Delete a resume and all its linked analysis results + opportunities."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Get linked opportunity IDs
        cursor.execute("""
            SELECT DISTINCT opportunity_id FROM analysis_results
            WHERE resume_id=? AND user_id=?
        """, (resume_id, user_id))
        opp_ids = [r['opportunity_id'] for r in cursor.fetchall()]

        # Delete analyses for this resume
        cursor.execute("DELETE FROM analysis_results WHERE resume_id=? AND user_id=?",
                       (resume_id, user_id))

        # Delete orphaned opportunities
        for oid in opp_ids:
            cursor.execute("SELECT COUNT(*) c FROM analysis_results WHERE opportunity_id=?", (oid,))
            if cursor.fetchone()['c'] == 0:
                cursor.execute("DELETE FROM opportunities WHERE id=?", (oid,))

        # Delete the resume itself
        cursor.execute("DELETE FROM resumes WHERE id=? AND user_id=?", (resume_id, user_id))
        conn.commit()
    finally:
        conn.close()
