import csv
import hashlib
import pandas as pd
from connect_psycop import connect_to_supabase

def generate_hash(row):
    """
    Create deterministic hash from row values
    """
    row_string = "|".join(row.values())
    return hashlib.sha256(row_string.encode()).hexdigest()

def load_orders():
    """
    Load CSV data into PostgreSQL/Supabase safely.
    """
    with connect_to_supabase() as conn:
        conn.autocommit = False

        with conn.cursor() as cursor:
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    row_hash VARCHAR PRIMARY KEY,
                    order_id INTEGER NOT NULL,
                    customer_id VARCHAR NOT NULL,
                    customer VARCHAR(255),
                    amount NUMERIC(10,2),
                    order_date DATE
                );
            """)

            with open("./data/orders.csv", "r", newline="") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    row_hash = generate_hash(row)

                    cursor.execute("""
                        INSERT INTO orders (
                            row_hash,
                            order_id,
                            customer_id,
                            customer,
                            amount,
                            order_date
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (row_hash) DO NOTHING;
                    """, (
                        row_hash,
                        int(row["order_id"]),
                        row["customer_id"],
                        row["customer"],
                        float(row["amount"]),
                        row["order_date"]
                    ))

        conn.commit()


def check_db_update():
    """
    Used to check updates in the Supabase database.
    """
    with connect_to_supabase() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM orders")

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(rows, columns=columns)

    print(df)


if __name__ == "__main__":
    load_orders()
    check_db_update()