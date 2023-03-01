<h1 align="center"> :email: RenAI Chat </h1>

<p align="center">
  <a href="https://github.com/Rubiksman78/RenAI-Chat/releases/latest">
    <img alt="Latest release" src="https://img.shields.io/github/v/release/Rubiksman78/RenAI-Chat">
  </a>
   <a href="https://github.com/Rubiksman78/RenAI-Chat/releases">
    <img alt="Release downloads" src="https://img.shields.io/github/downloads/Rubiksman78/RenAI-Chat/total">
  </a>
</p>

This project aims to create a fun interface to use conversational models in the form of a Visual Novel in Renpy.
It's using multiple AI models:
- [Pygmalion](https://huggingface.co/PygmalionAI) conversational AI based on GPT-J Finetuning
- [TTS Coqui-AI](https://github.com/coqui-ai/TTS) and [Tortoise-TTS](https://github.com/152334H/tortoise-tts-fast) for Text to Speech
- [OpenAI Whisper](https://github.com/openai/whisper) with [microphone option](https://github.com/mallorbc/whisper_mic) for Speech to Text

# Overview

## :boom: Installation

Check out the wiki [page](https://github.com/Rubiksman78/RenAI-Chat/wiki).

## :fire: Features

- Speak without scripted text using the latest chatbots
- Clone your character voice with a Text to Speech module using extracts of voiced dialogues
- Talk with your own voice thanks to Speech recognition

## :eyeglasses: How to add chatbot models

- Check the [wiki](https://github.com/Rubiksman78/RenAI-Chat/wiki/Chatbots-info) to setup your GPU and for pratical info about chatbots to use
- On Huggingface website go to the model page, for example `https://huggingface.co/PygmalionAI/pygmalion-2.7b`

- Follow the instructions to download the model like this on your Command Prompt or Powershell opened wherever you want:
```
git lfs install
git clone https://huggingface.co/PygmalionAI/pygmalion-2.7b
```
- Once the download is finished, put the folder created in `chatbot_models` in the RenAIChat folder. You will be able to choose it in your next login !


## :microphone: Customize voice

For Your TTS model (worse but faster, ~5s per turn):
You can change the voice used by placing extracts in the `coquiai_audios` folder. The longer the extract, the longer the TTS will take to generate the audio at each turn (~1min is good). It has to be `.wav` audio files, use an online converter if you have `.mp3` files.

For Tortoise TTS model (better but slower, ~40s per turn): You can change the voice samples in `tortoise_voices_` folder. Create your own character by adding a folder with the name of your character and put the audio samples in it. The samples must be around 10 seconds long and at the number of 5 maximum. Prefer `.wav` files too.

On CPU, it can take 10x more time to generate the voice (Tortoise TTS can have unexpected behaviour on CPU)

## :camera: Customize game appearance

In your RenAIChat folder with the Renpy files, add a transparent sprite of your character with the filename `char.png` and add a background named `bg.png` in the folder `game/images`. Don't forget to resize your BG to 1920x1080 and your character to the size you want (without being more than 1920x1080).

# Python installation

## ❓Installation

- Clone the repository or download the latest release (`source code.zip`)
- Go to the project folder with your favorite IDE
- Be sure to have Python installed (3.8 or 3.9), it is not tested and functional before 3.7 and after 3.10.

To setup all the libraries:
- Run these commands in a terminal opened within the project folder to install the packages:
    ```
    pip install -r requirements.txt
    ```
- If you have a CUDA compatible GPU, run this too:
    ```
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
    ```
- If there was an error returned during the installation of the packages, delete the corresponding line in `requirements.txt` and dowload the package concerned manually
- To download TTS (with Coqui AI TTS), run these commands:
    ```
    git clone https://github.com/coqui-ai/TTS
    cd TTS
    pip install -e .
    cd ../
    ```
- To download TTS (with Tortoise-TTS), run these commands:
    ```
    git clone https://github.com/152334H/tortoise-tts-fast
    cd tortoise-tts-fast
    pip install -e .
    cd ../
    ```
- `simpleaudio` or other packages might need to install Visual Studio C++ Tools too (see tutorial [here](https://stackoverflow.com/questions/64261546/how-to-solve-error-microsoft-visual-c-14-0-or-greater-is-required-when-inst)), for `simpleaudio` follow [this](https://stackoverflow.com/questions/67312738/error-command-errored-out-with-exit-status-1-python-when-installing-simple)
- If you want to use Pygmalion models, follow these intructions:
  - To use `int8` i.e. models taking less GPU RAM with `bitsandbytes`:
     - Download these 2 dll files from [here](https://github.com/DeXtmL/bitsandbytes-win-prebuilt). Move those files in your python packages folder, on Windows it is something like `C:\Users\MyName\AppData\Local\Programs\Python\Python39\Lib\site-packages\bitsandbytes`
     - Edit `bitsandbytes\cuda_setup\main.py`: 
       - Change `ct.cdll.LoadLibrary(binary_path)` to `ct.cdll.LoadLibrary(str(binary_path))` two times in the file.
       - Replace the this line ```if not torch.cuda.is_available(): return 'libsbitsandbytes_cpu.so', None, None, None, None``` with ```if torch.cuda.is_available(): return 'libbitsandbytes_cuda116.dll', None, None, None, None```
- For troubleshooting and other issues, don't hesitate to submit an issue
