
<h1 align="center">⧐ Intent Pilot </h1>

<p align="center">
    <a href="https://discord.com/invite/Gu35zMGxbx">
        <img alt="Discord" src="https://img.shields.io/discord/912752657662349312?logo=discord&style=flat&logoColor=white"/></a>
    <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=white&style=flat" alt="License"/>
    <br>
    <br>
    <strong>What can be said can be solved.</strong><br>
    <br><a href="https://askui.com">Get early access to the PTA model</a>‎ ‎ |‎ ‎ <a href="https://askui.com/">Scale on our shoulders</a><br>
</p>

<br>


![alt text](<images/opening-dialogue.png>)
# Intent Pilot 

Intent-Pilot is an orchestration of two tools: AskUI's object detector with OpenAI's GPT-4v to achieve automation. It is designed to automate repetitive tasks, and to assist users in performing complex tasks with ease. This repository is our attempt to understand the GPT-4v's potential in automation and building an end-to-end automation tool.

We are inspired by and improve upon [Self-Operating-Computer](https://github.com/OthersideAI/self-operating-computer) by a more accurate object detection model and an improved prompting strategy. We also provide a more user-friendly interface, and a more intuitive way to interact with the tool. For example, the notification feature to let users know what is happening and what to do next. Also, our tool **works across all keyboard layouts - US, German, etc**, which was one of the limitations of similar tools.

## Demo

[watch the demo](images/demo.mp4)

# Quick Start

## Setup

- Python 3.9 or later
- OpenAI Key
- AskUI token
    - For staters, we provide a global AskUI key with 4000 free credits. `ASKUI_WORKSPACE_ID`: 'e26b43ea-a18f-4cd8-a6f1-e1e41dddec18' and `ASKUI_TOKEN`: 'gbwdeDjlWBrsr8nLjOVB'
    - After that, you can get your own AskUI key by signing up at [AskUI](https://askui.com)
- You can also copy the .env.example file to .env and fill in the required details OR You can enter the credentials in the terminal when you start the app.

### Linux
- In case of linux, you may need to install the following packages:
```shell
sudo apt-get install xsel xclip python3-tk python3-dev
```
### MacOS
- In case of MacOS, you will have to grant permissions to the terminal to access the clipboard. You can do this by going to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Accessibility` and then adding the terminal to the list of apps that can control your computer.

### Windows

We are currently working on the Windows version of the tool. It will be available __*soon*__.

__Quick Fix__: The package also works on Windows but the Windows Defender is deleting the `src/intent_pilot/utils/screenshot.py` file. You have to restore the file from the quarantine and add it to the exclusion list.

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
# Join Our Discord Community

For real-time discussions and community support, join our Discord server:
- Join our [Discord Server](https://discord.com/invite/Gu35zMGxbx) and then navigate to the #intent-pilot channel.

# Contributing

Thank you for your interest in contributing! We welcome involvement from the community.

We are still deciding on the contribution guidelines. Please stay tuned for updates.

# Roadmap

We are currently in the process of building PTA (Prompt-to-Automation) model, a Multi-Modal Model that can understand and execute commands in natural language, in real-time and faster than any VPA (Virtual Personal Assistant) in the market.
