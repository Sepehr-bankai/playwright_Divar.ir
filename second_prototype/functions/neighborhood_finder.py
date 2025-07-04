import csv


#for loading, deleting duplicates, and removing spaces and ETC...
def load_districts(file_path):
    districts = set()
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\n")
            for part in parts:
                sub_parts = part.strip().split("،")
                for name in sub_parts:
                    clean = name.strip().replace('"', '')
                    if clean:
                        districts.add(clean)
    return list(districts)


#For Checking wether we have that District in our CSV file,
#which we gathered using Location file i have uploaded in District File.
def extract_district(text, districts):
    for district in districts:
        if district and district in text:
            return district
    return None #This Cause returning None if we couldnt find it in our CSV District.


#i used this address because we opened it via ["python -m path.main"]
def combination(neighborhood, file_path="second_prototype/divar.csv"):
    districts = load_districts(file_path)
    cleaned_neighborhood = extract_district(neighborhood, districts)
    return cleaned_neighborhood

