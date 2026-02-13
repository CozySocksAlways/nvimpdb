import pdb
import sys
import subprocess
import logging
from pathlib import Path

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

    # Override user_line
    def user_line(self, frame):
        filename = frame.f_code.co_filename

        # testing: echo the filename in neovim
        nvim_cmd(f"<Esc>:echo \"{filename}\"<CR>")

        super().user_line(frame)

def nbreak():
    debugger = NvimPdb()
    debugger.set_trace(sys._getframe().f_back)
