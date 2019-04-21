import io
import os

os.environ["MAGICK_HOME"] = "/usr/lib"

import requests
from discord import File
from discord.ext import commands
from wand.image import Image

from Plugin import BorobPlugin


class MagikPlugin(BorobPlugin):
    """Manipulates and destroys images."""

    @staticmethod
    def get_image(image: str) -> Image:
        """Retrieve an image object from a URL."""
        resp = requests.get(image)
        img = Image(file=io.BytesIO(resp.content))
        img.format = image.split("/")[-1].split(".")[-1].lower()
        return img
    
    @staticmethod
    def save_image(image: Image) -> io.BytesIO:
        """Save an image to a file-like object."""
        processed = io.BytesIO()
        image.save(file=processed)
        processed.seek(0)
        return processed

    @commands.command()
    async def magik(self, ctx: commands.Context, image: str, scale: float = None, destwidth: int = None, destheight: int = None):
        """Performs a magik destruction on an image."""
        img = self.get_image(image)
        img.transform(resize='800x800>')
        if not destwidth:
            destwidth = int(img.width * 0.5)
        if not destheight:
            destheight = int(img.height * 0.5)
        original_width = img.width
        original_height = img.height
        img.liquid_rescale(width=destwidth, height=destheight, delta_x=scale if scale else 1, rigidity=0)
        img.transform(resize=f'{original_width}x{original_height}!')
        processed = self.save_image(img)
        await ctx.send(file=File(processed, filename=image.split("/")[-1]))

    @commands.command()
    async def sinusoid(self, ctx: commands.Context, image: str, frequency: float = 3, phase_shift: int = 90, amplitude: float = 0.2, bias: float = 0.7):
        """Run a sinusoid function on the image."""
        img = self.get_image(image)
        img.function('sinusoid', [frequency, phase_shift, amplitude, bias])
        processed = self.save_image(img)
        await ctx.send(file=File(processed, filename=image.split("/")[-1]))

    @commands.command()
    async def charcoal(self, ctx: commands.Context, image: str, radius: float = 1.5, sigma: float = 0.5):
        """Emulate a charcoal drawing of an image."""
        img = self.get_image(image)
        img.charcoal(radius=radius, sigma=sigma)
        processed = self.save_image(img)
        await ctx.send(file=File(processed, filename=image.split("/")[-1]))
