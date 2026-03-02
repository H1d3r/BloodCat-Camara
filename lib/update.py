
#!/usr/bin/python3
# @Мартин.
# ███████╗              ██╗  ██╗    ██╗  ██╗     ██████╗    ██╗  ██╗     ██╗    ██████╗
# ██╔════╝              ██║  ██║    ██║  ██║    ██╔════╝    ██║ ██╔╝    ███║    ╚════██╗
# ███████╗    █████╗    ███████║    ███████║    ██║         █████╔╝     ╚██║     █████╔╝
# ╚════██║    ╚════╝    ██╔══██║    ╚════██║    ██║         ██╔═██╗      ██║     ╚═══██╗
# ███████║              ██║  ██║         ██║    ╚██████╗    ██║  ██╗     ██║    ██████╔╝
# ╚══════╝              ╚═╝  ╚═╝         ╚═╝     ╚═════╝    ╚═╝  ╚═╝     ╚═╝    ╚═════╝
import os
import re
import shutil
import tempfile
import requests
import subprocess

from lib.version import VERSION
from lib.log_cat import LogCat

log = LogCat()


class Updater:

    VERSION_URL = "https://raw.githubusercontent.com/MartinxMax/BloodCat/refs/heads/main/lib/version.py"
    REPO_URL = "https://github.com/MartinxMax/BloodCat.git"

    def check_current_version(self):
        try:
            r = requests.get(self.VERSION_URL, timeout=10)
            if r.status_code != 200:
                log.error("Network unreachable, unable to check for updates")
                return 0

            match = re.search(r'["\'](V[\d\.]+)["\']', r.text)
            if not match:
                log.error("Remote repository error, unable to parse version number")
                return 0

            remote_version = match.group(1)

            if remote_version == VERSION:
                log.info(f"Current version is already the latest [{VERSION}]")
                return 1

            log.info(f"New version detected [{remote_version}]")
            choice = input("Update now? (y/n): ").strip().lower()
            if choice == "y":
                log.info("Starting update, do not interrupt the program...")
                success = self.update()
                if success:
                    log.info(f"BloodCat {VERSION} successfully updated to {remote_version}")
                    return 3
                else:
                    log.error("Update failed, please check your network or Git installation")
                    return 0
            else:
                log.info("Bye...")
                return 2

        except Exception as e:
            log.error(f"Unexpected error occurred: {e}")
            return 0

    def update(self):
        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp()

            subprocess.check_call([
                "git", "clone", "--depth", "1",
                self.REPO_URL,
                temp_dir
            ])

            for root, dirs, files in os.walk(temp_dir):
                if ".git" in root:
                    continue
                rel_path = os.path.relpath(root, temp_dir)
                target_dir = os.path.join(os.getcwd(), rel_path)

                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                for file in files:
                    src_file = os.path.join(root, file)
                    dst_file = os.path.join(target_dir, file)

                    shutil.copy2(src_file, dst_file)

            return True

        except Exception as e:
            log.error(f"Error occurred during update: {e}")
            return False

        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)