from jigsaw import JigsawPlugin

from discord.ext.commands import Cog


class BorobPlugin(JigsawPlugin, Cog):

    def __init__(self, manifest, bot):
        JigsawPlugin.__init__(self, manifest)
        Cog.__init__(self)
        self.bot = bot

    def enable(self):
        self.bot.add_cog(self)