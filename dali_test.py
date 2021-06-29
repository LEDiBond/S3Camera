from dali.driver import hasseb
from dali.gear import general

dev = hasseb.SyncHassebDALIUSBDriver()
print(dev.device_found)