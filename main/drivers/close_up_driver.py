from main.controller.dome import Dome
from main.controller.telescope import Telescope
from main.common.IO.json_reader import Reader
from main.common.datatype.object_reader import ObjectReader
import time

global_config_object = ObjectReader(Reader(r'C:\Users\GMU Observtory1\-omegalambda\config\parameters_config.json'))

tel_obj = Telescope()
dome_obj = Dome()

dome_obj.SlaveDometoScope(False)
print("Disabled dome slaving")
dome_obj.MoveShutter('close')
print("Closing shutter")
tel_obj.Park()
print("Parking telescope")
dome_obj.Park()
print("Parking dome")

while tel_obj.Telescope.Slewing or dome_obj.Dome.Slewing:
    print("Waiting for dome and telescope to park, and shutter to close...")
    time.sleep(5)
if not tel_obj.Telescope.Slewing and not dome_obj.Dome.Slewing:
    tel_obj.disconnect()
    dome_obj.disconnect()
    print("Telescope and dome should now be parked, and shutter closed")