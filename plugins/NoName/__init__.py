import io
import os
from functools import partial
import random

os.environ["MAGICK_HOME"] = "/usr/lib"

import requests
from discord import File
from discord.ext import commands
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

from Plugin import BorobPlugin


class NoNamePlugin(BorobPlugin):
    @staticmethod
    def save_image(image: Image) -> io.BytesIO:
        """Save an image to a file-like object."""
        processed = io.BytesIO()
        image.save(file=processed)
        image.close()
        processed.seek(0)
        return processed

    async def run_async(self, function, *args, **kwargs):
        """Run a method in an asyncio executor, preventing blocking."""
        await self.bot.loop.run_in_executor(None, partial(function, *args, **kwargs))

    @commands.command()
    async def noname(self, ctx: commands.Context, text: str):
        with Image(height=1000, width=1000, background=Color("#fbdd00")) as image:
            with Drawing() as draw:
                draw.font = os.path.join(
                    self.manifest["path"], "fonts", "HelveticaNeue.ttf"
                )
                draw.font_size = 72
                draw.text(image.width / 3, image.height / 2, text)
                draw(image)
            processed = self.save_image(image)
            await ctx.send(file=File(processed, filename="noname.png"))
