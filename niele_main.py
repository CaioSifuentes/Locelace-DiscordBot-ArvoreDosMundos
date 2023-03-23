import discord
from discord.ext.commands import Bot
import json
import os

with open('config.json') as t:
    configData = json.load(t)

niele_client = Bot(command_prefix=">>", intents=discord.Intents.all())


# Denunciar \/
class ModalDenuncia(discord.ui.Modal):
    def __init__(self, reported_user: str, author_name: str, author_mention: str,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.reported_user = reported_user
        self.author_name = author_name
        self.author_mention = author_mention
        self.add_item(discord.ui.InputText(label="Escreva o motivo da denuncia:", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        # Define os parâmetros da Embed, respectivamente: Denunciador, Denunciado e Motivo da Denuncia.
        embed = discord.Embed(title=f"Usuário Denunciado:", description=self.reported_user)
        embed.set_author(name=f'Reportado por {self.author_name} \n{self.author_mention}')
        embed.add_field(name="Motivo da denuncia:", value=self.children[0].value)

        report_channel = niele_client.get_channel(1027708937316872234)
        await interaction.response.send_message(f"Usuário {self.reported_user} denunciado."
                                                f"\nA denuncia será revisada pelos supervisores adequados.",
                                                ephemeral=True)
        await report_channel.send(embeds=[embed])


@niele_client.slash_command(description='Denuncia um membro do servidor e envia a denúncia à moderação.')
async def denunciar(ctx, user: discord.Member):
    reported_user = user.mention
    reported_user_name = user.name
    author_name = ctx.author.name
    author_mention = ctx.author.mention
    modal = ModalDenuncia(title=f"Denunciar {reported_user_name}",
                          reported_user=reported_user,
                          author_name=author_name,
                          author_mention=author_mention)
    await ctx.send_modal(modal)
# Denunciar /\

for filename in os.listdir("./functions"):
    if filename.endswith(".py") and not filename.startswith("__"):
        niele_client.load_extension(f"functions.{filename[:-3]}")


# Avisa se o Bot está Online.
@niele_client.event
async def on_ready():
    print('\033[33m=' * 15)
    print(f'\033[35m{"Niele chegou!":^15}')
    print('\033[33m=\033[m' * 15)

    report_channel = niele_client.get_channel(1027708937316872234)
    if report_channel is None:
        print("Status: \033[31mCanal de denúncias: NOT FOUND")
    else:
        print("Status: \033[32mCanal de denúncias: OK")


niele_client.run(configData["TOKEN"])
