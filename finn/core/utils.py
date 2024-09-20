from pathlib import Path

import aiofiles
from fastapi import UploadFile


def sanitize_filename(filename: str):
    return "".join(c for c in filename if c.isalpha() or c.isdigit() or c == " ").rstrip()


async def save_file(file: UploadFile, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(path, "wb") as new_file:
        try:
            content = await file.read()
            await new_file.write(content)
        except Exception as e:
            print(f"Arquivo {str(path)} não pode ser salvo! {e}")
