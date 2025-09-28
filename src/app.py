import argparse, sqlite3, datetime, os

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'open',
      created_at TEXT NOT NULL
    )""")
    con.commit(); con.close()

def add_task(title: str):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT INTO tasks(title,status,created_at) VALUES(?,?,?)",
        (title, "open", datetime.datetime.utcnow().isoformat())
    )
    con.commit(); con.close()
    print(f"added: {title}")

def list_tasks():
    con = sqlite3.connect(DB_PATH)
    rows = con.execute(
        "SELECT id,title,status,created_at FROM tasks ORDER BY id"
    ).fetchall()
    con.close()
    if not rows:
        print("No tasks.")
    else:
        for i, t, s, c in rows:
            print(f"[{i}] {t} • {s} • {c[:19]}Z")

def mark_done(task_id: int):
    con = sqlite3.connect(DB_PATH)
    cur = con.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
    con.commit(); con.close()
    print("done" if cur.rowcount else "not found")

def main():
    init_db()
    p = argparse.ArgumentParser(prog="tasks", description="Simple CLI Task Tracker (SQLite)")
    sub = p.add_subparsers(dest="cmd")

    pa = sub.add_parser("add");  pa.add_argument("title")
    sub.add_parser("list")
    pd = sub.add_parser("done"); pd.add_argument("id", type=int)

    a = p.parse_args()
    if   a.cmd == "add":  add_task(a.title)
    elif a.cmd == "list": list_tasks()
    elif a.cmd == "done": mark_done(a.id)
    else: p.print_help()

if __name__ == "__main__":
    main()
