from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os,sys
import subprocess
import time
import simpleaudio as sa

from tts_api import my_TTS

import torch
import numpy as np

import IPython.display as ipd
from login_screen import CONFIG
import re

import yaml
import json

GAME_PATH = CONFIG["GAME_PATH"]
USE_TTS = CONFIG["USE_TTS"]
LAUNCH_YOURSELF = CONFIG["LAUNCH_YOURSELF"]
TTS_MODEL = CONFIG["TTS_MODEL"]
USE_SPEECH_RECOGNITION = CONFIG["USE_SPEECH_RECOGNITION"]
VOICE_SAMPLE_TORTOISE = CONFIG["VOICE_SAMPLE_TORTOISE"]
VOICE_SAMPLE_COQUI = CONFIG["VOICE_SAMPLE_COQUI"]
CHARACTER_JSON = CONFIG["CHARACTER_JSON"]

#Disable print from TTS Coqui AI
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

######LOAD CHATBOT CONFIG######
from chatbot.model import build_model_and_tokenizer_for
from run_chatbot import inference_fn
import gc 

with open("chatbot/chatbot_config.yml", "r") as f:
    CHAT_CONFIG = yaml.safe_load(f)

with open(f"char_json/{CHARACTER_JSON}", "r") as f:
    char_settings = json.load(f)
f.close()

model_name = CHAT_CONFIG["model_name"]
gc.collect()
torch.cuda.empty_cache()
chat_model, tokenizer = build_model_and_tokenizer_for(model_name)

generation_settings = {
    "max_new_tokens": CHAT_CONFIG["max_new_tokens"],
    "temperature": CHAT_CONFIG["temperature"],
    "repetition_penalty": CHAT_CONFIG["repetition_penalty"],
    "top_p": CHAT_CONFIG["top_p"],
    "top_k": CHAT_CONFIG["top_k"],
    "do_sample": CHAT_CONFIG["do_sample"],
    "typical_p":CHAT_CONFIG["typical_p"],
}

context_size = CHAT_CONFIG["context_size"]

with open("chat_history.txt", "a") as chat_history:
    chat_history.write("Conversation started at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")
#################################

#########Load the TTS model##########
with HiddenPrints():
    if USE_TTS:
        from tortoise.api import TextToSpeech,MODELS_DIR
        from tortoise.utils.audio import load_voices
        from voicefixer import VoiceFixer
        if TTS_MODEL == "Your TTS":
            tts_model = my_TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")
            sampling_rate = 16000
        elif TTS_MODEL == "Tortoise TTS":
            tts_model = TextToSpeech(
                    models_dir=MODELS_DIR,
                    high_vram=False,
                    kv_cache=True,
                )
            voice_samples, conditioning_latents = load_voices([VOICE_SAMPLE_TORTOISE], ["tortoise_audios"])
            vfixer = VoiceFixer()
            sampling_rate = 24000
        else:
            print("No TTS model selected")

def play_TTS(step,msg,play_obj):
    if USE_TTS:
        print("Using TTS")
        if step > 0:
            play_obj.stop()
        msg_audio = msg.replace("\n"," ")
        msg_audio = msg_audio.replace("{i}","")
        msg_audio = msg_audio.replace("{/i}",".")
        msg_audio = msg_audio.replace("~","!")
        msg_audio = emoji_pattern.sub(r'', msg_audio)
        msg_audio = uni_chr_re.sub(r'', msg_audio)
        with HiddenPrints():
            if TTS_MODEL == "Your TTS":
                audio = tts_model.tts(text=msg_audio,speaker_wav=f'coquiai_audios/{VOICE_SAMPLE_COQUI}', language='en')
            elif TTS_MODEL == "Tortoise TTS":
                gen, _ = tts_model.tts(
                        text=msg_audio,
                        k=1,
                        voice_samples=voice_samples,
                        conditioning_latents=conditioning_latents,
                        num_autoregressive_samples=8,
                        diffusion_iterations=20,
                        sampler="ddim",
                        return_deterministic_state=True,
                        latent_averaging_mode=1,
                        length_penalty=1.8,
                        max_mel_tokens=500,
                        cond_free_k=2,
                        top_p=0.85,
                        repetition_penalty=2.,
                    )
                audio = gen.squeeze(0).cpu().numpy()
        
        audio = ipd.Audio(audio, rate=sampling_rate)
        play_obj = sa.play_buffer(audio.data, 1, 2, sampling_rate)
        return play_obj
#####################################

####Load the speech recognizer#####
if USE_SPEECH_RECOGNITION:
    import speech_recognition as sr
    import whisper

    english = True
    def init_stt(model="base", english=True,energy=300, pause=0.8, dynamic_energy=False):
        if model != "large" and english:
            model = model + ".en"
        audio_model = whisper.load_model(model)    
        r = sr.Recognizer()
        r.energy_threshold = energy
        r.pause_threshold = pause
        r.dynamic_energy_threshold = dynamic_energy
        return r,audio_model

    r,audio_model = init_stt()
#####################################

GAME_PATH = GAME_PATH.replace("\\", "/")
clients = {}
addresses = {}
HOST = '127.0.0.1'
PORT = 12346
BUFSIZE = 1024
ADDRESS = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)
queued = False
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002500-\U00002BEF"  # chinese char
    u"\U00002702-\U000027B0"
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"
    u"\U00010000-\U0010ffff"
    u"\u2640-\u2642"
    u"\u2600-\u2B55"
    u"\u200d"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\ufe0f"  # dingbats
    u"\u3030"
    u"\u2014"
    "]+", flags=re.UNICODE)

uni_chr_re = re.compile(r'\\u[0-9a-fA-F]{4}')

#Launch the game
if not LAUNCH_YOURSELF:
    subprocess.Popen(GAME_PATH+'/DDLC.exe')

def listen():
	""" Wait for incoming connections """
	print("Waiting for connection...")
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has connected." % client_address)
		addresses[client] = client_address
		Thread(target = call, args = (client,)).start()

def call(client):
    thread = Thread(target=listenToClient, args=(client,), daemon=True)
    thread.start()


def sendMessage(msg, name=""):
    """ send message to all users present in 
    the chat room"""
    for client in clients:
        client.send(bytes(name, "utf8") + msg)

def send_answer(received_msg,msg):
    action_to_take = "none"
    action_to_take = action_to_take.encode("utf-8")           
    emotion = "".encode("utf-8")
    msg = msg.encode("utf-8")   
    msg_to_send = msg + b"/g" + emotion + b"/g" + action_to_take
    sendMessage(msg_to_send)


def listenToClient(client):
    """ Get client username """
    name = "User"
    clients[client] = name
    launched = False
    chat_count = 0
    play_obj = None
    if os.path.exists("char_history.txt"):
        history = open("char_history.txt","r").read()
        #Remove lines with the pattern "Conversation started at: 2023-02-14 14:14:17"
        history = re.sub(r"Conversation started at: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}","",history)
    else:
        history = ""
    while True:
        received_msg = client.recv(BUFSIZE).decode("utf-8") #Message indicating the mode used (chatbot,camera_int or camera)
        received_msg = received_msg.split("/m")
        rest_msg = received_msg[1]
        received_msg = received_msg[0]
        if received_msg == "chatbot":
            if '/g' in rest_msg:
                received_msg , step = rest_msg.split("/g")
            else:
                received_msg = client.recv(BUFSIZE).decode("utf-8") #Message containing the user input
                received_msg , step = received_msg.split("/g")
            step = int(step)
            #Speech to text
            if received_msg == "begin_record":
                if USE_SPEECH_RECOGNITION:
                    with sr.Microphone(sample_rate=16000) as source:
                        sendMessage("yes".encode("utf-8"))
                        #get and save audio to wav file
                        audio = r.listen(source)
                        torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                        audio_data = torch_audio
                        if english:
                            result = audio_model.transcribe(audio_data,language='english')
                        else:
                            result = audio_model.transcribe(audio_data)
                        received_msg = result['text']
                else:
                    sendMessage("no".encode("utf-8"))
                    continue
                       
            print("User: "+received_msg)
    
            while True: 
                if chat_count == 0:
                    sendMessage("server_ok".encode("utf-8"))
                    ok_ready = client.recv(BUFSIZE).decode("utf-8")
                    bot_message = inference_fn(chat_model,tokenizer,history, "",generation_settings,char_settings,history_length=context_size,count=chat_count)
                else:
                    bot_message = inference_fn(chat_model,tokenizer,history, received_msg,generation_settings,char_settings,history_length=context_size,count=chat_count)
                    history = history + "\n" + f"You: {received_msg}" + "\n" + f"{bot_message}"
                if received_msg != "QUIT":   
                    if received_msg == "REGEN":
                        history.replace("\n" + f"You: {received_msg}" + "\n" + f"{bot_message}","")
                        bot_message = inference_fn(chat_model,tokenizer,history, received_msg,generation_settings,char_settings,history_length=context_size,count=chat_count) 
                    bot_message = bot_message.replace("<USER>","Player")
                    play_obj = play_TTS(step,bot_message,play_obj)
                    print("Sent: "+ bot_message)    
                    send_answer(received_msg,bot_message)
                    chat_count += 1
                    if chat_count > 1:
                        with open("chat_history.txt", "a",encoding="utf-8") as f:
                            f.write(f"You: {received_msg}" + "\n" + f'{char_settings["char_name"]}: {bot_message}' + "\n")
                break                  


if __name__ == "__main__":
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=listen)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()