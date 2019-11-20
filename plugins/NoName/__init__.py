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

    @commands.command()
    async def magik(
        self,
        ctx: commands.Context,
        image: str,
        scale: float = 1,
        destwidth: int = None,
        destheight: int = None,
    ):
        """Performs a magik destruction on an image."""
        async with ctx.channel.typing():
            img = self.get_image(image)
            await self.run_async(img.transform, resize="800x800>")
            if not destwidth:
                destwidth = int(img.width * 0.5)
            if not destheight:
                destheight = int(img.height * 0.5)
            original_width = img.width
            original_height = img.height
            await self.run_async(
                img.liquid_rescale,
                width=destwidth,
                height=destheight,
                delta_x=scale,
                rigidity=0,
            )
            await self.run_async(
                img.transform, resize=f"{original_width}x{original_height}!"
            )
            processed = self.save_image(img)
            await ctx.send(file=File(processed, filename=image.split("/")[-1]))

    @commands.command()
    async def gmagik(self, ctx: commands.Context, image: str):
        """Magik, but for creating gifs."""
        async with ctx.channel.typing():
            img = self.get_image(image)
            await self.run_async(img.transform, resize="400x400>")
            destwidth = int(img.width * 0.7)
            destheight = int(img.height * 0.7)
            new_image = Image()
            frame = Image(image=img)
            frame.format = "GIF"
            new_image.sequence.append(frame)
            for i in range(10):
                await self.run_async(
                    frame.liquid_rescale,
                    width=destwidth,
                    height=destheight,
                    delta_x=1,
                    rigidity=0,
                )
                await self.run_async(
                    frame.liquid_rescale,
                    width=int(destwidth * 1.3),
                    height=int(destheight * 1.3),
                    delta_x=2,
                    rigidity=0,
                )
                await self.run_async(
                    frame.transform, resize=f"{img.width}x{img.height}!"
                )
                last_frame = frame
                new_image.sequence.append(frame)
            processed = self.save_image(new_image)
            await ctx.send(
                file=File(
                    processed, filename=image.split("/")[-1].split(".")[0] + ".gif"
                )
            )

    @commands.command()
    async def sinusoid(
        self,
        ctx: commands.Context,
        image: str,
        frequency: float = 3,
        phase_shift: int = 90,
        amplitude: float = 0.2,
        bias: float = 0.7,
    ):
        """Run a sinusoid function on the image."""
        img = self.get_image(image)
        await self.run_async(
            img.function, "sinusoid", [frequency, phase_shift, amplitude, bias]
        )
        processed = self.save_image(img)
        await ctx.send(file=File(processed, filename=image.split("/")[-1]))

    @commands.command()
    async def charcoal(
        self, ctx: commands.Context, image: str, radius: float = 1.5, sigma: float = 0.5
    ):
        """Emulate a charcoal drawing of an image."""
        img = self.get_image(image)
        await self.run_async(img.charcoal, radius=radius, sigma=sigma)
        processed = self.save_image(img)
        await ctx.send(file=File(processed, filename=image.split("/")[-1]))

