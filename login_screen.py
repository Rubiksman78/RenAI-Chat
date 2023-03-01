import os,sys
import tkinter as tk
import json
import yaml
# Configuration
args = sys.argv[1:]

save_ids = os.path.exists("save_text.txt")

root = tk.Tk()
root.title("RenAI Chat Login")
root.geometry("700x300")
root.configure(background='#333333')

def get_input():
    global GAME_PATH
    global USE_TTS
    global USE_CAMERA
    global TIME_INTERVALL
    global PYG_MODEL
    global LAUNCH_YOURSELF
    global USE_ACTIONS
    global TTS_MODEL
    global USE_SPEECH_RECOGNITION
    global VOICE_SAMPLE_TORTOISE
    global VOICE_SAMPLE_COQUI
    global CHARACTER_JSON
    USE_TTS = use_tts.get()
    GAME_PATH = game_path.get()
    LAUNCH_YOURSELF = launch_yourself.get()
    USE_CAMERA = use_camera.get()
    TIME_INTERVALL = time_intervall.get()
    PYG_MODEL = pyg_model.get()
    USE_ACTIONS = use_actions.get()
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
use_camera = tk.StringVar()
time_intervall = tk.StringVar()
pyg_model = tk.StringVar()
use_actions = tk.StringVar()
tts_model = tk.StringVar()
use_speech_recognition = tk.StringVar()
voice_sample_tortoise = tk.StringVar()
voice_sample_coqui = tk.StringVar()
character_json = tk.StringVar()

#General Settings
tk.Label(other_frame, text="Game Path",bg='#333333',fg='white').grid(row=1, column=0)
tk.Label(other_frame, text="Launch Yourself",bg='#333333',fg='white').grid(row=1, column=3)
tk.Label(other_frame, text="Use Actions",bg='#333333',fg='white').grid(row=2, column=0)
tk.Label(other_frame, text="Use TTS",bg='#333333',fg='white').grid(row=3, column=0)
tk.Label(other_frame, text="TTS model",bg='#333333',fg='white').grid(row=3, column=3)
tk.Label(other_frame, text="Pygmalion Model",bg='#333333',fg='white').grid(row=4, column=0)
tk.Label(other_frame, text="Use Camera",bg='#333333',fg='white').grid(row=5, column=0)
tk.Label(other_frame, text="Time Intervall For Camera",bg='#333333',fg='white').grid(row=5,column=3)
tk.Label(other_frame, text="Use Speech Recognition",bg='#333333',fg='white').grid(row=6, column=0)
tk.Label(other_frame, text="Voice Sample (Tortoise)",bg='#333333',fg='white').grid(row=7, column=0)
tk.Label(other_frame, text="Voice Sample (Your TTS)",bg='#333333',fg='white').grid(row=7, column=3)
tk.Label(other_frame, text="Character JSON",bg='#333333',fg='white').grid(row=4, column=2)

#Textual Inputs
tk.Entry(other_frame, textvariable=game_path,width=25).grid(row=1, column=1)
tk.Entry(other_frame, textvariable=time_intervall,width=10).grid(row=5, column=4)

#Scrollable Inputs
all_models = os.listdir("chatbot_models")
all_models = [x for x in all_models if not x.endswith(".txt")]
pyg_menu = tk.OptionMenu(other_frame, pyg_model, *all_models)
pyg_menu.config( bg='white',fg='black')
pyg_menu.grid(row=4, column=1)

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

tk.Radiobutton(other_frame, text="Yes", variable=use_actions, value=True,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=2, column=1)
tk.Radiobutton(other_frame, text="No", variable=use_actions, value=False,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=2, column=2)

tk.Radiobutton(other_frame, text="Yes", variable=use_tts, value=True,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=3, column=1)
tk.Radiobutton(other_frame, text="No", variable=use_tts, value=False,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=3, column=2)

tk.Radiobutton(other_frame, text="Yes", variable=use_camera, value=True,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=5, column=1)
tk.Radiobutton(other_frame, text="No", variable=use_camera, value=False,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=5, column=2)

tk.Radiobutton(other_frame, text="Yes", variable=use_speech_recognition, value=True,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=6, column=1)
tk.Radiobutton(other_frame, text="No", variable=use_speech_recognition, value=False,bg='#333333',activeforeground='white',fg='white',activebackground="#333333",selectcolor='#333333').grid(row=6, column=2)

button = tk.Button(root, text="Submit", command=get_input,bg='#FF3399',fg='white')
button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

#KEEP_CONFIG = int(KEEP_CONFIG)

if not os.path.exists("config.json"):
    #Set default values
    launch_yourself.set(0)
    time_intervall.set("10")
    use_tts.set(0)
    use_camera.set(0)
    pyg_model.set("NO_MODEL_SET")
    use_actions.set(0)
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
        USE_CAMERA = config["USE_CAMERA"]
        TIME_INTERVALL = config["TIME_INTERVALL"]
        LAUNCH_YOURSELF = config["LAUNCH_YOURSELF"]
        USE_ACTIONS = config["USE_ACTIONS"]
        TTS_MODEL = config["TTS_MODEL"]
        PYG_MODEL = config["PYG_MODEL"]
        USE_SPEECH_RECOGNITION = config["USE_SPEECH_RECOGNITION"]
        VOICE_SAMPLE_TORTOISE = config["VOICE_SAMPLE_TORTOISE"]
        VOICE_SAMPLE_COQUI = config["VOICE_SAMPLE_COQUI"]
        CHARACTER_JSON = config["CHARACTER_JSON"]
    #Set saved values
    launch_yourself.set(LAUNCH_YOURSELF)
    time_intervall.set(TIME_INTERVALL)
    use_tts.set(USE_TTS)
    use_camera.set(USE_CAMERA)
    pyg_model.set(PYG_MODEL)
    use_actions.set(USE_ACTIONS)
    tts_model.set(TTS_MODEL)
    use_speech_recognition.set(USE_SPEECH_RECOGNITION)
    voice_sample_tortoise.set(VOICE_SAMPLE_TORTOISE)
    voice_sample_coqui.set(VOICE_SAMPLE_COQUI)
    character_json.set(CHARACTER_JSON)

root.mainloop()

#Convert string to int (0 or 1, False or True)
USE_TTS = int(USE_TTS)
USE_CAMERA = int(USE_CAMERA)
TIME_INTERVALL = int(TIME_INTERVALL)
LAUNCH_YOURSELF = int(LAUNCH_YOURSELF)
USE_ACTIONS = int(USE_ACTIONS)
USE_SPEECH_RECOGNITION = int(USE_SPEECH_RECOGNITION)

#Save model chosen in pygmalion config
with open("pygmalion/pygmalion_config.yml", "r") as f:
    config_pyg = yaml.safe_load(f)
config_pyg["model_name"] = "chatbot_models/" + PYG_MODEL
with open("pygmalion/pygmalion_config.yml", "w") as f:
    yaml.dump(config_pyg, f)

#Save config to a json file
CONFIG = {
    "GAME_PATH": GAME_PATH,
    "USE_TTS": USE_TTS,
    "USE_CAMERA": USE_CAMERA,
    "TIME_INTERVALL": TIME_INTERVALL,
    "LAUNCH_YOURSELF": LAUNCH_YOURSELF,
    "USE_ACTIONS": USE_ACTIONS,
    "TTS_MODEL": TTS_MODEL,
    "PYG_MODEL": PYG_MODEL,
    "USE_SPEECH_RECOGNITION": USE_SPEECH_RECOGNITION,
    "VOICE_SAMPLE_TORTOISE": VOICE_SAMPLE_TORTOISE,
    "VOICE_SAMPLE_COQUI": VOICE_SAMPLE_COQUI,
    "CHARACTER_JSON": CHARACTER_JSON
}

with open("config.json", "w") as f:
    json.dump(CONFIG, f)