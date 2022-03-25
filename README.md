# Welcome to the GeeGeeRegFiller

## What does it do?

Looks through the geegeereg website for available uOtttawa gym slots, providing an easy select menu to book ✅

(Only Supports Minto Gym at the moment)🚨

Example:

<img src="list.png"
     alt="list"
     style="height: 200px; width: 220px;" />

## What Do I need to use it?

You will need the following:

- Python
- pip
- Selenium
- ChromeWebDriver
- Latest Chrome version

## Installation (Mac)

### pip

In terminal type:

```
python3 get-pip.py
```

### Selenium

In terminal type:

```
pip3 install -U selenium
```

### Chrome Driver Install (With Brew)

```
brew install --cask chromedriver
```

### Chrome Driver Install (Without Brew)

Go to the following website and download the correct version for your mac

<https://chromedriver.storage.googleapis.com/index.html?path=100.0.4896.20/>

Then simply unpack the folder and run the bash inside

## How to Use

Run the python script using the terminal/cmd

```
python3 GeeGeeRegFiller.py
```

Follow the terminal instructions and enjoy working out!

***The script stops at the checkout screen so you can double check details before submitting!***

## Common problems and fixes

### "The browser is not loading and is stuck on data:,"

This is a problem with the website itself to fix simply click on the url bar and press enter.

You may need to do this a second time after the webpage closes to display times

### "I get the message: An Error has occured please launch the program again!"

- Do not click away from the browser while it is running

- Relaunch the program

- empty your cart 
