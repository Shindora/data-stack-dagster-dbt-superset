import os 
import structlog
import polars as pl 
import psycopg2
from psycopg2.extras import execute_values
log = structlog.get_logger()

CONNECTION = psycopg2.connect(user=os.environ["POSTGRES_USER"],
                                password=os.environ["POSTGRES_PASSWORD"],
                                host=os.environ['POSTGRES_HOST'],
                                port="5432",
                                database=os.environ['POSTGRES_DB'])

def ingest_raw_customers(file_path: str, table_name: str) -> None:
    customer_df = pl.read_csv(file_path)
    log.info(f"Start ingesting to table: {table_name}")
    log.info(customer_df.head())
    log.info(f"Df length: {customer_df.shape[0]}")
    with CONNECTION as conn:
        cur = conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        cur.execute(f"""CREATE TABLE {table_name}(id bigint, 
                                                    created_at VARCHAR(255), 
                                                    email VARCHAR(255), 
                                                    default_address__zip VARCHAR(255), 
                                                    default_address__province VARCHAR(255), default_address__country VARCHAR(255))
                                                    """)
        conn.commit()
        
    with CONNECTION as conn:
        # Create a list of tuples for each row of the DataFrame
        rows = [row for row in customer_df.iter_rows()]
        # Define the insert query
        insert_query = f"INSERT INTO {table_name} (id, created_at, email, default_address__zip, default_address__province, default_address__country) VALUES %s"
        # Use execute_values to insert rows into the table
        execute_values(cur, insert_query, rows)
        conn.commit()
    log.info(f"Ingest to {table_name} successfully.")

def ingest_raw_items(file_path: str, table_name: str) -> None:
    item_df = pl.read_csv(file_path)
    log.info(f"Start ingesting to table: {table_name}")
    log.info(item_df.head())
    log.info(f"Df length: {item_df.shape[0]}")

    with CONNECTION as conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            cur.execute(f"""CREATE TABLE {table_name} (
                                order_id BIGINT,
                                id BIGINT,
                                gift_card BOOLEAN,
                                grams BIGINT,
                                name TEXT,
                                price FLOAT,
                                quantity BIGINT,
                                sku TEXT,
                                taxable BOOLEAN,
                                title TEXT,
                                total_discount FLOAT,
                                pre_tax_price FLOAT,
                                has_message BIGINT
                            )""")
            conn.commit()

    with CONNECTION as conn:
        with conn.cursor() as cur:
            rows = [row for row in item_df.iter_rows()]
            insert_query = f"""INSERT INTO {table_name} 
                                (order_id, id, gift_card, grams, name, price, 
                                quantity, sku, taxable, title, total_discount, 
                                pre_tax_price, has_message) 
                                VALUES %s"""
            execute_values(cur, insert_query, rows)
        conn.commit()

    log.info(f"Ingestion to {table_name} successfully.")

def ingest_raw_orders(file_path: str, table_name: str) -> None:
    order_df = pl.read_csv(file_path)
    log.info(f"Start ingesting to table: {table_name}")
    log.info(order_df.head())
    log.info(f"Df length: {order_df.shape[0]}")

    with CONNECTION as conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            cur.execute(f"""CREATE TABLE {table_name} (
                                id BIGINT,
                                created_at VARCHAR(255),
                                customer_id BIGINT,
                                contact_email VARCHAR(255),
                                billing_address__zip VARCHAR(255),
                                shipping_address__zip VARCHAR(255),
                                billing_address__province VARCHAR(255),
                                shipping_address__province VARCHAR(255),
                                billing_address__country VARCHAR(255),
                                shipping_address__country VARCHAR(255),
                                total_price_usd FLOAT,
                                total_tax FLOAT,
                                total_discounts FLOAT,
                                cancel_reason TEXT,
                                cancelled_at VARCHAR(255),
                                device_id VARCHAR(255),
                                gateway VARCHAR(255),
                                referring_site TEXT,
                                landing_site TEXT,
                                client_details__browser_width BIGINT,
                                buyer_accepts_marketing BOOLEAN
                            )""")
            conn.commit()


    with CONNECTION as conn:
        with conn.cursor() as cur:
            rows = [row for row in order_df.iter_rows()]
            insert_query = f"""INSERT INTO {table_name} 
                                (id, created_at, customer_id, contact_email, billing_address__zip, 
                                shipping_address__zip, billing_address__province, shipping_address__province, 
                                billing_address__country, shipping_address__country, total_price_usd, total_tax, 
                                total_discounts, cancel_reason, cancelled_at, device_id, gateway, referring_site, 
                                landing_site, client_details__browser_width, buyer_accepts_marketing) 
                                VALUES %s"""
            execute_values(cur, insert_query, rows)
        conn.commit()

    log.info(f"Ingestion to {table_name} successfully.")

def create_schema_dw(name: str) -> None:
    try:
        cursor = CONNECTION.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {name};")
        CONNECTION.commit()
        
        print(f"Schema '{name}' created successfully.")
    
    except Exception as e:
        log.error(f"Error: {e}")
    
    finally:
        if CONNECTION:
            cursor.close()
            CONNECTION.close()
            log.info("PostgreSQL connection is closed.")

ingest_raw_customers("shared/csv/interview_customers.csv", "raw_customers")
ingest_raw_items("shared/csv/interview_items.csv", "raw_items")
ingest_raw_orders("shared/csv/interview_orders.csv", "raw_orders")
create_schema_dw("data_warehouse")