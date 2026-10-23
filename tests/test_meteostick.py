# Copyright 2026 weewx-packages
# Distributed under the terms of the GNU Public License (GPLv3)
import binascii
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import Mock

import pytest
import weewx

spec = importlib.util.spec_from_file_location('meteostick', Path(__file__).parents[1] / 'bin/user/meteostick.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_crc_packet_and_corruption():
    data = bytes.fromhex('800985191b00')
    crc = binascii.crc_hqx(data, 0)
    raw = 'I 102 ' + ' '.join('%02X' % x for x in data + crc.to_bytes(2, 'big') + b'\xff\xff') + ' -65 5249944 202'
    result = m.Meteostick.parse_raw(raw, 1, 0, 0, 0, 0, .2)
    assert result['channel'] == 1
    corrupt = raw.replace('80 09', '80 08')
    with pytest.raises(ValueError, match='CRC error'):
        m.Meteostick.parse_raw(corrupt, 1, 0, 0, 0, 0, .2)


def test_reset_ignores_junk_and_flushes(monkeypatch):
    monkeypatch.setattr(m.time, 'sleep', lambda _: None)
    station = m.Meteostick()
    station.serial_port = Mock()
    station.serial_port.inWaiting.side_effect = [1, 1, 1, 0]
    station.serial_port.read.side_effect = [b'\xff', b'M', b'?']
    station.reset()
    station.serial_port.write.assert_called_once_with(b'\nr\n')
    station.serial_port.reset_output_buffer.assert_called_once()
    station.serial_port.flush.assert_called_once()


def test_timeout_resets_and_recovers(monkeypatch):
    monkeypatch.setattr(m.time, 'sleep', lambda _: None)
    station = m.Meteostick()
    station.get_readings = Mock(side_effect=['', 'B 1 2 3 4 5'])
    station.reset = Mock()
    station.configure = Mock()
    assert station.get_readings_with_retry(retry_wait=0) == 'B 1 2 3 4 5'
    station.reset.assert_called_once()
    station.configure.assert_called_once()


def test_timeout_retries_are_bounded(monkeypatch):
    monkeypatch.setattr(m.time, 'sleep', lambda _: None)
    station = m.Meteostick()
    station.get_readings = Mock(return_value='')
    station.reset = Mock()
    station.configure = Mock()
    with pytest.raises(weewx.RetriesExceeded, match='Max retries'):
        station.get_readings_with_retry(max_tries=2, retry_wait=0)
    assert station.reset.call_count == 2


def test_weewx_logging(caplog):
    with caplog.at_level('INFO'):
        m.loginf('serial fixture')
    assert 'serial fixture' in caplog.text


def test_standalone_entry_point():
    env = dict(os.environ, PYTHONPATH=str(Path(__file__).parents[1] / 'bin'))
    result = subprocess.run([sys.executable, '-m', 'user.meteostick', '--version'],
                            env=env, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    assert 'meteostick driver version' in result.stdout
