# Hack-O-Bot

## Table of Contents
[Introduction](#introduction)
[Installation](#installation)
[Usage](#usage)
[Contributing](#contributing)
[License](#license)

## Introduction

A discord bot that allows you to run fun commands all over discord, developed by the community for the community. To start working on the bot, you can read the [contributing guidelines](CONTRIBUTING.md) and make sure you have the latest version of [python](https://www.python.org/downloads/) installed. Make sure you have the latest version of [pip](https://pip.pypa.io/en/stable/installing/) installed as well as [git](https://git-scm.com/downloads).

For a basic introduction to the bot, you can read the [documentation](https://docs.google.com/document/d/1yKRCiG7FwYWyilc83dqd7OHISWuNf11sbqdXeq2wuEk/edit?usp=sharing).
## Features
Anything you would want in a discord bot, we want it too. From moderation to fun commands, we accept it all. Some basic commands are given in the Issues Section. If you want to add a command, you can make a pull request, and we will review it.
Make sure to put admin role requirements in the code, so that only admins can use server centric commands such as ban or kick. Treat the role **_"Admin"_** as the admin role.
Write descriptive `help` fields for the commands, so that the user knows what the command does.
## Installation
Install all the dependencies using the following command:
```console
pip install -r requirements.txt
```
## Running the Bot Locally
### Locally
First, you will need at least [`Python 3.8`](https://www.python.org/downloads/release/python-376/).

Clone the repo:

```console
$ git clone https://github.com/MicrosoftStudentChapter/Hack-O-Bot
$ cd Hack-O-Bot
```

Install dependencies:

```console
$ pip install -r requirements.txt
```
Rename the `.env.example` to `.env` and fill out the fields. If `.env.example` is nonexistent (hidden), create a text file named `.env` and copy the contents of [`.env.example`](https://raw.githubusercontent.com/kyb3r/modmail/master/.env.example) then modify the values.

Finally, start the bot.

```console
$ python discord_main.py
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Pull requests will be on a **first come first serve basis**. Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)