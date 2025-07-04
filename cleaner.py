import csv
import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder

#To show me the whole list of dataset with all its Rows.
pd.set_option("display.max_rows", None)

#Reading our CSV file which we got after Scraping the data from Divar.ir.
df = pd.read_csv("Final_info.csv")

#to clean the Rows which they got Persian alphabets in them.
#we turn it into STR then:
df["price per meter"] = df["price per meter"].astype(str).str.findall(r'\d+').str.join('')
df["price per meter"] = df["price per meter"].astype(int)
#Getting rid of Prices that are fake and not real.
df = df[df["price per meter"] >= 50_000_000]

#Again Getting rid of Persian Alphabets inside the Rows.
df["year"] = df["year"].astype(str).str.findall(r'\d+').str.join('')
df["year"] = df["year"].astype(int)

#encoding Districs which is not numeric so...
le = LabelEncoder()
df["neighborhood_encoded"] = le.fit_transform(df["neighborhood"])

df.drop(columns=["neighborhood"], inplace=True)
df.to_csv("this_is_final.csv", index=False)

print(df)
