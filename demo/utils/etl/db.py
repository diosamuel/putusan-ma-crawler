import clickhouse_connect
import datetime
import json
import logging
import datetime
client = clickhouse_connect.get_client(
    host="localhost",
    username="default",
    password=""
)

def insertData(data, table, columns):
    try:
        data["upload"] = datetime.datetime.strptime(data["upload"], "%Y-%m-%d").date()
        check_dup = client.query(f"""
            SELECT count(*) from {table} where hash_id = '{data["hash_id"]}'
        """)
        if check_dup.result_rows[0][0] >= 1:
            logging.warning(f"Skip {data['hash_id']}")
        else:
            insertedData = [list(data.values())]
            client.insert(table, insertedData, column_names=columns)
            logging.warning(f"Insert {data['hash_id']}")
    except Exception as e:
        logging.error(e)


def readData(column,table):
    try:
        retrieve = client.query(f"""
            SELECT {column} from {table}          
        """)

        return retrieve
    except Exception as e:
        print(e)

def initTable():
    putusan = '''
    CREATE TABLE IF NOT EXISTS putusan (
        hash_id String,
        nomor String,
        tingkat_proses String,
        klasifikasi String,
        kata_kunci String,
        tahun Int32,
        tanggal_register Date,
        lembaga_peradilan String,
        jenis_lembaga_peradilan String,
        hakim_ketua String,
        hakim_anggota String,
        panitera String,
        amar String,
        amar_lainnya String,
        catatan_amar String,
        tanggal_baca Date,
        kaidah String,
        abstrak String,
        putusan String,
        view Int32,
        download Int32,
        zip String,
        pdf String,
        tanggal_musyawarah Date,
        tanggal_dibacakan Date
    ) ENGINE = MergeTree()
    ORDER BY hash_id
    '''

    putusan_data = '''
    CREATE TABLE IF NOT EXISTS putusan_data (
        hash_id String,
        upload Date,
        link_detail String,
        nomor String,
        page UInt32,
        scraped_at String
    ) 
    ENGINE = MergeTree
    ORDER BY (nomor, upload);

    '''
    try:
        client.command(putusan)
        client.command(putusan_data)
        logging.info("Successfully init table")
    except Exception as e:
        logging.error(f"Error creating table: {e}")

initTable()

def insertPutusan(scraped_json):
    desc = scraped_json.get('description', {})
    DEFAULT_DATE = datetime.date(1970, 1, 1)
    def parse_date_safe(date_str):
        if not date_str:
            return DEFAULT_DATE
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return DEFAULT_DATE
        
    data = {
        'link_detail':scraped_json.get('url'),
        'update_at':datetime.datetime.now().strftime("%c"),
        'hash_id': scraped_json.get('hash_id'),
        'nomor': desc.get('nomor'),
        'tingkat_proses': desc.get('tingkat_proses'),
        'klasifikasi': desc.get('klasifikasi'),
        'kata_kunci': desc.get('kata_kunci'),
        'tahun': int(desc.get('tahun')) if desc.get('tahun') else None,
        'tanggal_register': parse_date_safe(desc.get('tanggal_register')),
        'lembaga_peradilan': desc.get('lembaga_peradilan'),
        'jenis_lembaga_peradilan': desc.get('jenis_lembaga_peradilan'),
        'hakim_ketua': desc.get('hakim_ketua'),
        'hakim_anggota': desc.get('hakim_anggota'),
        'panitera': desc.get('panitera'),
        'amar': desc.get('amar'),
        'amar_lainnya': desc.get('amar_lainnya'),
        'catatan_amar': desc.get('catatan_amar'),
        'kaidah': desc.get('kaidah'),
        'abstrak': desc.get('abstrak'),
        'putusan': json.dumps(desc.get('putusan', {})),
        'view': int(desc.get('view')) if desc.get('view') else 0,
        'download': int(desc.get('download')) if desc.get('download') else 0,
        'zip': desc.get('zip'),
        'pdf': desc.get('pdf'),
        'tanggal_musyawarah': parse_date_safe(desc.get('tanggal_musyawarah')),
        'tanggal_dibacakan': parse_date_safe(desc.get('tanggal_dibacakan')),
    }
    check_dup = client.query(f"""
        SELECT count(*) from putusan where hash_id = '{data["hash_id"]}'
    """)
    if check_dup.result_rows[0][0] >= 1:
        logging.warning(f"Skip {data['hash_id']}")
    else:
        client.insert("putusan", [list(data.values())], column_names=list(data.keys()))
        logging.warning(f"Success Insert {data['hash_id']}")