import os,sys
import tkinter as tk
import json
import yaml
# Configuration
args = sys.argv[1:]

save_ids = os.path.exists("save_text.txt")

root = tk.Tk()
root.title("RenAI Chat Login")
root.geometry("700x250")
root.configure(background='#333333')

def get_input():
    global GAME_PATH
    global USE_TTS
    global CHAT_MODEL
    global LAUNCH_YOURSELF
    global TTS_MODEL
    global USE_SPEECH_RECOGNITION
    global VOICE_SAMPLE_TORTOISE
    global VOICE_SAMPLE_COQUI
    global CHARACTER_JSON
    USE_TTS = use_tts.get()
    GAME_PATH = game_path.get()
    LAUNCH_YOURSELF = launch_yourself.get()
    CHAT_MODEL = chat_model.get()
    TTS_MODEL = tts_model.get()
    USE_SPEECH_RECOGNITION = use_speech_recognition.get()
    VOICE_SAMPLE_TORTOISE = voice_sample_tortoise.get()
    VOICE_SAMPLE_COQUI = voice_sample_coqui.get()
    CHARACTER_JSON =character_json.get()
    root.destroy()

other_frame = tk.LabelFrame(root,bg='#333333',text="General Settings",fg='white',font=("Helvetica", 16))
other_frame.grid(row=5, column=0)

use_tts = tk.StringVar()
game_path = tk.StringVar()
launch_yourself = tk.StringVar()
chat_model = tk.StringVar()
tts_model = tk.StringVar()
use_speech_recognition = tk.StringVar()
voice_sample_tortoise = tk.StringVar()
voice_sample_coqui = tk.StringVar()
character_json = tk.StringVar()

#General Settings
tk.Label(other_frame, text="Game Path",bg='#333333',fg='white').grid(row=1, column=0)
tk.Label(other_frame, text="Launch Yourself",bg='#333333',fg='white').grid(row=1, column=3)
tk.Label(other_frame, text="Use TTS",bg='#333333',fg='white').grid(row=3, column=0)
tk.Label(other_frame, text="TTS model",bg='#333333',fg='white').grid(row=3, column=3)
tk.Label(other_frame, text="Chatbot Model",bg='#333333',fg='white').grid(row=4, column=0)
tk.Label(other_frame, text="Use Speech Recognition",bg='#333333',fg='white').grid(row=6, column=0)
tk.Label(other_frame, text="Voice Sample (Tortoise)",bg='#333333',fg='white').grid(row=7, column=0)
tk.Label(other_frame, text="Voice Sample (Your TTS)",bg='#333333',fg='white').grid(row=7, column=3)
tk.Label(other_frame, text="Character JSON",bg='#333333',fg='white').grid(row=4, column=2)

#Textual Inputs
tk.Entry(other_frame, textvariable=game_path,width=25).grid(row=1, column=1)

#Scrollable Inputs
all_models = os.listdir("chatbot_models")
all_models = [x for x in all_models if not x.endswith(".txt")]
if len(all_models) == 0:
    all_models = ["No models found"]
chat_menu = tk.OptionMenu(other_frame, chat_model, *all_models)
chat_menu.config(bg='white',fg='black')
chat_menu.grid(row=4, column=1)

tts_menu = tk.OptionMenu(other_frame, tts_model, "Your TTS", "Tortoise TTS")
tts_menu.config( bg='white',fg='black')
tts_menu.grid(row=3, column=4)

all_voices_tortoise = os.listdir("tortoise_audios")
all_voices_tortoise = [x for x in all_voices_tortoise if not x.endswith(".txt")]
voice_menu = tk.OptionMenu(other_frame, voice_sample_tortoise, *all_voices_tortoise)
voice_menu.config( bg='white',fg='black')
voice_menu.grid(row=7, column=1)

all_voices_coquiai = os.listdir("coquiai_audios")
all_voices_coquiai = [x for x in all_voices_coquiai if x.endswith(".wav")]
if len(all_voices_coquiai) == 0:
    all_voices_coquiai = ["No voices found"]
voice_menu = tk.OptionMenu(other_frame, voice_sample_coqui, *all_voices_coquiai)
voice_menu.config( bg='white',fg='black')
voice_menu.grid(row=7, column=4)

all_characters = os.listdir("char_json")
all_characters = [x for x in all_characters if not x.endswith(".txt")]
character_menu = tk.OptionMenu(other_frame, character_json, *all_characters)
character_menu.config( bg='white',fg='black')
character_menu.grid(row=4, column=3)

#Yes/No Inputs
tk.Radiobutton(other_frame, text="Yes", variable=launch_yourself, value=True,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=1, column=4)
tk.Radiobutton(other_frame, text="No", variable=launch_yourself, value=False,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=1, column=5)

tk.Radiobutton(other_frame, text="Yes", variable=use_tts, value=True,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=3, column=1)
tk.Radiobutton(other_frame, text="No", variable=use_tts, value=False,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=3, column=2)

tk.Radiobutton(other_frame, text="Yes", variable=use_speech_recognition, value=True,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=6, column=1)
tk.Radiobutton(other_frame, text="No", variable=use_speech_recognition, value=False,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=6, column=2)

button = tk.Button(root, text="Submit", command=get_input,bg='#FF3399',fg='white')
button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

#KEEP_CONFIG = int(KEEP_CONFIG)

if not os.path.exists("config.json"):
    #Set default values
    launch_yourself.set(0)
    use_tts.set(0)
    chat_model.set("NO_MODEL_SET")
    tts_model.set("Your TTS")
    use_speech_recognition.set(0)
    voice_sample_tortoise.set("SELECT_A_VOICE")
    voice_sample_coqui.set("talk_13.wav")
    character_json.set("SELECT_A_CHARACTER")
else:
    with open("config.json", "r") as f:
        config = json.load(f)
        GAME_PATH = config["GAME_PATH"]
        USE_TTS = config["USE_TTS"]
        LAUNCH_YOURSELF = config["LAUNCH_YOURSELF"]
        TTS_MODEL = config["TTS_MODEL"]
        CHAT_MODEL = config["CHAT_MODEL"]
        USE_SPEECH_RECOGNITION = config["USE_SPEECH_RECOGNITION"]
        VOICE_SAMPLE_TORTOISE = config["VOICE_SAMPLE_TORTOISE"]
        VOICE_SAMPLE_COQUI = config["VOICE_SAMPLE_COQUI"]
        CHARACTER_JSON = config["CHARACTER_JSON"]
    #Set saved values
    launch_yourself.set(LAUNCH_YOURSELF)
    use_tts.set(USE_TTS)
    chat_model.set(CHAT_MODEL)
    tts_model.set(TTS_MODEL)
    use_speech_recognition.set(USE_SPEECH_RECOGNITION)
    voice_sample_tortoise.set(VOICE_SAMPLE_TORTOISE)
    voice_sample_coqui.set(VOICE_SAMPLE_COQUI)
    character_json.set(CHARACTER_JSON)

root.mainloop()

#Convert string to int (0 or 1, False or True)
USE_TTS = int(USE_TTS)
LAUNCH_YOURSELF = int(LAUNCH_YOURSELF)
USE_SPEECH_RECOGNITION = int(USE_SPEECH_RECOGNITION)

#Save model chosen in chatbot config
with open("chatbot/chatbot_config.yml", "r") as f:
    config_chat = yaml.safe_load(f)
config_chat["model_name"] = "chatbot_models/" + CHAT_MODEL
with open("chatbot/chatbot_config.yml", "w") as f:
    yaml.dump(config_chat, f)

#Save config to a json file
CONFIG = {
    "GAME_PATH": GAME_PATH,
    "USE_TTS": USE_TTS,
    "LAUNCH_YOURSELF": LAUNCH_YOURSELF,
    "TTS_MODEL": TTS_MODEL,
    "CHAT_MODEL": CHAT_MODEL,
    "USE_SPEECH_RECOGNITION": USE_SPEECH_RECOGNITION,
    "VOICE_SAMPLE_TORTOISE": VOICE_SAMPLE_TORTOISE,
    "VOICE_SAMPLE_COQUI": VOICE_SAMPLE_COQUI,
    "CHARACTER_JSON": CHARACTER_JSON
}

with open("config.json", "w") as f:
    json.dump(CONFIG, f)
