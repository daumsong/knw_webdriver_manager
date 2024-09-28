import os
import getpass
import re
import requests
import json
import platform
import zipfile
import shutil
import subprocess

def path_check():
    paths = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # 맥
        '/usr/bin/google-chrome-stable',
        '/usr/bin/google-chrome',
        '/opt/google/chrome/google-chrome'
    ]

    for path in paths:
        if not os.path.exists(path):
            continue
        return path

def get_chrome_version():
    version = None

    if platform.system() == 'Windows':
        # 레지스터리에서 버전정보 읽어오기
        cmd = r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
        version = re.search(r'(\d+\.\d+\.\d+\.\d+)', output).group(0)
        return version
    else:
        paths = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', # 맥
            '/usr/bin/google-chrome-stable',
            '/usr/bin/google-chrome',
            '/opt/google/chrome/google-chrome' # 리눅스
        ]

        for path in paths:
            if not os.path.exists(path):
                continue

            process = subprocess.Popen([path, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()

            # utf-8 or cp437 로 디코드
            try:
                output = output.decode('utf-8')
            except UnicodeDecodeError:
                output = output.decode('cp437')
            version = re.search(r'(\d+\.\d+\.\d+\.\d+)', output).group(0)
            break

        return version

def download(version):

    #os운영체제 및 비트수 체크
    os_name = platform.system()
    bit_value = platform.architecture()[0]
    processor = ''
    if os_name == 'Darwin':
        processor = platform.machine()

    #폴더만들기
    user = getpass.getuser()
    if os_name == "Windows":
        chromedriver_folder = f"C:/Users/{user}/knw_chromedriver/{version}"
        os.makedirs(chromedriver_folder, exist_ok=True)
        for file_name in os.listdir(chromedriver_folder):
            if file_name == 'chromedriver.exe':
                return os.path.join(chromedriver_folder, file_name)
    elif os_name == 'Darwin':  # 맥
        chromedriver_folder = f"/Users/{user}/knw_chromedriver/{version}"
        os.makedirs(chromedriver_folder, exist_ok=True)
        for file_name in os.listdir(chromedriver_folder):
            if file_name == 'chromedriver':
                return os.path.join(chromedriver_folder, file_name)
    elif os_name == 'Linux':  # 리눅스
        chromedriver_folder = f"/home/{user}/knw_chromedriver/{version}"
        os.makedirs(chromedriver_folder, exist_ok=True)
        for file_name in os.listdir(chromedriver_folder):
            if file_name == 'chromedriver.exe':
                return os.path.join(chromedriver_folder, file_name)

    #크롬드라이버 목록 받아오기
    response = requests.get(
        'https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build-with-downloads.json')  # https://github.com/GoogleChromeLabs/chrome-for-testing#json-api-endpoints
    version_json_data = json.loads(response.text)
    # json "builds"에서 버전 3째단까지의 숫자에 해당하는 모든 버전 리스트 추출 ex: ['115.0.1000','115.0.1000','115.0.1000'] 추후 뒷단 버전숫자까지 추가 됬을 경우 대비
    main_versions = [key for key in version_json_data["builds"].keys() if key.startswith(version)]

    first_version_value = re.search(r'^\d+', version).group(0)
    if first_version_value == "114":
        pass
    else:
        try:
            # 버전 3째단까지의 숫자를 기준으로 정렬하여 해당앞단의 최신 버전값 추출 ex. 114.0.5735
            latest_main_versions = sorted(main_versions, key=lambda x: list(map(int, x.split("."))))[-1]
            # print("latest_main_versions",latest_main_versions)
            # 해당버전의 최신 버전 chromedriver json 추출
            latest_main_versions_json = version_json_data['builds'][latest_main_versions]['downloads']['chromedriver']
        except:
            #stable. 즉 현재 최신제공 버전의 드라이버 크롬드라이버 목록 받아오기
            response = requests.get(
                'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json')  # https://github.com/GoogleChromeLabs/chrome-for-testing#json-api-endpoints
            version_json_data = json.loads(response.text)
            latest_main_versions_json = version_json_data["channels"]["Stable"]['downloads']['chromedriver']


    download_url = ''
    if first_version_value == "114":
        if os_name == "Windows" and bit_value == "64bit":  # 윈도우 64비트
            download_url = "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip"
        elif os_name == "Windows" and bit_value == "32bit":  # 윈도우 32비트
            download_url = "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_win32.zip"
        elif os_name == "Darwin" and processor == "x86_64":  # 인텔 맥
            download_url = "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_mac64.zip"
        elif os_name == "Darwin" and processor == "arm64":  # 암 맥
            download_url = "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_mac_arm64.zip"
        else:  # 리눅스
            download_url = "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip"
    else:
        if os_name == "Windows" and bit_value == "64bit":  # 윈도우 64비트
            for kinds in latest_main_versions_json:
                if kinds['platform'] == "win64":
                    download_url = kinds['url']
        elif os_name == "Windows" and bit_value == "32bit":  # 윈도우 32비트
            for kinds in latest_main_versions_json:
                if kinds['platform'] == "win32":
                    download_url = kinds['url']
        elif os_name == "Darwin" and processor == "x86_64":  # 인텔 맥
            for kinds in latest_main_versions_json:
                if kinds['platform'] == "mac-x64":  # mac-x64
                    download_url = kinds['url']
        elif os_name == "Darwin" and processor == "arm64":  # 암 맥
            for kinds in latest_main_versions_json:
                if kinds['platform'] == "mac-arm64":
                    download_url = kinds['url']
        else:  # 리눅스
            for kinds in latest_main_versions_json:
                if kinds['platform'] == "linux64":
                    download_url = kinds['url']

    #크롬드라이버 다운로드
    response = requests.get(download_url)
    file_path = os.path.join(chromedriver_folder, 'chromedriver.zip')
    # 압축파일 다운로드
    with open(file_path, 'wb') as f:
        f.write(response.content)

    if first_version_value == "114":
        file_reg = r'^chromedriver.*'
    else:
        file_reg = r'^chromedriver.*\/chromedriver'

    # 압축 풀기
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            if re.search(file_reg, member):
                filename = os.path.basename(member)
                source = zip_ref.open(member)
                target = open(os.path.join(chromedriver_folder, filename), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
                    if os_name in ['Darwin', 'Linux']:
                        os.chmod(os.path.join(chromedriver_folder, filename), 0o755) #권한부여
                    return os.path.join(chromedriver_folder, filename)

def install():
    version = get_chrome_version()
    install_path = download(re.search(r'(\d+\.\d+\.\d+)', version).group(0))
    return install_path
