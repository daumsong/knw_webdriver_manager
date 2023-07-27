Chromedriver_manager for knw / By archon.oh


############# [install] #############

pip install knw-Chromedriver-manager

#####################################


################################# [window use sample code] ##################################

from knw_Chromedriver_manager import Chromedriver_manager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
driver = webdriver.Chrome(service= Service(Chromedriver_manager.install()), options=options)
driver.get("https://www.daum.net/")

#############################################################################################


###################################### [mac use sample code] ################################

from knw_Chromedriver_manager import Chromedriver_manager

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.binary_location = Chromedriver_manager.path_check() # add code
driver = webdriver.Chrome(service=Service(Chromedriver_manager.install()), options=options)
driver.get("https://www.daum.net/")

#############################################################################################