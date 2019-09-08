import io
import os
from functools import partial
import random

os.environ["MAGICK_HOME"] = "/usr/lib"

import requests
from discord import File
from discord.ext import commands
from wand.image import Image
from wand.color import Color

from Plugin import BorobPlugin


class MagikPlugin(BorobPlugin):
    """Manipulates and destroys images."""

    @staticmethod
    def get_image(image: str) -> Image:
        """Retrieve an image object from a URL."""
        resp = requests.get(image)
        img = Image(file=io.BytesIO(resp.content))
        # img.format = image.split("/")[-1].split(".")[-1].lower()
        return img

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

    async def apply_arcweld(self, img):
        await self.run_async(img.transform, resize="800x800>")

        await self.run_async(img.evaluate, operator="leftshift", value=1, channel="red")

        await self.run_async(img.contrast_stretch, black_point=0.3)

        await self.run_async(
            img.evaluate, operator="thresholdblack", value=0.9, channel="red"
        )

        await self.run_async(img.sharpen)

        await self.run_async(
            img.liquid_rescale,
            width=int(img.width / 2),
            height=int(img.height / 3),
            delta_x=1,
            rigidity=0,
        )

        await self.run_async(
            img.liquid_rescale,
            width=int(img.width * 2),
            height=int(img.height * 3),
            delta_x=0.4,
            rigidity=0,
        )

        await self.run_async(img.implode, amount=0.2)

        await self.run_async(
            img.quantize,
            number_colors=8,
            colorspace_type="rgb",
            treedepth=0,
            dither=True,
            measure_error=False,
        )

    @commands.command()
    async def arcweld(self, ctx: commands.Context, image: str, iterations: int = 1):
        """Arc weld a given image."""
        img = self.get_image(image)

        for i in range(iterations):
            if img.sequence is not None:
                new_img = Image()
                for frame in img.sequence:
                    await self.apply_arcweld(frame)
                    new_img.sequence.append(frame)
                img = new_img
            else:
                await self.apply_arcweld(img)

        await ctx.send(file=File(self.save_image(img), filename=image.split("/")[-1]))
