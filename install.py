"""Install the RCA Tools Mallard plugin.

Usage:
    python3 install.py          # install / update
    python3 install.py remove   # uninstall
"""

import shutil
import subprocess
import sys
from pathlib import Path

INSTALL_DIR = Path.home() / ".rca_mcp"
PLUGIN_NAME = "RCA Tools"
SERVER_FILES = [
    "server.py",
    "handlers.py",
    "llm_interface.py",
    "prompts.py",
    "tools_schema.py",
]


def ensure_venv() -> None:
    venv_dir = INSTALL_DIR / "venv"
    pip = venv_dir / "bin" / "pip"
    if pip.exists():
        print("Venv exists — upgrading packages...")
        subprocess.check_call([str(pip), "install", "--upgrade", "mcp"])
        return
    print(f"Creating venv at {venv_dir}...")
    subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
    print("Installing mcp (one-time, may take a moment)...")
    subprocess.check_call([str(pip), "install", "mcp"])


def copy_server_files() -> None:
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).parent
    for name in SERVER_FILES:
        shutil.copy2(src / name, INSTALL_DIR / name)
    print(f"Server files copied to {INSTALL_DIR}")


def stage_and_install_plugin() -> None:
    src_plugin = Path(__file__).parent / "rca-tools.mplug"
    staged = INSTALL_DIR / "rca-tools.mplug"

    if staged.exists():
        shutil.rmtree(staged)
    shutil.copytree(src_plugin, staged)

    # Resolve {{env:HOME}} to the real home directory (handles pipx/uv installs too)
    server_yaml = staged / "mcp" / "rca-tools.yaml"
    server_yaml.write_text(
        server_yaml.read_text().replace("{{env:HOME}}", str(Path.home()))
    )

    # Remove any previous version before installing (makes re-runs idempotent)
    subprocess.run(["mallard", "plugin", "remove", PLUGIN_NAME], capture_output=True)
    # call mallard plugin install
    subprocess.check_call(["mallard", "plugin", "install", str(staged)])
    print(f"\n✅ {PLUGIN_NAME} plugin installed. Restart Claude Code to pick it up.")


def uninstall() -> None:
    subprocess.check_call(["mallard", "plugin", "remove", PLUGIN_NAME])
    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR)
    print(f"✅ {PLUGIN_NAME} removed.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        uninstall()
    else:
        copy_server_files()
        ensure_venv()
        stage_and_install_plugin()
