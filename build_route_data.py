"""Zbuduj gotowy plik danych dla trasy nr 9.

Skrypt łączy mały, zapisany wynik agregacji odsłon z zestawu nr 10 z aktualną
historią artykułów z publicznego API polskiej Wikipedii. Wynik trafia do
``docs/data/route-9.json``; lokalny cache API nie jest publikowany.

Przykłady:
    python build_route_data.py
    python build_route_data.py --without-api
    python build_route_data.py --refresh
"""

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
VIEWS_FILE = ROOT / "data_input" / "route-9-view-totals.json"
OUTPUT_FILE = ROOT / "docs" / "data" / "route-9.json"
CACHE_DIRECTORY = ROOT / "data_cache" / "route_9_kpi"
API_URL = "https://pl.wikipedia.org/w/api.php"


def load_articles():
    """Wczytaj 26 artykułów trasy oraz ich sumy odsłon.

    Mały plik wejściowy zawiera sumy z 126 miesięcznych plików zestawu nr 10,
    wcześniej zgrupowane po ``page_id``.
    """
    if not VIEWS_FILE.exists():
        raise FileNotFoundError(
            "Brakuje data_input/route-9-view-totals.json. "
            "Przywróć go z repozytorium projektu."
        )

    source = json.loads(VIEWS_FILE.read_text(encoding="utf-8"))
    articles = source["articles"]
    if len(articles) != 26:
        raise ValueError(f"Oczekiwano 26 artykułów trasy nr 9, znaleziono {len(articles)}.")

    return articles, source["metadata"], source["path_total_views"]


def cache_file(page_id):
    """Zwróć osobny plik cache dla jednego artykułu."""
    return CACHE_DIRECTORY / f"{page_id}.json"


def load_cached_kpi(page_id):
    """Odczytaj pełny wynik wcześniejszego zapytania API, jeśli istnieje."""
    file_path = cache_file(page_id)
    if not file_path.exists():
        return None

    data = json.loads(file_path.read_text(encoding="utf-8"))
    required_fields = {"public_revisions_count", "last_public_edit_utc", "checked_at_utc"}
    return data if required_fields <= data.keys() else None


def request_api(parameters, attempt=1):
    """Pobierz jedną odpowiedź JSON z API i łagodnie ponów chwilowy błąd."""
    request = Request(
        f"{API_URL}?{urlencode(parameters)}",
        headers={"User-Agent": "BI-NGO-Wikipedia25-learning-project/0.1 (local analysis)"},
    )

    try:
        with urlopen(request, timeout=45) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError) as error:
        if attempt >= 3:
            raise RuntimeError(f"API nie odpowiedziało po 3 próbach: {error}") from error

        # Nie wysyłamy od razu identycznego zapytania ponownie. Przy limicie
        # HTTP 429 API może podać własny czas oczekiwania w nagłówku.
        retry_after = error.headers.get("Retry-After") if isinstance(error, HTTPError) else None
        try:
            wait_seconds = max(float(retry_after), attempt * 5) if retry_after else attempt * 5
        except ValueError:
            wait_seconds = attempt * 5
        time.sleep(wait_seconds)
        return request_api(parameters, attempt + 1)


def download_revision_summary(page_id, delay_seconds):
    """Policz widoczne rewizje i zapamiętaj datę najnowszej.

    API zwraca najwyżej 500 rewizji naraz.  Pole ``continue`` mówi, jak pobrać
    następną porcję, dlatego pętla działa także dla często edytowanych haseł.
    Domyślna kolejność API jest od najnowszej rewizji, więc pierwszy znacznik
    czasu jest datą ostatniej publicznej edycji.
    """
    revision_count = 0
    latest_edit_utc = None
    continuation = {}

    while True:
        parameters = {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "pageids": page_id,
            "prop": "revisions",
            "rvprop": "ids|timestamp",
            "rvlimit": "max",
            **continuation,
        }
        response = request_api(parameters)
        revisions = response["query"]["pages"][0].get("revisions", [])

        if latest_edit_utc is None and revisions:
            latest_edit_utc = revisions[0]["timestamp"]
        revision_count += len(revisions)

        if "continue" not in response:
            return {
                "public_revisions_count": revision_count,
                "last_public_edit_utc": latest_edit_utc,
                "checked_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

        continuation = response["continue"]
        # Krótka przerwa jest uprzejma wobec publicznego API.
        time.sleep(delay_seconds)


def make_article_record(article, kpi=None, error=None):
    """Wybierz pola potrzebne stronie i zachowaj spójną strukturę JSON."""
    return {
        "step": article["year"] - 2000,
        "page_id": article["page_id"],
        "name": article["name"],
        "title": article["title"],
        "wikipedia_url": f"https://pl.wikipedia.org/wiki/{article['title']}",
        "year": article["year"],
        "created_date": article["created_date"],
        "total_views": article["total_views"],
        "months_with_record": article["months_with_record"],
        # Wartość null znaczy „nie pobrano jeszcze”, a nie zero rewizji.
        "public_revisions_count": None if kpi is None else kpi["public_revisions_count"],
        "last_public_edit_utc": None if kpi is None else kpi["last_public_edit_utc"],
        "kpi_checked_at_utc": None if kpi is None else kpi["checked_at_utc"],
        "kpi_error": error,
    }


def write_output(records, views_metadata, path_total_views):
    """Zapisz plik wynikowy również w trakcie pracy, aby nie utracić postępu."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "metadata": {
            "title": "25 stopni polskiej Wikipedii",
            "path_number": 9,
            "article_count": len(records),
            "direct_links_count": len(records) - 1,
            "first_article_year": 2001,
            "last_article_year": 2026,
            "views_period": f"{views_metadata['first_month']}–{views_metadata['last_month']}",
            "views_months": views_metadata["months"],
            "path_total_views": path_total_views,
            "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sources": [
                "dane/9-biografie.tsv",
                "dane/10-wyswietlenia_monthly_raw_data/*.tsv.gz",
                "https://pl.wikipedia.org/w/api.php (historia artykułów)",
            ],
        },
        "articles": records,
    }
    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Przygotuj JSON danych dla 26 puzzli trasy nr 9.")
    parser.add_argument(
        "--without-api",
        action="store_true",
        help="Zapisz dane lokalne bez pobierania historii artykułów.",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Pobierz historię ponownie także dla artykułów obecnych w cache.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Przerwa w sekundach między kolejnymi stronami API (domyślnie 2).",
    )
    args = parser.parse_args()

    articles, views_metadata, path_total_views = load_articles()
    CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    records = []

    for number, article in enumerate(articles, start=1):
        kpi = None if args.refresh else load_cached_kpi(article["page_id"])
        error = None

        if args.without_api:
            pass
        elif kpi is None:
            print(f"[{number}/26] Pobieram historię: {article['name']}", flush=True)
            try:
                kpi = download_revision_summary(article["page_id"], args.delay)
                cache_file(article["page_id"]).write_text(
                    json.dumps(kpi, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            except RuntimeError as exception:
                # Pozostałe artykuły nadal mogą zostać przygotowane. Przy kolejnym
                # uruchomieniu ten jeden nieudany wpis zostanie ponowiony.
                error = str(exception)
                print(f"  Pominięto chwilowo: {error}", flush=True)
        else:
            print(f"[{number}/26] Cache: {article['name']}", flush=True)

        records.append(make_article_record(article, kpi, error))
        # Zapis po każdym artykule daje prostą możliwość wznowienia pracy.
        write_output(records, views_metadata, path_total_views)

        if not args.without_api and number < len(articles):
            time.sleep(args.delay)

    print(f"Zapisano: {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
