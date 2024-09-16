import discord
import requests
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

API_URL = "http://localhost:5000"
API_KEY = "idan"

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

@bot.tree.command(name="generate_license", description="Generate a new license key.")
async def generate_license(interaction: discord.Interaction, admin: str, resource_name: str):
    response = requests.post(
        f"{API_URL}/generate_license",
        json={"admin": admin, "resource_name": resource_name},
        headers={"x-api-key": API_KEY}
    )

    if response.status_code == 200:
        data = response.json()
        await interaction.response.send_message(
            f"License generated successfully: **{data['license_key']}**\n"
            f"PowerShell Output: {data['powershell_output']['output']}"
        )
    else:
        await interaction.response.send_message("Failed to generate license: " + response.json().get("message", "Unknown error."))

@bot.tree.command(name="check_license", description="Check the validity of a license key.")
async def check_license(interaction: discord.Interaction, license_key: str):
    response = requests.post(
        f"{API_URL}/check_license",
        json={"license_key": license_key},
        headers={"x-api-key": API_KEY}
    )

    if response.status_code == 200:
        data = response.json()
        if data["valid"]:
            await interaction.response.send_message("License is valid.")
        else:
            await interaction.response.send_message("License is invalid.")
    else:
        await interaction.response.send_message("Failed to check license: " + response.json().get("message", "Unknown error."))


@bot.tree.command(name="remove_license", description="Remove a license key")
async def check_license(interaction: discord.Interaction, license_key: str):
    response = requests.post(
        f"{API_URL}/remove_license",
        json={"license_key": license_key},
        headers={"x-api-key": API_KEY}
    )

    if response.status_code == 200:
        data = response.json()
        await interaction.response.send_message("License Removed.")
    else:
        await interaction.response.send_message("Failed to remove license: " + response.json().get("message", "Unknown error."))

@bot.tree.command(name="list_licenses", description="List all licenses.")
async def list_licenses(interaction: discord.Interaction):
    response = requests.get(
        f"{API_URL}/list_licenses",
        headers={"x-api-key": API_KEY}
    )

    if response.status_code == 200:
        data = response.json()
        if data["licenses"]:
            licenses_list = "\n".join([f"{license['license_key']} - {license['resource_name']}" for license in data["licenses"]])
            await interaction.response.send_message(f"List of licenses:\n{licenses_list}")
        else:
            await interaction.response.send_message("No licenses found.")
    else:
        await interaction.response.send_message("Failed to retrieve licenses: " + response.json().get("message", "Unknown error."))


bot.run('')