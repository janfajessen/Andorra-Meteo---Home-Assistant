"""Andorra Meteo integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_ENTRY_TYPE,
    CONF_STATION_CODE,
    CONF_STATION_NAME,
    DOMAIN,
    ENTRY_TYPE_AVALANCHE,
    ENTRY_TYPE_STATION,
)
from .coordinator import (
    AvalancheCoordinator,
    MeteoclimaticCoordinator,
    StationDiscoveryCoordinator,
)

_LOGGER = logging.getLogger(__name__)

# Platforms used by each entry type
_STATION_PLATFORMS = [Platform.WEATHER, Platform.SENSOR]
_AVALANCHE_PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]

# Key used to store the shared discovery coordinator in hass.data
_DISCOVERY_KEY = f"{DOMAIN}_discovery"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Andorra Meteo from a config entry."""
    entry_type = entry.data[CONF_ENTRY_TYPE]

    if entry_type == ENTRY_TYPE_STATION:
        coordinator = MeteoclimaticCoordinator(
            hass,
            station_code=entry.data[CONF_STATION_CODE],
            station_name=entry.data[CONF_STATION_NAME],
        )
        await coordinator.async_config_entry_first_refresh()
        entry.runtime_data = coordinator
        await hass.config_entries.async_forward_entry_setups(entry, _STATION_PLATFORMS)

    elif entry_type == ENTRY_TYPE_AVALANCHE:
        coordinator = AvalancheCoordinator(hass)
        await coordinator.async_config_entry_first_refresh()
        entry.runtime_data = coordinator
        await hass.config_entries.async_forward_entry_setups(entry, _AVALANCHE_PLATFORMS)

    else:
        _LOGGER.error("Unknown Andorra Meteo entry type: %s", entry_type)
        return False

    # Start the shared discovery coordinator once (shared across all entries)
    await _async_setup_discovery(hass)

    return True


async def _async_setup_discovery(hass: HomeAssistant) -> None:
    """Start the station discovery coordinator if not already running."""
    if _DISCOVERY_KEY in hass.data:
        return  # Already running

    discovery = StationDiscoveryCoordinator(hass)
    hass.data[_DISCOVERY_KEY] = discovery

    # Register callback: notify when new stations are found
    async def _on_discovery_update() -> None:
        new_codes: list[str] = discovery.data or []
        if not new_codes:
            return
        codes_str = ", ".join(new_codes)
        hass.components.persistent_notification.async_create(
            title="Andorra Meteo — Noves estacions detectades",
            message=(
                f"S'han detectat estacions noves a Meteoclimatic que no estan "
                f"configurades a la integració:\n\n**{codes_str}**\n\n"
                "Si corresponen a noves parròquies (Andorra la Vella, La Massana...), "
                "consulta el repositori de la integració per actualitzar-la."
            ),
            notification_id=f"{DOMAIN}_new_stations",
        )

    discovery.async_add_listener(_on_discovery_update)
    await discovery.async_refresh()


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    entry_type = entry.data[CONF_ENTRY_TYPE]
    platforms = _STATION_PLATFORMS if entry_type == ENTRY_TYPE_STATION else _AVALANCHE_PLATFORMS
    unloaded = await hass.config_entries.async_unload_platforms(entry, platforms)

    # Remove discovery coordinator only when the last entry is unloaded
    remaining = [
        e for e in hass.config_entries.async_entries(DOMAIN)
        if e.entry_id != entry.entry_id
    ]
    if not remaining and _DISCOVERY_KEY in hass.data:
        hass.data.pop(_DISCOVERY_KEY)

    return unloaded
    