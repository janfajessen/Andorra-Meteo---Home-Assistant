"""DataUpdateCoordinators for Andorra Meteo."""
from __future__ import annotations

import logging
import re
from datetime import timedelta

import aiohttp
from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    AVALANCHE_URL,
    DOMAIN,
    METEOCLIMATIC_FEED_URL,
    SCAN_INTERVAL_AVALANCHE,
    SCAN_INTERVAL_STATION,
)

_LOGGER = logging.getLogger(__name__)

# Regex to extract encoded data block from Meteoclimatic RSS.
# Real format confirmed from live feed:
#   [[<CODE;(T;Tmax;Tmin;condition);(H;Hmax;Hmin);(B;Bmax;Bmin);(W;Wmax;Azim);(P);Name>]]
# The condition (e.g. "sun", "cloud", "rain") is the 4th element of the temp group.
_RSS_DATA_RE = re.compile(
    r"\[\[<([^;]+);"
    r"\(([^)]*)\);"   # temperature group: T;Tmax;Tmin;condition
    r"\(([^)]*)\);"   # humidity group:    H;Hmax;Hmin
    r"\(([^)]*)\);"   # pressure group:    B;Bmax;Bmin
    r"\(([^)]*)\);"   # wind group:        W;Wmax;Azim
    r"\(([^)]*)\);"   # precipitation:     P
    r"([^>]+)>]]"
)

# Meteoclimatic condition string → HA weather condition
# All known values from Meteoclimatic RSS feed documented here to avoid unknown warnings
_CONDITION_MAP: dict[str, str] = {
    "sun":        "sunny",
    "moon":       "clear-night",
    "hazemoon":   "fog",           # hazy night
    "haze":       "fog",
    "suncloud":   "partlycloudy",
    "mooncloud":  "partlycloudy",  # partly cloudy at night
    "sun-cloud":  "partlycloudy",
    "cloud":      "cloudy",
    "clouds":     "cloudy",
    "cloudy":     "cloudy",
    "fog":        "fog",
    "mist":       "fog",
    "rain":       "rainy",
    "rainy":      "rainy",
    "drizzle":    "rainy",
    "snow":       "snowy",
    "snowy":      "snowy",
    "storm":      "lightning-rainy",
    "thunder":    "lightning-rainy",
    "lightning":  "lightning",
    "wind":       "windy",
    "windy":      "windy",
    "hail":       "hail",
    "sleet":      "snowy-rainy",
}


def _parse_float(value: str) -> float | None:
    """Parse a European-style float string (comma as decimal separator).
    
    Meteoclimatic uses -99 as a sentinel value for broken/unavailable sensors.
    """
    try:
        result = float(value.replace(",", "."))
        return None if result <= -99.0 else result
    except (ValueError, AttributeError):
        return None


def _parse_group(raw: str) -> list[float | None]:
    """Split a semicolon-separated group into a list of optional floats."""
    return [_parse_float(v.strip()) for v in raw.split(";")]


class MeteoclimaticCoordinator(DataUpdateCoordinator):
    """Coordinator for a single Meteoclimatic station via RSS feed."""

    def __init__(self, hass: HomeAssistant, station_code: str, station_name: str) -> None:
        """Initialise."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_station_{station_code}",
            update_interval=timedelta(seconds=SCAN_INTERVAL_STATION),
        )
        self.station_code = station_code
        self.station_name = station_name
        self._url = METEOCLIMATIC_FEED_URL.format(station_code)
        self._last_successful_update: str | None = None  # ISO timestamp

    async def _async_update_data(self) -> dict:
        """Fetch and parse the RSS feed for this station."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(self._url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status != 200:
                    return self._return_cached_or_fail(
                        f"HTTP {resp.status} from Meteoclimatic feed"
                    )
                text = await resp.text(encoding="utf-8", errors="replace")
        except aiohttp.ClientError as err:
            return self._return_cached_or_fail(
                f"Network error fetching Meteoclimatic feed: {err}"
            )

        return self._parse_feed(text)

    def _return_cached_or_fail(self, reason: str) -> dict:
        """Return last known data if available, otherwise raise UpdateFailed."""
        if self.data:
            _LOGGER.warning(
                "Andorra Meteo: %s — keeping last known data from %s",
                reason,
                self._last_successful_update or "unknown time",
            )
            return self.data
        raise UpdateFailed(reason)

    def _parse_feed(self, text: str) -> dict:
        """Extract weather data from the RSS payload."""
        match = _RSS_DATA_RE.search(text)
        if not match:
            return self._return_cached_or_fail(
                f"No data block in feed for {self.station_code} — station may be offline"
            )

        code = match.group(1)
        temp_raw = match.group(2)   # "7,3;10,5;5,1;sun"
        hum_vals = _parse_group(match.group(3))    # H, Hmax, Hmin
        pres_vals = _parse_group(match.group(4))   # B, Bmax, Bmin
        wind_vals = _parse_group(match.group(5))   # W, Wmax, Azim
        prec_vals = _parse_group(match.group(6))   # P
        name_from_feed = match.group(7).strip()

        # Temperature group: T;Tmax;Tmin;condition  (condition is a string, not float)
        temp_parts = [p.strip() for p in temp_raw.split(";")]
        temp_current = _parse_float(temp_parts[0]) if len(temp_parts) > 0 else None
        temp_max     = _parse_float(temp_parts[1]) if len(temp_parts) > 1 else None
        temp_min     = _parse_float(temp_parts[2]) if len(temp_parts) > 2 else None
        condition_raw = temp_parts[3] if len(temp_parts) > 3 else None
        if condition_raw and condition_raw not in _CONDITION_MAP:
            _LOGGER.warning(
                "Andorra Meteo: unknown condition value '%s' from station %s — "
                "add it to _CONDITION_MAP in coordinator.py",
                condition_raw, code,
            )
        condition = _CONDITION_MAP.get(condition_raw) if condition_raw else None

        def _get(lst: list, idx: int) -> float | None:
            try:
                return lst[idx]
            except IndexError:
                return None

        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
        self._last_successful_update = now

        return {
            "station_code": code,
            "station_name": name_from_feed,
            "last_updated": now,
            # Temperature
            "temperature": temp_current,
            "temperature_max": temp_max,
            "temperature_min": temp_min,
            # Condition (mapped to HA standard string)
            "condition": condition,
            # Humidity
            "humidity": _get(hum_vals, 0),
            "humidity_max": _get(hum_vals, 1),
            "humidity_min": _get(hum_vals, 2),
            # Pressure
            "pressure": _get(pres_vals, 0),
            "pressure_max": _get(pres_vals, 1),
            "pressure_min": _get(pres_vals, 2),
            # Wind
            "wind_speed": _get(wind_vals, 0),
            "wind_gust": _get(wind_vals, 1),
            "wind_bearing": _get(wind_vals, 2),
            # Precipitation
            "precipitation": _get(prec_vals, 0),
        }


class StationDiscoveryCoordinator(DataUpdateCoordinator):
    """Daily coordinator that checks for new Andorra stations in Meteoclimatic."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialise."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_discovery",
            update_interval=timedelta(hours=24),
        )

    async def _async_update_data(self) -> list[str]:
        """Fetch the ADAND feed and return any unknown station codes."""
        from .const import METEOCLIMATIC_FEED_URL, STATION_BY_CODE

        url = METEOCLIMATIC_FEED_URL.format("ADAND")
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"HTTP {resp.status} fetching ADAND feed")
                text = await resp.text(encoding="utf-8", errors="replace")
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Network error fetching ADAND feed: {err}") from err

        # Extract all ADAND codes from the feed
        found_codes = set(re.findall(r"ADAND\w+", text))
        known_codes = set(STATION_BY_CODE.keys())
        new_codes = sorted(found_codes - known_codes)

        if new_codes:
            _LOGGER.info(
                "Andorra Meteo: new station(s) detected in Meteoclimatic: %s",
                new_codes,
            )

        return new_codes


# ---------------------------------------------------------------------------
# Avalanche coordinator
# ---------------------------------------------------------------------------

def _extract_danger_level(img_src: str) -> int:
    """Extract numeric danger level from image src like 'ico-risque/3.png'. Returns 0 if not found."""
    m = re.search(r"ico-risque/(\d)\.png", img_src)
    if m:
        val = int(m.group(1))
        return val if 1 <= val <= 5 else 0
    return 0


# Mapping from image filename fragment to Catalan problem description
_PROBLEM_MAP = {
    "neu_ventada": "Neu ventada",
    "neu_humida": "Neu humida",
    "neu_nova": "Neu nova",
    "placa": "Plaques",
    "allau_persistent": "Capes febles persistents",
    "allau_humida": "Allaus humides",
    "allau_fons": "Allaus de fons",
}


def _extract_problem_type(img_src: str) -> str | None:
    """Extract avalanche problem type from image filename, mapped to Catalan."""
    for key, label in _PROBLEM_MAP.items():
        if key in img_src:
            return label
    # Fallback: clean up the filename if no mapping found
    m = re.search(r"ico-risque/([^/]+)\.jpg", img_src)
    if m:
        return m.group(1).replace("_", " ").capitalize()
    return None


def _extract_trend(img_src: str) -> str | None:
    """Extract trend from image filename."""
    mapping = {
        "24_igual": "Estable",
        "24_puja": "En augment",
        "24_baixa": "En descens",
    }
    for key, val in mapping.items():
        if key in img_src:
            return val
    return None


class AvalancheCoordinator(DataUpdateCoordinator):
    """Coordinator for the meteo.ad avalanche bulletin."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialise."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_avalanche",
            update_interval=timedelta(seconds=SCAN_INTERVAL_AVALANCHE),
        )

    async def _async_update_data(self) -> dict:
        """Fetch and parse the avalanche bulletin page."""
        session = async_get_clientsession(self.hass)
        try:
            async with session.get(
                AVALANCHE_URL, timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"HTTP {resp.status} from meteo.ad avalanche page")
                html = await resp.text(encoding="utf-8", errors="replace")
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Network error fetching avalanche bulletin: {err}") from err

        return await self.hass.async_add_executor_job(self._parse_bulletin, html)

    @staticmethod
    def _parse_bulletin(html: str) -> dict:
        """Parse the avalanche bulletin HTML (runs in executor thread)."""
        soup = BeautifulSoup(html, "html.parser")

        # ---- validity dates ------------------------------------------------
        valid_text = ""
        for tag in soup.find_all(string=True):
            text = tag.strip()
            if "valid until" in text.lower() or "vàlid fins" in text.lower():
                valid_text = text
                break

        # Extract "Prepared on DD/MM/YYYY HH:MM, valid until DD/MM/YYYY"
        prepared_on = None
        valid_until = None
        date_match = re.search(
            r"(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2}).*?(\d{2}/\d{2}/\d{4})",
            valid_text,
        )
        if date_match:
            prepared_on = f"{date_match.group(1)} {date_match.group(2)}"
            valid_until = date_match.group(3)

        # ---- danger levels by zone -----------------------------------------
        # The page has three zone sections (North, Centre, South) in order.
        # Each contains an <img> with src matching "ico-risque/N.png".
        danger_imgs = [
            img for img in soup.find_all("img")
            if img.get("src", "") and "ico-risque/" in img["src"]
            and re.search(r"ico-risque/\d\.png", img["src"])
        ]

        def _safe_level(imgs: list, idx: int) -> int:
            try:
                return _extract_danger_level(imgs[idx]["src"])
            except IndexError:
                return 0

        danger_north = _safe_level(danger_imgs, 0)
        danger_centre = _safe_level(danger_imgs, 1)
        danger_south = _safe_level(danger_imgs, 2)

        # ---- avalanche problem types ----------------------------------------
        problem_imgs = [
            img for img in soup.find_all("img")
            if img.get("src", "") and "ico-risque/" in img["src"]
            and img["src"].endswith(".jpg")
        ]

        def _safe_problem(imgs: list, idx: int) -> str | None:
            try:
                return _extract_problem_type(imgs[idx]["src"])
            except IndexError:
                return None

        problem_north = _safe_problem(problem_imgs, 0)
        problem_centre = _safe_problem(problem_imgs, 1)
        problem_south = _safe_problem(problem_imgs, 2)

        # ---- trend ----------------------------------------------------------
        trend_imgs = [
            img for img in soup.find_all("img")
            if img.get("src", "") and "24_" in img["src"]
        ]
        trend_north = _extract_trend(trend_imgs[0]["src"]) if len(trend_imgs) > 0 else None
        trend_centre = _extract_trend(trend_imgs[1]["src"]) if len(trend_imgs) > 1 else None
        trend_south = _extract_trend(trend_imgs[2]["src"]) if len(trend_imgs) > 2 else None

        # ---- descriptive text blocks ----------------------------------------
        # The page has two main paragraph blocks: snowpack stability + snow quality.
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
        stability_text = ""
        quality_text = ""
        for i, para in enumerate(paragraphs):
            lower = para.lower()
            if any(kw in lower for kw in ["manto", "mantle", "mantell", "snowpack", "estabilitat"]):
                stability_text = para
            elif any(kw in lower for kw in ["qualitat", "quality", "calidad", "wind slab", "neu"]):
                if not stability_text or para != stability_text:
                    quality_text = para

        return {
            "prepared_on": prepared_on,
            "valid_until": valid_until,
            "danger_north": danger_north,
            "danger_centre": danger_centre,
            "danger_south": danger_south,
            "problem_north": problem_north,
            "problem_centre": problem_centre,
            "problem_south": problem_south,
            "trend_north": trend_north,
            "trend_centre": trend_centre,
            "trend_south": trend_south,
            "stability_text": stability_text,
            "quality_text": quality_text,
        }
        