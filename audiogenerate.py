from rvc_python.infer import RVCInference
from audio_separator.separator import Separator
from yt_dlp import YoutubeDL
from pydub import AudioSegment, effects
from pedalboard import Compressor, Gain, Pedalboard, Reverb
from pedalboard.io import AudioFile

## todo: make this a class or something -> refactor

def init(rvcmodel, rvcindex):
    global rvc, separator, dereverb
    rvc = RVCInference(device="cuda:0")
    rvc.load_model(rvcmodel, index_path=rvcindex)
    rvc.set_params(f0method="rmvpe")

    separator = Separator()
    # separator.load_model("model_bs_roformer_ep_368_sdr_12.9628.ckpt")
    # separator.load_model("mel_band_roformer_kim_ft3_unwa.ckpt")
    separator.load_model("vocals_mel_band_roformer.ckpt")
    dereverb = Separator()
    dereverb.load_model("dereverb_mel_band_roformer_anvuew_sdr_19.1729.ckpt")

def ytdownload(url):
    ydl_opts = {
        "source_address": "0.0.0.0",
        "outtmpl": "song.%(ext)s",
        "format": "140",
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def addEffects(input, output):
    # Make a Pedalboard object, containing multiple audio plugins:
    board = Pedalboard(
        [
            Compressor(ratio=4, threshold_db=-10),
            Reverb(room_size=0.2, damping=0.7, dry_level=0.6, wet_level=0.15),
            Gain(gain_db=1),
        ]
    )
    # Open an audio file for reading, just like a regular file:
    with AudioFile(input) as f:
    
        # Open an audio file to write to:
        with AudioFile(output, 'w', f.samplerate, f.num_channels) as o:
        
            # Read one second of audio at a time, until the file is empty:
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)
                
                # Run the audio through our pedalboard:
                effected = board(chunk, f.samplerate, reset=False)
                
                # Write the output to our output file:
                o.write(effected)

def mixAudio(wav1, wav2, mixed_path):
    sound1 = AudioSegment.from_wav(wav1)
    sound2 = AudioSegment.from_wav(wav2)

    # Mix the two audio files
    mixed = sound1.overlay(sound2)

    # Export mixed audio
    mixed.export(mixed_path, format="wav")

# generate
def generateAudioTrack(url, outputfile = "output.wav"):
    ytdownload(url)
    output_files = separator.separate('song.wav')
    dereverb_files = dereverb.separate(output_files[1])

    # mix instrumental with dereverbed for better inst sound
    mixAudio(output_files[0], dereverb_files[0], output_files[0])

    rvc.infer_file(dereverb_files[1], outputfile)
    song = AudioSegment.from_wav(outputfile)
    song = effects.normalize(song)  
    song.export(outputfile, "wav")
    return (outputfile, output_files[0])

#create("https://www.youtube.com/watch?v=fKyXvNkGQKc", "kingslayer.wav")
#create("https://www.youtube.com/watch?v=kXYiU_JCYtU", "numb.wav")
#https://www.youtube.com/watch?v=fKyXvNkGQKc kingslayer
#https://www.youtube.com/watch?v=I4rtcJnRd6s nightglow