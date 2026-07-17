"""
Popola il database con i dati estratti dai documenti della cartella Progetto.
Eseguire una volta sola: python seed_data.py
"""
import sys
from datetime import date

sys.path.insert(0, r'C:\Users\bs_udeschini\Desktop\Progetto\Avanzamento-contratti')
from app import app, db, Cliente, Progetto, Contratto, Ordine, Variante, Allegato, RigaFatturato

BASE = r'C:\Users\bs_udeschini\Desktop\Progetto'

with app.app_context():
    if Cliente.query.count() > 0:
        print("Database gia' popolato — uscita senza modifiche.")
        sys.exit(0)

    # ------------------------------------------------------------------ CLIENTI
    cr = Cliente(nome='Componenti Industriali Rossi S.p.A.', codice='CR',
                 note='P.IVA 05647382910 — Via Emilia 220, 41122 Modena (MO) — Rif. Sig. Paolo Rossi')
    mn = Cliente(nome='Meccanica Nord S.r.l.', codice='MN',
                 note='P.IVA 09876543210 — Via Torino 87, 10098 Rivoli (TO) — Rif. Sig.ra Elena Colombo')
    sv = Cliente(nome='Serramenti Veneti S.p.A.', codice='SV',
                 note='P.IVA 03321540266 — Via Postumia 56, 31100 Treviso (TV) — Rif. Sig. Luca Ferraro')
    db.session.add_all([cr, mn, sv])
    db.session.flush()

    # ------------------------------------------------------------------ PROGETTI
    p_cr = Progetto(cliente_id=cr.id, nome='Fornitura barre e profili alluminio',
                    codice='PROJ-CR-2026', stato='aperto',
                    descrizione='Barre, tubolari e profili speciali in alluminio estruso con lavorazioni CNC')
    p_mn = Progetto(cliente_id=mn.id, nome='Fornitura profili alluminio estruso',
                    codice='PROJ-MN-2026', stato='aperto',
                    descrizione='Profili estrusi lega 6060/6063 a disegno cliente')
    p_sv = Progetto(cliente_id=sv.id, nome='Fornitura profili serramenti verniciati',
                    codice='PROJ-SV-2026', stato='aperto',
                    descrizione='Profili alluminio estruso e verniciato a polvere per serramenti (ante, telai, fermavetro)')
    db.session.add_all([p_cr, p_mn, p_sv])
    db.session.flush()

    # ------------------------------------------------------------------ CONTRATTI
    c_cr = Contratto(
        cliente_id=cr.id, progetto_id=p_cr.id,
        codice='CON-2026-CR-001',
        descrizione='Barre, tubolari e profili speciali alluminio estruso — 24 mesi',
        valore_totale=301140.00,
        stato='in variante',
        data_apertura=date(2026, 10, 1),
        data_chiusura=date(2028, 9, 30),
        note='FCA Ciserano. Ri.Ba. 60gg dfm (due rate per consegne >50k). Fideiussione 20%. Ind. LME ±8% cap.'
    )
    c_mn = Contratto(
        cliente_id=mn.id, progetto_id=p_mn.id,
        codice='CON-2026-MN-001',
        descrizione='Profili alluminio estruso lega 6060/6063 — 12 mesi',
        valore_totale=129000.00,
        stato='in variante',
        data_apertura=date(2026, 9, 1),
        data_chiusura=date(2027, 8, 31),
        note='EXW Ciserano. Bonifico 60gg dfm. Prezzi fissi 6 mesi poi adeguamento LME >5%.'
    )
    c_sv = Contratto(
        cliente_id=sv.id, progetto_id=p_sv.id,
        codice='CON-2026-SV-001',
        descrizione='Profili alluminio estruso e verniciato per serramenti — 18 mesi',
        valore_totale=270260.00,
        stato='in variante',
        data_apertura=date(2026, 11, 1),
        data_chiusura=date(2028, 4, 30),
        note='DAP Treviso. Acconto 30% entro 10gg, saldo 70% a 45gg dfm. Verniciatura Qualicoat. Prezzi fissi 9 mesi.'
    )
    db.session.add_all([c_cr, c_mn, c_sv])
    db.session.flush()

    # ------------------------------------------------------------------ ORDINI
    db.session.add_all([
        Ordine(contratto_id=c_cr.id, numero_ordine='ORD-CR-2026-014',
               data=date(2026, 10, 12), importo=77025.00, stato='aperto',
               note='Primo ordinativo trimestrale call-off. Resa FCA Ciserano. Consegna entro 30gg lavorativi.'),
        Ordine(contratto_id=c_mn.id, numero_ordine='ORD-MN-2026-001',
               data=date(2026, 9, 5), importo=37350.00, stato='evaso',
               note='Primo call-off. Consegna 15-20/09/2026. Resa EXW Ciserano. Evaso (vd. DDT 0114 e 0119).'),
        Ordine(contratto_id=c_sv.id, numero_ordine='ORD-SV-2026-007',
               data=date(2026, 11, 10), importo=94450.00, stato='aperto',
               note='Primo programma mensile. Consegna entro 25gg lavorativi. Resa DAP Treviso. Colore RAL approvato.'),
    ])

    # ------------------------------------------------------------------ VARIANTI
    db.session.add_all([
        Variante(
            contratto_id=c_mn.id, numero=1, data=date(2027, 1, 15),
            descrizione=(
                'Addendum n.1 — Modifica quantitativi AL-PR-1042 (lega 6060 sez.40x40); '
                'annullamento integrale AL-PR-2075 (profilo speciale a disegno, non più richiesto dal cliente). '
                'Valore complessivo rideterminato in Allegato A.'
            ),
            valore_delta=0.0,
            percorso_allegato=BASE + r'\Revisione1_Meccanica_Nord.docx'
        ),
        Variante(
            contratto_id=c_cr.id, numero=1, data=date(2027, 2, 20),
            descrizione=(
                'Addendum n.1 — Aggiornamento prezzo AL-BR-3310 per variazione indice LME; '
                'incremento quantitativi AL-BR-3310; annullamento articolo non più necessario. '
                'Valore complessivo rideterminato in Allegato A.'
            ),
            valore_delta=0.0,
            percorso_allegato=BASE + r'\Revisione2_Componenti_Rossi.docx'
        ),
        Variante(
            contratto_id=c_sv.id, numero=1, data=date(2027, 3, 5),
            descrizione=(
                'Addendum n.1 — Riduzione quantitativo AL-SR-6210 (profilo anta 60mm); '
                'annullamento integrale AL-SR-7025 fermavetro (non incluso nella nuova gamma serramenti). '
                'Valore complessivo rideterminato in Allegato A.'
            ),
            valore_delta=0.0,
            percorso_allegato=BASE + r'\Revisione3_Serramenti_Veneti.docx'
        ),
    ])

    # ------------------------------------------------------------------ ALLEGATI
    # Componenti Rossi
    db.session.add_all([
        Allegato(contratto_id=c_cr.id, tipo='offerta',
                 nome='Offerta OFF-2026-0168 — 12/09/2026',
                 percorso=BASE + r'\Offerta_Componenti_Rossi.pdf',
                 note='Totale offerta €301.140. Validità 30gg. Base contratto firmato 01/10/2026.'),
        Allegato(contratto_id=c_cr.id, tipo='contratto',
                 nome='Contratto fornitura CON-2026-CR-001',
                 percorso=BASE + r'\Contratto_Fornitura_Componenti_Rossi.docx',
                 note='Firmato 01/10/2026. Durata 24 mesi. Foro Bergamo.'),
        Allegato(contratto_id=c_cr.id, tipo='ordine',
                 nome='Ordine ORD-CR-2026-014 — 12/10/2026',
                 percorso=BASE + r'\Ordine_Componenti_Rossi.pdf',
                 note='Primo call-off trimestrale. Importo €77.025.'),
        Allegato(contratto_id=c_cr.id, tipo='altro',
                 nome='Addendum n.1 — 20/02/2027',
                 percorso=BASE + r'\Revisione2_Componenti_Rossi.docx',
                 note='Modifica prezzi e quantitativi. Valore rideterminato in Allegato A.'),
    ])
    # Meccanica Nord
    db.session.add_all([
        Allegato(contratto_id=c_mn.id, tipo='offerta',
                 nome='Offerta OFF-2026-0142 — 10/08/2026',
                 percorso=BASE + r'\Offerta_Meccanica_Nord.pdf',
                 note='Totale offerta €129.000. Validità 30gg. Base contratto firmato 01/09/2026.'),
        Allegato(contratto_id=c_mn.id, tipo='contratto',
                 nome='Contratto fornitura CON-2026-MN-001',
                 percorso=BASE + r'\Contratto_Fornitura_Meccanica_Nord.docx',
                 note='Firmato 01/09/2026. Durata 12 mesi. Foro Bergamo.'),
        Allegato(contratto_id=c_mn.id, tipo='ordine',
                 nome='Ordine ORD-MN-2026-001 — 05/09/2026',
                 percorso=BASE + r'\Ordine_Meccanica_Nord.pdf',
                 note='Primo call-off. Importo €37.350. Evaso (DDT-2026-0114 e DDT-2026-0119).'),
        Allegato(contratto_id=c_mn.id, tipo='altro',
                 nome='Addendum n.1 — 15/01/2027',
                 percorso=BASE + r'\Revisione1_Meccanica_Nord.docx',
                 note='Annullamento AL-PR-2075. Valore rideterminato in Allegato A.'),
    ])
    # Serramenti Veneti
    db.session.add_all([
        Allegato(contratto_id=c_sv.id, tipo='offerta',
                 nome='Offerta OFF-2026-0201 — 15/10/2026',
                 percorso=BASE + r'\Offerta_Serramenti_Veneti.pdf',
                 note='Totale offerta €270.260. Validità 30gg. Base contratto firmato 01/11/2026.'),
        Allegato(contratto_id=c_sv.id, tipo='contratto',
                 nome='Contratto fornitura CON-2026-SV-001',
                 percorso=BASE + r'\Contratto_Fornitura_Serramenti_Veneti.docx',
                 note='Firmato 01/11/2026. Durata 18 mesi. Foro Bergamo.'),
        Allegato(contratto_id=c_sv.id, tipo='ordine',
                 nome='Ordine ORD-SV-2026-007 — 10/11/2026',
                 percorso=BASE + r'\Ordine_Serramenti_Veneti.pdf',
                 note='Primo programma mensile. Importo €94.450. Colore RAL da campione approvato.'),
        Allegato(contratto_id=c_sv.id, tipo='altro',
                 nome='Addendum n.1 — 05/03/2027',
                 percorso=BASE + r'\Revisione3_Serramenti_Veneti.docx',
                 note='Annullamento AL-SR-7025 fermavetro. Riduzione AL-SR-6210.'),
    ])

    # ------------------------------------------------------------------ FATTURATO
    # Fonte: Fatturato_Contratti_Parziale.xlsx — solo Meccanica Nord (81.675 €)
    righe_mn = [
        (date(2026,  9, 15), 'DDT-2026-0114', 21750.00,
         'AL-PR-1042 — 5.000 pz × €4,35 — Profilo estruso lega 6060, sez.40x40mm, L=6000mm'),
        (date(2026,  9, 20), 'DDT-2026-0119', 15600.00,
         'AL-PR-2075 — 2.000 pz × €7,80 — Profilo lega 6063, sez. speciale a disegno, L=6000mm'),
        (date(2026, 10, 10), 'DDT-2026-0152', 17400.00,
         'AL-PR-1042 — 4.000 pz × €4,35 — Profilo estruso lega 6060, sez.40x40mm, L=6000mm'),
        (date(2026, 10, 15), 'DDT-2026-0158', 11700.00,
         'AL-PR-2075 — 1.500 pz × €7,80 — Profilo lega 6063, sez. speciale a disegno, L=6000mm'),
        (date(2026, 11,  5), 'DDT-2026-0201', 15225.00,
         'AL-PR-1042 — 3.500 pz × €4,35 — Profilo estruso lega 6060, sez.40x40mm, L=6000mm'),
    ]
    for dt, ddt, importo, descr in righe_mn:
        db.session.add(RigaFatturato(
            contratto_id=c_mn.id,
            cliente_id=mn.id,
            progetto_id=p_mn.id,
            data_documento=dt,
            numero_documento=ddt,
            importo=importo,
            descrizione=descr,
            fonte='Fatturato_Contratti_Parziale.xlsx'
        ))

    db.session.commit()

    print("Database popolato con successo!")
    print(f"  Clienti:        {Cliente.query.count()}")
    print(f"  Progetti:       {Progetto.query.count()}")
    print(f"  Contratti:      {Contratto.query.count()}")
    print(f"  Ordini:         {Ordine.query.count()}")
    print(f"  Varianti:       {Variante.query.count()}")
    print(f"  Allegati:       {Allegato.query.count()}")
    print(f"  Righe fatturato:{RigaFatturato.query.count()}")
