#!/bin/bash

# Update the package list and upgrade all packages
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip (if not already installed)
sudo apt install -y python3 python3-pip

# Install Chrome browser
sudo apt install -y wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver (You may need to adjust the version to match your Chrome version)
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
rm chromedriver_linux64.zip

# Install necessary Python packages
pip3 install pandas tqdm selenium beautifulsoup4 lxml

# Set up the environment variable for ChromeDriver (if required)
echo 'export PATH=$PATH:/usr/local/bin/chromedriver' >> ~/.bashrc
source ~/.bashrc

# Display installation status
echo "Installation complete! All required dependencies have been installed."

# Instructions for the user
echo "Please ensure that you have the necessary permissions and paths configured."
