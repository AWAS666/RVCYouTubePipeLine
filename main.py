import shutil
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import zipfile, sys, os
from io import BytesIO

import audiogenerate


class Request(BaseModel):
    link: str = "https://www.youtube.com/watch?v=I4rtcJnRd6s"


pth_path = os.getenv("PTH_PATH", "")
index_path = os.getenv("INDEX_PATH", "")

audiogenerate.init(pth_path, index_path)
app = FastAPI()


def zipfiles(file_list):
    io = BytesIO()
    zip_sub_dir = "final_archive"
    zip_filename = "%s.zip" % zip_sub_dir
    with zipfile.ZipFile(io, mode="w", compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            zip.write(fpath)
        # close zip
        zip.close()
    return StreamingResponse(
        iter([io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment;filename=%s" % zip_filename},
    )


@app.post("/generate")
async def generate(body: Request):
    print(f"starting {body.link}")
    vocal, inst = audiogenerate.generateAudioTrack(body.link)
    effects = "singing.wav"
    shutil.move(inst,"inst.wav")
    audiogenerate.addEffects(vocal, effects)
    return zipfiles([effects, "inst.wav"])
