from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1] #Делает абсолютный (полный путь) из-за чего parents[1] всегда работает правильно указывая на корень
RAW = ROOT/"data"/"raw"
DB = ROOT/"data"/"promo.db"
FILES = {"transactions": "transaction_data.csv", "products": "product.csv",}

def main():
  conn = sqlite3.connect(DB)
  for table, filename in FILES.items():
    df = pd.read_csv(RAW/filename)
    df.columns = df.columns.str.lower()
    df.to_sql(table, conn, if_exists="replace", index=False, chunksize=100_000)
    n_db = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] #Сколько строк в базе
    print(f"{table}: csv={len(df):,} db={n_db:,}")
    
  conn.execute("CREATE INDEX IF NOT EXISTS idx_tr_product ON transactions(product_id)")
  conn.execute("CREATE INDEX IF NOT EXISTS idx_tr_week ON transactions(week_no)")
  conn.commit()
  conn.close()
    
if __name__ == "__main__":
  main()