import scrapy

class DemoItem(scrapy.Item):
    pass

class PutusanItem(scrapy.Item):
    hash_id = scrapy.Field()
    link_detail = scrapy.Field()
    upload = scrapy.Field()
    nomor = scrapy.Field()
    tanggal_putusan = scrapy.Field()
    page = scrapy.Field()
    scraped_at = scrapy.Field()

class DeskripsiPutusanItem(scrapy.Item):
    link_detail = scrapy.Field()
    hash_id = scrapy.Field()
    nomor = scrapy.Field()
    tingkat_proses = scrapy.Field()
    klasifikasi = scrapy.Field()
    kata_kunci = scrapy.Field()
    tahun = scrapy.Field() # YYYY
    tanggal_register = scrapy.Field() # YYYY-MM-DD
    lembaga_peradilan = scrapy.Field() 
    jenis_lembaga_peradilan = scrapy.Field()
    hakim_ketua = scrapy.Field()
    hakim_anggota = scrapy.Field()
    panitera = scrapy.Field()
    amar = scrapy.Field()
    amar_lainnya = scrapy.Field()
    catatan_amar = scrapy.Field()
    tanggal_baca = scrapy.Field()
    kaidah = scrapy.Field()
    abstrak = scrapy.Field()
    putusan = scrapy.Field()
    view = scrapy.Field()
    download = scrapy.Field()
    zip = scrapy.Field()
    pdf = scrapy.Field()
    tanggal_musyawarah = scrapy.Field() # YYYY-MM-DD
    tanggal_dibacakan = scrapy.Field()
    kaidah = scrapy.Field()
    abstrak = scrapy.Field()