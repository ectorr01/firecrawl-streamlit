# Firecrawl Streamlit Scraper
[![GitHub stars](https://img.shields.io/github/stars/ectorr01/firecrawl-streamlit?style=flat-square)](https://github.com/ectorr01/firecrawl-streamlit)
[![GitHub forks](https://img.shields.io/github/forks/ectorr01/firecrawl-streamlit?style=flat-square)](https://github.com/ectorr01/firecrawl-streamlit)
[![GitHub last commit](https://img.shields.io/github/last-commit/ectorr01/firecrawl-streamlit?style=flat-square)](https://github.com/ectorr01/firecrawl-streamlit/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/ectorr01/firecrawl-streamlit?style=flat-square)](https://github.com/ectorr01/firecrawl-streamlit)

Mini applicazione Streamlit per estrarre il contenuto di una pagina web tramite Firecrawl e visualizzarlo in formato Markdown.

## Funzionalità

- Inserimento di un URL tramite interfaccia web.
- Scraping della pagina con Firecrawl.
- Conversione del contenuto in Markdown.
- Visualizzazione dei metadati disponibili.
- Download del risultato come file `.md`.
- Gestione degli errori e validazione dell'URL.

## Requisiti

- Python 3.10 o superiore.
- Un account Firecrawl.
- Una Firecrawl API key.

## Installazione locale

Clona il repository e raggiungi la cartella del progetto:

```bash
git clone https://github.com/TUO-USERNAME/firecrawl-streamlit.git
cd firecrawl-streamlit
```

Crea e attiva un ambiente virtuale:

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installa le dipendenze:

```bash
pip install -r requirements.txt
```

## Configurazione della API key

Crea il file:

```text
.streamlit/secrets.toml
```

Inserisci al suo interno:

```toml
FIRECRAWL_API_KEY = "fc-la-tua-api-key"
```

Non pubblicare mai questo file su GitHub. Assicurati che `.gitignore` contenga:

```gitignore
.streamlit/secrets.toml
.venv/
__pycache__/
```

## Avvio dell'applicazione

Esegui:

```bash
streamlit run app.py
```

Apri quindi l'indirizzo mostrato nel terminale, normalmente:

```text
http://localhost:8501
```

## Struttura del progetto

```text
firecrawl-streamlit/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml
```

Il file `secrets.toml` deve rimanere solo in locale e non deve essere incluso nel repository.

## Pubblicazione su GitHub

Crea un nuovo repository su GitHub, senza aggiungere automaticamente README, `.gitignore` o licenza se questi file esistono già localmente.

Poi esegui dalla cartella del progetto:

```bash
git init
git add app.py requirements.txt README.md .gitignore
git commit -m "Aggiunge scraper Firecrawl con Streamlit"
git branch -M main
git remote add origin https://github.com/TUO-USERNAME/firecrawl-streamlit.git
git push -u origin main
```

Sostituisci `TUO-USERNAME` con il tuo username GitHub e verifica che l'URL del repository sia corretto.

## Deploy su Streamlit Community Cloud

1. Accedi a Streamlit Community Cloud.
2. Seleziona **Create app**.
3. Scegli il repository GitHub.
4. Seleziona il branch `main`.
5. Indica `app.py` come file principale.
6. Apri le impostazioni avanzate e inserisci nei Secrets:

```toml
FIRECRAWL_API_KEY = "fc-la-tua-api-key"
```

7. Avvia il deploy.

Non caricare `secrets.toml` nel repository: la API key deve essere configurata nei Secrets di Streamlit Community Cloud.

## Note di sicurezza

- Non condividere la Firecrawl API key.
- Non inserirla direttamente nel codice Python.
- Non committare `.streamlit/secrets.toml`.
- Se la chiave viene pubblicata per errore, revocala dal dashboard Firecrawl e generane una nuova.

## Licenza

Aggiungi una licenza al repository se intendi distribuire pubblicamente il progetto. Per un progetto personale puoi scegliere, ad esempio, MIT; verifica comunque che sia adatta al tuo caso d'uso.
