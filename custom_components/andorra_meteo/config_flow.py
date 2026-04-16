"""Config flow for Andorra Meteo."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_ENTRY_TYPE,
    CONF_PARISH,
    CONF_STATION_CODE,
    CONF_STATION_NAME,
    DOMAIN,
    ENTRY_TYPE_AVALANCHE,
    ENTRY_TYPE_STATION,
    METEOCLIMATIC_FEED_URL,
    PARISHES,
    STATION_BY_CODE,
)

_LOGGER = logging.getLogger(__name__)

# Special key used in the first dropdown to represent the avalanche bulletin option
_AVALANCHE_KEY = "__avalanche__"

# First step options: parishes + avalanche bulletin at the end
_FIRST_STEP_OPTIONS = {
    **{key: data["name"] for key, data in PARISHES.items()},
    _AVALANCHE_KEY: "Butlletí d'allaus — Principat d'Andorra",
}


class MeteoAndorraConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Andorra Meteo."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialise."""
        self._parish: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Step 1: choose parish or avalanche bulletin."""
        if user_input is not None:
            selection = user_input[CONF_PARISH]
            if selection == _AVALANCHE_KEY:
                return await self.async_step_avalanche()
            self._parish = selection
            parish_data = PARISHES[self._parish]
            # If parish has only one station, skip station selection step
            if len(parish_data["stations"]) == 1:
                return await self._create_station_entry(
                    parish_data["stations"][0]["code"]
                )
            return await self.async_step_station()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_PARISH): vol.In(_FIRST_STEP_OPTIONS)}
            ),
        )

    # ------------------------------------------------------------------
    # Avalanche bulletin — no further options needed
    # ------------------------------------------------------------------
    async def async_step_avalanche(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Set up the avalanche bulletin entry."""
        await self.async_set_unique_id(f"{DOMAIN}_avalanche")
        self._abort_if_unique_id_configured(error="single_instance_allowed")

        return self.async_create_entry(
            title="Butlletí d'allaus — Principat d'Andorra",
            data={CONF_ENTRY_TYPE: ENTRY_TYPE_AVALANCHE},
        )

    # ------------------------------------------------------------------
    # Station — only shown when parish has multiple stations (Escaldes)
    # ------------------------------------------------------------------
    async def async_step_station(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Step 2 (only for multi-station parishes): select station."""
        errors: dict[str, str] = {}
        parish_data = PARISHES[self._parish]
        station_options = {st["code"]: st["name"] for st in parish_data["stations"]}

        if user_input is not None:
            return await self._create_station_entry(
                user_input[CONF_STATION_CODE], errors
            )

        return self.async_show_form(
            step_id="station",
            data_schema=vol.Schema(
                {vol.Required(CONF_STATION_CODE): vol.In(station_options)}
            ),
            errors=errors,
            description_placeholders={"parish": parish_data["name"]},
        )

    async def _create_station_entry(
        self, code: str, errors: dict[str, str] | None = None
    ) -> ConfigFlowResult:
        """Validate and create a station config entry."""
        if errors is None:
            errors = {}

        ok, err_key = await self._validate_station(code)
        if not ok:
            errors["base"] = err_key
            # Re-show station form on error (only reached for multi-station parishes)
            parish_data = PARISHES[self._parish]
            station_options = {st["code"]: st["name"] for st in parish_data["stations"]}
            return self.async_show_form(
                step_id="station",
                data_schema=vol.Schema(
                    {vol.Required(CONF_STATION_CODE): vol.In(station_options)}
                ),
                errors=errors,
                description_placeholders={"parish": parish_data["name"]},
            )

        station_info = STATION_BY_CODE.get(code, {})
        station_name = station_info.get("name", code)
        parish_data = PARISHES[self._parish]

        await self.async_set_unique_id(f"{DOMAIN}_station_{code}")
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=f"{station_name} — {parish_data['name']}",
            data={
                CONF_ENTRY_TYPE: ENTRY_TYPE_STATION,
                CONF_STATION_CODE: code,
                CONF_STATION_NAME: station_name,
                CONF_PARISH: self._parish,
            },
        )

    async def _validate_station(self, code: str) -> tuple[bool, str]:
        """Fetch the RSS feed and confirm data is present."""
        session = async_get_clientsession(self.hass)
        url = METEOCLIMATIC_FEED_URL.format(code)
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return False, "cannot_connect"
                text = await resp.text()
                if code not in text and "BEGIN:" not in text:
                    return False, "station_offline"
                return True, ""
        except aiohttp.ClientError:
            return False, "cannot_connect"
        except Exception:  # noqa: BLE001
            return False, "unknown"
            