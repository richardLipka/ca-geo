# Data request to SITMP under article 6 (draft)

**Status:** draft, 2026-11-20 — to be reviewed, completed and signed by the author.
Written in Czech because it is official correspondence with a Czech authority (exception to
the repository's English-only convention).

Basis: *Pravidla pro poskytování dat a výstupů z datových souborů GIS města Plzně*
(RMP resolution No. 656 of 9 June 2016), article 6; application form **příloha č. 3c**
(https://mapy.plzen.eu/poskytovane-sluzby/poskytovani-dat-z-gis/); licence conditions
**příloha č. 2**. Requests are sent to **sluzbygis@plzen.eu**.

What the author must still do:

- [ ] check the requested data list and purpose, delete what is not needed;
- [ ] fill in phone and e-mail (left as placeholders on purpose — this file is in a public repository);
- [ ] transfer the form part into the official Word form 3c, sign it and add the university stamp
      (signature of an authorised person; check who may sign for ZČU / the faculty);
- [ ] attach the form to the e-mail below and send it to sluzbygis@plzen.eu.

Points that matter for ca-geo (why the letter asks what it asks):

1. Data provided under article 6 may be used only for the stated purpose and **must not be
   given to third parties in any form** (licence conditions, point 1.2) — this conflicts with
   a public repository and public web demos, so the letter asks explicitly for permission to
   publish derived outputs.
2. Data provided through **map viewing and download services** and open data are licensed
   **CC BY-SA 4.0** with the attribution "datový podklad © SITMP" (licence conditions,
   point 4) — the letter asks whether this covers the public ArcGIS services, which would
   allow reuse without the article-6 restrictions.
3. Article 6 data are free but only "in reasonable scope (e.g. a data sample) at the
   supplier's discretion" — the letter offers pilot areas and subsets.
4. Breach of the conditions carries a contractual penalty of 30 000 CZK (100 × the handling
   fee, price list).

---

## 1. Průvodní e-mail

**Komu:** sluzbygis@plzen.eu
**Předmět:** Žádost o poskytnutí dat z GIS města Plzně dle čl. 6 Pravidel – výzkumný projekt ZČU (simulace celulárními automaty)

Dobrý den,

v příloze zasílám žádost o bezplatné poskytnutí dat a výstupů z datových souborů GIS města
Plzně podle článku 6 Pravidel pro poskytování dat a výstupů (příloha č. 3c).

Data potřebujeme pro výzkumný projekt Západočeské univerzity v Plzni zaměřený na simulace
prostorových jevů celulárními automaty nad geografickými daty (tok vody a povodně, šíření
požárů, růst města, doprava aj.). Projekt je vyvíjen jako otevřený výzkumný a výukový nástroj;
jeho výsledky chceme prezentovat v odborných publikacích a ve formě interaktivních
demonstrací. Plzeň by byla hlavním pilotním územím, protože kvalita a rozsah dat města jsou
pro tento účel mimořádné.

Kromě samotné žádosti bych Vás rád požádal o vyjádření ke třem otázkám užití dat, které jsou
pro projekt zásadní:

1. **Licence dat z mapových služeb.** Vztahuje se bod 4 Licenčních podmínek (užití dat
   poskytovaných formou mapových prohlížecích a stahovacích služeb za podmínek licence
   CC BY-SA 4.0) i na data dostupná prostřednictvím veřejných mapových služeb ArcGIS města
   (https://ags.plzen.eu/arcgis/rest/services), např. vrstvy dopravního modelu, FCD nebo
   digitálního modelu terénu? Pokud ano, užívali bychom je za těchto podmínek s doložkou
   „datový podklad © SITMP“ a odkazem na http://mapy.plzen.eu.
2. **Zveřejnění odvozených výstupů.** U dat poskytnutých podle čl. 6 žádáme o souhlas se
   zveřejněním výstupů odvozených z dat – výsledků simulací, map, grafů a agregovaných či
   převzorkovaných vrstev (např. terén v hrubším rozlišení, souhrnné intenzity dopravy) – ve
   veřejně dostupných demonstracích, publikacích a ve veřejném repozitáři projektu, vždy
   s uvedením zdroje „datový podklad © SITMP“. Původní data bychom nezveřejňovali ani
   neposkytovali třetím osobám. Uvítáme, pokud nám sdělíte, v jaké podobě je takové
   zveřejnění přípustné.
3. **Data třetích stran.** U dat, jejichž autorem je jiný subjekt (např. data FCD, silniční
   síť CEDA, dopravní model), prosím o informaci, kdo je vlastníkem práv a za jakých podmínek
   je lze pro výzkum použít, případně na koho se máme obrátit.

Rozsah požadovaných dat jsme se snažili omezit na nezbytné minimum; pokud by byl pro
poskytnutí podle čl. 6 příliš velký, rádi jej upravíme (např. na pilotní území centra města
nebo kratší časové období). Jsem připraven(a) požadavky případně upřesnit telefonicky nebo
osobně.

Děkuji a jsem s pozdravem

Richard Lipka
Západočeská univerzita v Plzni
tel.: [DOPLNIT] · e-mail: [DOPLNIT]

---

## 2. Text pro formulář – příloha č. 3c

**ŽÁDOST o poskytnutí dat a výstupů veřejným výzkumným a vzdělávacím institucím**

| Pole formuláře | Vyplnit |
|---|---|
| Odběratel – veřejná výzkumná a vzdělávací instituce | Západočeská univerzita v Plzni [DOPLNIT fakultu / katedru] |
| Se sídlem | Univerzitní 2732/8, 301 00 Plzeň |
| IČO | 49777513 |
| Pověřená osoba | Richard Lipka, tel.: [DOPLNIT], e-mail: [DOPLNIT] |

*(IČO a sídlo ověřeny v registru ARES 2026-11-20.)*

### Požadovaná data a výstupy

Seřazeno podle priority; u každé položky je uveden zdroj, ve kterém jsme data identifikovali.

1. **Dopravní model – scénáře 1–4** (mapové služby `GIS_Doprava/GIS_Doprava_DM_scenar_01` až
   `_04`: před a po stavbě západního obchvatu, uzavírky 07/2024 a 07/2025) – úseky sítě se všemi
   atributy (edge_id, source, target, capacity, cost, speed, type, traffic, traffic_lvl),
   případně uzly sítě; **a stručný popis atributů** (jednotka a časový základ veličiny
   „traffic“, význam „type“, metodika modelu).
2. **Data FCD** (služba `GIS_Doprava/GIS_Doprava_FCD`) – vrstva úseků s atributy silniční sítě
   a **historie měření** (tabulka „FCD Historie“; postačí vzorek, např. jeden týden z období
   05/2025); popis kódů atributů sítě (FW, FC, SL, NC, ONEWAY …).
3. **Digitální model terénu Plzně 2022** (rozlišení 0,5 m; služba
   `GIS_DMT_DMR/DMT_Plzen_Georeal_2022`) – celé území města, případně pilotní území
   (povodí vybraných toků / centrum).
4. **Historické mapy města** (služby `GIS_Historicke`: Císařské otisky, 1840, 1864, 1891, 1912,
   1931, 1950, 1971 – případně jiný výběr dle dostupnosti) – georeferencované rastry.
5. **Smyčky dopravních detektorů s vazbou na řadiče SSZ** (služba
   `GIS_TEST_Smycky_detektoru`) a **archiv dat z detektorů** (intenzita, obsazenost; vzorek
   např. jeden měsíc); pokud je to možné, **signální plány** (pevné programy) pro 5–10
   vybraných křižovatek s detektory.
6. **Digitální technická mapa – dopravní plochy** (provozní plochy pozemních komunikací,
   dopravní ostrůvky, dělicí pásy, parkovací plochy, vodorovné dopravní značení, pokud je
   součástí) pro pilotní území centra města.
7. *(volitelně)* Vrstvy **povodní** (složka `GIS_Povodne`), pokud obsahují hloubky či průběhy
   historických povodní nad rámec otevřených dat.

### Účel použití

Výzkumný projekt Západočeské univerzity v Plzni: vývoj a validace simulačních modelů
prostorových jevů založených na celulárních automatech (tok vody a povodně, šíření požárů,
stékání studeného vzduchu, růst města, dopravní proudy). Data budou použita jako vstupy modelů
a jako referenční data pro kalibraci a ověření jejich výsledků. Výstupem projektu jsou odborné
publikace a otevřený výukový nástroj s interaktivními demonstracemi; zveřejňovány budou pouze
výsledky a odvozené výstupy v rozsahu odsouhlaseném dodavatelem (viz průvodní dopis), nikoli
poskytnutá data.

### Rozsah území

Území statutárního města Plzně; u položek 3, 5 a 6 lze omezit na pilotní území (centrum
města / vybrané povodí) dle možností dodavatele.

### Formát dat

- [x] SHP včetně dostupných atributů: všechny atributy uvedených vrstev
- Jiný (doplnit ručně do formuláře): **GeoTIFF** pro rastry (položky 3 a 4), **CSV** pro
  tabulky (historie FCD, data detektorů), souřadnicový systém S-JTSK (EPSG:5514)

### Prohlášení (text formuláře – ponechat beze změny)

Odběratel prohlašuje, že se před podpisem žádosti seznámil s Pravidly a jejich přílohami a
s Licenčními podmínkami a zavazuje se je dodržovat; při porušení uhradí smluvní pokutu ve výši
stonásobku manipulačního poplatku.

V Plzni, dne ..................          ............................................
                                          podpis oprávněné osoby odběratele, razítko
