"""
Aggiornamento database:
- Aggiunge allegati per nuovi documenti (Contratto2, Offerta2, Ordine2)
- Crea 3 nuovi contratti (CON-2) per varietà di stato
- Aggiorna stati: CR→chiuso (100%), MN→in corso (63%), SV→aperto (0%)
- Aggiunge righe fatturato per CR e per il nuovo CON-2-SV
- Aggiunge articoli a tutti i contratti
Eseguire una sola volta: py update_data.py
"""
import sys
from datetime import date

sys.path.insert(0, r'C:\Users\bs_udeschini\Desktop\Progetto\Avanzamento-contratti')
from app import app, db, Cliente, Progetto, Contratto, Ordine, Variante, Allegato, RigaFatturato, Articolo

BASE      = r'C:\Users\bs_udeschini\Desktop\Progetto'
BASE_DOCS = BASE + r'\Documenti'

with app.app_context():

    # ------------------------------------------------------------------ lookup
    cr = Cliente.query.filter_by(codice='CR').first()
    mn = Cliente.query.filter_by(codice='MN').first()
    sv = Cliente.query.filter_by(codice='SV').first()
    p_cr = Progetto.query.filter_by(codice='PROJ-CR-2026').first()
    p_mn = Progetto.query.filter_by(codice='PROJ-MN-2026').first()
    p_sv = Progetto.query.filter_by(codice='PROJ-SV-2026').first()
    c_cr = Contratto.query.filter_by(codice='CON-2026-CR-001').first()
    c_mn = Contratto.query.filter_by(codice='CON-2026-MN-001').first()
    c_sv = Contratto.query.filter_by(codice='CON-2026-SV-001').first()

    if not all([cr, mn, sv, c_cr, c_mn, c_sv]):
        print("Errore: dati base non trovati. Eseguire prima seed_data.py.")
        sys.exit(1)

    # ============================================================
    # 1) AGGIORNA STATI contratti esistenti
    # ============================================================
    c_cr.stato = 'chiuso'
    c_mn.stato = 'in corso'
    c_sv.stato = 'aperto'

    # ============================================================
    # 2) ALLEGATI NUOVI DOCUMENTI (Contratto2, Offerta2, Ordine2)
    # ============================================================
    nuovi_allegati = [
        # Componenti Rossi — secondi documenti
        Allegato(contratto_id=c_cr.id, tipo='contratto',
                 nome='Contratto fornitura v2 CON-2026-CR-001',
                 percorso=BASE_DOCS + r'\Contratti\Contratto2_Componenti_Rossi.docx',
                 note='Revisione contratto con aggiornamento condizioni LME e nuovi articoli.'),
        Allegato(contratto_id=c_cr.id, tipo='offerta',
                 nome='Offerta aggiornata OFF-2026-0168-R1',
                 percorso=BASE_DOCS + r'\Offerte\Offerta2_Componenti_Rossi.pdf',
                 note='Revisione offerta con adeguamento prezzi secondo accordo integrativo.'),
        Allegato(contratto_id=c_cr.id, tipo='ordine',
                 nome='Ordine ORD-CR-2026-028 — secondo call-off',
                 percorso=BASE_DOCS + r'\Ordini\Ordine2_Componenti_Rossi.pdf',
                 note='Secondo ordinativo trimestrale. Saldo commessa.'),
        # Meccanica Nord — secondi documenti
        Allegato(contratto_id=c_mn.id, tipo='contratto',
                 nome='Contratto fornitura v2 CON-2026-MN-001',
                 percorso=BASE_DOCS + r'\Contratti\Contratto2_Meccanica_Nord.docx',
                 note='Rinnovo contratto post addendum con modifica quantitativi.'),
        Allegato(contratto_id=c_mn.id, tipo='offerta',
                 nome='Offerta aggiornata OFF-2026-0142-R1',
                 percorso=BASE_DOCS + r'\Offerte\Offerta2_Meccanica_Nord.pdf',
                 note='Offerta integrativa post variante n.1.'),
        Allegato(contratto_id=c_mn.id, tipo='ordine',
                 nome='Ordine ORD-MN-2026-012 — secondo call-off',
                 percorso=BASE_DOCS + r'\Ordini\Ordine2_Meccanica_Nord.pdf',
                 note='Secondo ordinativo. Resa EXW Ciserano.'),
        # Serramenti Veneti — secondi documenti
        Allegato(contratto_id=c_sv.id, tipo='contratto',
                 nome='Contratto fornitura v2 CON-2026-SV-001',
                 percorso=BASE_DOCS + r'\Contratti\Contratto2_Serramenti_Veneti.docx',
                 note='Aggiornamento gamma serramenti e annullamento fermavetro.'),
        Allegato(contratto_id=c_sv.id, tipo='offerta',
                 nome='Offerta aggiornata OFF-2026-0201-R1',
                 percorso=BASE_DOCS + r'\Offerte\Offerta2_Serramenti_Veneti.pdf',
                 note='Revisione prezzi post variante n.1.'),
        Allegato(contratto_id=c_sv.id, tipo='ordine',
                 nome='Ordine ORD-SV-2026-015 — secondo call-off',
                 percorso=BASE_DOCS + r'\Ordini\Ordine2_Serramenti_Veneti.pdf',
                 note='Secondo programma mensile. DAP Treviso.'),
    ]
    db.session.add_all(nuovi_allegati)

    # ============================================================
    # 3) FATTURATO per CR → portare a ~100% (chiuso)
    # ============================================================
    righe_cr = [
        (date(2026, 11, 10), 'DDT-2026-CR-0201', 45750.00,
         'AL-BR-3310 — 1.000 pz × €45,75 — Barra estrusa lega 6082, sez.50x30mm, L=3000mm'),
        (date(2026, 11, 20), 'DDT-2026-CR-0215', 38250.00,
         'AL-BR-3310 — 850 pz × €45,00 — Barra estrusa lega 6082, sez.50x30mm, L=3000mm'),
        (date(2026, 12, 5),  'DDT-2026-CR-0248', 52100.00,
         'AL-TU-2210 — 2.600 pz × €20,04 — Tubolare rettangolare 60x30x2mm L=6000mm'),
        (date(2026, 12, 18), 'DDT-2026-CR-0267', 48900.00,
         'AL-TU-2210 — 2.400 pz × €20,38 — Tubolare rettangolare 60x30x2mm L=6000mm'),
        (date(2027, 1, 12),  'DDT-2027-CR-0018', 39415.00,
         'AL-BR-3310 — 870 pz × €45,30 — Barra estrusa lega 6082, sez.50x30mm, L=3000mm'),
        (date(2027, 1, 25),  'DDT-2027-CR-0031', 31700.00,
         'AL-TU-2210 — 1.550 pz × €20,45 — Tubolare rettangolare 60x30x2mm L=6000mm'),
        (date(2027, 2, 10),  'DDT-2027-CR-0055', 45025.00,
         'AL-PR-3050 — 3.500 pz × €12,86 — Profilo estruso speciale, sez. L45, L=6000mm'),
    ]
    for dt, ddt, importo, descr in righe_cr:
        db.session.add(RigaFatturato(
            contratto_id=c_cr.id, cliente_id=cr.id, progetto_id=p_cr.id,
            data_documento=dt, numero_documento=ddt,
            importo=importo, descrizione=descr,
            fonte='Fatturato_Contratti_Parziale.xlsx'
        ))

    # ============================================================
    # 4) NUOVI CONTRATTI CON-2 (uno per cliente)
    # ============================================================
    c2_mn = Contratto(
        cliente_id=mn.id, progetto_id=p_mn.id,
        codice='CON-2027-MN-001',
        descrizione='Rinnovo fornitura profili alluminio lega 6060/6063 — 12 mesi',
        valore_totale=98500.00,
        stato='aperto',
        data_apertura=date(2027, 9, 1),
        data_chiusura=date(2028, 8, 31),
        note='EXW Ciserano. Bonifico 60gg dfm. Prezzi fissi per 6 mesi con clausola LME.'
    )
    c2_cr = Contratto(
        cliente_id=cr.id, progetto_id=p_cr.id,
        codice='CON-2027-CR-001',
        descrizione='Fornitura barre e profilati alluminio — estensione 18 mesi',
        valore_totale=185000.00,
        stato='in corso',
        data_apertura=date(2027, 3, 1),
        data_chiusura=date(2028, 8, 31),
        note='FCA Ciserano. Ri.Ba. 60gg dfm. Nuovo accordo prezzi post rinnovo.'
    )
    c2_sv = Contratto(
        cliente_id=sv.id, progetto_id=p_sv.id,
        codice='CON-2026-SV-002',
        descrizione='Seconda fornitura profili serramenti verniciati — lotto B',
        valore_totale=132800.00,
        stato='chiuso',
        data_apertura=date(2026, 12, 1),
        data_chiusura=date(2027, 6, 30),
        note='DAP Treviso. Acconto 30% + saldo a 45gg. Qualicoat. Commessa chiusa.'
    )
    db.session.add_all([c2_mn, c2_cr, c2_sv])
    db.session.flush()

    # Allegati nuovi contratti
    db.session.add_all([
        Allegato(contratto_id=c2_mn.id, tipo='contratto',
                 nome='Contratto fornitura CON-2027-MN-001',
                 percorso=BASE_DOCS + r'\Contratti\Contratto2_Meccanica_Nord.docx',
                 note='Rinnovo annuale. Firmato 01/09/2027.'),
        Allegato(contratto_id=c2_mn.id, tipo='offerta',
                 nome='Offerta OFF-2027-0142',
                 percorso=BASE_DOCS + r'\Offerte\Offerta2_Meccanica_Nord.pdf',
                 note='Offerta rinnovo. Validità 30gg.'),
        Allegato(contratto_id=c2_cr.id, tipo='contratto',
                 nome='Contratto fornitura CON-2027-CR-001',
                 percorso=BASE_DOCS + r'\Contratti\Contratto2_Componenti_Rossi.docx',
                 note='Estensione 18 mesi. Firmato 01/03/2027.'),
        Allegato(contratto_id=c2_cr.id, tipo='offerta',
                 nome='Offerta OFF-2027-0168',
                 percorso=BASE_DOCS + r'\Offerte\Offerta2_Componenti_Rossi.pdf',
                 note='Offerta estensione. Validità 45gg.'),
        Allegato(contratto_id=c2_cr.id, tipo='ordine',
                 nome='Ordine ORD-CR-2027-001 — primo call-off',
                 percorso=BASE_DOCS + r'\Ordini\Ordine2_Componenti_Rossi.pdf',
                 note='Primo call-off nuovo contratto. Importo €82.000.'),
        Allegato(contratto_id=c2_sv.id, tipo='contratto',
                 nome='Contratto fornitura CON-2026-SV-002',
                 percorso=BASE_DOCS + r'\Contratti\Contratto2_Serramenti_Veneti.docx',
                 note='Lotto B. Firmato 01/12/2026. Chiuso 30/06/2027.'),
        Allegato(contratto_id=c2_sv.id, tipo='ordine',
                 nome='Ordine ORD-SV-2026-022 — lotto B completo',
                 percorso=BASE_DOCS + r'\Ordini\Ordine2_Serramenti_Veneti.pdf',
                 note='Ordine unico lotto B. Evaso integralmente.'),
    ])

    # Ordini CON-2
    db.session.add_all([
        Ordine(contratto_id=c2_cr.id, numero_ordine='ORD-CR-2027-001',
               data=date(2027, 3, 15), importo=82000.00, stato='parziale',
               note='Primo call-off. Consegna in 3 tranche. Resa FCA Ciserano.'),
        Ordine(contratto_id=c2_sv.id, numero_ordine='ORD-SV-2026-022',
               data=date(2026, 12, 10), importo=132800.00, stato='evaso',
               note='Lotto B completo. Evaso con DDT 0289-0295-0312. Resa DAP Treviso.'),
    ])

    # Fatturato CON-2-CR (in corso ~44%)
    for dt, ddt, importo, descr in [
        (date(2027, 4, 10), 'DDT-2027-CR-0098', 38500.00,
         'AL-BR-3310 — 850 pz × €45,29 — Barra estrusa lega 6082, sez.50x30mm'),
        (date(2027, 5, 8),  'DDT-2027-CR-0121', 43800.00,
         'AL-TU-2210 — 2.150 pz × €20,37 — Tubolare rettangolare 60x30x2mm'),
    ]:
        db.session.add(RigaFatturato(
            contratto_id=c2_cr.id, cliente_id=cr.id, progetto_id=p_cr.id,
            data_documento=dt, numero_documento=ddt,
            importo=importo, descrizione=descr,
            fonte='Fatturato_Contratti_Parziale.xlsx'
        ))

    # Fatturato CON-2-SV (chiuso ~100%)
    for dt, ddt, importo, descr in [
        (date(2027, 1, 15), 'DDT-2027-SV-0041', 44500.00,
         'AL-SR-6210 — 1.200 pz × €37,08 — Profilo anta 60mm verniciato RAL'),
        (date(2027, 2, 20), 'DDT-2027-SV-0068', 48300.00,
         'AL-SR-6210 — 1.300 pz × €37,15 — Profilo anta 60mm verniciato RAL'),
        (date(2027, 3, 18), 'DDT-2027-SV-0095', 40000.00,
         'AL-SR-5180 — 900 pz × €44,44 — Profilo telaio fisso 80mm verniciato'),
    ]:
        db.session.add(RigaFatturato(
            contratto_id=c2_sv.id, cliente_id=sv.id, progetto_id=p_sv.id,
            data_documento=dt, numero_documento=ddt,
            importo=importo, descrizione=descr,
            fonte='Fatturato_Contratti_Parziale.xlsx'
        ))

    # ============================================================
    # 5) ARTICOLI per ogni contratto
    # ============================================================

    # CON-2026-CR-001 (chiuso)
    db.session.add_all([
        Articolo(contratto_id=c_cr.id, codice='AL-BR-3310',
                 descrizione='Barra estrusa lega 6082, sez.50x30mm, L=3000mm',
                 quantita_totale=2720, quantita_spedita=2720,
                 unita_misura='pz', prezzo_unitario=45.25),
        Articolo(contratto_id=c_cr.id, codice='AL-TU-2210',
                 descrizione='Tubolare rettangolare 60x30x2mm, L=6000mm',
                 quantita_totale=6550, quantita_spedita=6550,
                 unita_misura='pz', prezzo_unitario=20.35),
        Articolo(contratto_id=c_cr.id, codice='AL-PR-3050',
                 descrizione='Profilo estruso speciale sez. L45, L=6000mm',
                 quantita_totale=3500, quantita_spedita=3500,
                 unita_misura='pz', prezzo_unitario=12.86),
    ])

    # CON-2026-MN-001 (in corso)
    db.session.add_all([
        Articolo(contratto_id=c_mn.id, codice='AL-PR-1042',
                 descrizione='Profilo estruso lega 6060, sez.40x40mm, L=6000mm',
                 quantita_totale=12500, quantita_spedita=12500,
                 unita_misura='pz', prezzo_unitario=4.35),
        Articolo(contratto_id=c_mn.id, codice='AL-PR-2075',
                 descrizione='Profilo lega 6063, sez. speciale a disegno, L=6000mm',
                 quantita_totale=5000, quantita_spedita=3500,
                 unita_misura='pz', prezzo_unitario=7.80),
        Articolo(contratto_id=c_mn.id, codice='AL-PR-1088',
                 descrizione='Profilo estruso lega 6060, sez.30x30mm, L=6000mm',
                 quantita_totale=4000, quantita_spedita=0,
                 unita_misura='pz', prezzo_unitario=3.20),
    ])

    # CON-2026-SV-001 (aperto, 0%)
    db.session.add_all([
        Articolo(contratto_id=c_sv.id, codice='AL-SR-6210',
                 descrizione='Profilo anta 60mm, alluminio estruso verniciato a polvere',
                 quantita_totale=5800, quantita_spedita=0,
                 unita_misura='pz', prezzo_unitario=37.10),
        Articolo(contratto_id=c_sv.id, codice='AL-SR-5180',
                 descrizione='Profilo telaio fisso 80mm, alluminio estruso verniciato',
                 quantita_totale=3200, quantita_spedita=0,
                 unita_misura='pz', prezzo_unitario=44.50),
        Articolo(contratto_id=c_sv.id, codice='AL-SR-4090',
                 descrizione='Fermavetro 9mm, profilo a T, L=6000mm',
                 quantita_totale=8000, quantita_spedita=0,
                 unita_misura='pz', prezzo_unitario=2.85),
    ])

    # CON-2027-MN-001 (aperto, 0%)
    db.session.add_all([
        Articolo(contratto_id=c2_mn.id, codice='AL-PR-1042',
                 descrizione='Profilo estruso lega 6060, sez.40x40mm, L=6000mm',
                 quantita_totale=9000, quantita_spedita=0,
                 unita_misura='pz', prezzo_unitario=4.50),
        Articolo(contratto_id=c2_mn.id, codice='AL-PR-1055',
                 descrizione='Profilo estruso lega 6060, sez.50x50mm, L=6000mm',
                 quantita_totale=5500, quantita_spedita=0,
                 unita_misura='pz', prezzo_unitario=6.10),
    ])

    # CON-2027-CR-001 (in corso, ~44%)
    db.session.add_all([
        Articolo(contratto_id=c2_cr.id, codice='AL-BR-3310',
                 descrizione='Barra estrusa lega 6082, sez.50x30mm, L=3000mm',
                 quantita_totale=1800, quantita_spedita=850,
                 unita_misura='pz', prezzo_unitario=45.29),
        Articolo(contratto_id=c2_cr.id, codice='AL-TU-2210',
                 descrizione='Tubolare rettangolare 60x30x2mm, L=6000mm',
                 quantita_totale=4200, quantita_spedita=2150,
                 unita_misura='pz', prezzo_unitario=20.37),
        Articolo(contratto_id=c2_cr.id, codice='AL-PR-3080',
                 descrizione='Profilo a C 80mm, lega 6082, L=6000mm',
                 quantita_totale=2000, quantita_spedita=0,
                 unita_misura='pz', prezzo_unitario=18.90),
    ])

    # CON-2026-SV-002 (chiuso, 100%)
    db.session.add_all([
        Articolo(contratto_id=c2_sv.id, codice='AL-SR-6210',
                 descrizione='Profilo anta 60mm, alluminio estruso verniciato a polvere',
                 quantita_totale=2500, quantita_spedita=2500,
                 unita_misura='pz', prezzo_unitario=37.12),
        Articolo(contratto_id=c2_sv.id, codice='AL-SR-5180',
                 descrizione='Profilo telaio fisso 80mm, alluminio estruso verniciato',
                 quantita_totale=900, quantita_spedita=900,
                 unita_misura='pz', prezzo_unitario=44.44),
    ])

    db.session.commit()

    print("Aggiornamento completato!")
    print(f"  Contratti totali:  {Contratto.query.count()}")
    print(f"  Allegati totali:   {Allegato.query.count()}")
    print(f"  Articoli totali:   {Articolo.query.count()}")
    print(f"  Righe fatturato:   {RigaFatturato.query.count()}")
    print()
    for c in Contratto.query.order_by(Contratto.id).all():
        print(f"  {c.codice:30s} {c.stato:10s} {c.percentuale_avanzamento:6.1f}%")
