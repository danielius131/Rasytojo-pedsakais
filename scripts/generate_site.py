import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

# Įkeliame CSV failus
rasytojai = pd.read_csv('data/rasytojai.csv')
nuotraukos = pd.read_csv('data/nuotraukos.csv')
vietos = pd.read_csv('data/vietos.csv')
kuriniai = pd.read_csv('data/kuriniai.csv')

# Nustatome šablonų vietą
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('writer_template.html')

# Užtikrinam, kad išvesties katalogas egzistuotų
os.makedirs('site', exist_ok=True)

# Generuojame kiekvieno rašytojo puslapį
for _, r in rasytojai.iterrows():
    r_id = r['id']

    # Nuotraukos pagal writer_id
    writer_photos = nuotraukos[nuotraukos['rasytojas_id'] == r_id]

    # Pagrindinė nuotrauka
    main_photo_row = writer_photos[writer_photos['yra_pagrindine'] == True]
    main_photo = main_photo_row.iloc[0]['failas'] if not main_photo_row.empty else writer_photos.iloc[0]['failas']

    # Visos nuotraukos ciklu
    all_photos = []
    for _, row in writer_photos.iterrows():
        all_photos.append(row['failas'])

    # Kūriniai pagal rasytojas_id
    writer_kuriniai = kuriniai[kuriniai['rasytojas_id'] == r_id]['pavadinimas'].tolist()

    # Vietos pagal writer_id
    writer_vietos = vietos[vietos['writer_id'] == r_id][['name', 'lat', 'lng', 'description']].to_dict('records')

    # Sukuriame HTML puslapį iš šablono
    html = template.render(
        name=r['name'],
        birth=r['birth'],
        death=r['death'],
        region=r['region'],
        genre=r['genre'],
        biography=r['biography'],
        photo=main_photo,
        photos = [{'failas': f} for f in all_photos],
        kuriniai=writer_kuriniai,
        places=writer_vietos
    )

    # Išsaugome sugeneruotą failą
    with open(f'site/writer_{r_id}.html', 'w', encoding='utf-8') as f:
        f.write(html)

print("✅ Svetainės puslapiai sugeneruoti sėkmingai.")
