import glob
from os import path
parent_dir = path.dirname(path.abspath(__file__))
geckodriver_path=path.join(parent_dir, '', "geckodriver.exe")
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
file_path = path.join(parent_dir, '', "web.gmx.txt")
resultFilePath  = path.join(parent_dir, '', "results")
screenSot = path.join(parent_dir, 'template', "iframe_screenshot.png")
template_files = glob.glob(path.join(f'{parent_dir}\\template', 'template*'))


