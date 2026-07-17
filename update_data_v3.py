"""
Espansione dataset dimostrativo:
- Aggiunge nuovi contratti per ciascun cliente esistente (con ordini, varianti, allegati,
  fatturato) riutilizzando i documenti gia' presenti in Documenti/ come allegati dimostrativi
- Amplia l'elenco articoli di TUTTI i contratti esistenti e nuovi
Eseguire una sola volta: py update_data_v3.py
"""
import sys
from datetime import date

sys.path.insert(0, r'C:\Users\bs_udeschini\Desktop\Progetto\Avanzamento-contratti')
from app import app, db, Cliente, Progetto, Contratto, Ordine, Variante, Allegato, RigaFatturato, Articolo

BASE      = r'C:\Users\bs_udeschini\Desktop\Progetto'
BASE_DOCS = BASE + r'\Documenti'

with app.app_context():

    cr = Cliente.query.filter_by(codice='CR').first()
    mn = Cliente.query.filter_by(codice='MN').first()
    sv = Cliente.query.filter_by(codice='SV').first()
    p_cr = Progetto.query.filter_by(codice='PROJ-CR-2026').first()
    p_mn = Progetto.query.filter_by(codice='PROJ-MN-2026').first()
    p_sv = Progetto.query.filter_by(codice='PROJ-SV-2026').first()

    if not all([cr, mn, sv, p_cr, p_mn, p_sv]):
        print("Errore: dati base non trovati. Eseguire prima seed_data.py e update_data.py.")
        sys.exit(1)

    # Documenti disponibili per cliente, riutilizzati come allegati dimostrativi
    DOCS = {
        'CR': {
            'contratti': [BASE + r'\Contratto_Fornitura_Componenti_Rossi.docx',
                          BASE_DOCS + r'\Contratti\Contratto2_Componenti_Rossi.docx',
                          BASE_DOCS + r'\Contratti\Contratto3_Fornitura_Componenti_Rossi.docx'],
            'offerte':   [BASE + r'\Offerta_Componenti_Rossi.pdf',
                          BASE_DOCS + r'\Offerte\Offerta2_Componenti_Rossi.pdf',
                          BASE_DOCS + r'\Offerte\Offerta_Componenti_Rossi3.pdf'],
            'ordini':    [BASE + r'\Ordine_Componenti_Rossi.pdf',
                          BASE_DOCS + r'\Ordini\Ordine2_Componenti_Rossi.pdf',
                          BASE_DOCS + r'\Offerte\Ordine3_Componenti_Rossi.pdf'],
            'revisioni': [BASE + r'\Revisione2_Componenti_Rossi.docx',
                          BASE_DOCS + r'\Revisioni\Revisione2.2_Componenti_Rossi.docx'],
        },
        'MN': {
            'contratti': [BASE + r'\Contratto_Fornitura_Meccanica_Nord.docx',
                          BASE_DOCS + r'\Contratti\Contratto2_Meccanica_Nord.docx',
                          BASE_DOCS + r'\Contratti\Contratto3_Fornitura_Meccanica_Nord.docx'],
            'offerte':   [BASE + r'\Offerta_Meccanica_Nord.pdf',
                          BASE_DOCS + r'\Offerte\Offerta2_Meccanica_Nord.pdf',
                          BASE_DOCS + r'\Offerte\Offerta_Meccanica_Nord3.pdf'],
            'ordini':    [BASE + r'\Ordine_Meccanica_Nord.pdf',
                          BASE_DOCS + r'\Ordini\Ordine2_Meccanica_Nord.pdf',
                          BASE_DOCS + r'\Offerte\Ordine3_Meccanica_Nord.pdf'],
            'revisioni': [BASE + r'\Revisione1_Meccanica_Nord.docx',
                          BASE_DOCS + r'\Revisioni\Revisione1.1_Meccanica_Nord.docx'],
        },
        'SV': {
            'contratti': [BASE + r'\Contratto_Fornitura_Serramenti_Veneti.docx',
                          BASE_DOCS + r'\Contratti\Contratto2_Serramenti_Veneti.docx',
                          BASE_DOCS + r'\Contratti\Contratto3_Fornitura_Serramenti_Veneti.docx'],
            'offerte':   [BASE + r'\Offerta_Serramenti_Veneti.pdf',
                          BASE_DOCS + r'\Offerte\Offerta2_Serramenti_Veneti.pdf',
                          BASE_DOCS + r'\Offerte\Offerta_Serramenti_Veneti3.pdf'],
            'ordini':    [BASE + r'\Ordine_Serramenti_Veneti.pdf',
                          BASE_DOCS + r'\Ordini\Ordine2_Serramenti_Veneti.pdf',
                          BASE_DOCS + r'\Offerte\Ordine3_Serramenti_Veneti.pdf'],
            'revisioni': [BASE + r'\Revisione3_Serramenti_Veneti.docx',
                          BASE_DOCS + r'\Revisioni\Revisione3.3_Serramenti_Veneti.docx'],
        },
    }

    # Catalogo articoli aggiuntivi per famiglia cliente (codice, descrizione, u.m., prezzo)
    CATALOGO_CR = [
        ('AL-BR-3310', 'Barra estrusa lega 6082, sez.50x30mm, L=3000mm', 'pz', 45.30),
        ('AL-TU-2210', 'Tubolare rettangolare 60x30x2mm, L=6000mm', 'pz', 20.40),
        ('AL-PR-3050', 'Profilo estruso speciale sez. L45, L=6000mm', 'pz', 12.90),
        ('AL-BR-3405', 'Barra estrusa lega 6060, sez. tonda D40mm, L=3000mm', 'pz', 15.20),
        ('AL-TU-2318', 'Tubolare quadro 40x40x2mm, L=6000mm', 'pz', 16.75),
        ('AL-PR-3620', 'Profilo a T 25mm, lega 6082, L=6000mm', 'pz', 9.60),
        ('AL-BR-3711', 'Barra piatta 60x8mm, lega 6060, L=4000mm', 'pz', 11.10),
        ('AL-PR-3855', 'Profilo a L 30x30x2mm, lega 6060, L=6000mm', 'pz', 7.85),
        ('AL-TU-2450', 'Tubolare tondo D50x2mm, L=6000mm', 'pz', 22.30),
        ('AL-PR-3920', 'Profilo speciale con lavorazione CNC di foratura', 'pz', 18.40),
    ]
    CATALOGO_MN = [
        ('AL-PR-1042', 'Profilo estruso lega 6060, sez.40x40mm, L=6000mm', 'pz', 4.40),
        ('AL-PR-2075', 'Profilo lega 6063, sez. speciale a disegno, L=6000mm', 'pz', 7.85),
        ('AL-PR-1088', 'Profilo estruso lega 6060, sez.30x30mm, L=6000mm', 'pz', 3.25),
        ('AL-PR-1055', 'Profilo estruso lega 6060, sez.50x50mm, L=6000mm', 'pz', 6.15),
        ('AL-PR-1120', 'Profilo estruso lega 6063, sez.25x25mm, L=6000mm', 'pz', 2.90),
        ('AL-PR-1140', 'Profilo estruso lega 6060, sez.60x20mm, L=6000mm', 'pz', 5.10),
        ('AL-PR-1165', 'Profilo estruso lega 6063 con foratura a disegno', 'pz', 8.70),
        ('AL-PR-1190', 'Profilo estruso lega 6060, sez.35x35mm, L=6000mm', 'pz', 3.95),
        ('AL-PR-1205', 'Profilo estruso lega 6082, sez.45x45mm, L=6000mm', 'pz', 6.80),
        ('AL-PR-1230', 'Profilo estruso lega 6060, sez. a C 40mm, L=6000mm', 'pz', 4.75),
    ]
    CATALOGO_SV = [
        ('AL-SR-6210', 'Profilo anta 60mm, alluminio estruso verniciato a polvere', 'pz', 37.15),
        ('AL-SR-5180', 'Profilo telaio fisso 80mm, alluminio estruso verniciato', 'pz', 44.50),
        ('AL-SR-4090', 'Fermavetro 9mm, profilo a T, L=6000mm', 'pz', 2.90),
        ('AL-SR-7015', 'Profilo anta scorrevole 70mm, verniciato RAL', 'pz', 41.20),
        ('AL-SR-6340', 'Profilo telaio mobile 60mm, verniciato a polvere', 'pz', 38.60),
        ('AL-SR-5520', 'Profilo giunzione angolare 45mm, verniciato', 'pz', 12.30),
        ('AL-SR-4890', 'Profilo copri filo 30mm, verniciato RAL a campione', 'pz', 6.45),
        ('AL-SR-7280', 'Profilo soglia ribassata 50mm, verniciato', 'pz', 27.90),
        ('AL-SR-6055', 'Profilo maniglione 100mm, alluminio anodizzato', 'pz', 19.80),
        ('AL-SR-5910', 'Profilo persiana a lamelle 40mm, verniciato RAL', 'pz', 33.40),
    ]
    CATALOGHI = {'CR': CATALOGO_CR, 'MN': CATALOGO_MN, 'SV': CATALOGO_SV}

    # ============================================================
    # 1) AMPLIA ARTICOLI DEI CONTRATTI ESISTENTI
    # ============================================================
    tutti_i_contratti = Contratto.query.order_by(Contratto.id).all()
    articoli_aggiunti = 0
    for c in tutti_i_contratti:
        codice_cliente = c.cliente.codice
        catalogo = CATALOGHI.get(codice_cliente, [])
        codici_presenti = {a.codice for a in c.articoli}
        pct_avanzamento_target = 1.0 if c.stato == 'chiuso' else (0.5 if c.stato == 'in corso' else 0.0)
        for codice, descr, um, prezzo in catalogo:
            if codice in codici_presenti:
                continue
            q_tot = 1000 + (hash(codice + c.codice) % 4000)
            q_sped = int(q_tot * pct_avanzamento_target)
            db.session.add(Articolo(
                contratto_id=c.id, codice=codice, descrizione=descr,
                quantita_totale=q_tot, quantita_spedita=q_sped,
                unita_misura=um, prezzo_unitario=prezzo
            ))
            articoli_aggiunti += 1

    # ============================================================
    # 2) NUOVI CONTRATTI (2 per cliente) CON ORDINI / VARIANTI / ALLEGATI / FATTURATO
    # ============================================================
    nuovi_contratti_def = [
        # (cliente, progetto, codice, descrizione, valore, stato, apertura, chiusura, note)
        (cr, p_cr, 'CON-2028-CR-001', 'Fornitura barre e profili speciali — lotto primaverile',
         215000.00, 'aperto', date(2028, 3, 1), date(2029, 2, 28),
         'FCA Ciserano. Ri.Ba. 60gg dfm. Ind. LME ±8% cap.'),
        (cr, p_cr, 'CON-2028-CR-002', 'Fornitura barre e tubolari — estensione linea CNC',
         168500.00, 'in corso', date(2028, 6, 1), date(2029, 5, 31),
         'FCA Ciserano. Bonifico 45gg dfm. Lavorazioni CNC incluse.'),
        (mn, p_mn, 'CON-2028-MN-001', 'Fornitura profili estrusi — nuova gamma sezioni',
         112000.00, 'aperto', date(2028, 2, 1), date(2029, 1, 31),
         'EXW Ciserano. Bonifico 60gg dfm.'),
        (mn, p_mn, 'CON-2028-MN-002', 'Rinnovo annuale fornitura profili 6060/6063',
         134750.00, 'chiuso', date(2027, 10, 1), date(2028, 9, 30),
         'EXW Ciserano. Commessa chiusa, saldo incassato.'),
        (sv, p_sv, 'CON-2028-SV-001', 'Fornitura profili serramenti — lotto C nuova gamma',
         198300.00, 'in corso', date(2028, 1, 1), date(2029, 6, 30),
         'DAP Treviso. Acconto 30% + saldo 45gg dfm. Qualicoat.'),
        (sv, p_sv, 'CON-2028-SV-002', 'Fornitura profili scorrevoli e persiane',
         145900.00, 'aperto', date(2028, 5, 1), date(2029, 4, 30),
         'DAP Treviso. Verniciatura Qualicoat. Prezzi fissi 9 mesi.'),
    ]

    nuovi_contratti = []
    for cliente_obj, progetto_obj, codice, descr, valore, stato, apertura, chiusura, note in nuovi_contratti_def:
        esistente = Contratto.query.filter_by(codice=codice).first()
        if esistente:
            nuovi_contratti.append(esistente)
            continue
        c = Contratto(
            cliente_id=cliente_obj.id, progetto_id=progetto_obj.id,
            codice=codice, descrizione=descr, valore_totale=valore, stato=stato,
            data_apertura=apertura, data_chiusura=chiusura, note=note
        )
        db.session.add(c)
        nuovi_contratti.append(c)
    db.session.flush()

    contratti_creati = 0
    for c in nuovi_contratti:
        if c.id and Allegato.query.filter_by(contratto_id=c.id).count() > 0:
            continue  # gia' popolato in un run precedente
        contratti_creati += 1
        cod_cli = c.cliente.codice
        docs = DOCS[cod_cli]

        # Allegati: contratto + offerta + ordine (documenti riutilizzati come demo)
        db.session.add_all([
            Allegato(contratto_id=c.id, tipo='contratto',
                     nome=f'Contratto fornitura {c.codice}',
                     percorso=docs['contratti'][contratti_creati % len(docs['contratti'])],
                     note=f'Firmato {c.data_apertura.strftime("%d/%m/%Y")}. Durata secondo capitolato.'),
            Allegato(contratto_id=c.id, tipo='offerta',
                     nome=f'Offerta base {c.codice}',
                     percorso=docs['offerte'][contratti_creati % len(docs['offerte'])],
                     note=f'Offerta a base del contratto {c.codice}. Validita\' 30gg.'),
            Allegato(contratto_id=c.id, tipo='ordine',
                     nome=f'Primo ordine {c.codice}',
                     percorso=docs['ordini'][contratti_creati % len(docs['ordini'])],
                     note='Primo call-off collegato al contratto.'),
        ])

        # Ordini (2-3 per contratto)
        n_ordini = 2 if c.stato == 'aperto' else 3
        for i in range(1, n_ordini + 1):
            db.session.add(Ordine(
                contratto_id=c.id,
                numero_ordine=f'ORD-{c.codice.split("-", 1)[1]}-{i:03d}',
                data=date(c.data_apertura.year, min(12, c.data_apertura.month + i * 2), 10),
                importo=round(c.valore_totale / (n_ordini + 1), 2),
                stato='evaso' if c.stato == 'chiuso' else ('parziale' if i < n_ordini else 'aperto'),
                note=f'Call-off n.{i} su contratto {c.codice}.'
            ))

        # Variante (solo se il contratto non e' appena aperto)
        if c.stato in ('in corso', 'chiuso'):
            db.session.add(Variante(
                contratto_id=c.id, numero=1,
                data=date(c.data_apertura.year, min(12, c.data_apertura.month + 6), 15),
                descrizione=f'Addendum n.1 — aggiornamento quantitativi e condizioni economiche {c.codice}.',
                valore_delta=0.0,
                percorso_allegato=docs['revisioni'][0]
            ))

        # Articoli (dal catalogo del cliente)
        catalogo = CATALOGHI[cod_cli]
        pct_target = 1.0 if c.stato == 'chiuso' else (0.45 if c.stato == 'in corso' else 0.0)
        for codice_art, descr_art, um, prezzo in catalogo[:7]:
            q_tot = 1200 + (hash(codice_art + c.codice) % 3500)
            q_sped = int(q_tot * pct_target)
            db.session.add(Articolo(
                contratto_id=c.id, codice=codice_art, descrizione=descr_art,
                quantita_totale=q_tot, quantita_spedita=q_sped,
                unita_misura=um, prezzo_unitario=prezzo
            ))

        # Fatturato coerente con lo stato (solo per in corso / chiuso)
        if c.stato in ('in corso', 'chiuso'):
            importo_riga = round(c.valore_totale * pct_target / 3, 2)
            for i in range(3):
                db.session.add(RigaFatturato(
                    contratto_id=c.id, cliente_id=c.cliente_id, progetto_id=c.progetto_id,
                    data_documento=date(c.data_apertura.year, min(12, c.data_apertura.month + i + 1), 20),
                    numero_documento=f'DDT-{c.codice}-{i+1:03d}',
                    importo=importo_riga,
                    descrizione=f'Spedizione parziale {i+1} — contratto {c.codice}',
                    fonte='Fatturato_Contratti_Parziale.xlsx'
                ))

    db.session.commit()

    print("Aggiornamento v3 completato!")
    print(f"  Contratti totali:   {Contratto.query.count()} (nuovi creati: {contratti_creati})")
    print(f"  Articoli totali:    {Articolo.query.count()} (aggiunti su esistenti: {articoli_aggiunti})")
    print(f"  Ordini totali:      {Ordine.query.count()}")
    print(f"  Varianti totali:    {Variante.query.count()}")
    print(f"  Allegati totali:    {Allegato.query.count()}")
    print(f"  Righe fatturato:    {RigaFatturato.query.count()}")
