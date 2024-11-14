import os
import sys
from unittest.mock import MagicMock

import pytest

from src.main import UI, Manager

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def ui_instance():
    ui = UI()
    ui.manager = MagicMock()
    ui.ram_label = MagicMock()
    return ui


def test_refresh_ram_info_low_usage(ui_instance):
    ui_instance.manager.show_ram_info.return_value = {
        "used": "4.0",
        "total": "16.0",
        "percent": 25.0,
    }
    ui_instance.refresh_ram_info()
    ui_instance.ram_label.classes.assert_any_call(remove="text-warning")
    ui_instance.ram_label.classes.assert_any_call(remove="text-negative")
    ui_instance.ram_label.classes.assert_any_call(add="text-positive")
    assert ui_instance.ram_label.text == "RAM usage: 4.0 GB / 16.0 GB (25.0%)"


def test_refresh_ram_info_medium_usage(ui_instance):
    ui_instance.manager.show_ram_info.return_value = {
        "used": "10.0",
        "total": "16.0",
        "percent": 62.5,
    }
    ui_instance.refresh_ram_info()
    ui_instance.ram_label.classes.assert_any_call(remove="text-positive")
    ui_instance.ram_label.classes.assert_any_call(remove="text-negative")
    ui_instance.ram_label.classes.assert_any_call(add="text-warning")
    assert ui_instance.ram_label.text == "RAM usage: 10.0 GB / 16.0 GB (62.5%)"


def test_refresh_ram_info_high_usage(ui_instance):
    ui_instance.manager.show_ram_info.return_value = {
        "used": "14.0",
        "total": "16.0",
        "percent": 87.5,
    }
    ui_instance.refresh_ram_info()
    ui_instance.ram_label.classes.assert_any_call(remove="text-warning")
    ui_instance.ram_label.classes.assert_any_call(remove="text-positive")
    ui_instance.ram_label.classes.assert_any_call(add="text-negative")
    assert ui_instance.ram_label.text == "RAM usage: 14.0 GB / 16.0 GB (87.5%)"


def test_bytes_to_gb_conversion():
    manager = Manager()
    assert manager.bytes_to_gb(1073741824) == "1.0"
    assert manager.bytes_to_gb(2147483648) == "2.0"


def test_show_ram_info():
    manager = Manager()
    ram_info = manager.show_ram_info()
    assert "total" in ram_info
    assert "used" in ram_info
    assert "percent" in ram_info
    assert isinstance(ram_info["percent"], float)


def test_get_cpu_name():
    manager = Manager()
    cpu_name = manager.get_cpu_name()
    assert isinstance(cpu_name, str)
    assert len(cpu_name) > 0
