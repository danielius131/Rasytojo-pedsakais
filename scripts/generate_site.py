import pandas as pd
from pathlib import Path

data_dir = Path("data")
output_dir = Path(".")

rasytojai = pd.read_csv(data_dir / "rasytojai.csv")
nuotraukos = pd.read_csv(data_dir / "nuotraukos.csv")

index_html = "<!DOCTYPE html><html lang='lt'><head><meta charset='UTF-8'><title>Rašytojų pėdsakai</title></head><body><h1>Rašytojų sąrašas</h1>"

for _, row in rasytojai.iterrows():
    r_id = row['id']
    main_photo = nuotraukos[(nuotraukos['rasytojas_id']==r_id) & (nuotraukos['yra_pagrindine']==True)]
    photo_tag = f"<img src='images/{main_photo.iloc[0]['failas']}' alt='{row['vardas']}' />" if not main_photo.empty else ""
    index_html += f"<div><h2>{row['vardas']}</h2>{photo_tag}<p>{row['aprasymas']}</p></div>"

index_html += "</body></html>"

(output_dir / "index.html").write_text(index_html, encoding='utf-8')
print("Index.html generated!")
