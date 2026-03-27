import discord
from discord.ext import commands
import os
from datetime import timedelta
from dotenv import load_dotenv
import random

load_dotenv('disckey.env')
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

playerlist = []
current_imposter = None
poll_message_id = None
poll_channel_id = None

worddict = {
    "Objects": ["book", "chair", "table", "phone", "laptop", "pen", "cup", "bottle", "key", "wallet"],
    "Animals": ["cat", "dog", "bird", "fish", "lion", "tiger", "elephant", "giraffe", "monkey", "bear"],
    "Celebrity": ["Taylor Swift", "Ed Sheeran", "Ariana Grande", "Justin Bieber", "Beyoncé", "Rihanna", "Bruno Mars", "Lady Gaga", "Drake", "Adele"]
}

@bot.tree.command(name="join_game", description="Join the game of imposter!")
async def join_game(interaction: discord.Interaction):
    if len(playerlist) >= 5:
        await interaction.response.send_message("The game is full! Maximum 5 players allowed.")
    elif interaction.user not in playerlist:
        playerlist.append(interaction.user)
        await interaction.response.send_message(f"{interaction.user.name} has joined the game!")
    else:
        await interaction.response.send_message(f"{interaction.user.name} is already in the game!")

@bot.tree.command(name="leave_game", description="Leave the game of imposter!")
async def leave_game(interaction: discord.Interaction):
    if interaction.user in playerlist:
        playerlist.remove(interaction.user)
        await interaction.response.send_message(f"{interaction.user.name} has left the game!")
    else:
        await interaction.response.send_message(f"{interaction.user.name} is not in the game!")

@bot.tree.command(name="list_players", description="List all players in the game!")
async def list_players(interaction: discord.Interaction):
    if not playerlist:
        await interaction.response.send_message("No players have joined the game yet!")
        return
    entries = "\n".join([f"**{i+1}.** {user.display_name}" for i, user in enumerate(playerlist)])
    embed = discord.Embed(title="📋 Player List", description=entries, color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="start_game", description="Start the game of imposter!")
async def start_game(interaction: discord.Interaction):
    global current_imposter, poll_message_id, poll_channel_id

    if len(playerlist) < 2:
        await interaction.response.send_message("Need at least 2 players to start!")
        return

    current_imposter = random.choice(playerlist)
    category = random.choice(list(worddict.keys()))
    word = random.choice(worddict[category])

    failed = []
    for player in playerlist:
        try:
            if player == current_imposter:
                await player.send("🔪 You are the **IMPOSTER!** Try to blend in! You do NOT know the word!")
            else:
                await player.send(f"✅ You are a **CREWMATE!** The category is **{category}** and the word is **{word}**!")
        except discord.Forbidden:
            failed.append(player.display_name)

    msg = f"🎮 Game started! The category is: **{category}**! Check your DMs for your role!"
    if failed:
        msg += f"\n⚠️ Couldn't DM: {', '.join(failed)}"
    await interaction.response.send_message(msg)

    # Create and send the poll, save the message ID
    poll = discord.Poll(
        question="🕵️ Who is the imposter?",
        duration=timedelta(hours=1),
        multiple=False
    )
    for player in playerlist:
        poll.add_answer(text=player.display_name)

    poll_message = await interaction.channel.send(poll=poll)
    poll_message_id = poll_message.id        # save message ID
    poll_channel_id = interaction.channel.id  # save channel ID

@bot.tree.command(name="end_game", description="End the game and reveal the results!")
async def end_game(interaction: discord.Interaction):
    global current_imposter, poll_message_id, poll_channel_id

    if current_imposter is None:
        await interaction.response.send_message("No game is running!", ephemeral=True)
        return

    if poll_message_id is None:
        await interaction.response.send_message("No poll found! Has the game started?", ephemeral=True)
        return

    # Fetch the poll message
    try:
        channel = bot.get_channel(poll_channel_id)
        message = await channel.fetch_message(poll_message_id)
    except:
        await interaction.response.send_message("Couldn't find the poll message!", ephemeral=True)
        return

    # Get poll answers and vote counts
    poll_data = message.poll
    if not poll_data:
        await interaction.response.send_message("No poll data found!", ephemeral=True)
        return

    # Find the answer with the most votes
    most_voted_answer = max(poll_data.answers, key=lambda a: a.vote_count)
    most_voted_name = most_voted_answer.text

    # Build results string
    results = "\n".join([f"**{a.text}** — {a.vote_count} votes" for a in poll_data.answers])

    # Compare to actual imposter
    if most_voted_name == current_imposter.display_name:
        outcome = f"✅ Correct! **{most_voted_name}** was the imposter!  **{current_imposter.display_name}** has lost! 🎉"
    else:
        outcome = f"❌ Wrong! **{most_voted_name}** was voted out but was innocent!\nThe real imposter was **{current_imposter.display_name}**! Imposter wins! 🔪"

    embed = discord.Embed(title="🗳️ Game Results", description=f"{results}\n\n{outcome}", color=discord.Color.gold())
    await interaction.response.send_message(embed=embed)

    # Reset everything
    playerlist.clear()
    current_imposter = None
    poll_message_id = None
    poll_channel_id = None





@bot.event
async def on_ready():
    guild = discord.Object(id=xx)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"Logged in as {bot.user} and commands synced!")

bot.run(token)