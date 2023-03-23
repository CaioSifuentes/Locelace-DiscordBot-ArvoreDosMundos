import discord
from discord.ext import commands


class RecompensaT20(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    nd_lista = []
    for nd in range(1, 21):
        nd_lista.append(nd)

    @commands.slash_command(description='Gera uma recompensa de missão para T20.')
    async def recompensa_t20(self, interaction: discord.Interaction,
                             nd: discord.Option(int, choices=nd_lista),
                             porcentagem: int):
        d_recompensa_t20 = {
            1: [250, 50],
            2: [500, 75],
            3: [750, 100],
            4: [1000, 250],
            5: [1250, 375],
            6: [1500, 500],
            7: [1750, 625],
            8: [2000, 750],
            9: [2250, 1000],
            10: [2500, 1500],
            11: [2750, 2000],
            12: [3000, 2500],
            13: [3250, 3250],
            14: [3500, 4250],
            15: [3750, 5500],
            16: [4000, 7750],
            17: [4250, 10000],
            18: [4500, 12500],
            19: [4750, 15000],
            20: [5000, 18000]
        }

        tibares_total = int(d_recompensa_t20[nd][1] * (porcentagem + 100) / 100)
        experiencia_total = int(d_recompensa_t20[nd][0] * (porcentagem + 100) / 100)
        await interaction.response.send_message(f'```(ND{nd}+{porcentagem}%/{experiencia_total}XP{tibares_total}T$)```')


def setup(bot: commands.Bot):
    bot.add_cog(RecompensaT20(bot))
