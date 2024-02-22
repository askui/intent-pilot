
<h1 align="center">⧐ Intent Pilot </h1>

What can be said can be automated

<p align="center">
    <a href="https://discord.com/invite/Gu35zMGxbx">
        <img alt="Discord" src="https://img.shields.io/discord/912752657662349312?logo=discord&style=flat&logoColor=white"/></a>
    <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=white&style=flat" alt="License"/>
    <br>
    <br>
    <strong>What can be said can be automated.</strong><br>
    <br><a href="https://askui.com">Get early access to the PTA model</a>‎ ‎ |‎ ‎ <a href="https://askui.com/">Scale on our shoulders</a><br>
</p>

<br>


![alt text](<images/opening-dialogue.png>)
# Intent Pilot 

Intent-Pilot is an orchestration of two tools: AskUI's object detector with OpenAI's GPT-4v to achieve automation. It is designed to automate repetitive tasks, and to assist users in performing complex tasks with ease. This repository is our attempt to understand the GPT-4v's potential in automation and building an end-to-end automation tool.

<br>

## Demo

--video-here


# Quick Start

## Setup

- Python 3.9 or later
- OpenAI Key
- AskUI Key
    - For staters, we provide a global AskUI key with 4000 free credits.
    - After that, you can get your own AskUI key by signing up at [AskUI](https://askui.com)

### Linux
- In case of linux, you may need to install the following packages:
```shell
sudo apt-get install xsel xclip 
sudo apt-get install python3-tk python3-dev
```
### MacOS
- In case of MacOS, you will have to grant permissions to the terminal to access the clipboard. You can do this by going to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Accessibility` and then adding the terminal to the list of apps that can control your computer.

### Windows

We are currently working on the Windows version of the tool. It will be available __*soon*__.

__Quick Fix__: The package also works on Windows but windows defender is deleting the `screenshot.py` file. You have to restore the file from the quarantine and add it to the exclusion list.

## Installation

```shell
pip install intent-pilot
```

### Terminal

After installation, simply run `intent` in your terminal:

```shell
intent
```

In case, you are unable to run the command, try running the following command:
```shell
python -m intent_pilot
```

# Contributing

Thank you for your interest in contributing! We welcome involvement from the community.

Please see our [contributing guidelines](docs/CONTRIBUTING.md) for more details on how to get involved.

# Roadmap

We are currently in the process of building PTA (Prompt-to-automation) model, a vision+language model that can understand and execute commands in natural language, in real-time and faster than any VPA (Virtual Personal Assistant) in the market.