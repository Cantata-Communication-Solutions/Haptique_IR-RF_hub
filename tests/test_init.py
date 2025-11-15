"""Test the Haptique IR/RF Hub init."""
import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.haptique_ir_rf_hub.const import DOMAIN

pytestmark = pytest.mark.asyncio


async def test_setup_entry(hass: HomeAssistant, init_integration: MockConfigEntry) -> None:
    """Test setup entry."""
    assert init_integration.state == ConfigEntryState.LOADED
    assert DOMAIN in hass.data


async def test_unload_entry(
    hass: HomeAssistant, init_integration: MockConfigEntry
) -> None:
    """Test unload entry."""
    assert await hass.config_entries.async_unload(init_integration.entry_id)
    await hass.async_block_till_done()
    assert init_integration.state == ConfigEntryState.NOT_LOADED
