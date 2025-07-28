
import clickhouse_connect
import os
from dotenv import load_dotenv
load_dotenv()
client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST", "localhost"),
    username=os.getenv("CLICKHOUSE_USER", "default"),
    password=os.getenv("CLICKHOUSE_PASSWORD", "default"),
    port=os.getenv("CLICKHOUSE_HTTP_PORT", "8123")
)

print(os.getenv("CLICKHOUSE_HOST", "localhost"))
print(client.raw_query("select 'iloveyou';"))