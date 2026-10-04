# 25 stopni polskiej Wikipedii

Interaktywna, statyczna wizualizacja przygotowana na Wolontariat #BI_NGO – III edycja.
Pokazuje 25 bezpośrednich linków między 26 biografiami polskojęzycznej Wikipedii:
od Marii Skłodowskiej-Curie do Igora Červeného. Kolejne artykuły powstały w latach
2001–2026.

Tytuł nawiązuje do idei [Six degrees of Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Six_degrees_of_Wikipedia).
Nie jest to jednak najkrótsza droga między hasłami, lecz celowo zbudowany,
chronologiczny łańcuch bieżących bezpośrednich linków.

## Zawartość

- `docs/` — gotowa strona GitHub Pages: HTML, CSS, JavaScript, dane wynikowe i grafiki;
- `data_input/route-9-view-totals.json` — mały, zagregowany wynik odsłon 26 artykułów;
- `build_route_data.py` — aktualizuje `docs/data/route-9.json` na podstawie tego wyniku i publicznego API;
- `prepare_portraits.py` — opcjonalnie odświeża lokalne miniatury i ich atrybucje.

Nie ma tu surowych plików `dane/`, miesięcznych TSV ani lokalnego cache. Są dostępne
w [publicznym repozytorium danych #BI_NGO](https://github.com/bi-ngo-wolontariat/BI_NGO-2026-Wikimedia-Polska).

## Podgląd i publikacja

Lokalny podgląd:

```powershell
C:\Python313\python.exe -m http.server 8000 --directory docs
```

W GitHub Pages wybierz **Deploy from a branch**, gałąź `main` i folder **`/docs`**.
Po publikacji otwórz adres w oknie incognito — strona wczytuje dane JSON oraz obrazy
z tego samego, publicznego repozytorium.

## Metodologia i źródła

1. Wybrano trasę nr 9 spośród 18 kompletnych tras znalezionych w zapisanym przebiegu
   wyszukiwania. Ma najwyższą sumę odsłon: 12 102 614 w okresie 2016-01–2026-06.
2. Zestaw nr 9 dostarczył biografie i daty utworzenia; zestaw nr 10 — miesięczne odsłony.
   Mały plik w `data_input/` jest tylko zagregowanym wynikiem dla 26 wybranych artykułów.
3. `build_route_data.py` pobiera z [API polskiej Wikipedii](https://pl.wikipedia.org/w/api.php)
   publicznie widoczne rewizje i datę ostatniej edycji.
4. Atrybucje 23 lokalnych miniatur Wikimedia Commons znajdują się na stronie oraz w
   `docs/data/photo_credits.json`; trzy pozostałe osoby mają monogramy.

Licencje danych: zestaw nr 10 — CC0 1.0; zestaw nr 9 — Wikidata CC0 1.0 oraz polska
Wikipedia CC BY-SA 4.0. Szczegóły: [słownik danych i licencje](https://github.com/bi-ngo-wolontariat/BI_NGO-2026-Wikimedia-Polska/blob/main/dictionary.md#źródła-danych-i-licencje).

Puzzle, ikony i logo Wikipedia 25 pochodzą z
[Wikipedia 25 Celebration Toolkit](https://meta.wikimedia.org/wiki/Wikipedia_25/Celebration_toolkit).
Logo Wikimedia Polska: [Holek, Leinad i Wikimedia Foundation, CC BY-SA 3.0](https://commons.wikimedia.org/wiki/File:Wikimedia_Polska_logo.svg).
Paleta i kroje pisma odwołują się do wskazówek Wikimedia:
[kolory](https://meta.wikimedia.org/wiki/Brand/colours) oraz
[typografia](https://meta.wikimedia.org/wiki/Brand/Typography).
