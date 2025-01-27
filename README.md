README

Test Automation – Login Flow (Approach 1)

Overview

This repository contains the implementation of the login flow automation for a mobile poker application using Airtest IDE. This approach focuses on a single-file execution method leveraging Airtest IDE's capabilities, with supporting test data and reference images for UI element verification.

Folder Structure

Poker_login.py: Main script for login flow automation.

ReferenceImages/: Contains images for UI element matching during automation.

data/: Contains the testdata.json file to manage test data.

TestResults/: Stores logs and test result reports.

Requirements

Tools:

Airtest IDE (Download: Airtest IDE)

Setup:

APK file of the mobile poker application (pre-provided).

**Setup Instructions**

1. Clone or download this repository:git clone https://github.com/ram-kali/WPT_Login_AirtestIDE.git

2. Ensure the following files and folders are present:

Poker_login.py

ReferenceImages/

data/testdata.json

TestResults/

3. Open the project in Airtest IDE.

4.Test Data Configuration

Open data/testdata.json and update the following fields as required:

Username: Define the test username.

Password: Define the test password.

Other Fields: Customize additional parameters as needed.

**Execution Steps**

  1.Launch Airtest IDE and open the Poker_login.py script.
  
  (Optional) Uncomment the install_game_application line in the script if APK installation is required. The APK file is included for automated installation.
  
  2.Click the Run button in Airtest IDE to execute the script.
  
  3.Monitor the logs in the console for real-time execution updates.
  
  4.Post-execution, review the following:
  
    a.Logs in TestResults/TestResults.log
    
    b.HTML report in TestResults/Report.html

**Deliverables**

Automation script: Poker_login.py

Logs: TestResults/TestResults.log

Report: TestResults/Report.html

**Notes**

Ensure that the mobile device/emulator is properly connected and recognized by the Airtest IDE.

Default APK installation is commented out for convenience; un-comment as needed.
