from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
import time

input_modules = ['button', 'ultrasonic']
output_modules = ['led', 'motor']

chrome_options = Options()
chrome_options.add_extension("/Users/dajungpark/Repos/ai-contents-code-translator/MODIstudio/modi-studio-chrome-app.crx") # 모디 스튜디오 익스텐션 설치
driver = webdriver.Chrome('/Users/dajungpark/Repos/ai-contents-code-translator/MODIstudio/chromedriver', options=chrome_options)

url = 'http://modi-cloud.s3-website.ap-northeast-2.amazonaws.com'
driver.get(url) # 크롬 앱스 접속
driver.maximize_window()
driver.find_element_by_class_name('moduleboxBtn').click()
time.sleep(2)

#drag input modules
for module in input_modules:
    source_element = driver.find_element_by_css_selector(f'div.module.{module}.input.hardware.ui-draggable.ui-draggable-handle')
    dest_element = driver.find_element_by_css_selector('ul.modulemap.dd-list.ui-droppable')
    ActionChains(driver).click_and_hold(source_element).move_to_element(dest_element).release(dest_element).perform()
#drag output modules
for module in output_modules:
    source_element = driver.find_element_by_css_selector(f'div.module.{module}.output.hardware.ui-draggable.ui-draggable-handle')
    dest_element = driver.find_element_by_css_selector('ul.modulemap.dd-list.ui-droppable')
    ActionChains(driver).click_and_hold(source_element).move_to_element(dest_element).release(dest_element).perform()
driver.find_element_by_xpath('/html/body/div[1]/div[5]').click() #close module box

#arrange modules
ActionChains(driver).context_click(dest_element).perform()
driver.find_element_by_xpath('/html/body/ul[2]/li[2]').click()


#drag IF
source_element = driver.find_element_by_css_selector('div.image.imageIf')
dest_element = driver.find_element_by_css_selector('li.helper.dd-item.dd-nochildren.helperAnimation')
ActionChains(driver).click_and_hold(source_element).pause(1).move_to_element(dest_element).release(dest_element).perform()

#버튼이 눌리
element = driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[1]/div[2]/input').send_keys("button0.Press Status") #button0.Press Status
element = driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[1]/div[4]/input').send_keys("==") #==
element = driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[1]/div[5]/input').send_keys("TRUE") #TRUE

#거나
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[1]/div[6]/div').click() #+
driver.find_element_by_xpath('//*[@id="box2"]/div[1]/input').click() #Or

#초음파 거리가 50보다 작으면
driver.find_element_by_xpath('//*[@id="box2"]/div[2]/input').click() #field
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[3]/div[1]/div[3]').click() #ultrasonic0
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[3]/div[1]/div[4]/div[1]').click() #Distance
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[3]/div[1]/div[11]').click() #<
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[3]/div[1]/div[5]').click() #50

driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[1]/div[7]/div').click() #Then

#drag motor
source_element = driver.find_element_by_xpath('//*[@id="motor0Image"]')
gui_element = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div')
ActionChains(driver).click_and_hold(source_element).pause(1).move_to_element_with_offset(gui_element, 100, 120).move_to_element_with_offset(gui_element, 180, 120).release().perform()
moved_motor = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[3]/div[1]')
ActionChains(driver).click_and_hold(moved_motor).pause(1).move_to_element_with_offset(gui_element, 300, 80).move_to_element_with_offset(gui_element, 350, 100).release().perform()

#set motor
driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[2]/ul/li/div[1]').click()
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[2]/div[1]/div[3]').click() #Speed
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[2]/div[1]/div[3]').click() #50
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[2]/div[1]/div[7]').click() #-50
driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[2]/ul/li/div[2]/div[1]/div[6]/div').click() #ok

#drag led
source_element = driver.find_element_by_xpath('//*[@id="led0Image"]')
ActionChains(driver).click_and_hold(source_element).pause(1).move_to_element_with_offset(gui_element, 100, 180).move_to_element_with_offset(gui_element, 180, 180).release().perform()

#set led
driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[2]/ul/li[2]/div[2]/div[2]/div[1]/div[1]').click() #Basic Color
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[2]/div[2]/div/div[2]/div').click() #Red
driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[2]/ul/li[2]/div[2]/div[1]/div[7]/div').click() #ok

#drag ELSE
source_element = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/ul/li[1]/div/div[1]')
ActionChains(driver).click_and_hold(source_element).pause(1).move_to_element_with_offset(gui_element, 20, 230).move_to_element_with_offset(gui_element, 10, 230).release().perform()
driver.find_element_by_xpath('/html/body/div[1]/div[18]/div/div/div[3]').click() #else
driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[3]/div[2]/div[1]/div[7]/div').click() #then

#drag motor
source_element = driver.find_element_by_xpath('//*[@id="motor0Image"]')
ActionChains(driver).click_and_hold(source_element).pause(1).move_to_element_with_offset(gui_element, 100, 280).move_to_element_with_offset(gui_element, 180, 280).release().perform()
moved_motor = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[4]/div[1]')
ActionChains(driver).click_and_hold(moved_motor).pause(1).move_to_element_with_offset(gui_element, 300, 240).move_to_element_with_offset(gui_element, 350, 260).release().perform()

#set motor
moved_motor.click()
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[2]/div[1]/div[3]').click() #Speed
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[2]/div[1]/div[5]').click() #0
driver.find_element_by_xpath('//*[@id="block0"]/div[2]/div[2]/div[1]/div[5]').click() #0
driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[3]/ul/li/div[2]/div[1]/div[6]/div').click() #ok

#drag led
source_element = driver.find_element_by_xpath('//*[@id="led0Image"]')
ActionChains(driver).click_and_hold(source_element).pause(1).move_to_element_with_offset(gui_element, 100, 340).move_to_element_with_offset(gui_element, 180, 340).release().perform()

#set led
driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[3]/ul/li[2]/div[2]/div[2]/div[1]/div[1]').click() #Basic Color
driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[3]/ul/li[2]/div[2]/div[2]/div[2]/div/div[6]/div').click() #Off
driver.find_element_by_xpath('/html/body/div[1]/div[4]/div[1]/div[1]/div/div/div/ul/li[3]/ul/li[2]/div[2]/div[1]/div[7]/div').click() #ok
