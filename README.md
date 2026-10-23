# Meteostick

Receive Davis wireless weather transmissions with a Meteostick connected by
serial/USB. The driver configures the receiver's raw format and decodes the
ISS, a separate anemometer, a leaf/soil station and up to two extra
temperature/humidity stations. It needs a physical Meteostick; it does not run
`rtl_433` or read cloud data.

This is an independent continuation of
[matthewwall/weewx-meteostick](https://github.com/matthewwall/weewx-meteostick)
with its history. See [NOTICE](NOTICE).

## Requirements

- A Meteostick and a Davis Vantage Vue, Pro or Pro2 station.
- Access to the serial device for the user running WeeWX.
- `pyserial` in the Python environment that runs WeeWX.

Activate the virtual environment of your WeeWX service, then install:

```sh
python -m pip install pyserial
```

The distribution is named `pyserial` and provides the `serial` import. Do not
install the different package named `serial`. Installing into an unrelated
virtual environment does not supply the running service. For an OS-packaged
WeeWX installation, use the distribution package instead, or move WeeWX and
its service to a virtual environment first.

## Installation

Install `meteostick` from the [WeeWX packages catalog](https://github.com/weewx-packages/catalog/blob/main/packages/meteostick.md).
The catalog page lists the current release, its WeeWX and Python
requirements, and the install, update and removal commands.

Then select the driver and restart WeeWX:

```sh
weectl station reconfigure --driver=user.meteostick --config=/path/to/weewx.conf
```

## Configuration

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

Options in `[Meteostick]`:

| Option | Default | Meaning |
|---|---|---|
| `driver` | | Must be `user.meteostick`. |
| `port` | `/dev/ttyUSB0` | Serial device of the Meteostick. |
| `baudrate` | `115200` | Serial rate. |
| `transceiver_frequency` | `EU` | Frequency plan: `EU`, `US` or `AU`. Select the plan for your hardware. |
| `iss_channel` | `1` | ISS transmitter channel, 1 through 8. |
| `anemometer_channel` | `0` | Separate wind transmitter, 1 through 8. 0 uses ISS wind. |
| `leaf_soil_channel` | `0` | Leaf/soil transmitter, 1 through 8. 0 disables it. |
| `temp_hum_1_channel`, `temp_hum_2_channel` | `0` | Extra temperature/humidity transmitters. 0 disables them. |
| `rain_bucket_type` | `1` | 1 for 0.2 mm, 0 for 0.01 inch per tip. |
| `rf_sensitivity` | `90` | RF sensitivity in -dB, up to 125. Higher values can admit noise and false readings. |
| `max_tries` | `10` | Read attempts before WeeWX gets a retries-exceeded error. An empty read resets the receiver. |
| `retry_wait` | `10` | Seconds between read attempts. |
| `debug_parse`, `debug_serial`, `debug_rain`, `debug_rf_sensitivity` | `0` | Debug message levels. |
| `sensor_map` | built-in mapping | Maps WeeWX fields to decoded observations. Entries extend or override the built-in map in [meteostick.py](bin/user/meteostick.py). |

The table lists the values used when an option is absent. The stanza that
`weectl station reconfigure` adds sets `debug_rf_sensitivity = 1`.

### Configure the receiver

Stop WeeWX before receiver diagnostics. After selecting this driver, the
device configurator shows the Meteostick options:

```sh
weectl device --help --config=/path/to/weewx.conf
```

To print the readings without WeeWX, run the driver directly in the Python
environment of WeeWX. It runs until interrupted. `--help` lists the options:

```sh
PYTHONPATH=/path/to/station/bin python -m user.meteostick --port=/dev/ttyUSB0 --freq=EU
```

## Limitations

- CRC handling and recovery after empty serial reads are covered by offline
  tests only. Reception after a receiver reset still needs checks on a device.

## Development

In a WeeWX environment with pytest and pyserial:

```sh
python -m pytest -q tests
```

## License

Copyright 2016-2020 Matthew Wall and Luc Heijst. Thanks to Frank Bandle and
kobuki for original testing and validation. The driver is GPL-3.0-or-later;
the installer is GPL-3.0-only. See [license](license) and [NOTICE](NOTICE).
