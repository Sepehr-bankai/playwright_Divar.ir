
#changing arabic numbers to English numbers,
#so we can easily use our Final CSV data via PANDAS.
def number_changer(text):
    translation_table = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    english_table = text.translate(translation_table)
    
    cleaned_number = english_table.replace("تومان", "").replace(" ","").replace("٬","").replace(",","").replace("قبل از","")

    return cleaned_number
