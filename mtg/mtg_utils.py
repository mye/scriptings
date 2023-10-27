from datetime import datetime, timedelta
from io import BytesIO

import pandas as pd
import requests
from diskcache import Cache
from PIL import Image, ImageDraw, ImageFont

cache = Cache("data/cache")

METAGAME_URL = "https://www.17lands.com/card_evaluation_metagame/data"
MTG_EXPANSION = "WOE"
MTG_FORMAT = "PremierDraft"
MTG_RARITIES = ["common", "uncommon", "rare", "mythic"]
MTG_COLORS = ["Multicolor", "White", "Blue", "Black", "Red", "Green", "Colorless"]

headers = {
    "Accept": "application/json",
    "Referer": "https://www.17lands.com/card_evaluation_metagame",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}


@cache.memoize()
def get_border_crop(card_name) -> Image:
    url = (
        f"https://api.scryfall.com/cards/named?exact={requests.utils.quote(card_name)}"
    )
    card_object = requests.get(url).json()
    img = requests.get(card_object["image_uris"]["border_crop"])
    img = Image.open(BytesIO(img.content))
    return img


class NoALSAError(Exception):
    def __init__(self, rarity, color):
        self.rarity = rarity
        self.color = color

    def __str__(self):
        return f"No ALSA available for {self.rarity} {self.color}."


def request_alsa(
    rarity, color, expansion=MTG_EXPANSION, format=MTG_FORMAT
) -> pd.DataFrame:
    yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    url = (
        f"{METAGAME_URL}?expansion={expansion}&format={format}"
        f"&rarity={rarity}&color={color}"
        f"&start_date={yesterday}&end_date={yesterday}"
    )
    response = requests.get(url, headers=headers)
    data = response.json()
    try:
        cards = data["cards"]
        pick_avg = data["data"][yesterday]
        cards_df = pd.DataFrame.from_dict(cards, orient="index")
        pick_df = pd.DataFrame.from_dict(pick_avg, orient="index")
        df = cards_df.join(pick_df, lsuffix="_cards", rsuffix="_picks")
        df["rarity"] = rarity
        df["color"] = color
        df["date"] = yesterday
        return df
    except KeyError:
        raise NoALSAError(rarity, color)


def get_alsa_metagame() -> pd.DataFrame:
    dfs = []
    for rarity in MTG_RARITIES:
        for color in MTG_COLORS:
            try:
                df = request_alsa(rarity, color)
                dfs.append(df)
            except NoALSAError:
                pass
    return pd.concat(dfs)


# def render_group(group):
#     group["image"] = [get_card_image(url) for url in group["image_url"]]
#     group["image"] = [
#         img.resize((256, int(256 * img.height / img.width))) for img in group["image"]
#     ]
#     widths, heights = zip(*(i.size for i in group["image"]))
#     total_width = sum(widths)
#     max_height = max(heights)
#     new_img = Image.new("RGB", (total_width, max_height))
#     x_offset = 0
#     font = ImageFont.truetype("data/Roboto-Regular.ttf", size=150)
#     for _, row in group.iterrows():
#         img = row["image"]
#         draw = ImageDraw.Draw(img)
#         gih = str(int(row["GIH WR"]))
#         draw.text(
#             (20, 40), gih, fill="black", font=font, stroke_width=3, stroke_fill="black"
#         )
#         draw.text((20, 40), gih, fill="yellow", font=font)
#         new_img.paste(img, (x_offset, 0))
#         x_offset += img.width
#     return new_img


def add_text_to_border_crop(image, alsa: int, winrate: int, ata: int, iwd: int):
    font_size = 48
    font = ImageFont.truetype("data/Roboto-Regular.ttf", size=font_size)
    draw = ImageDraw.Draw(image)

    # alsa_ata = f"{alsa}/{ata}"
    # winrate_iwd = f"{winrate}{iwd:+}"
    ata = str(ata)
    top = 70
    left = 36
    draw.text(
        (left, top),
        ata,
        fill="black",
        font=font,
        stroke_width=4,
        stroke_fill="black",
    )
    draw.text((left, top), ata, fill="yellow", font=font)
    # draw.text(
    #     (left, top + font_size + 3),
    #     winrate_iwd,
    #     fill="black",
    #     font=font,
    #     stroke_width=4,
    #     stroke_fill="black",
    # )
    # draw.text((left, top + font_size + 5), winrate_iwd, fill="yellow", font=font)
    return image


def stack_images_vertically_with_overlap(images, overlap):
    # Determine the width and height of the output image
    width = max(img.width for img in images)
    height = sum(img.height for img in images) - overlap * (len(images) - 1)

    # Create a new image with a white background
    stacked_image = Image.new("RGB", (width, height), "white")

    # Paste each image into the appropriate position in the new image
    y_offset = 0
    for img in images:
        stacked_image.paste(img, (0, y_offset))
        y_offset += img.height - overlap

    return stacked_image


def concat_vertical(images) -> Image:
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    new_img = Image.new("RGB", (total_width, max(heights)))

    x_offset = 0
    for img in images:
        new_img.paste(img, (x_offset, 0))
        x_offset += img.width
    return new_img
