import io
import os

os.environ["MAGICK_HOME"] = "/usr/lib"

import requests
from discord import File
from discord.ext import commands
from wand.image import Image

from Plugin import BorobPlugin


class MagikPlugin(BorobPlugin):
    """Provides magik-type functionality."""

    @commands.command()
    async def magik(self, ctx: commands.Context, image: str, scale: float = None, destwidth: int = None, destheight: int = None):
        """Performs a magik destruction on an image."""
        resp = requests.get(image)
        img = Image(file=io.BytesIO(resp.content))
        img.format = image.split("/")[-1].split(".")[-1].lower()
        img.transform(resize='800x800>')
        if not destwidth:
            destwidth = int(img.width * 0.5)
        if not destheight:
            destheight = int(img.height * 0.5)
        original_width = img.width
        original_height = img.height
        img.liquid_rescale(width=destwidth, height=destheight, delta_x=scale if scale else 1, rigidity=0)
        processed = io.BytesIO()
        img.transform(f'{original_width}x{original_height}')
        img.save(file=processed)
        processed.seek(0)
        await ctx.send(file=File(processed, filename=image.split("/")[-1]))
