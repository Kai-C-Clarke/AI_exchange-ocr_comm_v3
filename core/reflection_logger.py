import logging
from datetime import datetime
from core import config

def save_reflection(response: str, prompt: str, frames: int, reason: str, speaker: str):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    date = datetime.now().strftime("%Y-%m-%d")
    path = config.REFLECTIONS_FOLDER / f"kai_reflections_{date}_{speaker}.txt"
    meta = config.META_FILE

    with open(path, "a") as f:
        f.write(f"\n[{now}] {speaker} REPLY:\n{response}\n")
        f.write(f"Source prompt: {prompt}\n")
        f.write(f"Frames captured: {frames} | Stop reason: {reason}\n\n")

    with open(meta, "a") as f:
        f.write(f"[{now}] {speaker} replied. Prompt: {prompt}\n")

    logging.info(f"💾 Reflection saved for {speaker} ({frames} frames)")
