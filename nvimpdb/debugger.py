import pdb
import sys
import subprocess
import logging
from pathlib import Path
from types import FrameType

#TODO
# -1. Make pdb silent, don't have to print the line now
# 0. Add the package to path or something so that it can easily installed
# 1. There is a exception on exit fix that
# 2. Check if file changed before loading file again
# 3. Add the breakpoint to snippet
# 4. Look at using breakpoint()
# 5. Instantiate NvimPdb only once

NVIM_SERVER = "/tmp/pdb_nvim"
log_file = Path.home() / "logs" / "nvim_pdb.log"
logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt='%d-%m-%Y %I:%M:%S %p'
        )
logger = logging.getLogger('NvimPdbLogger')

def nvim_cmd(cmd):
    try:
        subprocess.run(["nvim",
                        "--server", NVIM_SERVER,
                        "--remote-send", cmd])
    except subprocess.CalledProcessError as e:
        output = (e.stdout or "") + (e.stderr or "")
        logger.exception(output)

class NvimPdb(pdb.Pdb):
    
    def __init__(self, *args, **kwargs):
        print("Welome to Pdb Integrated with Nvim")
        super().__init__(*args, **kwargs)

        # Some basic visual stuff
        #TODO: there was setcursorline here which was added to rc,
        # that caused relativenumber! below this to fail
        nvim_cmd("<Esc>:set relativenumber!<CR>")

    # Override user_line
    def user_line(self, frame: FrameType) -> None:
        filename = frame.f_code.co_filename
        lineno = frame.f_lineno

        nvim_cmd((
            "<Esc>"
            f":view {filename}<CR>"
            f":{lineno}<CR>"
            "zz"
            ))
        super().user_line(frame)

def nbreak():
    debugger = NvimPdb()
    debugger.set_trace(sys._getframe().f_back)
