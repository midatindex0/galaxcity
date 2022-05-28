import discord, aiohttp
from discord.ext import commands

class Info(commands.Cog):
    """A COG TO GET INFORMATION ABOUT SPACE AND SPACE STATION"""
    def __init__(self,bot:commands.Bot):
        self.bot=bot
    
    @commands.command(name="locate",aliases=["iss"],help="Get the location of the ISS")
    async def locate(self,ctx):
        """
        GET THE LOCATION OF THE ISS
        """
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.wheretheiss.at/v1/satellites/25544') as response:
                json = await response.json()
        lat=json["latitude"]
        lon=json["longitude"]
        zoom="3"

        url=f"https://static-maps.yandex.ru/1.x/?z={zoom}&lang=en_US&ll={lon},{lat}&size=450,450&l=sat,trf,skl&pt={lon},{lat},vkbkm"
        em=discord.Embed(
            description="Current Location of the ISS",
            color=discord.Color.random(),
            timestamp=ctx.message.created_at
        ).add_field(
            name="Latitude",
            value=json["latitude"],
            inline=False
        ).add_field(
            name="Longitude",
            value=json["longitude"],
            inline=False
        ).add_field(
            name="Altitude",
            value=str(json["altitude"])+" km",
            inline=False
        ).add_field(
            name="Velocity",
            value=str(json["velocity"])+" km/h",
            inline=False
        ).add_field(
            name="Visibility",
            value=json["visibility"],
            inline=False
        ).set_thumbnail(
            url="https://www.nasa.gov/sites/default/files/thumbnails/image/nasa-logo-web-rgb.png"
        ).set_image(
            url="http://www.nasa.gov/sites/default/files/thumbnails/image/final_configuration_of_iss.jpg"
        ).set_image(
            url=url
        )
        await ctx.send(embed=em)
        
    @commands.command(name="picture-of-the-day",aliases=["potd"],help="Get the picture of the day for NASA")
    async def potd(self,ctx):
        """GET THE PICTURE OF THE DAY FOR NASA """
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.nasa.gov/planetary/apod?api_key=1VPdcmokG1qNJ7wv3VC2H8SQS48OXfytFBtEnRkC') as response:
                json = await response.json()
            em=discord.Embed(
                description="Picture of the Day",
                color=discord.Color.random(),
                timestamp=ctx.message.created_at
            ).add_field(
                name="Title",
                value=json["title"],
                inline=False
            ).add_field(
                name="Date",
                value=json["date"],
                inline=False
            ).add_field(
                name="Explanation",
                value=json["explanation"],
                inline=False
            ).add_field(
                name="URL",
                value=f"[click here]({json['url']})",
                inline=False
            ).set_image(
                url=json["url"]
            ).set_thumbnail(
                url="https://www.nasa.gov/sites/default/files/thumbnails/image/nasa-logo-web-rgb.png"
            )
            await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Info(bot))