"""Pobierz miniatury biografii i przygotuj dane do ich atrybucji.

Skrypt czyta trasę z ``docs/data/route-9.json`` i korzysta wyłącznie z publicznego
API polskiej Wikipedii. Dla każdego artykułu prosi rozszerzenie PageImages o
wolną grafikę, a następnie pobiera jej miniaturę oraz metadane licencji.

Wyniki:
* ``docs/assets/portraits/<page_id>.<ext>`` — lokalne, niewielkie miniatury;
* ``docs/data/photo_credits.json`` — dane potrzebne do pokazania atrybucji.

Przykład oczekiwanego pliku ``docs/data/route-9.json``:

{
  "articles": [
    {"page_id": 3544, "name": "Maria Skłodowska-Curie"},
    {"page_id": 126, "name": "Albert Einstein"}
  ]
}

Może to być również zwykła lista takich obiektów. Skrypt nie wybiera zdjęć
ręcznie. Jeżeli API nie zwróci wolnej grafiki, zapisuje rekord bez zdjęcia;
strona może wtedy pokazać inicjały albo neutralny placeholder.
"""

import argparse
import json
import time
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


# Wszystkie ścieżki liczymy od folderu skryptu, a nie od bieżącego katalogu
# konsoli. Dzięki temu polecenie działa tak samo z dowolnego miejsca.
ROOT = Path(__file__).resolve().parent
API_URL = "https://pl.wikipedia.org/w/api.php"
DEFAULT_ROUTE = ROOT / "docs" / "data" / "route-9.json"
DEFAULT_OUTPUT = ROOT / "docs"
DEFAULT_THUMB_WIDTH = 420
USER_AGENT = "BI-NGO-Wikipedia25-learning-project/0.1 (static-site preparation)"


class TextOnlyHTMLParser(HTMLParser):
    """Usuń znaczniki HTML, które API czasem zwraca w polu autora."""

    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain_text(value):
    """Zamień fragment HTML z metadanych Commons na zwykły, bezpieczny tekst."""
    parser = TextOnlyHTMLParser()
    parser.feed(value or "")
    parser.close()
    return " ".join(unescape("".join(parser.parts)).split())


def api_get(parameters):
    """Wykonaj jedno zapytanie do publicznego API Wikipedii i odczytaj JSON."""
    url = f"{API_URL}?{urlencode(parameters)}"
    request = Request(url, headers={"User-Agent": USER_AGENT})

    with urlopen(request, timeout=45) as response:
        return json.load(response)


def normalise_title(title):
    """Ujednolić drobne różnice zapisu tytułów zwracanych przez API."""
    return title.replace("_", " ").strip()


def load_route(route_file):
    """Wczytaj listę artykułów z małego, łatwego do ręcznej edycji JSON-a."""
    raw_data = json.loads(route_file.read_text(encoding="utf-8"))

    if isinstance(raw_data, list):
        raw_articles = raw_data
    else:
        # Obsługujemy trzy naturalne nazwy klucza, aby plik nie był kruchy
        # podczas dalszego rozwijania projektu.
        raw_articles = (
            raw_data.get("articles")
            or raw_data.get("route")
            or raw_data.get("path")
        )

    if not isinstance(raw_articles, list) or not raw_articles:
        raise ValueError(
            "Plik trasy musi zawierać niepustą listę w kluczu 'articles', "
            "'route' lub 'path'."
        )

    articles = []
    for item in raw_articles:
        page_id = item.get("page_id")
        # ``name`` jest nazwą stosowaną w obecnych skryptach projektu, ale
        # przyjmujemy też ``title`` dla wygody ręcznej edycji JSON-a.
        name = item.get("name") or item.get("title")

        if page_id is None or not name:
            raise ValueError("Każdy artykuł musi mieć pola 'page_id' i 'name'.")

        articles.append({"page_id": int(page_id), "name": str(name)})

    return articles


def get_page_images(articles, thumb_width):
    """Odczytaj nazwę pliku i adres miniatury dla wszystkich artykułów naraz."""
    # Trasa ma 26 pozycji, czyli mieści się w limicie 50 tytułów tego API.
    response = api_get(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "pageimages",
            "piprop": "name|thumbnail",
            "pithumbsize": thumb_width,
            # Nie pobieramy lokalnych plików fair use ani innych niewolnych grafik.
            "pilicense": "free",
            "titles": "|".join(article["name"] for article in articles),
        }
    )

    images = {}
    for page in response["query"]["pages"]:
        image_name = page.get("pageimage")
        thumbnail = page.get("thumbnail", {}).get("source")
        if image_name and thumbnail:
            images[normalise_title(page["title"])] = {
                "file_name": image_name,
                "thumbnail_url": thumbnail,
            }

    return images


def get_image_metadata(file_names, thumb_width):
    """Pobierz autora, licencję i trwały link strony pliku z Commons/Wikipedii."""
    if not file_names:
        return {}

    response = api_get(
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "iiurlwidth": thumb_width,
            # Pobieramy tylko pola potrzebne do krótkiej, konkretnej atrybucji.
            "iiextmetadatafilter": (
                "Artist|Credit|LicenseShortName|LicenseUrl|UsageTerms|"
                "AttributionRequired"
            ),
            "titles": "|".join(f"File:{file_name}" for file_name in file_names),
        }
    )

    metadata = {}
    for page in response["query"]["pages"]:
        image_info = page.get("imageinfo", [])
        if not image_info:
            continue

        info = image_info[0]
        # API polskiej Wikipedii pokazuje strony plików z prefiksem „Plik:”,
        # ale nazwa po dwukropku pozostaje wspólna z nazwą zwróconą przez PageImages.
        # W odpowiedzi ImageInfo spacje w nazwie są zwykle dosłowne, podczas
        # gdy PageImages zwraca tę samą nazwę z podkreśleniami. Klucz
        # normalizujemy, aby prawidłowo połączyć oba wyniki.
        file_name = normalise_title(page["title"].split(":", maxsplit=1)[-1])
        extmetadata = info.get("extmetadata", {})

        def metadata_value(key):
            return plain_text(extmetadata.get(key, {}).get("value", ""))

        metadata[file_name] = {
            "file_page_url": info.get("descriptionurl"),
            "author": metadata_value("Artist") or "Autor niepodany w API",
            "credit": metadata_value("Credit"),
            "license": metadata_value("LicenseShortName")
            or metadata_value("UsageTerms")
            or "Licencja niepodana w API",
            "license_url": extmetadata.get("LicenseUrl", {}).get("value"),
            "attribution_required": metadata_value("AttributionRequired"),
        }

    return metadata


def extension_from_content_type(content_type):
    """Wybierz rozszerzenie lokalnego pliku na podstawie nagłówka odpowiedzi."""
    content_type = (content_type or "").split(";", maxsplit=1)[0].lower()
    extensions = {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }
    return extensions.get(content_type, ".jpg")


def download_thumbnail(url, target_file):
    """Zapisz małą miniaturę lokalnie i zwróć jej rzeczywiste rozszerzenie."""
    request = Request(url, headers={"User-Agent": USER_AGENT})

    with urlopen(request, timeout=60) as response:
        content = response.read()
        extension = extension_from_content_type(response.headers.get("Content-Type"))

    final_file = target_file.with_suffix(extension)
    final_file.write_bytes(content)
    return final_file


def build_credit_record(article, image, metadata, output_root, dry_run):
    """Pobierz obraz jednej osoby lub zapisz jawny rekord bez zdjęcia."""
    base_record = {
        "page_id": article["page_id"],
        "article_name": article["name"],
        # Każda grafika zostanie pokazana jako mała, okrągła miniatura w CSS.
        # Informacja pozwala uczciwie zaznaczyć zmianę także przy CC BY-SA.
        "modification": "Zmniejszona miniatura; kadrowanie wykonywane przez CSS strony.",
    }

    if image is None:
        return {
            **base_record,
            "image_available": False,
            "reason": "Brak wolnej grafiki zwróconej automatycznie przez PageImages.",
        }

    image_metadata = metadata.get(normalise_title(image["file_name"]))
    if image_metadata is None:
        # Nie publikujemy pliku, jeżeli nie udało się uzyskać jego danych
        # licencyjnych. Bezpieczniej pozostawić placeholder niż zgadywać autora.
        return {
            **base_record,
            "image_available": False,
            "reason": "Nie udało się pobrać metadanych licencji pliku.",
        }

    if dry_run:
        local_path = None
    else:
        portrait_dir = output_root / "assets" / "portraits"
        portrait_dir.mkdir(parents=True, exist_ok=True)
        downloaded_file = download_thumbnail(
            image["thumbnail_url"], portrait_dir / str(article["page_id"])
        )
        # Ścieżkę zapisujemy względem folderu ``docs``, bo stamtąd będzie
        # publikowana strona GitHub Pages.
        local_path = downloaded_file.relative_to(output_root).as_posix()

    return {
        **base_record,
        "image_available": True,
        "local_path": local_path,
        "file_name": image["file_name"],
        **image_metadata,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Pobierz lokalne portrety i dane atrybucji dla trasy Wikipedii 25."
    )
    parser.add_argument("--route", type=Path, default=DEFAULT_ROUTE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--thumb-width", type=int, default=DEFAULT_THUMB_WIDTH)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Sprawdź API i zapisz tylko JSON bez pobierania plików obrazów.",
    )
    args = parser.parse_args()

    if not args.route.is_file():
        raise FileNotFoundError(f"Nie znaleziono pliku trasy: {args.route}")
    if args.thumb_width < 80:
        raise ValueError("Szerokość miniatury powinna mieć co najmniej 80 px.")

    articles = load_route(args.route)
    print(f"Wczytano {len(articles)} biografii z: {args.route}")
    print("Pobieram listę wolnych grafik z PageImages...", flush=True)
    images_by_title = get_page_images(articles, args.thumb_width)
    print(f"Znaleziono {len(images_by_title)} grafik. Pobieram metadane licencji...", flush=True)
    metadata_by_file = get_image_metadata(
        [image["file_name"] for image in images_by_title.values()], args.thumb_width
    )

    records = []
    for number, article in enumerate(articles, start=1):
        image = images_by_title.get(normalise_title(article["name"]))
        record = build_credit_record(
            article, image, metadata_by_file, args.output, args.dry_run
        )
        records.append(record)
        status = "zdjęcie" if record["image_available"] else "placeholder"
        print(f"{number:>2}/{len(articles)} {article['name']}: {status}", flush=True)

        # Krótka pauza ogranicza liczbę kolejnych zapytań do serwerów Wikimedia.
        if image is not None and not args.dry_run:
            time.sleep(0.15)

    output_data_dir = args.output / "data"
    output_data_dir.mkdir(parents=True, exist_ok=True)
    credits_file = output_data_dir / "photo_credits.json"
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Publiczne API polskiej Wikipedii: PageImages i ImageInfo.",
        "credits": records,
    }
    credits_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    with_images = sum(record["image_available"] for record in records)
    print(f"\nGotowe: {with_images}/{len(records)} portretów.")
    print(f"Atrybucje: {credits_file}")
    if args.dry_run:
        print("Tryb --dry-run: nie pobrano żadnych plików obrazów.")


if __name__ == "__main__":
    main()
