"use strict";

const HORIZONTAL_STEP = 19.0393317;
// 2188 px / 20244 px — pionowy krok oficjalnego puzzla w pełnym płótnie trasy.
const VERTICAL_STEP = 10.8081407;

const ROUTE_POSITIONS = [
  [0, 0], [1, 0], [2, 0], [3, 0], [4, 0],
  [4, 1],
  [4, 2], [3, 2], [2, 2], [1, 2], [0, 2],
  [0, 3],
  [0, 4], [1, 4], [2, 4], [3, 4], [4, 4],
  [4, 5],
  [4, 6], [3, 6], [2, 6], [1, 6], [0, 6],
  [0, 7],
  [0, 8], [1, 8]
];

const COPY = {
  pl: {
    locale: "pl-PL",
    pageTitle: "25 stopni polskiej Wikipedii",
    description: "25 bezpośrednich linków przez 26 biografii polskojęzycznej Wikipedii, od 2001 do 2026 roku.",
    heroEyebrow: "WIKIPEDIA 25 · PODRÓŻ PO LINKACH",
    heroTitle: "25 stopni polskiej Wikipedii",
    heroLede: "25 bezpośrednich linków prowadzi przez 26 biografii polskojęzycznej Wikipedii — od Marii Skłodowskiej-Curie do Igora Červeného. Kolejne artykuły powstały w latach 2001–2026. Dziękujemy wszystkim redaktorkom i redaktorom.",
    languageToggleLabel: "Przełącz na język angielski",
    summaryAria: "Najważniejsze dane trasy",
    summaryBiographies: "biografii",
    summaryLinks: "bezpośrednich linków",
    summaryViews: "odsłon w latach 2016–2026",
    summaryYears: "lata utworzenia artykułów",
    howTitle: "Jak czytać tę trasę?",
    howCopy: "Każdy puzzel oznacza artykuł biograficzny. Przejście do kolejnego puzzla znaczy, że aktualna wersja poprzedniego artykułu zawiera bezpośredni link do następnego. Kliknij dowolną osobę, aby zobaczyć jej kartę danych.",
    methodCopy: "Tytuł nawiązuje do idei „Six degrees of Wikipedia”, lecz nie pokazuje najkrótszej możliwej drogi. To celowo zbudowany łańcuch 25 linków, w którym kolejne biografie pochodzą z kolejnych lat polskiej Wikipedii.",
    routeKicker: "INTERAKTYWNA TRASA",
    routeTitle: "Wybierz puzzel",
    routeNote: "Wszystkie puzzle mają tę samą skalę i orientację, dzięki czemu ich wypusty i wcięcia łączą się w jedną trasę. Możesz użyć także klawisza Tab oraz Entera lub Spacji.",
    routeMapAria: "Łańcuch 26 biografii",
    loading: "Wczytywanie danych…",
    noData: "brak danych",
    detailViewsLabel: "odsłon w latach 2016–2026",
    detailCreatedLabel: "data utworzenia artykułu",
    detailEditsLabel: "publicznie dostępne rewizje",
    openArticle: "Otwórz artykuł w Wikipedii ↗",
    lastEdit: "ostatnia:",
    publicRevisions: "publicznie dostępne rewizje",
    articleCreatedIn: "artykuł utworzony w",
    directLinkTo: "Bezpośredni link prowadzi dalej do",
    finalBiography: "To ostatnia biografia jubileuszowej trasy.",
    photoPrefix: "Zdjęcie:",
    photoUnavailable: "Dla tej osoby nie znaleziono automatycznie wolnej grafiki — pokazano monogram.",
    statusSelected: "Wybrano: {name}. Karta danych została zaktualizowana.",
    footerSources: "Źródła danych:",
    sourceRepo: "#BI_NGO — zbiory 9 i 10",
    sourceApi: "API polskiej Wikipedii",
    footerViews: "Odsłony obejmują okres 2016-01–2026-06.",
    footerCaveat: "Łańcuch został sprawdzony na aktualnych wersjach artykułów. Linki w Wikipedii mogą się zmieniać, dlatego wynik opisuje stan zweryfikowany 4 października 2026 r.",
    footerLicences: "Licencje danych: zestaw 10 — CC0 1.0; zestaw 9 — Wikidata CC0 1.0 i polska Wikipedia CC BY-SA 4.0.",
    dataDictionary: "Słownik danych i licencje",
    photoCredits: "Atrybucje zdjęć",
    footerGraphics: "Elementy graficzne:",
    sourceWmplLogo: "logo Wikimedia Polska",
    wmplAttribution: "(Holek, Leinad i Wikimedia Foundation; CC BY-SA 3.0).",
    footerProject: "Projekt przygotowany na Wolontariat #BI_NGO – III edycja.",
    loadError: "Nie udało się wczytać danych strony. Przy podglądzie lokalnym uruchom prosty serwer HTTP, np. python -m http.server 8000 w katalogu docs."
  },
  en: {
    locale: "en-GB",
    pageTitle: "25 Degrees of Polish Wikipedia",
    description: "25 direct links through 26 biographies in the Polish-language Wikipedia, from 2001 to 2026.",
    heroEyebrow: "WIKIPEDIA 25 · A JOURNEY THROUGH LINKS",
    heroTitle: "25 Degrees of Polish Wikipedia",
    heroLede: "25 direct links lead through 26 biographies in the Polish-language Wikipedia — from Maria Skłodowska-Curie to Igor Červený. The articles were created from 2001 to 2026. Thank you to all editors.",
    languageToggleLabel: "Switch to Polish",
    summaryAria: "Key route figures",
    summaryBiographies: "biographies",
    summaryLinks: "direct links",
    summaryViews: "pageviews, 2016–2026",
    summaryYears: "article creation years",
    howTitle: "How to read this route",
    howCopy: "Each puzzle represents a biographical article. Moving to the next puzzle means that the current version of the previous article contains a direct link to the next one. Select any person to see their data card.",
    methodCopy: "The title alludes to the idea of “Six degrees of Wikipedia”, but this is not the shortest possible route. It is a deliberately constructed chain of 25 links, in which successive biographies were created in successive years of the Polish Wikipedia.",
    routeKicker: "INTERACTIVE ROUTE",
    routeTitle: "Choose a puzzle",
    routeNote: "All puzzles share the same scale and orientation, so their notches and blanks form one route. You can also use Tab, Enter and Space.",
    routeMapAria: "A chain of 26 biographies",
    loading: "Loading data…",
    noData: "no data",
    detailViewsLabel: "pageviews, 2016–2026",
    detailCreatedLabel: "article creation date",
    detailEditsLabel: "publicly available revisions",
    openArticle: "Open article in Wikipedia ↗",
    lastEdit: "last:",
    publicRevisions: "publicly available revisions",
    articleCreatedIn: "article created in",
    directLinkTo: "A direct link leads to",
    finalBiography: "This is the final biography in the anniversary route.",
    photoPrefix: "Photo:",
    photoUnavailable: "No freely licensed graphic was found automatically for this person — a monogram is shown.",
    statusSelected: "Selected: {name}. The data card has been updated.",
    footerSources: "Data sources:",
    sourceRepo: "#BI_NGO — datasets 9 and 10",
    sourceApi: "Polish Wikipedia API",
    footerViews: "Pageviews cover January 2016–June 2026.",
    footerCaveat: "The chain was checked against the current article versions. Wikipedia links may change, so the result describes the state verified on 4 October 2026.",
    footerLicences: "Data licences: dataset 10 — CC0 1.0; dataset 9 — Wikidata CC0 1.0 and Polish Wikipedia CC BY-SA 4.0.",
    dataDictionary: "Data dictionary and licences",
    photoCredits: "Photo credits",
    footerGraphics: "Graphic elements:",
    sourceWmplLogo: "Wikimedia Polska logo",
    wmplAttribution: "(Holek, Leinad and Wikimedia Foundation; CC BY-SA 3.0).",
    footerProject: "Prepared for #BI_NGO Volunteering — 3rd edition.",
    loadError: "The site data could not be loaded. For a local preview, run a simple HTTP server, for example python -m http.server 8000 in the docs folder."
  }
};

const mapElement = document.querySelector("#route-map");
const statusElement = document.querySelector("#route-status");
const creditListElement = document.querySelector("#photo-credits-list");
const languageToggle = document.querySelector("#language-toggle");

let routeArticles = [];
let routeMetadata = null;
let routeCredits = [];
let creditsByPageId = new Map();
let puzzleButtons = [];
let selectedArticleId = null;
let currentLanguage = "pl";

function text(key) {
  return COPY[currentLanguage][key];
}

function formatNumber(value) {
  return new Intl.NumberFormat(text("locale")).format(value);
}

function formatCompactNumber(value) {
  if (value >= 1_000_000) {
    const formatted = (value / 1_000_000).toLocaleString(text("locale"), {
      maximumFractionDigits: 1
    });
    return currentLanguage === "pl" ? `${formatted} mln` : `${formatted}M`;
  }

  return formatNumber(value);
}

function formatDate(isoDate) {
  if (!isoDate) return text("noData");

  const date = new Date(`${isoDate.slice(0, 10)}T12:00:00Z`);
  return new Intl.DateTimeFormat(text("locale"), {
    day: "numeric",
    month: "long",
    year: "numeric"
  }).format(date);
}

function formatRevisions(value) {
  if (value === null) return text("noData");
  if (currentLanguage === "en") {
    return `${formatNumber(value)} ${value === 1 ? "revision" : "revisions"}`;
  }

  const lastDigit = value % 10;
  const lastTwoDigits = value % 100;
  const noun = value === 1
    ? "rewizja"
    : lastDigit >= 2 && lastDigit <= 4 && !(lastTwoDigits >= 12 && lastTwoDigits <= 14)
      ? "rewizje"
      : "rewizji";
  return `${formatNumber(value)} ${noun}`;
}

function initials(name) {
  const words = name.split(/\s+/).filter(Boolean);
  const first = words[0]?.[0] || "?";
  const last = words[words.length - 1]?.[0] || "";
  return `${first}${last}`.toUpperCase();
}

function createExternalLink(href, label) {
  const link = document.createElement("a");
  link.href = href;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = label;
  return link;
}

function createPortrait(article, credit, className) {
  const portrait = document.createElement("span");
  portrait.className = className;

  if (credit?.image_available && credit.local_path) {
    const image = document.createElement("img");
    image.src = credit.local_path;
    image.alt = "";
    image.loading = "lazy";
    portrait.append(image);
  } else {
    portrait.textContent = initials(article.name);
  }

  return portrait;
}

function renderRoute() {
  if (routeArticles.length !== ROUTE_POSITIONS.length) {
    throw new Error("Trasa i układ puzzli mają różną liczbę elementów.");
  }

  const fragment = document.createDocumentFragment();

  routeArticles.forEach((article, index) => {
    const [column, row] = ROUTE_POSITIONS[index];
    const credit = creditsByPageId.get(article.page_id);
    const button = document.createElement("button");
    button.type = "button";
    button.className = "puzzle";
    button.dataset.articleId = String(article.page_id);
    button.setAttribute("aria-pressed", "false");
    button.setAttribute("aria-controls", "detail-card");
    button.setAttribute("aria-label", `${article.name}, ${text("articleCreatedIn")} ${article.year}`);
    button.style.left = `${column * HORIZONTAL_STEP}%`;
    button.style.top = `${row * VERTICAL_STEP}%`;

    const shape = document.createElement("img");
    shape.className = "puzzle-shape";
    shape.src = "assets/blue-puzzle-piece.png";
    shape.alt = "";

    const content = document.createElement("span");
    content.className = "puzzle-content";
    content.append(
      createPortrait(article, credit, "puzzle-portrait"),
      Object.assign(document.createElement("span"), {
        className: "puzzle-name",
        textContent: article.name
      })
    );

    button.append(shape, content);
    button.addEventListener("click", () => selectArticle(article.page_id));
    fragment.append(button);
  });

  mapElement.replaceChildren(fragment);
  puzzleButtons = [...mapElement.querySelectorAll(".puzzle")];
}

function updateNextLink(article) {
  const nextElement = document.querySelector("#detail-next");
  const currentIndex = routeArticles.findIndex((item) => item.page_id === article.page_id);
  const nextArticle = routeArticles[currentIndex + 1];

  if (!nextArticle) {
    nextElement.textContent = text("finalBiography");
    return;
  }

  const label = document.createElement("span");
  label.textContent = text("directLinkTo");
  const strong = document.createElement("strong");
  strong.append(createExternalLink(nextArticle.wikipedia_url, nextArticle.name));
  nextElement.replaceChildren(label, strong);
}

function updatePhotoCredit(credit) {
  const target = document.querySelector("#detail-photo-credit");

  if (!credit?.image_available) {
    target.textContent = text("photoUnavailable");
    return;
  }

  target.replaceChildren(document.createTextNode(`${text("photoPrefix")} ${credit.author}; `));
  target.append(
    credit.license_url
      ? createExternalLink(credit.license_url, credit.license)
      : document.createTextNode(credit.license),
    document.createTextNode(". "),
    createExternalLink(credit.file_page_url, "Wikimedia Commons")
  );
}

function selectArticle(pageId, announce = true) {
  const article = routeArticles.find((item) => item.page_id === pageId);
  if (!article) return;

  selectedArticleId = article.page_id;
  const credit = creditsByPageId.get(article.page_id);
  document.querySelector("#detail-title").textContent = article.name;
  document.querySelector("#detail-views").textContent = formatNumber(article.total_views);
  document.querySelector("#detail-created").textContent = formatDate(article.created_date);
  document.querySelector("#detail-edits").textContent = formatRevisions(article.public_revisions_count);
  document.querySelector("#detail-edits-label").textContent = article.last_public_edit_utc
    ? `${text("lastEdit")} ${formatDate(article.last_public_edit_utc)}`
    : text("publicRevisions");

  const wikipediaLink = document.querySelector("#detail-link");
  wikipediaLink.href = article.wikipedia_url;
  wikipediaLink.textContent = currentLanguage === "pl"
    ? `Otwórz artykuł „${article.name}” w Wikipedii ↗`
    : `Open “${article.name}” in Wikipedia ↗`;

  updateNextLink(article);
  updatePhotoCredit(credit);

  puzzleButtons.forEach((button) => {
    const isActive = Number(button.dataset.articleId) === article.page_id;
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });

  if (announce) {
    statusElement.textContent = text("statusSelected").replace("{name}", article.name);
  }
}

function renderSummary(metadata) {
  document.querySelector("#summary-biographies").textContent = metadata.article_count;
  document.querySelector("#summary-links").textContent = metadata.direct_links_count;
  document.querySelector("#summary-views").textContent = formatCompactNumber(metadata.path_total_views);
  document.querySelector("#summary-years").textContent = `${metadata.first_article_year}–${metadata.last_article_year}`;
}

function renderCredits(credits) {
  const fragment = document.createDocumentFragment();

  credits.forEach((credit) => {
    const item = document.createElement("li");

    if (!credit.image_available) {
      item.textContent = currentLanguage === "pl"
        ? `${credit.article_name}: ${credit.reason}`
        : `${credit.article_name}: ${text("photoUnavailable")}`;
      fragment.append(item);
      return;
    }

    item.append(
      createExternalLink(credit.file_page_url, credit.article_name),
      document.createTextNode(` — ${credit.author}; `),
      credit.license_url
        ? createExternalLink(credit.license_url, credit.license)
        : document.createTextNode(credit.license),
      document.createTextNode(currentLanguage === "pl"
        ? `. ${credit.modification}`
        : ". Resized thumbnail; cropped by the site CSS.")
    );
    fragment.append(item);
  });

  creditListElement.replaceChildren(fragment);
}

function applyLanguage(language) {
  currentLanguage = language;
  document.documentElement.lang = language;
  document.title = text("pageTitle");
  document.querySelector("#page-description").setAttribute("content", text("description"));

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = text(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
    element.setAttribute("aria-label", text(element.dataset.i18nAriaLabel));
  });

  languageToggle.textContent = language === "pl" ? "EN" : "PL";
  languageToggle.setAttribute("aria-label", text("languageToggleLabel"));
  languageToggle.setAttribute("aria-pressed", String(language === "en"));

  if (routeMetadata) {
    renderSummary(routeMetadata);
    renderRoute();
    renderCredits(routeCredits);
    selectArticle(selectedArticleId || routeArticles[0].page_id, false);
  }
}

function showLoadError(error) {
  console.error(error);
  mapElement.replaceChildren(Object.assign(document.createElement("p"), {
    className: "load-error",
    textContent: text("loadError")
  }));
  document.querySelector("#detail-title").textContent = text("noData");
}

async function loadSite() {
  try {
    const [routeResponse, creditsResponse] = await Promise.all([
      fetch("data/route-9.json"),
      fetch("data/photo_credits.json")
    ]);

    if (!routeResponse.ok) {
      throw new Error(`Nie udało się wczytać danych trasy (${routeResponse.status}).`);
    }

    const routeData = await routeResponse.json();
    const creditsData = creditsResponse.ok ? await creditsResponse.json() : { credits: [] };
    routeArticles = routeData.articles;
    routeMetadata = routeData.metadata;
    routeCredits = creditsData.credits;
    creditsByPageId = new Map(routeCredits.map((credit) => [credit.page_id, credit]));

    renderSummary(routeMetadata);
    renderRoute();
    renderCredits(routeCredits);
    selectArticle(routeArticles[0].page_id);
  } catch (error) {
    showLoadError(error);
  }
}

languageToggle.addEventListener("click", () => {
  applyLanguage(currentLanguage === "pl" ? "en" : "pl");
});

applyLanguage("pl");
loadSite();
