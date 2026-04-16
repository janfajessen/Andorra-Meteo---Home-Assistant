"""Binary sensor for the Andorra Meteo avalanche module."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import AVALANCHE_WARN_LEVEL, DOMAIN
from .coordinator import AvalancheCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensor for avalanche module."""
    coordinator: AvalancheCoordinator = entry.runtime_data

    device_info = DeviceInfo(
        identifiers={(DOMAIN, "avalanche")},
        name="Butlletí d'allaus — Principat d'Andorra",
        manufacturer="Servei Meteorològic Nacional d'Andorra",
        model="Butlletí d'allaus",
        entry_type=DeviceEntryType.SERVICE,
        configuration_url="https://www.meteo.ad/neu",
    )
    async_add_entities([AvalancheWarningBinarySensor(coordinator, device_info)])


class AvalancheWarningBinarySensor(
    CoordinatorEntity[AvalancheCoordinator], BinarySensorEntity
):
    """Binary sensor: True when avalanche danger is Considerable (≥3) in any zone."""

    _attr_has_entity_name = True
    _attr_name = "Avís d'allaus actiu"
    _attr_device_class = BinarySensorDeviceClass.SAFETY
    _attr_icon = "mdi:alert-octagon"

    def __init__(self, coordinator: AvalancheCoordinator, device_info: DeviceInfo) -> None:
        """Initialise."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_avalanche_warning"
        self._attr_device_info = device_info

    @property
    def is_on(self) -> bool:
        """Return True if any zone has danger level >= AVALANCHE_WARN_LEVEL."""
        data = self.coordinator.data
        levels = [
            data.get("danger_north"),
            data.get("danger_centre"),
            data.get("danger_south"),
        ]
        return any(
            isinstance(level, int) and level >= AVALANCHE_WARN_LEVEL
            for level in levels
        )

    @property
    def extra_state_attributes(self) -> dict:
        """Return danger levels per zone as attributes."""
        data = self.coordinator.data
        return {
            "danger_north": data.get("danger_north"),
            "danger_centre": data.get("danger_centre"),
            "danger_south": data.get("danger_south"),
            "valid_until": data.get("valid_until"),
            "prepared_on": data.get("prepared_on"),
        }
        