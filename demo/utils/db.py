import clickhouse_connect
from typing import Dict, Any
import logging

class ClickHouseDB:
    def __init__(self, host='localhost', port=8123, username='default', password='', database='default'):
        """Initialize ClickHouse connection"""
        try:
            self.client = clickhouse_connect.get_client(
                host=host,
                port=port,
                username=username,
                password=password,
                database=database
            )
            logging.info(f"Connected to ClickHouse at {host}:{port}")
        except Exception as e:
            logging.error(f"Failed to connect to ClickHouse: {e}")
            raise

    def create_putusan_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS putusan (
            hashid String
            title String,
            nomor String,
            tingkat_proses String,
            klasifikasi String,
            kata_kunci String,
            tahun UInt16,
            tanggal_register String,
            lembaga_peradilan String,
            jenis_lembaga_peradilan String,
            hakim_ketua String,
            hakim_anggota String,
            panitera String,
            amar String,
            amar_lainnya String,
            catatan_amar String,
            tanggal_musyawarah String,
            tanggal_dibacakan String,
            kaidah String,
            abstrak String,
            created_at DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (tahun, nomor)
        """
        
        try:
            self.client.command(create_table_query)
            logging.info("Putusan table created successfully")
        except Exception as e:
            logging.error(f"Failed to create table: {e}")
            raise

    def insert_putusan(self, data: Dict[str, Any]):
        """Insert flattened putusan data into the table"""
        # Flatten the nested data structure
        flattened_data = {
            'title': data.get('title', ''),
            'nomor': data.get('data', {}).get('Nomor', ''),
            'tingkat_proses': data.get('data', {}).get('Tingkat Proses', ''),
            'klasifikasi': data.get('data', {}).get('Klasifikasi', ''),
            'kata_kunci': data.get('data', {}).get('Kata Kunci', ''),
            'tahun': int(data.get('data', {}).get('Tahun', 0)) if data.get('data', {}).get('Tahun', '').isdigit() else 0,
            'tanggal_register': data.get('data', {}).get('Tanggal Register', ''),
            'lembaga_peradilan': data.get('data', {}).get('Lembaga Peradilan', ''),
            'jenis_lembaga_peradilan': data.get('data', {}).get('Jenis Lembaga Peradilan', ''),
            'hakim_ketua': data.get('data', {}).get('Hakim Ketua', ''),
            'hakim_anggota': data.get('data', {}).get('Hakim Anggota', ''),
            'panitera': data.get('data', {}).get('Panitera', ''),
            'amar': data.get('data', {}).get('Amar', ''),
            'amar_lainnya': data.get('data', {}).get('Amar Lainnya', ''),
            'catatan_amar': data.get('data', {}).get('Catatan Amar', ''),
            'tanggal_musyawarah': data.get('data', {}).get('Tanggal Musyawarah', ''),
            'tanggal_dibacakan': data.get('data', {}).get('Tanggal Dibacakan', ''),
            'kaidah': data.get('data', {}).get('Kaidah', ''),
            'abstrak': data.get('data', {}).get('Abstrak', '')
        }

        insert_query = """
        INSERT INTO putusan (
            title, nomor, tingkat_proses, klasifikasi, kata_kunci, tahun,
            tanggal_register, lembaga_peradilan, jenis_lembaga_peradilan,
            hakim_ketua, hakim_anggota, panitera, amar, amar_lainnya,
            catatan_amar, tanggal_musyawarah, tanggal_dibacakan, kaidah, abstrak
        ) VALUES (
            %(title)s, %(nomor)s, %(tingkat_proses)s, %(klasifikasi)s, %(kata_kunci)s, %(tahun)s,
            %(tanggal_register)s, %(lembaga_peradilan)s, %(jenis_lembaga_peradilan)s,
            %(hakim_ketua)s, %(hakim_anggota)s, %(panitera)s, %(amar)s, %(amar_lainnya)s,
            %(catatan_amar)s, %(tanggal_musyawarah)s, %(tanggal_dibacakan)s, %(kaidah)s, %(abstrak)s
        )
        """

        try:
            self.client.insert('putusan', [flattened_data])
            logging.info(f"Successfully inserted putusan: {flattened_data.get('nomor', 'Unknown')}")
        except Exception as e:
            logging.error(f"Failed to insert putusan data: {e}")
            raise

    def insert_batch_putusan(self, data_list: list):
        """Insert multiple putusan records in batch"""
        flattened_data_list = []
        
        for data in data_list:
            flattened_data = {
                'title': data.get('title', ''),
                'nomor': data.get('data', {}).get('Nomor', ''),
                'tingkat_proses': data.get('data', {}).get('Tingkat Proses', ''),
                'klasifikasi': data.get('data', {}).get('Klasifikasi', ''),
                'kata_kunci': data.get('data', {}).get('Kata Kunci', ''),
                'tahun': int(data.get('data', {}).get('Tahun', 0)) if data.get('data', {}).get('Tahun', '').isdigit() else 0,
                'tanggal_register': data.get('data', {}).get('Tanggal Register', ''),
                'lembaga_peradilan': data.get('data', {}).get('Lembaga Peradilan', ''),
                'jenis_lembaga_peradilan': data.get('data', {}).get('Jenis Lembaga Peradilan', ''),
                'hakim_ketua': data.get('data', {}).get('Hakim Ketua', ''),
                'hakim_anggota': data.get('data', {}).get('Hakim Anggota', ''),
                'panitera': data.get('data', {}).get('Panitera', ''),
                'amar': data.get('data', {}).get('Amar', ''),
                'amar_lainnya': data.get('data', {}).get('Amar Lainnya', ''),
                'catatan_amar': data.get('data', {}).get('Catatan Amar', ''),
                'tanggal_musyawarah': data.get('data', {}).get('Tanggal Musyawarah', ''),
                'tanggal_dibacakan': data.get('data', {}).get('Tanggal Dibacakan', ''),
                'kaidah': data.get('data', {}).get('Kaidah', ''),
                'abstrak': data.get('data', {}).get('Abstrak', '')
            }
            flattened_data_list.append(flattened_data)

        try:
            self.client.insert('putusan', flattened_data_list)
            logging.info(f"Successfully inserted {len(flattened_data_list)} putusan records")
        except Exception as e:
            logging.error(f"Failed to insert batch putusan data: {e}")
            raise

    def close(self):
        """Close the ClickHouse connection"""
        if hasattr(self, 'client'):
            self.client.close()
            logging.info("ClickHouse connection closed")

# Example usage
if __name__ == "__main__":
    # Sample data
    sample_data = {
        "title": "Putusan PN BREBES Nomor 77/Pid.B/2025/PN Bbs",
        "data": {
            "Nomor": "77/Pid.B/2025/PN Bbs",
            "Tingkat Proses": "Pertama",
            "Klasifikasi": "Pidana Umum Pidana Umum Pencurian",
            "Kata Kunci": "Pencurian",
            "Tahun": "2025",
            "Tanggal Register": "27 Mei 2025",
            "Lembaga Peradilan": "PN BREBES",
            "Jenis Lembaga Peradilan": "PN",
            "Hakim Ketua": "Hakim Ketua Kukuh Kurniawan",
            "Hakim Anggota": "Hakim Anggota Imam Munandar, Br Hakim Anggota Nurachmat",
            "Panitera": "Panitera Pengganti Nugroho Argo Wibowo",
            "Amar": "Lain-lain",
            "Amar Lainnya": "PIDANA PENJARA WAKTU TERTENTU",
            "Catatan Amar": "MENGADILI : Menyatakan Terdakwa Muhamad Miftahudin Alias Mif Bin Warso tersebut diatas, terbukti secara sah dan meyakinkan bersalah melakukan tindak pidana ?pencurian? sebagaimana dalam dakwaan Tunggal Penuntut Umum ; Menjatuhkan pidana penjara kepada Terdakwa oleh karena itu dengan pidana penjara selama 3 (tiga) Tahun ; Menetapkan masa penangkapan dan penahanan yang telah dijalani Terdakwa dikurangkan seluruhnya dari pidana yang dijatuhkan ; Menetapkan Terdakwa tetap ditahan ; Menetapkan barangbuktiberupa : 1 (satu) buah Flashdisc berisi rekaman CCTV ; Uang tunai sebesar Rp.15.600.000,- (lima belas juta enam ratus ribu rupiah) ; Dikembalikan kepada saksi Ika Susiana Binti Kusnan 3. 1 (satu) potong Kaos oblong lengan pendek warna hitam bertuliskan ? ENJOY RELAX? ; Dirampas untuk dimusnahkan 4. 1 (satu) unit sepeda motor merk Honda Beat warna hitam tahun 2016, Nopol : G-6760-CU, No Rangka : MH1JFP215GK287751, No Mesin : JFP2E1288433, berikut STNK atas nama : Warso alamat Dk. Menteng Rt.07 Rw.01 Desa Ragatunjung Kec. Paguyangan Kab. Brebes ; Dikembalikan kepada Terdakwa. 6. Membebankan kepada Terdakwamembayar biaya perkara sejumlahRp. 5.000,-(lima ribu rupiah);",
            "Tanggal Musyawarah": "14 Juli 2025",
            "Tanggal Dibacakan": "14 Juli 2025",
            "Kaidah": "—",
            "Abstrak": ""
        }
    }

    # Initialize database connection
    db = ClickHouseDB()
    
    try:
        # Create table
        db.create_putusan_table()
        
        # Insert single record
        db.insert_putusan(sample_data)
        
        print("Data inserted successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()
