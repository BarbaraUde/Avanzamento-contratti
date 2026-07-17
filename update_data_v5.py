"""
Rinomina i progetti con nomi brevi in stile "Metro Milano": tipologia di trasporto + città.
Eseguire una sola volta: py update_data_v5.py
"""
import sys

sys.path.insert(0, r'C:\Users\bs_udeschini\Desktop\Progetto\Avanzamento-contratti')
from app import app, db, Progetto

RINOMINE = {
    'PROJ-CR-2026': {
        'nome': 'Metro Milano',
        'descrizione': 'Componenti e carrelli in alluminio estruso per i convogli della metropolitana di Milano'
    },
    'PROJ-MN-2026': {
        'nome': 'Regionale Torino',
        'descrizione': 'Profili in alluminio estruso per le casse dei treni regionali dell\'area di Torino'
    },
    'PROJ-SV-2026': {
        'nome': 'Tram Venezia',
        'descrizione': 'Profili verniciati per finestrini e porte dei tram della rete di Venezia-Mestre'
    },
}

with app.app_context():
    aggiornati = 0
    for codice, dati in RINOMINE.items():
        p = Progetto.query.filter_by(codice=codice).first()
        if not p:
            print(f'Progetto {codice} non trovato, saltato.')
            continue
        p.nome = dati['nome']
        p.descrizione = dati['descrizione']
        aggiornati += 1

    db.session.commit()
    print(f'Progetti rinominati: {aggiornati}')
    for p in Progetto.query.order_by(Progetto.id).all():
        print(f'  {p.codice:15s} {p.nome}')
