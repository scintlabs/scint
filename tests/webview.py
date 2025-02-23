import sys
import asyncio
import subprocess
from pprint import pp
from datetime import datetime as dt
from typing import List

import aiohttp
import aiofiles
from pydantic import BaseModel
from bs4 import BeautifulSoup
import PyPDF2


class Link(BaseModel):
    url: str
    description: str


class View(BaseModel):
    links: List[Link] = []


class WebView(BaseModel):
    url: str
    views: List[View] = []
    created: str = str(dt.now())


def snapshot_to_images(pdf_path: str):
    command = ["magick", "-density", "300", pdf_path, "output_%03d.png"]
    subprocess.run(command, check=True)


async def download(url: str, type: str):
    name = "".join(url.split(".")).split("/")[-1]
    filename = f"{name}.{type}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(filename, mode="wb") as file:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        await file.write(chunk)

                    print(f"Successfully downloaded {filename}.")
                    return filename
            else:
                print(f"Failed to download {filename}.")


async def get_snapshot(url: str):
    params = {"url": url, "pdf": "true"}
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.microlink.io", params=params) as response:
            if response.status == 200:
                res = await response.json()
                data = res.get("data")
                link = data["pdf"]["url"]
                pdf_path = await download(link, "pdf")
                snapshot_to_images(pdf_path)
                return pdf_path


async def get_anchors(html: str):
    soup = BeautifulSoup(html, "html.parser")
    anchor_data = {}
    for a_tag in soup.find_all("a", href=True):
        link = a_tag["href"]
        text = a_tag.get_text(strip=False)
        anchor_data[link] = text
    return anchor_data


def merge_links(anchors, annotations):
    links = []
    for k, v in annotations.items():
        for i, n in anchors.items():
            if k == i and n is not None:
                links.append(Link(url=k, description=n))
    model = View(links=links)
    return model


async def get_annotations(url: str):
    pdf_path = await get_snapshot(url)
    html_path = await download(url, "html")

    with open(html_path, "rb") as html:
        anchors = await get_anchors(html)

    with open(pdf_path, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf)
        annos = {}
        for k, v in enumerate(reader.pages):
            if "/Annots" in v:
                annotations = v["/Annots"]
                for annot in annotations:
                    annot_obj = annot.get_object()
                    if annot_obj.get("/Subtype") == "/Link":
                        if "/A" in annot_obj:
                            action = annot_obj["/A"]
                            if action.get("/S") == "/URI":
                                annos[action.get("/URI")] = None
            else:
                print("  No annotations on this page.")

        model = merge_links(anchors, annos)
        pp(model.model_dump())
        return model


async def parse_website():
    if len(sys.argv) < 2:
        print("Usage: python extract_links.py <pdf_file>")
        sys.exit(1)
    url = sys.argv[1]
    return await get_annotations(url)


if __name__ == "__main__":
    asyncio.run(parse_website())
