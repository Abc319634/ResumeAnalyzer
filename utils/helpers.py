import datetime

def format_date(date_str):
    try:
        dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%B %d, %Y")
    except:
        return date_str

def get_page_count(text):
    # Rough estimate
    return max(1, len(text) // 3000)
