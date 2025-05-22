# Youtube to RVC song pipeline
This projects aims to be a one stop shop to convert any song from youtube to a rvc song cover.

Example:
https://github.com/user-attachments/assets/4e7a18d9-5b88-4f4f-93a4-159ed11306e8

## Install
Install torch <2.5 (audio-seperator)
``` 
pip install torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu118
```

Install requirements
```
pip install -r requirements.txt
```

You will likely need ffmpeg

## Train your models
This repo doesn't include training.

Just copy your model you trained using the [rvc main repo](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) into "rvc"

## Run webui
```python 
python3 webui.py
```

## Models
List by best vocals: 
audio-separator -l --list_filter=vocals --list_limit=5

## Todo
- [x] basic pipeline in script
- [x] fastapi endpoint
- [x] gradio ui
- [x] effects like reverb -> pedalboard
    - [ ] improve effects and make them changeble in the webui
- [ ] suno integration
