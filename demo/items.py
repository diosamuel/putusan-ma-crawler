# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PutusanItem(scrapy.Item):
    hash_id = scrapy.Field()
    link_detail = scrapy.Field()
    pengadilan = scrapy.Field()
    kategori = scrapy.Field()
    register = scrapy.Field()
    putus = scrapy.Field()
    upload = scrapy.Field()
    nomor_putusan = scrapy.Field()
    tanggal_putusan = scrapy.Field()
    pihak = scrapy.Field()
    view = scrapy.Field()
    download = scrapy.Field()

class DeskripsiPutusanItems(scrapy.Item):
    # Dynamic fields from the table will be added at runtime
    hash_id = scrapy.Field()
    nomor = scrapy.Field()
    tingkat_proses = scrapy.Field()
    klasifikasi = scrapy.Field()
    kata_kunci = scrapy.Field()
    tahun = scrapy.Field()
    tanggal_register = scrapy.Field()
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
    tanggal_musyawarah = scrapy.Field()
    tanggal_dibacakan = scrapy.Field()
    kaidah = scrapy.Field()
    abstrak = scrapy.Field()
