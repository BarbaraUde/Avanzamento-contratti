// Aggiorna dinamicamente il dropdown Progetto al cambio Cliente
function initClienteProgettoFilter(clienteSelId, progettoSelId) {
    const clienteSel = document.getElementById(clienteSelId);
    const progettoSel = document.getElementById(progettoSelId);
    if (!clienteSel || !progettoSel) return;

    clienteSel.addEventListener('change', function () {
        const cid = this.value;
        progettoSel.innerHTML = '<option value="">— tutti —</option>';
        if (!cid) return;
        fetch('/api/progetti?cliente_id=' + cid)
            .then(r => r.json())
            .then(data => {
                data.forEach(p => {
                    const opt = document.createElement('option');
                    opt.value = p.id;
                    opt.textContent = p.nome;
                    progettoSel.appendChild(opt);
                });
            });
    });
}

// Copia percorso di rete negli appunti
function copyPercorso(el) {
    const text = el.dataset.path;
    navigator.clipboard.writeText(text).then(() => {
        el.title = 'Copiato!';
        setTimeout(() => { el.title = 'Copia percorso'; }, 1500);
    });
}

// Toggle sezione "aggiungi" (ordini, varianti, allegati, articoli)
function toggleAddForm(id) {
    const el = document.getElementById(id);
    if (!el) return;
    el.style.display = el.style.display === 'none' ? 'block' : 'none';
}

// Apri modale anteprima file (PDF / immagini) via /file/serve
function apriAnteprima(path, nome) {
    const modal = document.getElementById('modalAnteprima');
    if (!modal) return;
    const iframe = document.getElementById('previewIframe');
    const titolo = document.getElementById('modalAnteprimaTitolo');
    const dlLink = document.getElementById('previewDownloadLink');
    const serveUrl = '/file/serve?path=' + encodeURIComponent(path);
    titolo.textContent = nome || path.split(/[\\/]/).pop();
    iframe.src = serveUrl;
    dlLink.href = serveUrl;
    new bootstrap.Modal(modal).show();
    // Pulisci iframe alla chiusura
    modal.addEventListener('hidden.bs.modal', function onHide() {
        iframe.src = '';
        modal.removeEventListener('hidden.bs.modal', onHide);
    }, { once: true });
}

// Gestione delegata per pulsanti anteprima (usa data-anteprima-path/nome)
document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-anteprima-path]');
    if (btn) {
        apriAnteprima(btn.dataset.anteprimaPath, btn.dataset.anteprimaNome || '');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    // Chiudi alert flash dopo 4s
    document.querySelectorAll('.alert.alert-success, .alert.alert-warning').forEach(a => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(a);
            bsAlert.close();
        }, 4000);
    });
});
