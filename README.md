# Hack-O-Bot

## Table of Contents
- [Hack-O-Bot](#hack-o-bot)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Running the Bot Locally](#running-the-bot-locally)
    - [Locally](#locally)
  - [Commands](#commands)
  - [Contributing](#contributing)
  - [License](#license)

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
## Commands 
Here is a list of all the commands that the bot has:

Fun commands
|Command|Description|
|:---|:---|
|`.8ball`|Use the magic 8 ball to get a random answer|
|`.roll`|Roll a `n` sided die|
|`.horoscope`|Get your horoscope for today based on your *discord birthday*|
|`.emoji`|Emoji-fy your text|
|`.github`|Get information about a random Github Repository|
|`.dog`|Send an adorable dog image, optionally with a specified breed|
|`.cat`|Send a cute cat image, optionally with some text!|
|`.duck`|Send a random duck image!|
|`.richest`|Get information about the richest person according to the Forbes list|

Moderation commands
|Command|Description|
|:---|:---|
|`.ban`|Ban a user from the server|
|`.kick`|Kick a user from the server|
|`.unban`|Unban a user from the server|
|`.timeout`|Restricts a User from sending messages for some time|
|`.addrole`|Gives specified roles to the provided members|
|`.server_info`|Basics information about the server|

Image manipulation commands
|Command|Description|
|:---|:---|
|`.wanted`|Make yourself the most wanted person in all of the wild west|

Utility commands
|Command|Description|
|:---|:---|
|`.ping`|Get the bot's latency|
|`.help`|Get help with the bot|
|`.invite`|Get the bot's invite link|
|`.enable`|Enables Different Categories    Access: Administrator|
|`.disable`|Disables Different Categories    Access: Administrator|
|`.about`|Get the info about Hacktoberfest and MLSC's contribution to it|
|`.contributors`|Get the info about the contributors|

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Pull requests will be on a **first come first serve basis**. Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)