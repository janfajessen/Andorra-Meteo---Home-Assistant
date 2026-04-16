"""Weather entity for Andorra Meteo (station module)."""
from __future__ import annotations

from homeassistant.components.weather import WeatherEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPressure, UnitOfSpeed, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_PARISH, CONF_STATION_CODE, CONF_STATION_NAME, DOMAIN, PARISHES, STATION_BY_CODE
from .coordinator import MeteoclimaticCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the weather entity."""
    coordinator: MeteoclimaticCoordinator = entry.runtime_data
    async_add_entities([MeteoAndorraWeather(coordinator, entry)])


class MeteoAndorraWeather(CoordinatorEntity[MeteoclimaticCoordinator], WeatherEntity):
    """Weather entity for a Meteoclimatic station in Andorra."""

    _attr_has_entity_name = True
    _attr_name = None  # Uses the device name as entity name
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
    _attr_native_pressure_unit = UnitOfPressure.HPA

    def __init__(
        self,
        coordinator: MeteoclimaticCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialise."""
        super().__init__(coordinator)
        self._entry = entry
        station_code = entry.data[CONF_STATION_CODE]
        self._attr_unique_id = f"{DOMAIN}_{station_code}_weather"
        parish_key = entry.data.get(CONF_PARISH, "")
        parish_name = PARISHES.get(parish_key, {}).get("name", "")
        station_name = entry.data[CONF_STATION_NAME]
        location = STATION_BY_CODE.get(station_code, {}).get("location", "")

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, station_code)},
            name=f"{station_name} — {parish_name}",
            model=location,
            configuration_url=f"https://www.meteoclimatic.net/perfil/{station_code}",
        )

    @property
    def condition(self) -> str | None:
        """Return current weather condition from Meteoclimatic feed.

        Meteoclimatic sends 'sun' during the day and 'moon' at night,
        so day/night detection is handled natively by the data source.
        """
        return self.coordinator.data.get("condition")

    @property
    def native_temperature(self) -> float | None:
        """Return current temperature."""
        return self.coordinator.data.get("temperature")

    @property
    def humidity(self) -> float | None:
        """Return current humidity."""
        return self.coordinator.data.get("humidity")

    @property
    def native_pressure(self) -> float | None:
        """Return current pressure."""
        return self.coordinator.data.get("pressure")

    @property
    def native_wind_speed(self) -> float | None:
        """Return current wind speed."""
        return self.coordinator.data.get("wind_speed")

    @property
    def wind_bearing(self) -> float | None:
        """Return current wind bearing in degrees."""
        return self.coordinator.data.get("wind_bearing")
        