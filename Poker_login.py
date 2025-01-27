# -*- encoding=utf8 -*-
__author__ = "Ram K"

import json
import subprocess
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
import logging


logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
with open('./data/testData.json') as jsonFile:
    testData = json.load(jsonFile)


def get_config_value(key):
    return testData['config'].get(key, f"'{key}' not found in config")


def get_imagePath(key):
    return testData['imagePath'].get(key, f"'{key}' not found in imagePath")

def empty_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove files or symbolic links
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directories
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")


folder_path = "./TestResult"
empty_folder(folder_path)
logging.basicConfig(level=logging.INFO, filename="./TestResult/TestResult.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

class Poker:

    def __init__(self, deviceId):
        print("Execution as started")
        if not cli_setup():
            auto_setup(__file__, logdir="./TestResult",
                       devices=[deviceId, ])            

    def step_pass(self, statement):
        print(f"Step Pass: {str(statement)}")
        logging.info(f"Step Pass: {str(statement)}")

    def step_fail(self, statement):
        print(f"Step Fail: {str(statement)}")
        logging.error(f"Step Fail: {str(statement)}")

    def step_info(self, statement):
        print(f"Step Info: {str(statement)}")
        logging.info(f"Step Info: {str(statement)}")

    def install_game_application(self, apkPath):
        try:
            install(apkPath)
            self.step_pass(f"Install Application from path '{apkPath}'")
        except Exception as e:
            self.step_fail(F"Failed to install Application '{apkPath}' . Error: {str(e)}")

    def start_new_game_application(self, appPackage, appName):
        try:
            clear_app(appPackage)
            start_app(appPackage)
            self.step_pass(f"Start '{appName}' Game Application")
        except Exception as e:
            self.step_fail(
                f"Failed to start Application '{appName}' as new Application. Error" + str(e))

    def stop_application(self, appPackage, appName):
        try:
            stop_app(appPackage)
            self.step_pass(f"Stop '{appName}' Game Application")
        except Exception as e:
            self.step_fail(
                f"Failed to Stop Application '{appName}' as new Application. Error" + str(e))

    def return_to_game_application(self, appPackage, appName):
        try:
            start_app(appPackage)
            self.step_pass(f"Return to '{appName}' Game Application")
        except Exception as e:
            self.step_fail(
                f"Failed to return to  '{appName}' game Application. Error" + str(e))

    def find_image_Element(self, imagePath):
        return Template(imagePath)

    def tap_on(self, imagePath, times=1, duration=0.1):
        try:
            element = touch(self.find_image_Element(imagePath), times=times, duration=duration)
            if element is not None:
                self.step_pass(f"Tap On: '{imagePath.split('/')[-1].split('.')[0]}'")
            return element
        except Exception as e:
            self.step_fail(f"Failed to tap on '{imagePath.split('/')[-1].split('.')[0]}' . Error: {str(e)}")

    def wait_for(self, imagePath, time_out):
        try:
            return wait(self.find_image_Element(imagePath), timeout=time_out)
        except Exception as e:
            self.step_info(f"Wait- '{imagePath.split('/')[-1].split('.')[0]}' is not displayed. Wait Time: {time_out}.")

    def is_exists(self, imagePath):
        try:
            return exists(self.find_image_Element(imagePath))
        except:
            self.step_info(f"Exists- '{imagePath.split('/')[-1].split('.')[0]}' is not found.")

    def type_text(self, inputText):
        try:
            subprocess.call(f"adb shell input keyboard text '{inputText}'", shell=True)
            self.step_pass(f"Type: Text '{inputText}'")
        except Exception as e:
            self.step_fail(f"Failed to type text '{inputText}' . Error: {str(e)}")


wpt = Poker(get_config_value("device_URL"))
# Install Application
# wpt.install_game_application(get_config_value("apkPath"))


# Test Case:1
wpt.step_info("#### Test Case:1 ####")
# Start Application
wpt.start_new_game_application(get_config_value("appPackage"), get_config_value("appName"))

# Manage Popups
wpt.step_info("#Manage Popups")
if wpt.wait_for(get_imagePath("whileUsingThisApp"), time_out=7):
    wpt.tap_on(get_imagePath("whileUsingThisApp"))
while wpt.wait_for(get_imagePath("allow_Button"), time_out=10):
    wpt.tap_on(get_imagePath("allow_Button"))

# Login flow as invalid user
wpt.step_info("#Login with User Name '" + get_config_value("userName") + "'")
username= get_config_value("userName")
invalid_password = get_config_value("invalid_password")
wpt.tap_on(get_imagePath("playNow_Button"))
wpt.tap_on(get_imagePath("userName_TextBox"))
wpt.type_text(username)
sleep(2)
wpt.tap_on(get_imagePath("password_TextBox"), times=2)
wpt.type_text(invalid_password)
sleep(1)
wpt.tap_on(get_imagePath("login_Button"), times=2)
if wpt.is_exists(get_imagePath("login_Error")):
    wpt.step_fail(f"Failed to Login as user: {username} and password: {invalid_password}")
    wpt.tap_on(get_imagePath("close_Button"))
sleep(5)

# Test Case:2

wpt.step_info("#### Test Case:2 ####")
# Start Application
wpt.start_new_game_application(get_config_value("appPackage"), get_config_value("appName"))

# Manage Popups
wpt.step_info("#Manage Popups")
if wpt.wait_for(get_imagePath("whileUsingThisApp"), time_out=7):
    wpt.tap_on(get_imagePath("whileUsingThisApp"))
while wpt.wait_for(get_imagePath("allow_Button"), time_out=10):
    wpt.tap_on(get_imagePath("allow_Button"))

# Login flow as valid user
wpt.step_info("#Login with User Name '" + get_config_value("userName") + "'")
wpt.tap_on(get_imagePath("playNow_Button"))
wpt.tap_on(get_imagePath("userName_TextBox"))
wpt.type_text(get_config_value("userName"))
sleep(2)
wpt.tap_on(get_imagePath("password_TextBox"), times=2)
wpt.type_text(get_config_value("password"))
sleep(1)
wpt.tap_on(get_imagePath("login_Button"), times=2)
sleep(5)

# Validate player Name and player Id Images
if not wpt.is_exists(get_imagePath("WPT_icon")):
    wpt.return_to_game_application(get_config_value("appPackage"), get_config_value("appName"))
while wpt.wait_for(get_imagePath("okay_Button"), 5):
    wpt.tap_on(get_imagePath("okay_Button"))
    sleep(3)

wpt.step_info("Verify User Details")
wpt.tap_on(get_imagePath("player_icon"), times=2)
if wpt.is_exists(get_imagePath("player_name")):
    wpt.step_pass("Verification of Player name for user '" + get_config_value("userName") + "' is successful!")
else:
    wpt.step_fail("Failed to verify of Player name for user '" + get_config_value(
        "userName") + "'. Please check the Player Name and UserName inputs!")
if wpt.is_exists(get_imagePath("player_id")):
    wpt.step_pass("Verification of Player Id for user '" + get_config_value("userName") + "' is successful!")
else:
    wpt.step_fail("Failed to verify of Player name for user '" + get_config_value(
        "userName") + "'. Please check the Player Name and UserName inputs!")
# Stop Applicationa
wpt.stop_application(get_config_value("appPackage"), get_config_value("appName"))

simple_report(__file__, logpath=True, logfile='./log.txt', output='./TestResult/Report.html')
