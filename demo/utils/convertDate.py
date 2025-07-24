from datetime import datetime
mapperDate = {
    "januari": "january",
    "februari": "february",
    "maret": "march",
    "april": "april",
    "mei": "may",
    "juni": "june",
    "juli": "july",
    "agustus": "august",
    "september": "september",
    "oktober": "october",
    "nopember": "november",
    "desember": "december"
}

def convert_to_ymd(date_str):
    parts = date_str.strip().lower().split()
    if len(parts) != 3:
        return None
    day, month_id, year = parts
    month_en = mapperDate.get(month_id)
    if not month_en:
        return None
    date_en = f"{day} {month_en} {year}"
    dt = datetime.strptime(date_en, "%d %B %Y")
    return dt.strftime("%Y-%m-%d")
