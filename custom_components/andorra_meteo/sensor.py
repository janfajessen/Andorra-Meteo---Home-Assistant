"""Sensor entities for Andorra Meteo."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    DEGREE,
    PERCENTAGE,
    UnitOfPrecipitationDepth,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_ENTRY_TYPE,
    CONF_PARISH,
    CONF_STATION_CODE,
    CONF_STATION_NAME,
    DOMAIN,
    ENTRY_TYPE_AVALANCHE,
    ENTRY_TYPE_STATION,
    PARISHES,
    STATION_BY_CODE,
)
from .coordinator import AvalancheCoordinator, MeteoclimaticCoordinator


# ---------------------------------------------------------------------------
# Station sensor descriptors
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StationSensorDescription(SensorEntityDescription):
    """Descriptor for station sensors, adding a data key."""
    data_key: str = ""


STATION_SENSORS: tuple[StationSensorDescription, ...] = (
    StationSensorDescription(
        key="temperature",
        data_key="temperature",
        name="Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="temperature_max",
        data_key="temperature_max",
        name="Daily Max Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="temperature_min",
        data_key="temperature_min",
        name="Daily Min Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="humidity",
        data_key="humidity",
        name="Humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="humidity_max",
        data_key="humidity_max",
        name="Daily Max Humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="humidity_min",
        data_key="humidity_min",
        name="Daily Min Humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="pressure",
        data_key="pressure",
        name="Pressure",
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="pressure_max",
        data_key="pressure_max",
        name="Daily Max Pressure",
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="pressure_min",
        data_key="pressure_min",
        name="Daily Min Pressure",
        native_unit_of_measurement=UnitOfPressure.HPA,
        device_class=SensorDeviceClass.PRESSURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="wind_speed",
        data_key="wind_speed",
        name="Wind Speed",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="wind_gust",
        data_key="wind_gust",
        name="Daily Max Wind Speed",
        native_unit_of_measurement=UnitOfSpeed.KILOMETERS_PER_HOUR,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="wind_bearing",
        data_key="wind_bearing",
        name="Wind Bearing",
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:compass-rose",
    ),
    StationSensorDescription(
        key="wind_direction",
        data_key="wind_bearing",
        name="Wind Direction",
        icon="mdi:compass-rose",
    ),
    StationSensorDescription(
        key="precipitation",
        data_key="precipitation",
        name="Daily Precipitation",
        native_unit_of_measurement=UnitOfPrecipitationDepth.MILLIMETERS,
        device_class=SensorDeviceClass.PRECIPITATION,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    StationSensorDescription(
        key="last_updated",
        data_key="last_updated",
        name="Última actualització",
        icon="mdi:clock-check-outline",
    ),
)


# ---------------------------------------------------------------------------
# Avalanche sensor descriptors
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class AvalancheSensorDescription(SensorEntityDescription):
    """Descriptor for avalanche sensors."""
    data_key: str = ""
    extra_attrs_keys: tuple[str, ...] = ()


AVALANCHE_SENSORS: tuple[AvalancheSensorDescription, ...] = (
    # --- Danger levels per zone ---
    AvalancheSensorDescription(
        key="danger_north",
        data_key="danger_north",
        name="Nivell de perill d'allaus — Nord",
        icon="mdi:landslide-outline",
        state_class=SensorStateClass.MEASUREMENT,
        extra_attrs_keys=("trend_north", "stability_text", "quality_text",
                          "prepared_on", "valid_until"),
    ),
    AvalancheSensorDescription(
        key="danger_centre",
        data_key="danger_centre",
        name="Nivell de perill d'allaus — Centre",
        icon="mdi:landslide-outline",
        state_class=SensorStateClass.MEASUREMENT,
        extra_attrs_keys=("trend_centre", "prepared_on", "valid_until"),
    ),
    AvalancheSensorDescription(
        key="danger_south",
        data_key="danger_south",
        name="Nivell de perill d'allaus — Sud",
        icon="mdi:landslide-outline",
        state_class=SensorStateClass.MEASUREMENT,
        extra_attrs_keys=("trend_south", "prepared_on", "valid_until"),
    ),
    # --- Problem type per zone (text sensor, changes with snowpack type) ---
    AvalancheSensorDescription(
        key="problem_north",
        data_key="problem_north",
        name="Tipus de neu — Zona nord",
        icon="mdi:snowflake-alert",
    ),
    AvalancheSensorDescription(
        key="problem_centre",
        data_key="problem_centre",
        name="Tipus de neu — Zona centre",
        icon="mdi:snowflake-alert",
    ),
    AvalancheSensorDescription(
        key="problem_south",
        data_key="problem_south",
        name="Tipus de neu — Zona sud",
        icon="mdi:snowflake-alert",
    ),
    # --- Bulletin validity ---
    AvalancheSensorDescription(
        key="valid_until",
        data_key="valid_until",
        name="Butlletí vàlid fins",
        icon="mdi:calendar-clock",
        extra_attrs_keys=("prepared_on",),
    ),
)


# ---------------------------------------------------------------------------
# Platform setup
# ---------------------------------------------------------------------------

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities."""
    entry_type = entry.data[CONF_ENTRY_TYPE]

    if entry_type == ENTRY_TYPE_STATION:
        coordinator: MeteoclimaticCoordinator = entry.runtime_data
        station_code = entry.data[CONF_STATION_CODE]
        parish_key = entry.data.get(CONF_PARISH, "")
        parish_name = PARISHES.get(parish_key, {}).get("name", "")
        station_name = entry.data[CONF_STATION_NAME]
        location = STATION_BY_CODE.get(station_code, {}).get("location", "")

        device_info = DeviceInfo(
            identifiers={(DOMAIN, station_code)},
            name=f"{station_name} — {parish_name}",
            model=location,
            configuration_url=f"https://www.meteoclimatic.net/perfil/{station_code}",
        )
        async_add_entities(
            StationSensor(coordinator, description, station_code, device_info)
            for description in STATION_SENSORS
        )

    elif entry_type == ENTRY_TYPE_AVALANCHE:
        av_coordinator: AvalancheCoordinator = entry.runtime_data
        device_info = DeviceInfo(
            identifiers={(DOMAIN, "avalanche")},
            name="Butlletí d'allaus — Principat d'Andorra",
            manufacturer="Servei Meteorològic Nacional d'Andorra",
            model="Butlletí d'allaus",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url="https://www.meteo.ad/neu",
        )
        async_add_entities(
            AvalancheSensor(av_coordinator, description, device_info)
            for description in AVALANCHE_SENSORS
        )


# ---------------------------------------------------------------------------
# Wind bearing → compass direction (16-point rose, Catalan abbreviations)
# Same abbreviations used in CA, ES, FR — only difference would be O vs W
# which is not relevant since we use Catalan as the base language.
# ---------------------------------------------------------------------------

_COMPASS_POINTS = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]


def _bearing_to_direction(degrees: float | None) -> str | None:
    """Convert a bearing in degrees to an 8-point compass abbreviation."""
    if degrees is None:
        return None
    idx = round(float(degrees) / 45.0) % 8
    return _COMPASS_POINTS[idx]


# ---------------------------------------------------------------------------
# Station sensor entity
# ---------------------------------------------------------------------------

class StationSensor(CoordinatorEntity[MeteoclimaticCoordinator], SensorEntity):
    """A sensor from a Meteoclimatic station."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MeteoclimaticCoordinator,
        description: StationSensorDescription,
        station_code: str,
        device_info: DeviceInfo,
    ) -> None:
        """Initialise."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{station_code}_{description.key}"
        self._attr_device_info = device_info

    @property
    def native_value(self) -> float | str | None:
        """Return the sensor value, converting bearing to direction text when needed."""
        raw = self.coordinator.data.get(self.entity_description.data_key)
        if self.entity_description.key == "wind_direction":
            return _bearing_to_direction(raw)
        return raw


_AVALANCHE_ZONE_DESCRIPTION = {
    "danger_north": "Ordino, Canillo (Arcalís, Grandvalira nord, El Serrat)",
    "danger_centre": "Encamp, Escaldes-Engordany (Grandvalira central, Pas de la Casa)",
    "danger_south": "Sant Julià de Lòria, Andorra la Vella",
}

_AVALANCHE_LEVEL_NAMES_FULL = {
    0: "Sense perill",
    1: "Feble",
    2: "Limitat",
    3: "Marcat",
    4: "Fort",
    5: "Molt fort",
}


# ---------------------------------------------------------------------------
# Avalanche sensor entity
# ---------------------------------------------------------------------------

class AvalancheSensor(CoordinatorEntity[AvalancheCoordinator], SensorEntity):
    """A sensor from the avalanche bulletin."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: AvalancheCoordinator,
        description: AvalancheSensorDescription,
        device_info: DeviceInfo,
    ) -> None:
        """Initialise."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_avalanche_{description.key}"
        self._attr_device_info = device_info

    @property
    def native_value(self) -> Any:
        """Return the sensor value (numeric for danger levels, text for problem types)."""
        return self.coordinator.data.get(self.entity_description.data_key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        attrs: dict[str, Any] = {}
        data = self.coordinator.data
        for key in self.entity_description.extra_attrs_keys:
            attrs[key] = data.get(key)

        # Add human-readable level name and zone description for danger sensors
        if self.entity_description.key.startswith("danger"):
            val = data.get(self.entity_description.data_key)
            level = val if isinstance(val, int) else 0
            attrs["level_name"] = _AVALANCHE_LEVEL_NAMES_FULL.get(level, "")
            zone_desc = _AVALANCHE_ZONE_DESCRIPTION.get(self.entity_description.key, "")
            if zone_desc:
                attrs["zones"] = zone_desc

        return attrs
        