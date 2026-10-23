# Meteostick for WeeWX

Receive Davis wireless weather transmissions with a Meteostick connected by
serial/USB. The driver configures the receiver's raw format and decodes ISS,
separate anemometer, leaf/soil and up to two extra temperature/humidity stations.
Frequency plans are `EU`, `US` and `AU`; select the plan for your hardware.

This independent continuation preserves
[matthewwall/weewx-meteostick](https://github.com/matthewwall/weewx-meteostick)
history. Version 0.68.1 fixes byte-based CRC handling and bounded recovery after
empty serial reads. Physical reception after a reset still needs device checks.

## Install

An existing WeeWX station is required. Replace `/path/to/weewx.conf`
with its configuration file before running the commands.

The catalog release requires Python >=3.10 and WeeWX >=5.2,<6.

Before running the commands, activate the existing virtual environment that
runs your WeeWX service. Both `python` and `weectl` must come from that
environment. For an OS-packaged WeeWX installation, use compatible distribution
packages instead, or migrate WeeWX and its service to a virtual environment
first. Installing into an unrelated virtual environment will not supply the
running service with dependencies.

Install `pyserial` into the WeeWX Python environment:

```sh
python -m pip install 'pyserial==3.5'
```

The distribution is named `pyserial`; it provides the `serial` import.
Do not install the different package named `serial`.

Use the `weectl` from your WeeWX Python environment:

```sh
weectl extension install https://github.com/weewx-packages/weewx-meteostick/releases/download/v0.68.1/weewx-meteostick-0.68.1.zip --config=/path/to/weewx.conf
weectl station reconfigure --driver=user.meteostick --config=/path/to/weewx.conf
```

Stock WeeWX 5 accepts this fixed URL or a downloaded copy of the same archive.
No catalog integration is required. Restart WeeWX yourself after configuration
changes.

## Select transmitters

```ini
[Station]
    station_type = Meteostick
[Meteostick]
    driver = user.meteostick
    port = /dev/ttyUSB0
    transceiver_frequency = EU
    iss_channel = 1
    rain_bucket_type = 1
```

Give the WeeWX service user access to the serial device. The default serial rate
is 115200 baud. Set `iss_channel` to the transmitter channel, 1 through 8.
`rain_bucket_type = 1` means 0.2 mm per tip; `0` means 0.01 inch per tip.

Optional `anemometer_channel`, `leaf_soil_channel`, `temp_hum_1_channel` and
`temp_hum_2_channel` select additional transmitters. Zero disables an extra
transmitter; anemometer zero uses ISS wind. `[[sensor_map]]` extends or overrides
the built-in observation map in [meteostick.py](bin/user/meteostick.py).

The default `rf_sensitivity` is 90, meaning -90 dB. Increasing it can admit noise
and false readings. `max_tries` and `retry_wait` bound recovery attempts. This
package needs a physical Meteostick; it does not run `rtl_433` or read cloud data.

Stop WeeWX before receiver diagnostics. After selecting this driver, inspect
its device configurator options without opening hardware:

```sh
weectl device --help --config=/path/to/weewx.conf
```

The standalone `python -m user.meteostick` entry point fails on modern WeeWX
logging with an undefined `syslog`; use the device configurator instead.

Copyright 2016-2020 Matthew Wall and Luc Heijst. Thanks to Frank Bandle and
kobuki for original testing and validation. The driver is GPL-3.0-or-later;
the installer is GPL-3.0-only. See [license](license) and [NOTICE](NOTICE).

<!-- Documentation updated 2026-10-23 by weewx-packages. -->
