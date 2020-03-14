import discord
from secrets import DISCORD_KEY, CHROME_DRIVER_PATH
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException 
import time
import PySimpleGUI as sg

bot = commands.Bot(command_prefix = 'so.')

@bot.event
async def on_ready():
	await bot.wait_until_ready()
	print('Bot is ready.')

@bot.command()
async def q(ctx, *, question):
    await ctx.send("Searching..")
    try:
        result = []
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        path = CHROME_DRIVER_PATH
        chrome_driver = path
        driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
        driver.get("http://www.google.com"); 
        element = driver.find_element_by_name("q")
        element.send_keys("StackOverflow " + question);
        element.submit();
        time.sleep(1.5)
        r_class = driver.find_elements_by_class_name('r')
        link = r_class[0].find_element_by_tag_name('a')
        link.click()
        time.sleep(1.5)
        answer_cell = driver.find_element_by_class_name("answercell")

        code_tags = answer_cell.find_elements_by_tag_name("code")
        for tag in code_tags:
            result.append(tag.text)

    except NoSuchElementException:
        result.append("Could not find anything with this query.")

    result = " \n".join(result)
    

    await ctx.send(f'{question}:')
    if (result == ''):
    	await ctx.send("Cannot find anything with this query.")
    elif (len(result)  > 1990):
    	result = result[:1990]
    	print(result)
    await ctx.send(f'```{result}```')

@bot.command()
async def close(ctx):
	await ctx.send("Closing")
	await bot.logout()

key = DISCORD_KEY
bot.run(key)