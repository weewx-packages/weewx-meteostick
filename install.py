# installer for meteostick driver
# Modified 2026-10-22 by weewx-packages.
# Copyright 2016 Matthew Wall
# Distributed under the terms of the GNU Public License (GPLv3)

from weecfg.extension import ExtensionInstaller

def loader():
    return MeteostickInstaller()

class MeteostickInstaller(ExtensionInstaller):
    def __init__(self):
        super(MeteostickInstaller, self).__init__(
            version="0.68.1",
            name='meteostick',
            description='Collect data from meteostick via serial port',
            author="Matthew Wall",
            author_email="mwall@users.sourceforge.net",
            files=[('bin/user', ['bin/user/meteostick.py'])]
            )
