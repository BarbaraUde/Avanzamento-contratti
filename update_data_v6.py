"""
Ogni cliente aveva un solo progetto con tutti i contratti agganciati sotto lo stesso nome.
Crea invece piu' progetti distinti per cliente (tipologia di trasporto + citta') e
ridistribuisce i contratti esistenti su progetti diversi.
Eseguire una sola volta: py update_data_v6.py
"""
import sys

sys.path.insert(0, r'C:\Users\bs_udeschini\Desktop\Progetto\Avanzamento-contratti')
from app import app, db, Cliente, Progetto, Contratto

# Per ciascun cliente: progetto esistente (rinominato/riusato) + nuovi progetti.
# Il primo elemento riutilizza il progetto gia' presente, gli altri vengono creati.
PIANO = {
    'CR': [
        ('PROJ-CR-2026', 'Metro Milano',
         'Componenti e carrelli in alluminio estruso per i convogli della metropolitana di Milano'),
        ('PROJ-CR-2027', 'Regionale Bologna',
         'Profili e barre in alluminio per treni regionali sulla direttrice bolognese'),
        ('PROJ-CR-2028A', 'Alta Velocita\' Firenze',
         'Componenti in alluminio ad alta resistenza per convogli alta velocita\' Firenze'),
        ('PROJ-CR-2028B', 'Tram Modena',
         'Profili e tubolari in alluminio per la rete tranviaria di Modena'),
    ],
    'MN': [
        ('PROJ-MN-2026', 'Regionale Torino',
         'Profili in alluminio estruso per le casse dei treni regionali dell\'area di Torino'),
        ('PROJ-MN-2027', 'Metro Torino',
         'Profili estrusi lega 6060/6063 per le casse dei convogli della metropolitana di Torino'),
        ('PROJ-MN-2028A', 'Tram Novara',
         'Profili in alluminio estruso per il rinnovo del parco tram di Novara'),
        ('PROJ-MN-2028B', 'Regionale Genova',
         'Profili in alluminio per treni regionali della linea genovese'),
    ],
    'SV': [
        ('PROJ-SV-2026', 'Tram Venezia',
         'Profili verniciati per finestrini e porte dei tram della rete di Venezia-Mestre'),
        ('PROJ-SV-2027', 'Regionale Verona',
         'Profili alluminio verniciato per finestrini e porte di treni regionali veronesi'),
        ('PROJ-SV-2028A', 'Alta Velocita\' Padova',
         'Profili verniciati per finestrini e porte di convogli alta velocita\' in transito da Padova'),
        ('PROJ-SV-2028B', 'Tram Vicenza',
         'Profili verniciati per finestrini e porte della rete tranviaria di Vicenza'),
    ],
}

with app.app_context():
    for codice_cliente, progetti_def in PIANO.items():
        cliente = Cliente.query.filter_by(codice=codice_cliente).first()
        if not cliente:
            print(f'Cliente {codice_cliente} non trovato, saltato.')
            continue

        contratti = Contratto.query.filter_by(cliente_id=cliente.id).order_by(Contratto.id).all()
        if len(contratti) != len(progetti_def):
            print(f'{codice_cliente}: attesi {len(progetti_def)} contratti, trovati {len(contratti)} — '
                  f'assegno quelli disponibili in ordine.')

        for i, (codice_prog, nome, descr) in enumerate(progetti_def):
            progetto_esistente = Progetto.query.filter_by(cliente_id=cliente.id).first() if i == 0 else None
            if i == 0 and progetto_esistente:
                p = progetto_esistente
                p.codice = codice_prog
                p.nome = nome
                p.descrizione = descr
            else:
                p = Progetto.query.filter_by(codice=codice_prog).first()
                if not p:
                    p = Progetto(cliente_id=cliente.id, codice=codice_prog, nome=nome,
                                 descrizione=descr, stato='aperto')
                    db.session.add(p)
                else:
                    p.nome = nome
                    p.descrizione = descr
            db.session.flush()

            if i < len(contratti):
                contratti[i].progetto_id = p.id

    db.session.commit()

    print('Struttura cliente → progetti → contratti aggiornata:')
    for cl in Cliente.query.order_by(Cliente.id).all():
        print(cl.nome)
        for p in cl.progetti:
            codici = [c.codice for c in p.contratti]
            print(f'  {p.nome:30s} {codici}')
