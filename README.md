# weewx-meteostick

Read data from a meteostick via serial connection.


Installation

0) Install weewx, select Simulator as the weather station

    http://weewx.com/docs/usersguide.htm

1) Download the driver

    wget -O weewx-meteostick.zip https://github.com/matthewwall/weewx-meteostick/archive/master.zip

2) Install the driver

    sudo wee_extension --install weewx-meteostick.zip

3) Configure the driver

    sudo wee_config --reconfigure

4) Start weewx

    sudo /etc/init.d/weewx start

## Independent continuation

This repository continues `matthewwall/weewx-meteostick` with its original history.
The driver is GPL-3.0-or-later; the installer is GPL-3.0-only. See `license`.
Version 0.68.0 accepts WeeWX 5.2 byte-based CRC input, tolerates reset noise,
flushes an incomplete serial command before reset, and resets/reconfigures the
receiver after an empty read. Retries remain bounded by `max_tries`.

Install using `weectl extension install` with
`https://github.com/weewx-packages/weewx-meteostick/archive/refs/tags/v0.68.0.zip`.
Run `python -m pytest -q tests` for CRC, reset, recovery, and logging tests.
Physical RF reception after a reset remains to verify on a Meteostick.
