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
    async def magik(self, ctx: commands.Context, image: str, scale: int = None):
        """Performs a magik destruction on an image."""
        resp = requests.get(image)
        img = Image(file=io.BytesIO(resp.content))
        img.format = image.split("/")[-1].split(".")[-1]
        img.liquid_rescale(width=int(img.width * 0.5), height=int(img.height * 0.5), delta_x=int(0.5 * scale) if scale else 1, rigidity=0)
        processed = io.BytesIO()
        img.save(file=processed)
        processed.seek(0)
        await ctx.send(file=File(processed, filename=image.split("/")[-1]))
