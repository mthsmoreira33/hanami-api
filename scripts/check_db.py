import sqlite3

conn = sqlite3.connect("data/processed/hanami.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tabelas:", cursor.fetchall())

cursor.execute("SELECT COUNT(*) FROM vendas;")
print("Linhas na tabela vendas:", cursor.fetchone()[0])

conn.close()
