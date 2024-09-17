
<h1 align="center">⧐ Intent Pilot </h1>

<p align="center">
    <a href="https://discord.com/invite/Gu35zMGxbx">
        <img alt="Discord" src="https://img.shields.io/discord/912752657662349312?logo=discord&style=flat&logoColor=white"/></a>
    <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=white&style=flat" alt="License"/>
    <br>
    <br>
    <strong>What can be said can be solved.</strong><br>
    <br><a href="https://askui.com?utm_campaign=github&utm_medium=community&utm_source=github&utm_content=intent-pilot">Get early access to the PTA model</a>‎ ‎ |‎ ‎ <a href="https://askui.com?utm_campaign=github&utm_medium=community&utm_source=github&utm_content=intent-pilot">Scale on our shoulders</a><br>
</p>

<br>


![alt text](<images/opening-dialogue.png>)

# Intent Pilot 

_IntentPilot_ is an orchestration of two tools: AskUI's object detector with OpenAI's GPT-4v to achieve automation. It is designed to automate repetitive tasks, and to assist users in performing complex tasks with ease. This repository is our attempt to understand the GPT-4v's potential in automation and building an end-to-end automation tool.

We are inspired by and improve upon [Self-Operating-Computer](https://github.com/OthersideAI/self-operating-computer) by a more accurate object detection model and an improved prompting strategy. We also provide a more user-friendly interface, and a more intuitive way to interact with the tool. For example, the notification feature to let users know what is happening and what to do next. Also, our tool **works across all keyboard layouts - US, German, etc**, which was one of the limitations of similar tools.

## Demo

https://github.com/askui/intent-pilot/assets/106730702/582d7dec-e3ff-43fd-9ab7-0cad9103b366


## Quick Start

### Setup

- Python 3.11 or later
- OpenAI Key
- AskUI credentials
    - `ASKUI_WORKSPACE_ID` and `ASKUI_TOKEN` are needed in `.env` file to get the product running.
    - You can get your own AskUI credentials by signing up at [AskUI](https://askui.com)
- You can also copy the `.env.example` file to `.env` and fill in the required details OR You can enter the credentials in the terminal when you start the app.

**⚠️IMPORTANT: If you saved the credentials with the flag `-c --config`, you MUST delete them with the flag `-d --deleteconfig` again for the local `.env` file to be read again.**

#### Linux

- In case of linux, you may need to install the following packages:
```shell
sudo apt-get install xsel xclip python3-tk python3-dev
```

#### macOS

- In case of MacOS, you will have to grant permissions to the terminal to access the clipboard. You can do this by going to `System Preferences` -> `Security & Privacy` -> `Privacy` -> `Accessibility` and then adding the terminal to the list of apps that can control your computer.

#### Windows

We are currently working on the Windows version of the tool. It will be available __*soon*__.

__Quick Fix__: The package also works on Windows but the Windows Defender is deleting the `src/intent_pilot/utils/screenshot.py` file. You have to restore the file from the quarantine and add it to the exclusion list.

### Installation

```shell
pip install intent-pilot
```

#### Terminal

After installation, run `intent` in your terminal:

```shell
intent
```

In case, you are unable to run the command, try running the following command:
```shell
python -m intent_pilot
```

## Build from Source

We recommend using [PDM](https://pdm-project.org/) to build and run _Intent Pilot_

### Step 0: Install PDM

Run the following command in a terminal to install PDM:
```sh
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

### Step 1: Install Dependencies for _Intent Pilot_

Run the following command to install all the dependencies needed for _Intent Pilot_:
```sh
pdm install
```

### Step 2: Run _Intent Pilot_

Start the _Intent Pilot_ by running this command:
```sh
pdm run intent
```

## Flags

* `--debug`: Prints debug output to the console
* `--model -m <modelname>`: The model to use - `llava` or default `gpt4v`
* `-c --config`: Prompts to save the credentials configuration to `~/.askui/intent-pilot.env`
* `-d --deleteconfig`: Prompts to delete the credentials from `~/.askui/intent-pilot.env`



## Use Local llava Model Instead of gpt4-Vision
Install [Ollama for your system from their Website](https://ollama.com/).

* `ollama serve` to start the API locally
* `ollama run llava` to start the model locally
* Start the _Intent Pilot_ with the flag `-m llava`

## Join Our Discord Community

For real-time discussions and community support, join our Discord server:
- Join our [Discord Server](https://discord.com/invite/Gu35zMGxbx) and then navigate to the #intent-pilot channel.

## Contributing

Thank you for your interest in contributing! We welcome involvement from the community.

## Roadmap

We are currently in the process of building _PTA_ (Prompt-to-Automation) model, a Multi-Modal Model that can understand and execute commands in natural language, in real-time and faster than any _Virtual Personal Assistant_ (VPA) in the market.
