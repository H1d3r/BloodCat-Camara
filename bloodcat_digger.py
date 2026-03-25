#!/usr/bin/python3
# @Мартин.
# ███████╗              ██╗  ██╗    ██╗  ██╗     ██████╗    ██╗  ██╗     ██╗    ██████╗
# ██╔════╝              ██║  ██║    ██║  ██║    ██╔════╝    ██║ ██╔╝    ███║    ╚════██╗
# ███████╗    █████╗    ███████║    ███████║    ██║         █████╔╝     ╚██║     █████╔╝
# ╚════██║    ╚════╝    ██╔══██║    ╚════██║    ██║         ██╔═██╗      ██║     ╚═══██╗
# ███████║              ██║  ██║         ██║    ╚██████╗    ██║  ██╗     ██║    ██████╔╝
# ╚══════╝              ╚═╝  ╚═╝         ╚═╝     ╚═════╝    ╚═╝  ╚═╝     ╚═╝    ╚═════╝
import re
import socket
import base64
import random
import argparse
import time

LOGO = r'''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣠⣤⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⣈⡉⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⠿⠿⣦⡀⠢⡀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⢀⣴⣿⣿⡇⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡷⢀⣹⣿⠦⠈⠢⡈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⢀⡴⠿⣯⣽⣿⠃⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⢄⠀⣐⣒⣀⠀⠈⠢⡈⠻⢿⣿⣿⡿⠿⠛⢛⣛⣛⣛⣛⣛⡛⠿⠿⣿⣿⣿⠿⠋⠀⢀⣤⣍⣉⠉⢩⣿⠇⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠐⠚⠛⠿⠃⠀⠀⠈⠑⠒⠾⠑⢶⡾⢿⡿⣿⣿⡿⢿⣿⣿⢓⠲⡶⠄⠒⠀⢀⠔⢉⠐⠛⠻⠿⣿⡏⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠹⠙⠂⠀⠀⠀⠀⠀⣀⣀⠀⢠⠁⠟⠇⣷⡀⣻⣇⣀⠂⠀⠀⠀⠚⠃⢘⣾⣭⣴⣿⣿⢀⠀⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡆⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⡆⠀⠘⢿⠀⢺⢀⡆⠀⣮⠁⠀⠸⢻⠀⠠⠀⡀⠀⠀⠈⠙⠿⣿⣌⡻⢼⢠⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣾⣷⡀⠀⠀⠀⠀⠀⢀⣶⣶⣤⣦⡌⠀⠀⠀⠀⠈⠄⠅⠘⠈⠂⠀⠀⠰⢲⢄⣁⠀⠶⢀⣀⠀⠙⡁⠨⠡⠂⣸⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣧⠀⠀⠀⢀⣤⣖⠨⠽⠤⠌⠁⠀⠀⠀⠀⠀⠀⠀⣄⠀⠈⠀⠀⠀⠀⣀⠁⢴⣦⣉⣏⣀⣉⠀⠀⡔⣰⣿⣿⣿⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠁⠀⠀⠛⠛⠙⠃⣠⣤⠀⠀⠀⠀⠀⠀⠀⠀⢤⠀⠀⠀⠀⠀⠀⠀⢨⣭⡀⢉⠻⣿⣿⣿⣆⠰⣷⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⢸⡂⠀⠀⠀⠀⠀⣀⠻⠰⡄⠀⢰⡆⡀⣸⣿⡗⠈⠐⢬⣍⣻⣿⣷⡈⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣷⠀⠀⠀⠀⠀⢢⠀⠙⠷⣬⠟⣁⡀⠀⠀⠀⠀⣸⣦⡈⠣⣦⣈⠻⠤⠟⠋⠀⠈⠀⣈⣟⣉⣻⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠈⡳⢶⣄⠀⠀⠀⠀⠀⠠⠘⣿⣿⣇⠀⠘⣯⠧⠀⠀⠀⠀⠀⣼⡿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⡀⠀⠀⢰⣿⣿⣿⡏⠀⢀⣿⡤⠀⣀⠀⠀⣼⠋⢉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠞⠛⠿⣿⣧⡀⠈⣻⡗⠛⠿⠄⠈⠀⠠⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⡀⠁⢀⣼⣏⣛⣡⡴⠋⠉⠙⠟⠛⠯⣭⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠉⠶⢿⡍⣭⣍⡺⢶⣉⠩⠙⣱⣞⣒⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⡤⠀⠀⠲⢂⣀⣽⣿⢦⣁⠀⣵⣖⣬⣽⡟⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣿⣿⡏⢤⡘⠿⢮⠿⢿⣿⣿⣿⣿⡿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠦⠺⠛⠛⠁⠀⠁⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
[Maptnh@S-H4CK13]      [Blood Cat Path Digger](Hikvision)    [https://github.com/MartinxMax]⠀
---------------------------------------------------------------------------------------------'''
class digger:
    def __init__(self, timeout=3):
        self.TIMEOUT = timeout
        self.USER_AGENTS = [
            "VLC/3.0.18 LibVLC/3.0.18",
            "FFplay/5.0",
            "Mozilla/5.0"
        ]

    def b64(self, user, pwd):
        return base64.b64encode(f"{user}:{pwd}".encode()).decode()

    def random_ua(self):
        return random.choice(self.USER_AGENTS)

    def send(self, req, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.TIMEOUT)
        try:
            s.connect((ip, port))
            s.sendall(req.encode())
            data = s.recv(8192)
            return data.decode(errors="ignore")
        except Exception:
            return None
        finally:
            s.close()

    def describe_path(self, ip, port, path, auth=None):
        hdr = ""
        if auth:
            hdr = f"Authorization: Basic {auth}\r\n"
        ua = self.random_ua()
        req = (
            f"DESCRIBE rtsp://{ip}:{port}{path} RTSP/1.0\r\n"
            f"CSeq: 3\r\n"
            f"Accept: application/sdp\r\n"
            f"User-Agent: {ua}\r\n"
            f"{hdr}\r\n"
        )
        return self.send(req, ip, port)

    def status(self, resp):
        if not resp:
            return None
        try:
            return int(resp.splitlines()[0].split()[1])
        except Exception:
            return None

    def parse_rtsp(self, rtsp_url):
        pattern = r"rtsp://(.*?):(.*?)@(.*?):(\d+)/(.*)"
        match = re.match(pattern, rtsp_url)
        if not match:
            raise ValueError("Invalid RTSP URL! Example: rtsp://user:pass@ip:554/path/")
        user, pwd, ip, port, path = match.groups()
        port = int(port)
        base_path = f"/{path}"
        return user, pwd, ip, port, base_path

if __name__ == "__main__":
    print(LOGO)
    parser = argparse.ArgumentParser(description="RTSP Channel Scanner")
    parser.add_argument("--rtsp", required=True, help="RTSP Base URL")
    parser.add_argument("--id", required=True, type=int, help="Start Channel ID")
    args = parser.parse_args()

    scanner = digger(timeout=2)
    username, password, ip, port, base_path = scanner.parse_rtsp(args.rtsp)
    auth = scanner.b64(username, password)

    current_id = args.id
    fail_count = 0
    MAX_FAIL = 10

    while True:
        full_path = f"{base_path}{current_id}"
        resp = scanner.describe_path(ip, port, full_path, auth)
        code = scanner.status(resp)

        if code == 200:
            print(f"[+] Valid: {args.rtsp}{current_id}")
            fail_count = 0
        else:
            fail_count += 1
            
        if fail_count >= MAX_FAIL:
            break

        current_id += 100
        time.sleep(0.5)