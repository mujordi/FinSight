# FinSight - Portfolio Feature

## ✅ IMPLEMENTAT

### 🎯 **FUNCIONALITAT:**
Tab **PORTAFOLIO** (2n després de MODEL) on cada usuari pot gestionar el seu portfolio personal.

---

## 📋 **CARACTERÍSTIQUES:**

### 1. **Afegir Productes Manualment**
- Camp: **Nom del producte** (obligatori)
- Camp: **Ticker** (opcional)
- Camp: **% Portfolio** (obligatori)
- Botó: **➕ Add**

### 2. **Classificació Automàtica**
El sistema classifica automàticament cada producte en:
- **Tipus**: Stock, ETF, Fund, Cash, RSU/ESPP, Other
- **Model**: Gold, Crypto, Thematic, Fixed Income, High Beta, Growth, Equities, Macro

**Lògica de classificació:**
```
Gold: gold, silver, precious metals
Crypto: bitcoin, crypto, blockchain
Thematic: semiconductor, uranium, quantum, nvidia, amd
Fixed Income: bond, treasury, yield
High Beta: 3x, leveraged, sqqq, tqqq
Growth: META, GOOGL, AAPL, MSFT, TSLA
Macro: cash, money market, dxy
Default: Equities
```

### 3. **Import CSV**
- Botó: **📄 Import CSV**
- Format: `name, ticker, percentage`
- Exemple: `portfolio_example.csv`

### 4. **Export CSV**
- Botó: **📥 Export CSV**
- Descarrega tots els productes en format CSV

### 5. **Vista de Distribució**
Grid amb 8 cards (un per model):
- 🥇 Gold
- 📈 Equities
- ₿ Crypto
- 🎯 Thematic
- 🚀 Growth
- ⚡ High Beta
- 📊 Fixed Income
- 🌍 Macro

**Mostra:**
- % assignat a cada model
- Highlight si té allocation (border blau)
- Total allocation (color-coded: verd=100%, groc<100%, vermell>100%)

### 6. **Taula de Holdings**
Columnes:
- Product
- Ticker
- Type (badge)
- Model (badge)
- % Portfolio
- Actions (🗑️ delete)

---

## 🗄️ **STORAGE:**

### Per Usuari:
- Cada usuari té el seu fitxer: `portfolios/{username}.json`
- Format:
```json
{
  "username": "demo",
  "products": [
    {
      "id": "uuid",
      "name": "NVIDIA",
      "ticker": "NVDA",
      "type": "Stock",
      "model": "Thematic",
      "percentage": 15.0
    }
  ]
}
```

---

## 🔌 **API ENDPOINTS:**

### `GET /api/portfolio`
Retorna el portfolio de l'usuari autenticat

### `POST /api/portfolio/add`
```json
{
  "name": "NVIDIA",
  "ticker": "NVDA",
  "percentage": 15.0
}
```

### `DELETE /api/portfolio/remove/{product_id}`
Elimina un producte

### `POST /api/portfolio/import-csv`
Upload CSV file (multipart/form-data)

---

## 📁 **FITXERS CREATS:**

1. **`portfolio_manager.py`** - Backend logic
   - Gestió de portfolios per usuari
   - Classificació automàtica
   - Import/Export CSV

2. **`templates/tabs/portafolio.html`** - UI del tab
   - Formulari d'afegir producte
   - Vista de distribució
   - Taula de holdings

3. **`static/portfolio.js`** - Frontend logic
   - CRUD operations
   - Actualització dinàmica
   - Import/Export

4. **`static/styles.css`** - Estils (afegits)
   - Portfolio section styles
   - Distribution cards
   - Form styles

5. **`portfolio_example.csv`** - Exemple d'import

---

## 🎨 **UI/UX:**

### Colors:
- Cards actius: Border blau (`--accent-primary`)
- Total 100%: Verd
- Total <100%: Groc
- Total >100%: Vermell

### Responsive:
- Desktop: Grid 4 cols
- Tablet (≤768px): Grid 2 cols
- Mobile (≤480px): Grid 1 col

---

## 📊 **EXEMPLE D'ÚS:**

### 1. Afegir Manual:
```
Name: NVIDIA
Ticker: NVDA
%: 15.0
→ Click "Add"
→ Classificat automàticament: Stock → Thematic
```

### 2. Import CSV:
```csv
name,ticker,percentage
NVIDIA,NVDA,15.0
AMD (RSU),AMD,9.0
Cash Daily,,7.5
```
→ Upload → 3 products added!

### 3. Vista:
```
Distribution:
  Thematic: 24.0% ✅
  Macro: 7.5% ✅
  Total: 31.5% (groc - falta 68.5%)
```

---

## 🔐 **SEGURETAT:**

- ✅ Tots els endpoints requereixen autenticació
- ✅ Cada usuari només veu el seu portfolio
- ✅ Storage separat per usuari
- ✅ Validació de inputs

---

## 🚀 **PRÒXIMS PASSOS (OPCIONAL):**

### Fase 2 (si vols):
- [ ] Editar productes existents
- [ ] Reordenar taula
- [ ] Filtrar per model
- [ ] Gràfic pie chart de distribució
- [ ] Tracking de performance (si afegim cost basis)
- [ ] Alertes de rebalancing

---

## 📖 **COM USAR-HO:**

1. **Login** a l'aplicació
2. **Click** al tab "💼 Portfolio"
3. **Afegir productes**:
   - Manual: Omple el formulari
   - CSV: Upload `portfolio_example.csv`
4. **Veure distribució** per model
5. **Gestionar** (eliminar productes si cal)
6. **Exportar** a CSV

---

**Data:** 2026-01-16
**Status:** ✅ COMPLET - MVP Funcional
**Per usuari:** ✅ Cada usuari té el seu portfolio
**Classificació:** ✅ Automàtica per keywords
**Import/Export:** ✅ CSV suportat

