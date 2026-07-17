"""
Rinomina i progetti con denominazioni coerenti con il settore ferroviario
(Metra Rail fornisce componenti in alluminio per il materiale rotabile).
Eseguire una sola volta: py update_data_v4.py
"""
import sys

sys.path.insert(0, r'C:\Users\bs_udeschini\Desktop\Progetto\Avanzamento-contratti')
from app import app, db, Progetto

RINOMINE = {
    'PROJ-CR-2026': {
        'nome': 'Fornitura componenti in alluminio per carrelli ferroviari',
        'descrizione': 'Barre, tubolari e profili speciali in alluminio estruso con lavorazioni CNC '
                        'per carrelli e strutture portanti di materiale rotabile ferroviario'
    },
    'PROJ-MN-2026': {
        'nome': 'Fornitura profili alluminio per casse vagoni ferroviari',
        'descrizione': 'Profili estrusi lega 6060/6063 a disegno cliente per la realizzazione '
                        'di strutture di cassa di vagoni ferroviari'
    },
    'PROJ-SV-2026': {
        'nome': 'Fornitura profili verniciati per finestrini e porte carrozze ferroviarie',
        'descrizione': 'Profili alluminio estruso e verniciato a polvere per finestrini, '
                        'porte e telai di carrozze ferroviarie'
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
