import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import json
from db import criar_usuario
from db import pegar_usuario
from db import pegar_dinheiro

load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print("Iniciado")


@bot.command()
async def ola(ctx:discord.Message):
    await ctx.reply(f"ola {ctx.author.mention}")

@bot.command()
async def moeda(ctx):
    user_id = str(ctx.author.id)
    file_path = 'dados.json'

    if not os.path.exists(file_path):
        await ctx.send("O sistema de níveis não foi inicializado.")
        return
    
    with open(file_path, 'r') as f:
        users = json.load(f)

    # 3. Pega o nível se o usuário existir, senão define nível 1
    if user_id in users:
        nivel = users[user_id]['nivel']
        xp = users[user_id]['xp']
        dinheiro = users[user_id]['dinheiro']
        await ctx.send(f"{ctx.author.mention}, você está no nível {nivel} com {xp} XP e com {dinheiro} moedas!")
    else:
        await ctx.send(f"{ctx.author.mention}, você ainda não tem um nível. Converse mais!")


@bot.command()
async def register(ctx):

    usuario = pegar_usuario(ctx.author.id)

    if usuario:

        await ctx.send(
            "Você já possui cadastro."
        )

        return


    await ctx.send(
        "Qual seu nickname?"
    )


    def check(m):

        return (
            m.author == ctx.author
            and m.channel == ctx.channel
        )


    resposta_nome = await bot.wait_for(
        "message",
        check=check
    )

    nome = resposta_nome.content



    criar_usuario(
        ctx.author.id,
        nome,
    )


    await ctx.send(
        f"Cadastro criado com sucesso, {nome}!"
    )

@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    
    autor_id = ctx.author.id

    usuario = pegar_usuario(autor_id)
    if not usuario:
        await ctx.send("Usuário não cadastrado.")
        return
    
    # 'money' vai receber apenas o número (ex: 100)
    money = pegar_dinheiro(autor_id)
    
    # A mensagem vai exibir apenas o número puro dentro das crases
    await ctx.send(f"💰 **|** {ctx.author.mention}, você resgatou suas moedas! Seu saldo atual é: `{money}`")



TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)