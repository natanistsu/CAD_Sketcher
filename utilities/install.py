import site
import sys
import importlib
import subprocess
from importlib import reload

from .. import global_data


def check_module(package):
    """
    Note: Blender might be installed in a directory that needs admin rights
    and thus defaulting to a user installation. That path however might not
    be in sys.path
    """

    p = site.USER_SITE
    if p not in sys.path:
        sys.path.append(p)
    try:
        importlib.import_module(package)

    except ModuleNotFoundError as e:
        raise e


def install_pip():
    """Subprocess call ensurepip module"""
    cmd = [global_data.PYPATH, "-m", "ensurepip", "--upgrade"]
    return not subprocess.call(cmd)


def update_pip():
    cmd = [global_data.PYPATH, "-m", "pip", "install", "--upgrade", "pip"]
    return not subprocess.call(cmd)


def refresh_path():
    """refresh path to packages found after install"""
    reload(site)


def install_package(package: str, no_deps: bool = True):
    update_pip()
    base_call = [global_data.PYPATH, "-m", "pip", "install"]
    args = ["--upgrade"]
    if no_deps:
        args += ["--no-deps"]
    cmd = base_call + args + package.split(" ")
    ret_val = subprocess.call(cmd)
    refresh_path()
    return ret_val == 0


def ensure_pip():
    if subprocess.call([global_data.PYPATH, "-m", "pip", "--version"]):
        return install_pip()
    return True


def show_package_info(package: str):
    try:
        subprocess.call([global_data.PYPATH, "-m", "pip", "show", package])
    except Exception as e:
        print(e)
        pass
