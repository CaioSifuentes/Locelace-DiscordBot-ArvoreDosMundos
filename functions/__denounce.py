import discord
from discord.ext import commands


class ModalDenuncia(discord.ui.Modal):
    def __init__(self, reported_user: str, author_name: str, author_mention: str, client: commands.Cog,
                 *args, **kwargs):
        super().__init__(client, *args, **kwargs)

        self.client = client
        self.reported_user = reported_user
        self.author_name = author_name
        self.author_mention = author_mention
        self.add_item(discord.ui.InputText(label="Escreva o motivo da denuncia:", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        # Define os parâmetros da Embed, respectivamente: Denunciador, Denunciado e Motivo da Denuncia.
        embed = discord.Embed(title=f"Usuário Denunciado:", description=self.reported_user)
        embed.set_author(name=f'Reportado por {self.author_name} \n{self.author_mention}')
        embed.add_field(name="Motivo da denuncia:", value=self.children[0].value)

        report_channel = self.bot.get_channel(1027708937316872234)
        await interaction.response.send_message(f"Usuário {self.reported_user} denunciado."
                                                f"\nA denuncia será revisada pelos supervisores adequados.",
                                                ephemeral=True)
        await report_channel.send(embeds=[embed])


class DenunciaCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Denuncia um membro do servidor e envia a denúncia à moderação.')
    async def denunciar(self, ctx, user: discord.Member):
        reported_user = user.mention
        reported_user_name = user.name
        author_name = ctx.author.name
        author_mention = ctx.author.mention
        modal = ModalDenuncia(title=f"Denunciar {reported_user_name}",
                              reported_user=reported_user,
                              author_name=author_name,
                              author_mention=author_mention)
        await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(DenunciaCommands(bot))
