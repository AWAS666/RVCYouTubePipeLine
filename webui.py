import os
import shutil
import time
import gradio as gr
from pydub import AudioSegment
import audiogenerate

# Set up fixed folders
RVC_FOLDER = "./rvc"
os.makedirs(RVC_FOLDER, exist_ok=True)


def list_files_with_ext(folder, ext):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(ext)]


def get_pth_files():
    return list_files_with_ext(RVC_FOLDER, ".pth")


def get_index_files():
    return list_files_with_ext(RVC_FOLDER, ".index")



def generate_func(pth_file, index_file, url):

    # todo change, so this is only done once
    audiogenerate.init(pth_file, index_file)

    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)
    wav1, wav2 = audiogenerate.generateAudioTrack(
        url, os.path.join(output_folder, "output.wav")
    )

    mixed_path = os.path.join(output_folder, "mixed.wav")
    audiogenerate.mixAudio(wav1, wav2, mixed_path)

    effects = os.path.join(output_folder, "effects.wav")
    mixedEffects = os.path.join(output_folder, "mixedEffects.wav")
    audiogenerate.addEffects(wav1, effects)
    audiogenerate.mixAudio(effects, wav2, mixedEffects)

    # clean up the rest of the files -> add delete option
    remfiles = list_files_with_ext(".", ".wav")
    for rem in remfiles:
        shutil.move(rem, os.path.join(output_folder, rem))


    return wav1, wav2, mixed_path, mixedEffects

if __name__ == "__main__":
    iface = gr.Interface(
    fn=generate_func,
    inputs=[
        gr.Dropdown(choices=get_pth_files(), label="Select .pth file"),
        gr.Dropdown(choices=get_index_files(), label="Select .index file"),
        gr.Textbox(label="Enter URL"),
    ],
    outputs=[
        gr.Audio(label="Vocals", type="filepath"),
        gr.Audio(label="Instrumental", type="filepath"),
        gr.Audio(label="Mixed Audio", type="filepath"),
        gr.Audio(label="Effects", type="filepath"),
    ],
    title="Youtube to RVC",
    description="Select model files and enter a URL to generate audio outputs.",
    )

    iface.launch()