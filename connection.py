
from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()
pasw = os.getenv("PASSWORD_DB")


async def connection_db():
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="postgres",
        database="shop_bot_db",
        password=pasw
    )
    return conn


async def create_table():
    conn = await connection_db()
    try:
        await conn.execute("""
        create table if not exists products(
            id serial primary key,
            owner_id bigint not null,
            title varchar(100) not null,
            category varchar(100) not null,
            price int not null check (price > 0),
            stock int not null check (stock >= 0),
            photo_file_id text not null
        );
        create table if not exists orders(
            id serial primary key,
            user_id bigint not null,
            product_id int not null references products(id),
            purchase_price int not null,
            purchased_at timestamp not null default now()
        );
        """)
        print("✅ Table created")
    except Exception as Error:
        print(f"❌ Create Error: {Error}")
    finally:
        await conn.close()