"""
Aggiornamento database — nuovi documenti caricati nella cartella Documenti:
- Contratto3_* (terza revisione contratto) -> allegati
- Offerta_*3.pdf (terza offerta) -> allegati
- Ordine3_* (terzo ordine, cartella Offerte) -> allegati
- Revisione1.1 / 2.2 / 3.3 (secondo addendum) -> varianti
Eseguire una sola volta: py update_data_v2.py
"""
import sys
from datetime import date

sys.path.insert(0, r'C:\Users\bs_udeschini\Desktop\Progetto\Avanzamento-contratti')
from app import app, db, Cliente, Contratto, Variante, Allegato

BASE_DOCS = r'C:\Users\bs_udeschini\Desktop\Progetto\Documenti'

with app.app_context():
    c_cr = Contratto.query.filter_by(codice='CON-2026-CR-001').first()
    c_mn = Contratto.query.filter_by(codice='CON-2026-MN-001').first()
    c_sv = Contratto.query.filter_by(codice='CON-2026-SV-001').first()

    if not all([c_cr, c_mn, c_sv]):
        print("Errore: contratti base non trovati. Eseguire prima seed_data.py e update_data.py.")
        sys.exit(1)

    gia_presenti = {a.percorso for a in Allegato.query.all()} | \
                   {v.percorso_allegato for v in Variante.query.all() if v.percorso_allegato}

    # ============================================================
    # 1) ALLEGATI — Contratto3 / Offerta*3 / Ordine3
    # ============================================================
    nuovi_allegati = [
        Allegato(contratto_id=c_cr.id, tipo='contratto',
                 nome='Contratto fornitura v3 CON-2026-CR-001',
                 percorso=BASE_DOCS + r'\Contratti\Contratto3_Fornitura_Componenti_Rossi.docx',
                 note='Terza revisione contratto post addendum n.2.'),
        Allegato(contratto_id=c_cr.id, tipo='offerta',
                 nome='Offerta OFF-2026-0168-R2',
                 percorso=BASE_DOCS + r'\Offerte\Offerta_Componenti_Rossi3.pdf',
                 note='Terza revisione offerta.'),
        Allegato(contratto_id=c_cr.id, tipo='ordine',
                 nome='Ordine ORD-CR-2026 — terzo call-off',
                 percorso=BASE_DOCS + r'\Offerte\Ordine3_Componenti_Rossi.pdf',
                 note='Terzo ordinativo trimestrale.'),

        Allegato(contratto_id=c_mn.id, tipo='contratto',
                 nome='Contratto fornitura v3 CON-2026-MN-001',
                 percorso=BASE_DOCS + r'\Contratti\Contratto3_Fornitura_Meccanica_Nord.docx',
                 note='Terza revisione contratto post addendum n.2.'),
        Allegato(contratto_id=c_mn.id, tipo='offerta',
                 nome='Offerta OFF-2026-0142-R2',
                 percorso=BASE_DOCS + r'\Offerte\Offerta_Meccanica_Nord3.pdf',
                 note='Terza revisione offerta.'),
        Allegato(contratto_id=c_mn.id, tipo='ordine',
                 nome='Ordine ORD-MN-2026 — terzo call-off',
                 percorso=BASE_DOCS + r'\Offerte\Ordine3_Meccanica_Nord.pdf',
                 note='Terzo ordinativo.'),

        Allegato(contratto_id=c_sv.id, tipo='contratto',
                 nome='Contratto fornitura v3 CON-2026-SV-001',
                 percorso=BASE_DOCS + r'\Contratti\Contratto3_Fornitura_Serramenti_Veneti.docx',
                 note='Terza revisione contratto post addendum n.2.'),
        Allegato(contratto_id=c_sv.id, tipo='offerta',
                 nome='Offerta OFF-2026-0201-R2',
                 percorso=BASE_DOCS + r'\Offerte\Offerta_Serramenti_Veneti3.pdf',
                 note='Terza revisione offerta.'),
        Allegato(contratto_id=c_sv.id, tipo='ordine',
                 nome='Ordine ORD-SV-2026 — terzo programma',
                 percorso=BASE_DOCS + r'\Offerte\Ordine3_Serramenti_Veneti.pdf',
                 note='Terzo programma mensile.'),
    ]
    aggiunti_allegati = 0
    for a in nuovi_allegati:
        if a.percorso not in gia_presenti:
            db.session.add(a)
            aggiunti_allegati += 1

    # ============================================================
    # 2) VARIANTI — secondo addendum (Revisione1.1 / 2.2 / 3.3)
    # ============================================================
    nuove_varianti = [
        Variante(
            contratto_id=c_mn.id, numero=2, data=date(2027, 4, 10),
            descrizione=(
                'Addendum n.2 — Ulteriore aggiornamento quantitativi e condizioni economiche '
                'a seguito della prima revisione. Valore complessivo rideterminato in Allegato A.'
            ),
            valore_delta=0.0,
            percorso_allegato=BASE_DOCS + r'\Revisioni\Revisione1.1_Meccanica_Nord.docx'
        ),
        Variante(
            contratto_id=c_cr.id, numero=2, data=date(2027, 5, 12),
            descrizione=(
                'Addendum n.2 — Seconda revisione prezzi per variazione indice LME e adeguamento '
                'quantitativi. Valore complessivo rideterminato in Allegato A.'
            ),
            valore_delta=0.0,
            percorso_allegato=BASE_DOCS + r'\Revisioni\Revisione2.2_Componenti_Rossi.docx'
        ),
        Variante(
            contratto_id=c_sv.id, numero=2, data=date(2027, 6, 3),
            descrizione=(
                'Addendum n.2 — Ulteriore riduzione quantitativi e aggiornamento gamma serramenti. '
                'Valore complessivo rideterminato in Allegato A.'
            ),
            valore_delta=0.0,
            percorso_allegato=BASE_DOCS + r'\Revisioni\Revisione3.3_Serramenti_Veneti.docx'
        ),
    ]
    aggiunte_varianti = 0
    for v in nuove_varianti:
        if v.percorso_allegato not in gia_presenti:
            db.session.add(v)
            aggiunte_varianti += 1

    db.session.commit()

    print("Aggiornamento v2 completato!")
    print(f"  Allegati aggiunti:  {aggiunti_allegati}")
    print(f"  Varianti aggiunte:  {aggiunte_varianti}")
    print(f"  Allegati totali:    {Allegato.query.count()}")
    print(f"  Varianti totali:    {Variante.query.count()}")
