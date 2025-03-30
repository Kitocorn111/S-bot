import asyncio
import discord
from discord.ext import commands, tasks
import json
import sys
import os
from dotenv import load_dotenv
import re
import logging
import requests
import time
from colorama import Fore, init
import socket

with open('conf.json') as config_file:
    config = json.load(config_file)

init(autoreset=True)

print(Fore.RED + r"""
                   ██████   ██████  ██▓▓█████▄ 
                 ▒██    ▒ ▒██    ▒ ▓██▒▒██▀ ██▌
                 ░ ▓██▄   ░ ▓██▄   ▒██▒░██   █▌
                   ▒   ██▒  ▒   ██▒░██░░▓█▄   ▌
                 ▒██████▒▒▒██████▒▒░██░░▒████▓ 
                 ▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░░▓   ▒▒▓  ▒ 
                 ░ ░▒  ░ ░░ ░▒  ░ ░ ▒ ░ ░ ▒  ▒ 
                 ░  ░  ░  ░  ░  ░   ▒ ░ ░ ░  ░ 
                       ░        ░   ░     ░    
                                        ░       
   
                         discord.gg/ssid 
""")



bot = commands.Bot(command_prefix=config["command_prefix"], help_command=None, intents=discord.Intents.all(), self_bot=True)

@bot.event
async def on_ready():
    print(f'{bot.user.name} we are inside!')

@bot.command()
async def ltc(ctx, price: float):
    await ctx.message.delete()
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
        data = response.json()
        ltc_price = data['litecoin']['usd']
        ltc_amount = price / ltc_price

        await ctx.send(
            f"**🚀 Payment Instructions 🚀**\n"
            f"***🪙 Litecoin Wallet Address:*** `{config['ltc_address']}`\n"
            f"***💵 Total Amount Due:*** `${price}`\n"
            f"***🔄 Equivalent LTC:*** `{ltc_amount:.6f} LTC`\n"
            f"*Please complete your payment and notify me when it's done. Thank you!*"
        )
    except Exception as e:
        await ctx.send(f"🚨 Oops! Something went wrong: {str(e)}")

@bot.command()
async def btc(ctx, price: float):
    await ctx.message.delete()
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        data = response.json()
        btc_price = data['bitcoin']['usd']
        btc_amount = price / btc_price

        await ctx.send(
            f"**🚀 Payment Instructions 🚀**\n"
            f"***₿ Bitcoin Wallet Address:*** `{config['btc_address']}`\n"
            f"***💵 Total Amount Due:*** `${price}`\n"
            f"***🔄 Equivalent BTC:*** `{btc_amount:.6f} BTC`\n"
            f"*Please complete your payment and notify me when it's done. Thank you!*"
        )
    except Exception as e:
        await ctx.send(f"🚨 Oops! Something went wrong: {str(e)}")

@bot.command()
async def eth(ctx, price: float):
    await ctx.message.delete()
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
        data = response.json()
        eth_price = data['ethereum']['usd']
        eth_amount = price / eth_price

        await ctx.send(
            f"**🚀 Payment Instructions 🚀**\n"
            f"***🪙 Ethereum Wallet Address:*** `{config['eth_address']}`\n"
            f"***💵 Total Amount Due:*** `${price}`\n"
            f"***🔄 Equivalent ETH:*** `{eth_amount:.6f} ETH`\n"
            f"*Please complete your payment and notify me when it's done. Thank you!*"
        )
    except Exception as e:
        await ctx.send(f"🚨 Oops! Something went wrong: {str(e)}")


@bot.command()
async def pp(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(f"**# YOUR PAYPAL: {config['paypal_address']} **\n"
                   f"** · Send {arg}$; **\n"
                   f"** · Send SS of Payment and Summary; **\n"
                   f"** · Send From Card = No Refund / Product; **\n"
                   f"** · Only F&F; **\n"
                   f"** · No Notes / No Card **\n")

@bot.command()
async def link(ctx):
    await ctx.message.delete()
    await ctx.send(
        f"**🔗 Useful Links 🔗**\n"
        f"**🌐 Discord Invite:** *<{config['discord_link']}>*\n"
        f"**🛡️ SellAuth Link:** *<{config['sellauth_link']}>*\n"
        f"**💡 Click the links above for easy access!**"
    )

@bot.command()
async def vouch(ctx, member: discord.Member):
    await ctx.message.delete()
    await ctx.send(
        ">>> # PLEASE LEAVE A VOUCH\n\n"
        f"Please leave a vouch for {member.mention} in <#1340429374301798471>\n\n"
        "**+vouch 577209327622946818 LEGIT | Nord VPN Code $3.3 LTC (USD) EACH!!**"
    )  

@bot.command()
async def help(ctx):
    await ctx.message.delete()
    await ctx.send(
        "***The commands are:***\n"
        "```\n"
        "**· .help** - Show all commands\n"
        "**· .ltc <price>** - Show your LTC payment instructions\n"
        "**· .btc <price>** - Show your BTC payment instructions\n"
        "**· .pp <price>** - Show your PayPal payment instructions\n"
        "**· .ex <amount> <±percentage>** - Calculate adjusted amounts (e.g., 10-7%=9.3)\n"
        "**· .sellauth** - Show SellAuth link\n"
        "**· .tos** - Show the Terms of Service\n"
        "**· .clear <number>** - Clear a specified number of messages in the channel/DM\n"
        "**· .bal <addy>** - Show LTC balance, total LTC received, or unconfirmed LTC\n"
        "**· .clone** - Clone the server with all permissions\n"
        "**· .e2u** - Convert Euro to USD\n"
        "**· .u2e** - Convert USD to Euro\n"
        "**· .userinfo <id/@username>** - Show information about a user or ID\n"
        "**· .link** - Show Discord and SellAuth links\n"
        "**· .vouch** - Show the vouch message\n"
        "**· .afk** - Enable AFK auto-reply\n"
        "**· .noafk** - Disable AFK mode\n"
        "**· .ltcpp** - Send a legit message for LTC to PayPal exchange\n"
        "**· .ppltc** - Send a legit message for PayPal to LTC exchange\n"
        "**· .ip <address>** - Lookup IP address or domain info\n"
        "**· .schedule channel/user <id> <HH:MM> <message>** - Schedule a message (India timezone)\n"
        "**· .list_scheduled** - List all scheduled messages\n"
        "**· .cancel_schedule <task_id>** - Cancel a scheduled message\n"
        "**· .edit_schedule <task_id> <HH:MM> <new message>** - Edit a scheduled message\n"
        "```\n"
        "Use these commands responsibly!"
    )


emoji_freccia = "<a:freccia:1287001136729034792>"
emoji_nitro = "<a:nitroboost:1277753224618573958>"
emoji_token = "<a:nitrocool:1285633322604564510>"
emoji_stake = "<:stake:1287337705390211132>"

@bot.command()
async def tos(ctx):
    await ctx.message.delete()
    await ctx.send(
        "```md\n"
        "# 🛡️ Terms of Service – Lunar Store\n\n"
        "## ✅ Code Validity\n"
        "Each purchased code is valid for **730 days (2 years)** from the date of activation.\n\n"
        "## 📧 Account Requirement\n"
        "- **New Customers:** If this is your first time purchasing a code from our store, you need to create a **new N0rdVPN account** to redeem the code.\n"
        "- **Stackable Codes:** You can stack as many codes as you want to extend the duration.\n"
        "- However, if you prefer, you’re free to create a new account for each redemption.\n\n"
        "## 🚫 No Revoke Policy\n"
        "Once activated, the code **will not be revoked or reversed**.\n\n"
        "## ⚠️ No Warranty\n"
        "The product is sold **\"as is\"**, and no refunds or replacements will be issued.\n\n"
        "## ❗ Important\n"
        "Please read the instructions carefully after purchasing to ensure a smooth activation process.\n"
        "## 🔄 The TOS May Be Changed At Any Time\n"
        "- By continuing to use our services, you agree to any changes.\n\n"
        "```"
    )

@bot.command()
async def addy(ctx):
    await ctx.message.delete()
    await ctx.send(f"**🔗 Payment Address**\n"
                   f"**=======================**\n"
                   f"**🌐 Your LTC Address:**\n"
                   f"```{config['ltc_address']}```\n"
                   f"**💰 Ensure to double-check the address before sending!**\n"
                   f"**=======================**")



@bot.command()
async def ip(ctx, target: str):
    await ctx.message.delete()

    def is_valid_ip(ip):
        pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
        return pattern.match(ip)

    if is_valid_ip(target):
        ip_address = target
    else:
        try:
            ip_address = socket.gethostbyname(target)
        except socket.gaierror:
            await ctx.send(f"**🚫 Invalid IP Address or Domain: {target}**")
            return

    api_key = config['vpnapi_key']
    url = f"https://vpnapi.io/api/{ip_address}?key={api_key}"
    response = requests.get(url)
    data = response.json()

    ip_info = data.get("ip", "Unknown")
    country = data.get("location", {}).get("country", "Unknown")
    region = data.get("location", {}).get("region", "Unknown")
    city = data.get("location", {}).get("city", "Unknown")
    timezone = data.get("location", {}).get("time_zone", "N/A")

    vpn_detected = "🟢 Yes" if data.get("security", {}).get("vpn", False) else "🚫 No"
    proxy_detected = "🟢 Yes" if data.get("security", {}).get("proxy", False) else "🚫 No"

    zip_code = data.get("location", {}).get("postal_code", "N/A")
    isp = data.get("network", {}).get("autonomous_system_organization", "N/A")

    if zip_code == "N/A" or isp == "N/A":
        previous_api_url = f"http://ip-api.com/json/{ip_address}"
        previous_response = requests.get(previous_api_url)
        previous_data = previous_response.json()

        if previous_data['status'] == 'success':
            if zip_code == "N/A":
                zip_code = previous_data.get("zip", "N/A")
            if isp == "N/A":
                isp = previous_data.get("isp", "N/A")

    await ctx.send(f"**🔍 IP Lookup Results**\n"
                   f"**=======================**\n"
                   f"**🌍 IP Address:** `{ip_info}`\n"
                   f"**🏳 Country:** {country}\n"
                   f"**🏙 City:** {city}\n"
                   f"**📍 Region:** {region}\n"
                   f"**📦 ZIP Code:** {zip_code}\n"
                   f"**📶 ISP:** {isp}\n"
                   f"**🕒 Timezone:** {timezone}\n"
                   f"**🔒 VPN Detected:** {vpn_detected}\n"
                   f"**🛡️ Proxy Detected:** {proxy_detected}\n"
                   f"**=======================**")


@bot.command()
async def svouch(ctx):
    await ctx.send("**Vouch Here: channel**")
    await ctx.message.delete()    

@bot.command()
async def e2u(ctx, euro: float):
    """Converting Euro > USD."""
    response = requests.get('https://api.exchangerate-api.com/v4/latest/EUR')
    
    if response.status_code == 200:
        data = response.json()
        rate = data['rates']['USD']
        usd = euro * rate
        await ctx.send(f"{euro}€ = {usd:.2f}$.")
    else:
        await ctx.send("Error.")

@bot.command()
async def u2e(ctx, usd: float):
    """Converting USD > Euro."""
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    
    if response.status_code == 200:
        data = response.json()
        rate = data['rates']['EUR']
        euro = usd * rate 
        await ctx.send(f"{usd}$ = {euro:.2f}€.")
    else:
        await ctx.send("Error fetching exchange rate.")        

@bot.command()
async def clear(ctx, amount: int):
    """Delete a specified number of messages."""
    if ctx.guild:
        if not ctx.author.guild_permissions.manage_messages:
            return await ctx.send("You do not have permission to manage messages.")
    
    if amount < 1:
        return await ctx.send("You must specify a number greater than 0.")
    
    if ctx.guild:
        deleted = await ctx.channel.purge(limit=amount)
        await ctx.send(f"Deleted {len(deleted)} messages.", delete_after=5)
    else:
        async for message in ctx.channel.history(limit=amount + 1):
            if message.author == bot.user:
                await message.delete()
        
        await ctx.send(f"Deleted your last **{amount}** messagges.", delete_after=2.5)


@bot.command()
async def clone(ctx, source_guild_id: int, target_guild_id: int):
    source_guild = bot.get_guild(source_guild_id)
    target_guild = bot.get_guild(target_guild_id)

    if not source_guild or not target_guild:
        await ctx.send("** One of the servers could not be found. Check the IDs. **")
        return

    try:
        # Clonar roles
        for role in source_guild.roles:
            if role.is_default():
                continue
            await target_guild.create_role(
                name=role.name,
                permissions=role.permissions,
                colour=role.colour,
                hoist=role.hoist,
                mentionable=role.mentionable
            )
            await asyncio.sleep(1)  # Pausa de 1 segundo para evitar rate limit
        await ctx.send("** Roles copied successfully! **")
    except Exception as e:
        await ctx.send(f"** Error copying roles: {e} **")

    try:
        # Crear mapeo de roles
        role_mapping = {role.name: role for role in target_guild.roles}

        # Clonar categorías y canales
        for category in source_guild.categories:
            new_category = await target_guild.create_category(name=category.name, position=category.position)

            for channel in category.channels:
                overwrites = {
                    role_mapping.get(overwrite[0].name, target_guild.default_role): overwrite[1]
                    for overwrite in channel.overwrites.items()
                }

                if isinstance(channel, discord.TextChannel):
                    await new_category.create_text_channel(
                        name=channel.name,
                        topic=channel.topic,
                        position=channel.position,
                        overwrites=overwrites
                    )
                elif isinstance(channel, discord.VoiceChannel):
                    await new_category.create_voice_channel(
                        name=channel.name,
                        position=channel.position,
                        overwrites=overwrites
                    )
                await asyncio.sleep(1)  # Pausa para evitar rate limit
        await ctx.send("** Channels and categories successfully copied, including permissions! **")
    except Exception as e:
        await ctx.send(f"** Error copying channels: {e} **")

def get_ltc_balance_in_eur(address):
    balance_url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"
    balance_response = requests.get(balance_url).json()
    
    if "error" in balance_response:
        return f"Error: {balance_response['error']}"
    
    current_balance_ltc = balance_response['balance'] / 1e8
    total_received_ltc = balance_response['total_received'] / 1e8
    unconfirmed_balance_ltc = balance_response['unconfirmed_balance'] / 1e8

    exchange_url = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=eur"
    exchange_response = requests.get(exchange_url).json()
    ltc_to_eur_rate = exchange_response['litecoin']['eur']

    current_balance_eur = current_balance_ltc * ltc_to_eur_rate
    total_received_eur = total_received_ltc * ltc_to_eur_rate
    unconfirmed_balance_eur = unconfirmed_balance_ltc * ltc_to_eur_rate

    return (
        f"Address: `{address}`\n"
        f"Current LTC Balance:** {current_balance_eur:.2f}** €\n"
        f"Total LTC Received:** {total_received_eur:.2f}** €\n"
        f"Unconfirmed LTC:** {unconfirmed_balance_eur:.2f}** €\n"
    )

@bot.command()
async def bal(ctx, address: str):
    result = get_ltc_balance_in_eur(address)
    await ctx.send(result)

@bot.command()
async def delchannels(ctx):
    await ctx.message.delete()
    deleted_channels = 0
    failed_deletions = 0
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            deleted_channels += 1
        except Exception as e:
            failed_deletions += 1
            await ctx.send(f"[ERROR]: Failed to delete channel {channel.name} - {e}")
    await ctx.send(
        f"✅ **Deletion Complete**: {deleted_channels} channels deleted.\n"
        f"⚠️ **Failed Deletions**: {failed_deletions} channels could not be deleted."
    )

@bot.command()
async def sellauth(ctx):
    await ctx.message.delete()
    await ctx.send(f"# ** · [Sellauth Link]({config['sellauth_link']}) ** #")      

def calculate_subtraction(amount: int, percentage: float) -> float:
    return amount - (amount * abs(percentage) / 100)

@bot.command(name="ex")
async def ex(ctx, *, input_str: str):
    await ctx.message.delete()
    try:
        match = re.match(r"(\d+(?:\.\d+)?)\s*([-+])\s*(-?\d+(?:\.\d+)?)%", input_str)
        
        if match:
            amount = float(match.group(1))
            operator = match.group(2)
            percentage_value = float(match.group(3))
            
            if operator == "+":
                new_amount = amount + (amount * percentage_value / 100)
            else:
                new_amount = amount - (amount * percentage_value / 100)
            
            await ctx.send(f"# {new_amount:.2f} # ")
        else:
            await ctx.send("`Error: Please use the correct format. (Ex: .exch x±x% o .exch x ± x%)`")
    
    except ValueError:
        await ctx.send("`Error: Make sure the amount is a valid number and the percentage is valid (es: ±10%).`")

@bot.command()
async def userinfo(ctx, user: discord.User = None):
    await ctx.message.delete()
    if user is None:
        await ctx.send("`Please specify a user using an ID or tag.`")
        return

    try:
        creation_date = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        avatar_url = user.avatar_url if user.avatar else "**` No avatar set `**"

        response = (
            f"** · ID: {user.id} ## **\n"
            f"** · Username: {user.name} ## **\n" 
            f"** · Account Creation Date: {creation_date} ## **\n"
            f"** · Avatar: [Avatar]({avatar_url}) ## **\n"
        )

        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")          

last_responded = {}

RESPONSE_TIMEOUT = 30
bot.auto_respond_dm_enabled = False

@bot.command()
async def afk(ctx):
    bot.auto_respond_dm_enabled = True
    await ctx.send("** # AFK Enabled!**")
    await ctx.message.delete()

@bot.command()
async def noafk(ctx):
    bot.auto_respond_dm_enabled = False
    await ctx.send("** # AFK Disabled!**")
    await ctx.message.delete()

def should_respond(user_id):
    current_time = time.time()
    if user_id in last_responded:
        last_time = last_responded[user_id]
        if current_time - last_time < RESPONSE_TIMEOUT:
            return False
    last_responded[user_id] = current_time
    return True

@bot.event
async def on_message(message):
    if bot.auto_respond_dm_enabled and message.author != bot.user:
        if message.guild is None and should_respond(message.author.id):
            await message.channel.send(config['afk_message'])
        elif message.guild is not None and bot.user in message.mentions and should_respond(message.author.id):
            await message.channel.send(f"** # Hi {message.author.mention}, {config['afk_message']}**")
    await bot.process_commands(message)

import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Global counter for scheduled messages (sequential IDs)
schedule_counter = 0

# Dictionary to store scheduled tasks.
# Key: sequential ID (as string); Value: task info.
scheduled_tasks = {}

@bot.command()
async def schedule(ctx, target_type: str, target_id: int, schedule_time: str, *, content: str):
    """
    Schedules a message to be sent at a specific time (HH:MM 24-hour format, India timezone).
    
    Usage:
      .schedule channel 123456789012345678 16:32 Your message here.
      .schedule user 987654321098765432 09:15 Your DM message here.
    """
    await ctx.message.delete()
    
    global schedule_counter
    schedule_counter += 1
    custom_id = str(schedule_counter)
    
    # Get current time in India Standard Time (GMT+5:30)
    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    try:
        # Expect time format "HH:MM"
        target_time = datetime.strptime(schedule_time, "%H:%M")
        # Set target_time to today's date with given time
        target_time = now.replace(hour=target_time.hour, minute=target_time.minute, second=0, microsecond=0)
        # If the time has already passed, schedule for tomorrow.
        if target_time < now:
            target_time += timedelta(days=1)
        delay = (target_time - now).total_seconds()
    except Exception as e:
        await ctx.send("**[Error]** Invalid time format. Please use HH:MM (24-hour format).")
        return

    async def send_scheduled_message():
        try:
            await asyncio.sleep(delay)
            if target_type.lower() == "channel":
                channel = bot.get_channel(target_id)
                if channel:
                    await channel.send(content)
            elif target_type.lower() == "user":
                user = bot.get_user(target_id)
                if user:
                    await user.send(content)
        except asyncio.CancelledError:
            return
        finally:
            scheduled_tasks.pop(custom_id, None)

    task = asyncio.create_task(send_scheduled_message())
    scheduled_tasks[custom_id] = {
        "task": task,
        "target_type": target_type.lower(),
        "target_id": target_id,
        "schedule_time": target_time.strftime("%Y-%m-%d %H:%M"),
        "content": content
    }
    
    await ctx.send(f"**[Scheduled]** Message scheduled excellently with ID `{custom_id}` to be sent at {target_time.strftime('%H:%M')} India time.")

@bot.command()
async def list_scheduled(ctx):
    """
    Lists all scheduled messages.
    """
    await ctx.message.delete()
    if not scheduled_tasks:
        await ctx.send("There are no scheduled messages.")
        return

    message = "Scheduled Messages:\n"
    for tid, info in scheduled_tasks.items():
        message += (f"ID: `{tid}` | Type: {info['target_type']} | Target ID: {info['target_id']} | "
                    f"Time: {info['schedule_time']} | Content: {info['content']}\n")
    await ctx.send(f"```{message}```")

@bot.command()
async def cancel_schedule(ctx, task_id: str):
    """
    Cancels a scheduled message by its ID.
    
    Usage:
      .cancel_schedule <task_id>
    """
    await ctx.message.delete()
    if task_id in scheduled_tasks:
        scheduled_tasks[task_id]["task"].cancel()
        scheduled_tasks.pop(task_id, None)
        await ctx.send(f"Scheduled message with ID `{task_id}` has been cancelled successfully.")
    else:
        await ctx.send("No scheduled message found with that ID.")

@bot.command()
async def edit_schedule(ctx, task_id: str, new_time: str, *, new_content: str):
    """
    Edits an existing scheduled message by canceling the old task and creating a new one with updated parameters.
    
    Usage:
      .edit_schedule <task_id> <HH:MM> <new message>
    """
    await ctx.message.delete()
    if task_id not in scheduled_tasks:
        await ctx.send("No scheduled message found with that ID.")
        return

    info = scheduled_tasks[task_id]
    # Cancel the old task.
    info["task"].cancel()

    target_type = info["target_type"]
    target_id = info["target_id"]

    now = datetime.now(ZoneInfo("Asia/Kolkata"))
    try:
        new_target_time = datetime.strptime(new_time, "%H:%M")
        new_target_time = now.replace(hour=new_target_time.hour, minute=new_target_time.minute, second=0, microsecond=0)
        if new_target_time < now:
            new_target_time += timedelta(days=1)
        delay = (new_target_time - now).total_seconds()
    except Exception as e:
        await ctx.send("**[Error]** Invalid time format. Please use HH:MM (24-hour format).")
        return

    async def send_new_message():
        try:
            await asyncio.sleep(delay)
            if target_type.lower() == "channel":
                channel = bot.get_channel(target_id)
                if channel:
                    await channel.send(new_content)
            elif target_type.lower() == "user":
                user = bot.get_user(target_id)
                if user:
                    await user.send(new_content)
        except asyncio.CancelledError:
            return
        finally:
            scheduled_tasks.pop(task_id, None)

    new_task = asyncio.create_task(send_new_message())
    scheduled_tasks[task_id] = {
        "task": new_task,
        "target_type": target_type.lower(),
        "target_id": target_id,
        "schedule_time": new_target_time.strftime("%Y-%m-%d %H:%M"),
        "content": new_content
    }
    
    await ctx.send(f"Scheduled message with ID `{task_id}` has been updated successfully to be sent at {new_target_time.strftime('%H:%M')} India time.")

bot.run(config["token"], bot=False)