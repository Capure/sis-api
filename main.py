from download import download_timetable
from parse import parse_timetable
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    html = download_timetable()
    return parse_timetable(html)