# 케이앤웍스 크롬드라이버 매니저
<br>
개발자 : archon.oh (knworks)


## 크롬드라이버 매니저 사용법<br>

### \# **인스톨**<br>
```python
pip install knw-Chromedriver-manager
```
<br><br>

### \# **윈도우 및 리눅스 사용자**<br>
```python
from knw_Chromedriver_manager import Chromedriver_manager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
driver = webdriver.Chrome(service= Service(Chromedriver_manager.install()), options=options)
driver.get("https://www.daum.net/")
```
<br><br>

### \# **맥 사용자**<br>
```python
from knw_Chromedriver_manager import Chromedriver_manager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.binary_location = Chromedriver_manager.path_check() # add code
driver = webdriver.Chrome(service=Service(Chromedriver_manager.install()), options=options)
driver.get("https://www.daum.net/")
```
