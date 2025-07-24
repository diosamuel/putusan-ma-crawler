import clickhouse_connect
import datetime
import json
import logging
import datetime
client = clickhouse_connect.get_client(
    host="clickhouse",
    username="default",
    password="default",
    port=8123
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
        logging.error(f"SQL Error: {str(e)}")
        raise Exception(f"Failed to retrieve data from database: {str(e)}")

def initTable():
    informasi_putusan = '''
    CREATE TABLE IF NOT EXISTS informasi_putusan (
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

    list_putusan = '''
    CREATE TABLE IF NOT EXISTS list_putusan (
        hash_id String,
        upload Date,
        link_detail String,
        nomor String,
        page UInt32,
        scraped_at String
    ) 
    ENGINE = MergeTree()
    ORDER BY (nomor, upload);

    '''
    try:
        client.command(informasi_putusan)
        client.command(list_putusan)
        logging.info("Successfully init table")
    except Exception as e:
        logging.error(f"Error creating table: {e}")

initTable()

def insertPutusan(scraped_json):
    desc = scraped_json.get('description', {})
    DEFAULT_DATE = datetime.date(1970, 1, 1)

    def safeDate(date_str):
        if not date_str:
            return DEFAULT_DATE
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception:
            return DEFAULT_DATE
    def safeStr(val):
        return val if (val is not None and isinstance(val, str)) else ''
    
    data = {
        'link_detail':scraped_json.get('url'),
        'update_at':datetime.datetime.now().strftime("%c"),
        'hash_id': safeStr(scraped_json.get('hash_id')),
        'nomor': safeStr(desc.get('nomor')),
        'tingkat_proses': safeStr(desc.get('tingkat_proses')),
        'klasifikasi': safeStr(desc.get('klasifikasi')),
        'kata_kunci': safeStr(desc.get('kata_kunci')),
        'tahun': int(desc.get('tahun')) if desc.get('tahun') else None,
        'tanggal_register': safeDate(desc.get('tanggal_register')),
        'lembaga_peradilan': safeStr(desc.get('lembaga_peradilan')),
        'jenis_lembaga_peradilan': safeStr(desc.get('jenis_lembaga_peradilan')),
        'hakim_ketua': safeStr(desc.get('hakim_ketua')),
        'hakim_anggota': safeStr(desc.get('hakim_anggota')),
        'panitera': safeStr(desc.get('panitera')),
        'amar': safeStr(desc.get('amar')),
        'amar_lainnya': safeStr(desc.get('amar_lainnya')),
        'catatan_amar': safeStr(desc.get('catatan_amar')),
        'kaidah': safeStr(desc.get('kaidah')),
        'abstrak': safeStr(desc.get('abstrak')),
        'putusan': json.dumps(desc.get('putusan', {})),
        'view': int(desc.get('view')) if desc.get('view') else 0,
        'download': int(desc.get('download')) if desc.get('download') else 0,
        'zip': safeStr(desc.get('zip')),
        'pdf': safeStr(desc.get('pdf')),
        'tanggal_musyawarah': safeDate(desc.get('tanggal_musyawarah')),
        'tanggal_dibacakan': safeDate(desc.get('tanggal_dibacakan')),
    }
    check_dup = client.query(f"""
        SELECT count(*) from informasi_putusan where hash_id = '{data["hash_id"]}'
    """)
    if check_dup.result_rows[0][0] >= 1:
        logging.warning(f"Skip {data['hash_id']}")
    else:
        client.insert("informasi_putusan", [list(data.values())], column_names=list(data.keys()))
        logging.warning(f"Success Insert {data['hash_id']}")





"""
create table ekstraksi_pdf (
    hash_id String,
    peran_pihak String,
    tempat_lahir String,
    tanggal_lahir String,
    usia String,
    jenis_kelamin String,
    pekerjaan String,
    agama String,
    nomor_ktp String,
    nomor_kk String,
    nomor_akta_kelahiran String,
    nomor_paspor String
) ENGINE = MergeTree()
ORDER BY hash_id;
"""

"""
create table putusan_pdf (
    hash_id String,
    nomor String,
    s3 String,
    link String,
    upload_date String
) ENGINE = MergeTree()
ORDER BY hash_id;
"""