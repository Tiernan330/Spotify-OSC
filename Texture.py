from PIL import Image, ImageDraw, ImageFont
from colorthief import ColorThief
from colorsys import rgb_to_hls, hls_to_rgb


def changeSongName(song):
    W = 414
    H = 896
    addTexts = Image.open("Texture.png")
    if len(song) > 25:
        songName = song[0:25] + "..."
    else:
        songName = song
    clear = addTexts.copy()
    Artist = ImageDraw.Draw(clear)
    myFont = ImageFont.truetype(
        "SpotifyImages//CircularSpotifyText-Black.otf", 22)
    w, h = Artist.textsize(songName, font=myFont)
    Artist.text((26, 582), songName, fill=(255, 255, 255), font=myFont)
    clear.save("Texture.png")
    # addTexts.show()


def adjust_color_lightness(r, g, b, factor):
    h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)


def gradientBackground(album) -> Image:
    w = 414
    h = 896
    dominant_color = album.get_color(quality=1)

    # ------------------------------------------------------------------------------------------------------------------

    if dominant_color[0] < 25 and dominant_color[1] < 25 and dominant_color[2] < 25:
        color2 = adjust_color_lightness(dominant_color[0], dominant_color[1], dominant_color[2], 3)
    else:
        color2 = adjust_color_lightness(dominant_color[0], dominant_color[1], dominant_color[2], .30)
    if dominant_color[0] > 150 and dominant_color[1] > 150 and dominant_color[2] > 150:
        color = adjust_color_lightness(dominant_color[0], dominant_color[1], dominant_color[2], .75)
    else:
        color = dominant_color

    # ------------------------------------------------------------------------------------------------------------------

    def generate_gradient() -> Image:
        """Generate a vertical gradient."""
        base = Image.new('RGB', (w, h), color)
        top = Image.new('RGB', (w, h), color2)
        mask = Image.new('L', (w, h))
        mask_data = []
        for y in range(h):
            mask_data.extend([int(255 * (y / h))] * w)
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        # base = base.save("gradient.png")
        return base

    gradient = generate_gradient()
    return gradient


def changeAlbumArt():
    GetDomColor = ColorThief('album.png')
    W = 414
    H = 896
    backGround = gradientBackground(GetDomColor)
    album = Image.open("album.png")
    albumArt = album.resize((int(album.size[0] * 0.573), int(album.size[1] * 0.573)))
    # gradient = Image.open('gradient.png')
    w, h = albumArt.size

    combined = backGround.copy()
    combined.paste(albumArt, (int((W - w) / 2), 160))
    UI = Image.open("SpotifyImages//UI.png")
    combined.paste(UI, (0, 0), UI)
    color_thief = ColorThief('album.png')
    dominant_color = color_thief.get_color(quality=1)
    if dominant_color[0] < 25 and dominant_color[1] < 25 and dominant_color[2] < 25:
        dominant_color = adjust_color_lightness(dominant_color[0], dominant_color[1], dominant_color[2], 6)
    if dominant_color[0] > 150 and dominant_color[1] > 150 and dominant_color[2] > 150:
        dominant_color = adjust_color_lightness(dominant_color[0], dominant_color[1], dominant_color[2], .60)
    else:
        dominant_color = dominant_color
    lyricsBox = Image.new('RGB', (W, H), dominant_color)
    mask = Image.open("SpotifyImages//lyricsMask.png").convert('L')
    combined.paste(lyricsBox, (0, 0), mask=mask)
    # combined.show()
    combined.save("Texture.png")


def changeArtistName(artist):
    W = 414
    H = 896
    addTexts = Image.open("Texture.png")
    if len(artist) > 35:
        artistName = artist[0:35] + "..."
    else:
        artistName = artist
    Artist = ImageDraw.Draw(addTexts)
    myFont = ImageFont.truetype(
        "SpotifyImages//CircularSpotifyTxT-Book.ttf", 14)
    w, h = Artist.textsize(artistName, font=myFont)
    Artist.text(((W - w) / 2, 72), artistName, fill=(255, 255, 255), font=myFont)
    Artist.text((26, 612), artistName, fill=(255, 255, 255), font=myFont)
    addTexts.save("Texture.png")
    # addTexts.show()


def Button(button):
    backGround = Image.open("Texture.png")
    if button is False:
        combined = backGround.copy()
        UI = Image.open("SpotifyImages//playButton.png")
        combined.paste(UI, (0, 0), UI)
        combined.save("Texture.png")
    if button is True:
        combined = backGround.copy()
        UI = Image.open("SpotifyImages//pauseButton.png")
        combined.paste(UI, (0, 0), UI)
        combined.save("Texture.png")
    else:
        pass


def Shuffle(shuffle):
    backGround = Image.open("Texture.png")
    if shuffle is True:
        combined = backGround.copy()
        UI = Image.open("SpotifyImages//shuffleGreen.png")
        combined.paste(UI, (0, 0), UI)
        combined.save("Texture.png")
    else:
        combined = backGround.copy()
        UI = Image.open("SpotifyImages//shuffleWhite.png")
        combined.paste(UI, (0, 0), UI)
        combined.save("Texture.png")


def repeat(repeat):
    backGround = Image.open("Texture.png")
    if repeat == "off":
        combined = backGround.copy()
        UI = Image.open("SpotifyImages//repeatWhite.png")
        combined.paste(UI, (0, 0), UI)
        combined.save("Texture.png")
    else:
        combined = backGround.copy()
        UI = Image.open("SpotifyImages//repeat Green.png")
        combined.paste(UI, (0, 0), UI)
        combined.save("Texture.png")


def Time(time):
    millis = time * .60

    def convert(mil):
        intTime = int(mil)
        seconds = (intTime / 1000) % 60
        seconds = int(seconds)
        minutes = (intTime / (1000 * 60)) % 60
        minutes = int(minutes)
        return "%d:%d" % (minutes, seconds)

    rightTime = "-" + convert(millis)

    addTexts = Image.open("Texture.png")
    clear = addTexts.copy()
    Artist = ImageDraw.Draw(clear)
    myFont = ImageFont.truetype(
        "SpotifyImages//CircularSpotifyTxT-Book.ttf", 12)
    w, h = Artist.textsize(rightTime, font=myFont)
    Artist.text((363, 670), rightTime, fill=(255, 255, 255), font=myFont)
    clear.save("Texture.png")

    millis = time * .40
    leftTime = convert(millis)
    addTexts = Image.open("Texture.png")
    clear = addTexts.copy()
    Artist = ImageDraw.Draw(clear)
    myFont = ImageFont.truetype(
        "SpotifyImages//CircularSpotifyTxT-Book.ttf", 12)
    w, h = Artist.textsize(leftTime, font=myFont)
    Artist.text((23, 670), leftTime, fill=(255, 255, 255), font=myFont)
    clear.save("Texture.png")


class CreateTexture:

    def __init__(self, songname, artistname, playbutton, shuffle, repeatbutton, time):
        self.songName = songname
        self.artistName = artistname
        self.playButton = playbutton
        self.shuffle = shuffle
        self.repeatButton = repeatbutton
        self.time = time

    def createTexture(self):
        print("Creating texture...")
        print("Creating Background...")
        changeAlbumArt()
        print("Creating Buttons...")
        Button(self.playButton)
        Shuffle(self.shuffle)
        repeat(self.repeatButton)
        print("Getting Time...")
        Time(self.time)
        print("Getting artist and song names...")
        changeArtistName(self.artistName)
        changeSongName(self.songName)
        print("Done!")

