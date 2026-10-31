#!/usr/bin/env python3
"""Generates the static affiliate site into ./site"""
import html, os, shutil, urllib.parse, json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "public")   # what Netlify publishes
STYLE = os.path.join(HERE, "style.css")              # edit styles here
SITE = "The Shortlist"
DOMAIN = "https://the-shortlist-top10best.netlify.app"   # change after you buy a domain
UPDATED = "October 2026"
UPDATED_ISO = "2026-10-28"
UPDATED_LONG = "October 28, 2026"

ICONS = {
 "tv": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="4" width="56" height="36" rx="4"/><path d="M24 52h16M32 40v12"/><path d="M12 32l10-10 7 7 9-11 14 14" stroke-width="2.5" opacity=".7"/></svg>',
 "projector": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="22" width="40" height="22" rx="5"/><circle cx="32" cy="33" r="6"/><path d="M38 28l22-16M38 38l22 14M60 12v40" stroke-width="2.5" opacity=".7"/><path d="M12 44v5M36 44v5"/><circle cx="13" cy="30" r="1.5" fill="currentColor"/></svg>',
 "shaver": '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="18" y="4" width="28" height="14" rx="5"/><path d="M22 11h20" stroke-width="2" opacity=".7"/><path d="M24 18l-2 40h20l-2-40"/><circle cx="32" cy="34" r="3"/><path d="M27 48h10" stroke-width="2.5" opacity=".7"/></svg>',
 "headphones": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M10 38V30a22 22 0 0 1 44 0v8"/><rect x="6" y="34" width="12" height="18" rx="4"/><rect x="46" y="34" width="12" height="18" rx="4"/></svg>',
 "vacuum": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><circle cx="32" cy="30" r="22"/><circle cx="32" cy="30" r="8"/><path d="M14 22h8M42 22h8"/></svg>',
 "espresso": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="10" y="4" width="44" height="12" rx="3"/><path d="M14 16v34h36V16"/><path d="M24 22h16M32 22v6"/><path d="M24 34h14v8a5 5 0 0 1-5 5h-4a5 5 0 0 1-5-5z"/><path d="M38 37h3a3 3 0 0 1 0 6h-3"/></svg>',
 "desk": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><rect x="6" y="14" width="52" height="6" rx="2"/><path d="M18 20v26M46 20v26M10 50h16M38 50h16"/><path d="M22 14V8h20v6"/></svg>',
 "earbuds": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M18 10a8 8 0 0 1 8 8v4a8 8 0 0 1-8 8h0V10z"/><path d="M18 30v16"/><path d="M46 10a8 8 0 0 0-8 8v4a8 8 0 0 0 8 8h0V10z"/><path d="M46 30v16"/></svg>',
 "mattress": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><rect x="6" y="20" width="52" height="18" rx="5"/><path d="M6 30h52M12 38v8M52 38v8"/><rect x="10" y="12" width="14" height="8" rx="3"/></svg>',
 "hairdryer": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M8 18h30a12 12 0 0 1 0 24H8z"/><path d="M28 42l-4 12h8l4-12"/><path d="M50 26h8M50 34h8"/></svg>',
 "gift": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="20" width="48" height="12" rx="2"/><path d="M12 32v20h40V32M32 20v32"/><path d="M32 20c-4-10-16-12-16-4 0 4 8 4 16 4zM32 20c4-10 16-12 16-4 0 4-8 4-16 4z"/></svg>',
 "chair": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><rect x="20" y="4" width="24" height="24" rx="6"/><path d="M16 32h32M32 32v12M20 52l12-8 12 8"/></svg>',
 "luggage": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><rect x="18" y="12" width="28" height="36" rx="5"/><path d="M26 12V6h12v6M26 20v20M38 20v20M24 52h0M40 52h0"/></svg>',
 "cookware": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M8 26h40v14a10 10 0 0 1-10 10H18A10 10 0 0 1 8 40z"/><path d="M48 30h10M20 26v-4a8 8 0 0 1 16 0v4M28 14v-4"/></svg>',
 "airfryer": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><rect x="12" y="4" width="40" height="48" rx="10"/><path d="M12 26h40M26 36h12"/><circle cx="32" cy="15" r="4"/></svg>',
}

PHOTOS = {
 "chair": dict(id="1626379501846-0df4067b8bb9", alt="A black office chair in a bright room", by="Giorgio Trovato", user="giorgiotrovato", page="https://unsplash.com/photos/black-and-silver-office-rolling-chair-beside-mirror-gI9rvJK61L8"),
 "luggage": dict(id="1639597784714-4905e95de813", alt="Three pieces of white luggage in a room", by="American Green Travel", user="americangreentravel", page="https://unsplash.com/photos/three-pieces-of-white-luggage-sitting-in-a-room-Whnjjhi8OfQ"),
 "cookware": dict(id="1580929753603-10519c6e480a", alt="Stainless steel pots on a gas stove", by="Janko Ferli\u010d", user="itfeelslikefilm", page="https://unsplash.com/photos/stainless-steel-cooking-pots-on-gas-stove-KwU5Cl0LSXs"),
 "desk": dict(id="1623177623442-979c1e42c255", alt="Wooden standing desk in a home office", by="ergonofis", user="ergonofis", page="https://unsplash.com/photos/wooden-standing-desk-in-home-office-tdnYk4qOGhc"),
 "mattress": dict(id="1762199904138-d163fe89540a", alt="A neatly made bed with white linens", by="Dina Makhmutova", user="dinamakhmutova", page="https://unsplash.com/photos/a-neatly-made-bed-with-white-linens-and-pillows-ooDvIpnXkwo"),
 "hairdryer": dict(id="1727755868077-22f0d2ff8353", alt="A red hair dryer on a table", by="Shubham Dhage", user="theshubhamdhage", page="https://unsplash.com/photos/a-red-hair-dryer-sitting-on-top-of-a-table-a5Ekb8Q3q-0"),
 "earbuds": dict(id="1770292170233-5d9e235ec739", alt="White wireless earbuds and charging case", by="atelierbyvineeth", user="atelierbyvineeth", page="https://unsplash.com/photos/white-wireless-earbuds-and-charging-case-on-dark-background-rN1hLIGV4gE"),
 "airfryer": dict(id="1630384060421-cb20d0e0649d", alt="A basket of crispy french fries", by="Mitchell Luo", user="mitchel3uo", page="https://unsplash.com/photos/a-basket-of-french-fries-sitting-on-top-of-a-wooden-table-ChXHveqrb28"),
 "vacuum": dict(id="1653990480360-31a12ce9723e", alt="A robot vacuum on a wooden floor", by="Onur Binay", user="onurbinay", page="https://unsplash.com/photos/a-black-robot-vacuum-on-a-wooden-floor-uhJgh4FHi6I"),
 "home": dict(id="1730909352933-614f1673ac21", alt="Modern living room with a large wall-mounted TV", by="Li Zhang", user="sunx", page="https://unsplash.com/photos/a-living-room-with-a-big-screen-tv-on-the-wall-zSAZG5uQGvk"),
 "tv": dict(id="1738168259543-d0c58e2b91ed", alt="Living room with a large television on the wall", by="Prydumano Design", user="prydumanodesign", page="https://unsplash.com/photos/a-living-room-with-a-large-television-on-a-wall-AL9YkVEHc3U"),
 "projector": dict(id="1756729924464-7e6a0ec1c82a", alt="Projector on a wooden coffee table in a living room", by="Valerion", user="valerion_official", page="https://unsplash.com/photos/modern-projector-sits-on-a-wooden-coffee-table-581yTDyi5C0"),
 "espresso": dict(id="1504194377022-9e04c123352f", alt="Making espresso at home in a kitchen", by="Becca Tapert", user="beccatapert", page="https://unsplash.com/photos/person-using-espresso-inside-kitchen-nHLlgE6DDag"),
 "shaver": dict(id="1533245270348-821d4d5c7514", alt="Man getting a shave and trim at a barber", by="F\u00e1bio Alves", user="barncreative", page="https://unsplash.com/photos/person-shaving-hair-DYetcnz0jRY"),
}

def photo(key, sizes="(max-width: 820px) 100vw, 50vw", eager=False):
    ph = PHOTOS[key]
    base = f"https://images.unsplash.com/photo-{ph['id']}?auto=format&fit=crop&q=75"
    src = ",".join(f"{base}&w={w} {w}w" for w in (480, 800, 1200, 1600))
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{base}&w=1200" srcset="{src}" sizes="{sizes}" alt="{html.escape(ph["alt"])}" '
            f'{load} decoding="async">')

def credit(key):
    ph = PHOTOS[key]
    return (f'<span class="credit">Photo: <a href="https://unsplash.com/@{ph["user"]}?utm_source=the_shortlist&amp;utm_medium=referral" target="_blank" rel="noopener">{html.escape(ph["by"])}</a> / '
            f'<a href="https://unsplash.com/?utm_source=the_shortlist&amp;utm_medium=referral" target="_blank" rel="noopener">Unsplash</a></span>')

ASIN = {'LG C6 OLED': 'B0GRK5D3RW', 'Samsung S95H QD-OLED': 'B0H5G3H55T', 'TCL QM8L': 'B0GPSYT2KN', 'Hisense U7SG': 'B0GR9BLPJ8', 'Vizio Mini LED Quantum 4K': 'B0GVV3NXPV', 'TCL X11L': 'B0GFDJGFG7', 'Hisense C2 Ultra': 'B0DHLH7VPH', 'Epson Home Cinema LS11000': 'B09TS2M1ZS', 'Hisense PX4-Pro': 'B0H6DDBCNQ', 'AWOL Vision Aetherion Max': 'B0GN3XX19L', 'BenQ W2720i': 'B0DPJDK31N', 'Hisense M2 Pro': 'B0F6ZV1367', 'Sony Bravia Projector 8': 'B0DGRCB57X', 'JVC DLA-NZ800': 'B0D45ZGZ4N', 'Aurzen ZIP Tri-Fold': 'B0DYJP2JY6', 'Braun Series 9 Pro+': 'B0FGLF3SDT', 'Philips Norelco i9000 Prestige Ultra': 'B0F1P4RZMK', 'Panasonic Arc5 (ES-LV67-K)': 'B07W7XK55Q', 'Braun Series 8': 'B0CFBV91YQ', 'Philips Norelco 7800': 'B0BPZR1MBC', 'Philips Norelco 5400': 'B0BF9QHHLJ', 'Philips Norelco OneBlade 360': 'B0BZDPFH45', 'Remington F5-5800': 'B00BB5YHEI', 'Philips Norelco Shaver 3600': 'B0CLWDF9NK', 'Philips Norelco Head Shaver Pro 7000': 'B0FHJ55R4L', 'Breville Barista Express Impress': 'B0BBYNPV33', "De'Longhi La Specialista Touch": 'B0F6DY1DGR', 'Breville Bambino Plus': 'B07JVD78TT', 'Breville Bambino': 'B0B1JPPG2L', 'Gaggia Classic E24': 'B07RQ3NL76', "De'Longhi Stilosa": 'B08C96BG9H', 'Ninja Luxe Café Premier': 'B0D45PK5V4', 'Terra Kaffe Demi': 'B0FGWSD63C', 'Nespresso VertuoPlus': 'B01N7GO468', 'Sony WF-1000XM6': 'B0G6HLWS6Q', 'Apple AirPods Pro 3': 'B0FQFB8FMG', 'Bose QuietComfort Ultra Earbuds (2nd Gen)': 'B0F7M3HPBD', 'Samsung Galaxy Buds 4 Pro': 'B0G1PJLWLZ', 'Google Pixel Buds Pro 2': 'B0D79ND3N7', 'Beats Powerbeats Pro 2': 'B0DT2344N3', 'Sony WF-C710N': 'B0DWHPBK42', 'Soundcore Liberty 4 NC': 'B0BZV4QFP8', 'Sony WF-C510': 'B0D9R4GYTN', 'Ninja Air Fryer Max XL': 'B07S6529ZZ', 'Ninja AF101 Air Fryer': 'B07FDJMC9Q', 'Cosori TurboBlaze': 'B0C33CHG99', 'Instant Vortex Plus ClearCook': 'B096N3FTZP', 'Ninja Foodi DualZone 2-Basket': 'B089TQWJKK', 'Ninja Speedi Rapid Cooker': 'B0B3QT6H7H', 'Breville Smart Oven Air Fryer Pro': 'B01N5UPTZS', 'Dreo ChefMaker Combi Fryer': 'B0C5JHKGFP', 'Typhur Dome 2': 'B0CKP6Y6KB', 'BLACK+DECKER Purifry 2-Quart': 'B0D384TSVC', 'Dreame X60 Max Ultra Complete': 'B0G5X4H4PS', 'Roborock Saros 10R': 'B0DHCJ571Z', 'Roborock Saros 20': 'B0G64MM1HM', 'Shark PowerDetect UV Reveal': 'B0GJFVJGXL', 'Dyson Spot+Scrub Ai': 'B0GKC52QZP', 'Roborock QV 35S': 'B0FB419PLY', 'Dreame L40 Ultra': 'B0D6VS4SLX', 'Shark Matrix Plus': 'B0B8B6N2G4', 'SwitchBot Mini K10+': 'B0CHBC7BW1', 'Dreame D10 Plus Gen 2': 'B0D6TTRTPL', 'Branch Duo Standing Desk': 'B0C3WS16XP', 'FlexiSpot E7 Pro': 'B08B3X9CKH', 'Uplift V3': 'B07HYGZXP7', 'Fully Jarvis Bamboo': 'B07GVQF5HM', 'Secretlab Magnus Pro': 'B0G1S75G2K', 'ApexDesk Elite Pro (Curved)': 'B09CJJHJSJ', 'FEZIBO Electric Standing Desk': 'B0F8MHPVPH', 'FlexiSpot M7 Desk Converter': 'B078HGW7FP', 'FlexiSpot H7 Mobile Table': 'B0B2VZZQVG', 'Helix Midnight Luxe': 'B0D3SJ2FXN', 'DreamCloud Hybrid': 'B0DP3F2RWH', 'Nectar Premier': 'B0DCXHY632', 'Tuft & Needle Mint Hybrid': 'B0BV5CS62W', 'Leesa Sapira Chill Hybrid': 'B0F7B18GGP', 'Nolah Evolution': 'B0CDJ9RZ2T', 'Brooklyn Bedding Aurora Luxe': 'B0GQH4CL4L', 'Helix Plus': 'B0D54YMPNT', 'T3 AireLuxe': 'B09SPBNKGR', 'Dyson Supersonic Nural': 'B0DMXJPM4T', 'BaBylissPRO Nano Titanium': 'B091KB6H1F', 'Dyson Airwrap Multi-Styler': 'B0B61XH5YT', 'Shark FlexStyle': 'B0B89P16MC', 'Shark SpeedStyle Pro Flex': 'B0DDYDWVD1', 'Revlon One-Step Volumizer': 'B097CNMZF5', 'GA.MA iQ Perfetto': 'B092RD44N3', 'Therabody Theragun Pro': 'B0B6RL7NQJ', 'Solo Stove Bonfire 2.0': 'B0B7BFJ5Y6', 'Ooni Karu 12': 'B083WGMTGZ', 'LEGO Technic McLaren MCL39 F1 Car': 'B0FMZRRYFP', 'Leatherman ARC': 'B0D7JTK4KM', 'Cuisinart Griddler': 'B002YD99Y4', 'Ekster Leather Smart Wallet': 'B0F3P42YK1', 'KitchenAid Artisan Stand Mixer': 'B01H424IU4', 'Swarovski Matrix Tennis Bracelet': 'B0FG49S9N5', 'Hatch Restore 3': 'B0DLLSCVZW', 'Bearaby Cotton Weighted Blanket': 'B0C1F9MFH1', 'LEGO Botanicals Pretty Pink Bouquet': 'B0DHLJ6TR9', 'Capri Blue Volcano Candle': 'B07H14RYTV', 'Grace & Stella Under Eye Masks': 'B01DZ7C502', 'KODAK Luma 350 Projector': 'B07RB7P439', 'Aura Carver Digital Photo Frame': 'B0CBQRVL7H', 'TUMI Alpha Split Travel Kit': 'B09J1Q6F6B', 'Logitech MX Keys Mini': 'B098JPSVKY', 'Anker MagGo Power Bank': 'B0CFDSMNT7', 'Harry & David Meat & Cheese Gift Box': 'B07D19J4J1', 'YETI Rambler Colster': 'B0BVGF1DJG', 'Sunbeam Royal Luxe Heated Throw': 'B008BF2OF0', 'LEGO Botanicals Orchid': 'B09Q4L157D', 'LANEIGE Lip Sleeping Mask': 'B07XXPHQZK', 'TheraFace Mask Glo': 'B0FKD3826X', 'Tell Me Your Life Story, Mom': '1952568099', 'Steelcase Series 2': 'B08L8GCCDV', 'Branch Verve Chair': 'B0CK3NSMM6', 'Herman Miller Aeron': 'B007WU4NFO', 'Steelcase Leap V2': 'B00TYE4SKG', 'LiberNovo Omni': 'B0FYCKPWP9', 'Autonomous ErgoChair Pro': 'B0FL2JGMK5', 'SIHOO Doro C300 Pro V2': 'B0GSFPTKD5', 'FlexiSpot C7': 'B0DPQQ2L22', 'SIHOO M57': 'B07BDFW1Y7', 'CALPAK Ambeur Carry-On': 'B0HLSB3PGC', 'CALPAK Ambeur Large': 'B0HNNP4JWZ', 'Osprey Sojourn Porter 46L': 'B0CB6YWXNJ', 'CALPAK Luka Duffel': 'B0GKV9M82F', 'All-Clad D3 Stainless 10-Piece': 'B008PLB15Y', 'All-Clad HA1 Nonstick 10-Piece': 'B016SJHAOA', 'Made In 10-Piece Stainless': 'B09HR6MV21', 'HexClad Hybrid 12-Piece': 'B0CVH8FXKB', 'GreenPan Valencia Pro 11-Piece': 'B071HVQL76', 'Caraway 12-Piece Ceramic': 'B08XM1B6ZX', 'Tramontina Tri-Ply Clad 10-Piece': 'B00JDL0TA8', 'Calphalon Ceramic 12-Piece': 'B0GS7KS6MB', 'T-fal Advanced Nonstick 12-Piece': 'B076682L7W', 'Tramontina PrimaWare 18-Piece': 'B01M5H9UCV'}
QUERY = {'LG G6 OLED': 'LG G6 OLED evo 2026 TV', 'Sony Bravia 9 II': 'Sony BRAVIA 9 II Mini LED TV', 'Hisense UR9': 'Hisense UR9 RGB MiniLED TV', 'LG C5 OLED (2025)': 'LG C5 OLED evo TV 2025', 'Nebula Capsule 3 GTV': 'NEBULA Capsule 3 GTV projector', 'Breville Oracle': 'Breville Oracle dual boiler espresso machine', 'Apple AirPods 5': 'Apple AirPods 5', 'FlexiSpot E7 Plus': 'FlexiSpot E7 Plus standing desk', 'Allswell Luxe': 'Allswell Luxe hybrid mattress', 'Plank Firm': 'Plank Firm mattress Brooklyn Bedding', 'Bio Ionic PowerLight Pro': 'Bio Ionic PowerLight Pro hair dryer', 'BondiBoost Blowout Brush Pro': 'BondiBoost Blowout Brush Pro', 'YETI Rambler 20 oz Travel Mug': 'YETI Rambler 20 oz travel mug', 'Oura Ring 4': 'Oura Ring 4', 'Omnilux Contour Face': 'Omnilux Contour Face LED mask', 'Birdsnap TUC Smart Bird Feeder': 'Birdsnap TUC smart bird feeder', 'Hoka Clifton 10': 'Hoka Clifton 10 men', 'Ember Mug 3': 'Ember Mug 3 10 oz', 'Kindle Paperwhite': 'Kindle Paperwhite', 'Le Creuset Signature Dutch Oven (5.5 qt)': 'Le Creuset Signature round Dutch oven 5.5 qt', 'Boulies EP200': 'boulies EP200 ergonomic office chair', 'Away The Bigger Carry-On': 'Away The Bigger Carry-On', 'Samsonite Freeform Carry-On': 'Samsonite Freeform carry-on spinner', 'Monos Carry-On Pro Plus': 'Monos Carry-On Pro Plus', 'Samsonite Proxis Global Carry-On': 'Samsonite Proxis Global carry-on spinner', 'Briggs & Riley Baseline Essential': 'Briggs & Riley Baseline Essential carry-on expandable spinner', 'Amazon Basics 21" Hardside Spinner': 'Amazon Basics 21 inch hardside carry-on spinner'}

def amz(name):
    """Direct product page when we've matched the exact listing, otherwise a focused search."""
    if name in ASIN:
        return "https://www.amazon.com/dp/" + ASIN[name]
    return "https://www.amazon.com/s?k=" + urllib.parse.quote_plus(QUERY.get(name, name))

# ---------------------------------------------------------------- data
GIFT_NOTES = {"$":"Under $50","$$":"About $50–$150","$$$":"About $150–$300","$$$$":"$300+"}
CATS = [
 {
  "slug": "best-tvs", "icon": "tv", "tint": "tint-tv", "short": "TVs",
  "title": "The 10 Best TVs to Buy in 2026",
  "card": "OLED, Mini-LED and budget 4K sets for every room and price.",
  "lead": "From the OLED most reviewers rank first to big-screen bargains, these are the TVs worth your money right now.",
  "filters": [("oled","OLED"),("miniled","Mini-LED"),("gaming","Gaming"),("bright","Bright rooms"),("budget","Budget"),("big","Big screens")],
  "products": [
   dict(name="LG C6 OLED", badge="Best overall", price="$$$", f=["oled","gaming"],
        tags=["OLED","42–83 in","Gaming"],
        summary="If you only read one recommendation, make it this one. The C6 has taken the top spot in several major 2026 roundups by pairing OLED's perfect blacks with noticeably more brightness than earlier C-series models, at a price well below the flagships.",
        pros=["Deep contrast and rich, accurate color","Excellent for console and PC gaming","Sizes from a 42-inch desk set up to 83 inches"],
        cons=["Not as bright as flagship OLEDs in very sunny rooms","Built-in speakers are just okay — budget for a soundbar"]),
   dict(name="Samsung S95H QD-OLED", badge="Best flagship OLED", price="$$$$", f=["oled","gaming","bright"],
        tags=["QD-OLED","Matte screen","165Hz"],
        summary="Samsung's 2026 flagship has been measured as one of the brightest OLEDs ever tested, and its matte anti-glare finish keeps reflections under control. A top pick for anyone who wants OLED picture quality in a room with windows.",
        pros=["Exceptionally bright for an OLED","Matte screen tames glare from lamps and windows","165Hz refresh rate for fast gaming"],
        cons=["No Dolby Vision support","Premium price"]),
   dict(name="LG G6 OLED", badge="Best for movie lovers", price="$$$$", f=["oled"],
        tags=["OLED","Gallery design","HDR"],
        summary="LG's step-up OLED is brighter than the C6 and built to hang flush on a wall like a picture frame. Reviewers single it out as a superb choice for dim-room movie nights.",
        pros=["Stunning HDR highlights and contrast","Slim design that sits flat against the wall","Strong all-round smart features"],
        cons=["Large price jump over the C6","Gains over the C6 are smaller in a dark room"]),
   dict(name="Sony Bravia 9 II", badge="Best for bright rooms", price="$$$$", f=["miniled","bright"],
        tags=["RGB Mini-LED","Sony processing"],
        summary="Sony's newest Mini-LED uses RGB backlighting for huge brightness and very natural color. If your TV room is flooded with daylight, this is the one that holds up best.",
        pros=["Extremely bright — great for daytime viewing and sports","Sony's natural, accurate picture processing","Excellent upscaling of cable and streaming content"],
        cons=["Dark scenes are less inky than on OLED","Fewer gaming extras than rivals"]),
   dict(name="Hisense UR9", badge="Best value RGB Mini-LED", price="$$$", f=["miniled","bright"],
        tags=["RGB Mini-LED","Value"],
        summary="Hisense brings the new RGB Mini-LED technology to a far more affordable price, making it one of the most aggressive value plays of the year.",
        pros=["Flagship-style brightness for much less","Vivid, punchy color","Good choice for sports and bright rooms"],
        cons=["Picture tuning less refined than Sony's","Viewing angles are narrower than OLED"]),
   dict(name="LG C5 OLED (2025)", badge="Best OLED deal", price="$$", f=["oled","gaming","budget"],
        tags=["OLED","Last year's model"],
        summary="Last year's award-winning OLED is now heavily discounted. You give up a little brightness versus the C6, but you still get true OLED contrast and full gaming features for far less money.",
        pros=["OLED picture at a mid-range price","Proven, well-reviewed model","Great for gaming"],
        cons=["Dimmer than the 2026 models","Stock will run out as retailers clear inventory"]),
   dict(name="TCL QM8L", badge="Best big screen on a budget", price="$$", f=["miniled","budget","big","bright"],
        tags=["Mini-LED","Up to 98 in"],
        summary="Named the best low-cost big screen in one major 2026 roundup, the QM8L gives you a very bright Mini-LED picture at sizes that would cost thousands more from the premium brands.",
        pros=["Huge screen sizes for the money","Very bright HDR","Google TV built in"],
        cons=["Some blooming around bright objects on dark backgrounds","Processing not as polished as Sony or LG"]),
   dict(name="Hisense U7SG", badge="Best mid-range Mini-LED", price="$$", f=["miniled","gaming","budget"],
        tags=["Mini-LED","Gaming"],
        summary="A 2026 addition to RTINGS' recommended list, this Mini-LED set delivers strong brightness and gaming features at a mid-range price.",
        pros=["Bright, colorful picture","Fast refresh rate for gaming","Good value per inch"],
        cons=["Contrast can't match OLED","Built-in sound is basic"]),
   dict(name="Vizio Mini LED Quantum 4K", badge="Best budget pick", price="$", f=["miniled","budget"],
        tags=["Mini-LED","Entry level"],
        summary="If you want a good-looking 4K TV without spending much, this budget Mini-LED from Vizio is a recommended entry point — ideal for a bedroom, kids' room or first apartment.",
        pros=["Mini-LED backlight at an entry-level price","Simple smart platform","Good for everyday TV and streaming"],
        cons=["Less bright and less precise than pricier sets","Limited gaming features"]),
   dict(name="TCL X11L", badge="Best giant-screen flagship", price="$$$$", f=["miniled","big","bright"],
        tags=["Mini-LED","75–98 in"],
        summary="TCL's 2026 flagship pushes Mini-LED brightness to the extreme in 75- to 98-inch sizes. It's a home-cinema-sized screen without the hassle of a projector.",
        pros=["Massive screen sizes","Extreme brightness for big, bright rooms","A true 'wow' centerpiece"],
        cons=["Very expensive","Needs a large room — and a strong wall or stand"]),
  ],
  "tips": [
   ("OLED or Mini-LED?","OLED gives perfect blacks and is best for movie nights in a dim room. Mini-LED gets brighter and resists glare, so it suits sunny living rooms and daytime sports."),
   ("Pick the right size","A simple rule: measure your seating distance in inches and divide by about 1.6. Sitting 8 feet (96\") away? A 55–65 inch screen is a good fit."),
   ("Gamers: check the ports","Look for HDMI 2.1, 120Hz or higher refresh rate and VRR so a PS5, Xbox or gaming PC runs smoothly."),
   ("Plan for sound","Thin TVs have small speakers. Even a modest soundbar is a big upgrade for dialogue."),
  ],
  "faq": [
   ("What is the best TV overall in 2026?","The LG C6 OLED is the most common top pick across major review sites thanks to its balance of picture quality, gaming features and price."),
   ("Is last year's model worth buying?","Often, yes. Models like the LG C5 get big discounts once the new year's sets arrive, and the differences are usually small."),
   ("Do I need 8K?","No. There is very little 8K content, and 8K sets are becoming rare. A good 4K TV is the smart buy."),
  ],
  "sources": [
   ("TechRadar — Best TVs","https://www.techradar.com/news/best-tv"),
   ("RTINGS — Best 4K TVs","https://www.rtings.com/tv/reviews/best/by-resolution/4k-ultra-hd-uhd"),
   ("What Hi-Fi? — Best TVs","https://www.whathifi.com/best-buys/best-tv"),
   ("StereoNET — Best TVs 2026","https://www.stereonet.com/buyers-guides/best-tvs-2026"),
  ],
 },
 {
  "slug": "best-projectors", "icon": "projector", "tint": "tint-projector", "short": "Projectors",
  "title": "The 10 Best Projectors to Buy in 2026",
  "card": "Home theater, ultra-short-throw and portable projectors for a giant screen.",
  "lead": "Want a 100-inch picture? These are the projectors reviewers rate highest right now, from pocket-size portables to serious home cinema machines.",
  "filters": [("4k","4K"),("ust","Ultra-short throw"),("portable","Portable"),("gaming","Gaming"),("theater","Home theater"),("budget","Budget")],
  "products": [
   dict(name="Hisense C2 Ultra", badge="Best overall", price="$$$", f=["4k","gaming"],
        tags=["4K laser","Compact","Designed for Xbox"],
        summary="Tom's Guide crowned it the best projector you can buy, and Crutchfield calls it the best for gaming. It's bright, has excellent color accuracy, and its built-in stand makes it easy to aim at any wall or ceiling.",
        pros=["Bright, accurate picture","Flexible, simple setup with built-in stand","Low input lag for console gaming"],
        cons=["Built-in software is fast but somewhat restrictive","Premium price for a lifestyle projector"]),
   dict(name="Epson Home Cinema LS11000", badge="Best for a home theater room", price="$$$$", f=["4k","theater"],
        tags=["4K PRO-UHD","Laser","3LCD"],
        summary="A long-time customer favorite at Crutchfield. Epson's 3LCD design avoids the 'rainbow' color flicker some people notice on single-chip projectors, and the laser light source needs no lamp replacements.",
        pros=["Rich, stable color with no rainbow effect","Lens shift makes ceiling or shelf mounting easy","Laser light source lasts for years"],
        cons=["No built-in streaming — add a Roku or Apple TV","Large and heavy"]),
   dict(name="Hisense PX4-Pro", badge="Best value ultra-short throw", price="$$$", f=["4k","ust","gaming"],
        tags=["UST laser","3,500 lumens"],
        summary="An ultra-short-throw 'laser TV' that sits just inches from the wall. With 3,500 ANSI lumens and wide color coverage, it's bright enough for a living room with the lights on.",
        pros=["Sits on a TV stand right against the wall","Very bright for daytime viewing","Accurate, wide-gamut color"],
        cons=["Best with a special ALR screen (extra cost)","Pricey compared with a TV of the same size"]),
   dict(name="AWOL Vision Aetherion Max", badge="Best premium ultra-short throw", price="$$$$", f=["4k","ust","theater"],
        tags=["UST laser","Premium"],
        summary="What Hi-Fi? named this its best ultra-short-throw pick in October 2026. It launched at $4,499 and aims to replace a giant TV with a 100-inch-plus image.",
        pros=["Top-tier UST picture quality","Huge image from inches away","Ideal TV replacement for big rooms"],
        cons=["Expensive","Needs a flat wall or screen to look its best"]),
   dict(name="BenQ W2720i", badge="Best mid-range", price="$$$", f=["4k","theater"],
        tags=["4K DLP","Smart"],
        summary="An award winner that reviewers describe as having no obvious weaknesses. It's a balanced choice for a first 'real' home theater projector.",
        pros=["Natural, film-like color","Built-in smart features","Great value for its picture quality"],
        cons=["Needs a dark room for the best contrast","Not as bright as laser UST models"]),
   dict(name="Hisense M2 Pro", badge="Best compact 4K", price="$$", f=["4k","portable","budget"],
        tags=["4K laser","Small size"],
        summary="Small in size but big on performance, the M2 Pro won What Hi-Fi?'s award as the best projector at its price. Easy to move between rooms or take to a friend's house.",
        pros=["Compact and easy to set up","4K laser picture","Good built-in sound for its size"],
        cons=["Not as bright as larger models","Not designed for a dedicated theater"]),
   dict(name="Sony Bravia Projector 8", badge="Best high-end", price="$$$$", f=["4k","theater"],
        tags=["Native 4K","SXRD laser"],
        summary="For a dedicated cinema room with a serious budget, reviewers call Sony's Bravia Projector 8 a powerhouse — one of the best home cinema projectors available.",
        pros=["Reference-level picture quality","Native 4K resolution","Superb motion and contrast"],
        cons=["Very expensive","Best installed professionally"]),
   dict(name="JVC DLA-NZ800", badge="Best for videophiles", price="$$$$", f=["4k","theater"],
        tags=["Native 4K","8K e-shift","Laser"],
        summary="JVC has long been the brand serious home theater fans swear by. The NZ800 offers precision optics, a bright laser light source and optional 8K processing at about half the price of JVC's top model.",
        pros=["Outstanding contrast and black levels","Precision optics and laser light","8K e-shift option"],
        cons=["Expensive and large","Overkill for a casual living room"]),
   dict(name="Aurzen ZIP Tri-Fold", badge="Best pocket portable", price="$", f=["portable","budget"],
        tags=["Portable","Folding design"],
        summary="Picked by Tom's Guide as the best portable projector, this folding mini projector slips into a bag for travel, camping or sleepovers.",
        pros=["Truly pocketable","Fast to set up anywhere","Low price"],
        cons=["Dim compared with home projectors — best in a dark room","Small built-in speaker"]),
   dict(name="Nebula Capsule 3 GTV", badge="Best budget portable", price="$", f=["portable","budget"],
        tags=["1080p","Battery","Google TV"],
        summary="A soda-can-sized projector with a built-in battery and Google TV, so Netflix and YouTube are ready out of the box. Perfect for backyard movie nights.",
        pros=["Built-in battery for cordless movie nights","Google TV with all the major apps","Very portable"],
        cons=["1080p, not 4K","Best on screens under about 100 inches in the dark"]),
  ],
  "tips": [
   ("Brightness matters most","Look for ANSI lumens. Around 1,500+ is fine for a dark room; 2,500–3,500+ is better if you'll watch with lights on or daylight."),
   ("Know your throw type","Long-throw projectors sit at the back of the room. Ultra-short-throw (UST) models sit inches from the wall on a TV stand. Portables go anywhere."),
   ("The screen makes a difference","A plain white wall works, but an ambient-light-rejecting (ALR) screen greatly improves contrast — especially for UST projectors."),
   ("Gaming? Check input lag","For consoles, look for low input lag and a dedicated game mode. Models marked for gaming feel much more responsive."),
  ],
  "faq": [
   ("Is a projector better than a TV?","For the biggest picture per dollar, yes. For bright rooms and everyday convenience, a big TV is often easier."),
   ("Do I need a screen?","No, but it helps. A smooth, white or light grey wall is a fine start; a dedicated screen boosts contrast and brightness."),
   ("What about lamp replacement?","Most models on this list use laser or LED light that lasts many thousands of hours, so there are no lamps to replace."),
  ],
  "sources": [
   ("Tom's Guide — Best projectors","https://www.tomsguide.com/best-picks/best-projectors"),
   ("Crutchfield — Best home theater projectors","https://www.crutchfield.com/learn/best-home-theater-projectors.html"),
   ("What Hi-Fi? — Best projectors","https://www.whathifi.com/best-buys/home-cinema/best-projectors"),
   ("ecoustics — Best home theater projectors","https://www.ecoustics.com/articles/best-projectors/"),
  ],
 },
 {
  "slug": "best-electric-shavers", "icon": "shaver", "tint": "tint-shaver", "short": "Electric Shavers",
  "title": "The 10 Best Electric Shavers to Buy in 2026",
  "card": "Foil, rotary and hybrid shavers for every beard and skin type.",
  "lead": "A good electric shaver saves time and skips the razor burn. Here are the models reviewers rate highest for closeness, comfort and value.",
  "filters": [("foil","Foil"),("rotary","Rotary"),("sensitive","Sensitive skin"),("thick","Thick beards"),("budget","Budget"),("head","Head shaving")],
  "products": [
   dict(name="Braun Series 9 Pro+", badge="Best overall", price="$$$", f=["foil","thick","sensitive"],
        tags=["Foil","Wet & dry","Cleaning station"],
        summary="The shaver everything else gets compared to. Reviewers consistently describe it as one of the closest electric shaves you can get while still staying comfortable on the skin.",
        pros=["Exceptionally close, quick shave","Comfortable even on the neck","Wet or dry use; cleaning station available"],
        cons=["Expensive","Cleaning cartridges are an ongoing cost"]),
   dict(name="Philips Norelco i9000 Prestige Ultra", badge="Best for sensitive skin", price="$$$", f=["rotary","sensitive"],
        tags=["Rotary","Smart sensing"],
        summary="Philips' flagship rotary shaver is the top pick for men whose skin gets irritated easily. Its heads follow the contours of the face and it adjusts power to your beard.",
        pros=["Very gentle on sensitive skin","Close shave with rotary flexibility","Premium build and long battery life"],
        cons=["High price","Rotary heads can take time to get used to"]),
   dict(name="Panasonic Arc5 (ES-LV67-K)", badge="Best for thick beards", price="$$", f=["foil","thick"],
        tags=["Foil","5 blades"],
        summary="A long-running favorite for thick, fast-growing beards. Its five-blade head and very fast motor are known for one of the closest shaves available.",
        pros=["Extremely close shave","Powers through coarse, dense stubble","Good value for its performance"],
        cons=["Louder than most rivals","Can feel harsh on very sensitive skin"]),
   dict(name="Braun Series 8", badge="Best mid-range", price="$$", f=["foil","sensitive"],
        tags=["Foil","Wet & dry"],
        summary="Much of the Series 9's comfort at a lower price. A great middle ground if you want a premium feel without paying flagship money.",
        pros=["Comfortable, gentle shave","Solid build quality","Lower price than the Series 9"],
        cons=["Not quite as close as the Series 9","Fewer accessories"]),
   dict(name="Philips Norelco 7800", badge="Best premium rotary value", price="$$", f=["rotary","sensitive"],
        tags=["Rotary","Wet & dry"],
        summary="A step below the i9000 in price with many of the same comfort benefits. A strong choice if you already like how rotary shavers feel.",
        pros=["Comfortable rotary shave","Wet or dry use","Good battery life"],
        cons=["Not as close as top foil shavers on stubborn patches","Replacement heads add cost over time"]),
   dict(name="Philips Norelco 5400", badge="Best mid-range rotary", price="$", f=["rotary","budget"],
        tags=["Rotary","Value"],
        summary="An affordable rotary shaver that handles everyday shaving well. A sensible choice for anyone switching from a disposable razor.",
        pros=["Good everyday performance","Easy to use and clean","Affordable"],
        cons=["Takes a few more passes than premium models","Basic accessories"]),
   dict(name="Philips Norelco OneBlade 360", badge="Best hybrid shaver & trimmer", price="$", f=["sensitive","budget"],
        tags=["Hybrid","Trim, edge & shave"],
        summary="Sits between a trimmer and a shaver. It won't shave as close as a foil shaver, but it's gentle on skin and can trim, edge and shave with one tool.",
        pros=["One tool for stubble, edges and shaving","Very gentle — rarely irritates","Low price; cheap replacement blades"],
        cons=["Not a truly close shave","Blades need replacing every few months"]),
   dict(name="Remington F5-5800", badge="Best budget foil shaver", price="$", f=["foil","budget"],
        tags=["Foil","Under $60"],
        summary="Frequently named the best shaver under $100, it's an easy, inexpensive way to try electric shaving.",
        pros=["Low price","Surprisingly close shave","Pop-up trimmer for sideburns"],
        cons=["Louder than premium models","Less comfortable on the neck"]),
   dict(name="Philips Norelco Shaver 3600", badge="Best budget rotary", price="$", f=["rotary","budget","sensitive"],
        tags=["Rotary","Entry level"],
        summary="A well-rated entry-level rotary shaver that's comfortable on skin — a good gift or starter shaver.",
        pros=["Comfortable rotary heads","Affordable","Good battery life for the price"],
        cons=["Not as close as premium models","Fewer features"]),
   dict(name="Philips Norelco Head Shaver Pro 7000", badge="Best for bald heads", price="$$", f=["rotary","head"],
        tags=["Head shaver","Rotary"],
        summary="Head-shaving specialists rate Philips' Head Shaver Pro range as the best all-round choice for keeping a bald head smooth, thanks to its reliability and easy handling.",
        pros=["Designed for the shape of the head","Reliable and easy to handle","Works wet or dry"],
        cons=["Bulkier than face shavers","Not ideal for detailed face shaving"]),
  ],
  "tips": [
   ("Foil or rotary?","Foil shavers (Braun, Panasonic) move in straight lines and usually shave closest. Rotary shavers (Philips Norelco) use circular heads that follow face contours — many find them more comfortable."),
   ("Match your skin and beard","Sensitive skin: try Braun or Philips' premium models. Thick, coarse beards: a fast multi-blade foil like the Panasonic Arc5."),
   ("Wet or dry","Wet & dry models let you shave with gel or in the shower, which many people find gentler."),
   ("Budget for heads","Plan to replace shaving heads or foils every 12–18 months to keep shaves close and comfortable."),
  ],
  "faq": [
   ("Do electric shavers shave as close as razors?","The best foil shavers get very close, though most people find a blade razor still slightly closer. The trade-off is far less irritation and nicks."),
   ("How long does it take to adjust?","Give your skin 2–3 weeks to adapt when switching from a blade razor."),
   ("Is a cleaning station worth it?","It's convenient and keeps the shaver hygienic, but cartridges add cost. Rinsing under water works fine for most wet & dry models."),
  ],
  "sources": [
   ("Stuff — Best electric shavers","https://www.stuff.tv/features/best-electric-shavers/"),
   ("Shaving Advisor — Best electric shavers","https://shavingadvisor.com/electric-shavers/electric-shavers-for-men/"),
   ("Shaving Advisor — Best head shavers","https://shavingadvisor.com/electric-shavers/best-electric-head-shavers/"),
   ("ShaverCheck — Best head shavers","https://shavercheck.com/best-head-shaver/"),
  ],
 },

 {
  "slug": "best-espresso-machines", "icon": "espresso", "tint": "tint-espresso", "short": "Espresso Machines",
  "title": "The 10 Best Espresso Machines to Buy in 2026",
  "card": "Café-quality espresso at home, from easy beginner machines to barista favorites.",
  "lead": "Whether you want push-button lattes or to pull shots like a barista, these are the espresso machines reviewers rate highest right now.",
  "filters": [("grinder","Built-in grinder"),("beginner","Beginner-friendly"),("compact","Compact"),("milk","Auto milk"),("budget","Budget"),("enthusiast","Enthusiast")],
  "products": [
   dict(name="Breville Barista Express Impress", badge="Best overall", price="$$", f=["grinder","beginner"],
        tags=["Built-in grinder","Assisted tamping","PID"],
        summary="An all-in-one machine that grinds, doses and helps you tamp, so beginners get consistent shots while still learning real barista skills. One 2026 roundup ranks it the best espresso machine overall.",
        pros=["Built-in grinder — no extra purchase","Assisted tamping takes the guesswork out","Precise temperature control and quick heat-up"],
        cons=["Grinder isn't fine enough for very light roasts","Steam pressure dips after several milk drinks in a row"]),
   dict(name="De'Longhi La Specialista Touch", badge="Best guided experience", price="$$", f=["grinder","beginner","milk"],
        tags=["Touchscreen","Built-in grinder","Auto milk"],
        summary="Tom's Guide's top pick. A responsive touchscreen walks you through each drink, it helps you dial in the grind, and it can steam milk automatically.",
        pros=["Easy touchscreen with guided grinding","Tasty espresso out of the box","Strong steam wand plus automatic milk"],
        cons=["Steam wand can be fiddly for hand-steaming","Tamping is guided, not automatic"]),
   dict(name="Breville Bambino Plus", badge="Best compact", price="$$", f=["compact","beginner","milk"],
        tags=["Compact","Auto milk","Fast heat-up"],
        summary="A narrow machine that heats up almost instantly and textures milk for you at the press of a button — ideal for small kitchens and latte lovers.",
        pros=["Very fast heat-up","Automatic milk texturing for lattes and cappuccinos","Fits on small counters"],
        cons=["Needs a separate grinder","Small water tank needs frequent refills"]),
   dict(name="Breville Bambino", badge="Best under $300", price="$", f=["compact","budget"],
        tags=["Compact","PID","Steam wand"],
        summary="The Bambino Plus's smaller sibling keeps the precise temperature control and quick heat-up but skips automatic milk to save about $100.",
        pros=["Excellent value","Precise temperature control","Includes a milk jug"],
        cons=["Milk steaming is manual","No built-in grinder"]),
   dict(name="Gaggia Classic E24", badge="Best for enthusiasts", price="$$", f=["enthusiast"],
        tags=["58mm portafilter","Brass boiler"],
        summary="A long-loved classic that hobbyists swear by. It makes great espresso, has a powerful steam wand, and is famously reliable and easy to upgrade.",
        pros=["Excellent espresso quality","Powerful steam wand","Built to last for years"],
        cons=["Real learning curve — you control the shot yourself","No grinder, and few accessories included"]),
   dict(name="De'Longhi Stilosa", badge="Best budget", price="$", f=["budget","compact"],
        tags=["Manual","Under $150"],
        summary="The cheapest way to make real pump espresso at home. It's small, heats up quickly and has a capable steam wand for the price.",
        pros=["Very affordable","Small and light","Quick heat-up"],
        cons=["Mostly plastic build and a flimsy tamper","Manual operation takes practice"]),
   dict(name="Ninja Luxe Café Premier", badge="Best all-in-one", price="$$", f=["grinder","beginner","milk"],
        tags=["Espresso + drip + cold brew","Built-in grinder"],
        summary="One machine for espresso, regular drip coffee and cold brew. It grinds and doses for you, which makes it a great fit for households with different coffee tastes.",
        pros=["Three kinds of coffee in one machine","Automated grinding and dosing","Hands-free milk frothing"],
        cons=["Less control for serious coffee hobbyists","Large footprint"]),
   dict(name="Terra Kaffe Demi", badge="Best fully automatic", price="$$", f=["grinder","beginner","compact"],
        tags=["Super-automatic","Built-in grinder"],
        summary="Press a button and it grinds, brews and serves. Reviewers praise its easy interface, quick heat-up and consistently good shots in a compact, attractive design.",
        pros=["True one-touch espresso","Consistent results","Compact and good-looking"],
        cons=["Milk frother sold separately","Small water tank and limited grind settings"]),
   dict(name="Nespresso VertuoPlus", badge="Easiest to use", price="$", f=["beginner","compact","budget"],
        tags=["Capsules","One-touch"],
        summary="If you want coffee with zero effort, this capsule machine is the simplest option. Pop in a pod and press a button — no grinding or cleanup.",
        pros=["Effortless and consistent","Small footprint","Quick heat-up"],
        cons=["Not true pump espresso","Highest cost per cup, and locked into Vertuo capsules"]),
   dict(name="Breville Oracle", badge="Best splurge", price="$$$", f=["grinder","milk","enthusiast"],
        tags=["Dual boiler","Automated grinding & tamping"],
        summary="A premium dual-boiler machine that automates grinding, dosing and tamping, and can brew and steam at the same time — café workflow for serious home baristas.",
        pros=["Brew and steam at the same time","Automated grinding, dosing and tamping","Consistent automatic milk"],
        cons=["Very expensive","Large and heavy"]),
  ],
  "tips": [
   ("Grinder in or out?","Fresh grinding matters a lot. A built-in grinder is simplest; machines without one need a separate espresso grinder, so budget for it."),
   ("How hands-on do you want to be?","Manual and semi-automatic machines reward practice. Super-automatic and capsule machines make coffee at the press of a button."),
   ("Lattes? Check the milk system","If you mostly drink milk drinks, look for automatic milk texturing or a strong steam wand."),
   ("Mind your counter","Measure your space. Compact machines like the Bambino fit small kitchens; all-in-ones can be big."),
  ],
  "faq": [
   ("What's the best espresso machine for beginners?","Machines with guidance and automation — like the Breville Barista Express Impress or De'Longhi La Specialista Touch — help you get good shots quickly."),
   ("Do I need a separate grinder?","Only if your machine doesn't have one built in. Pre-ground coffee works, but freshly ground beans taste noticeably better."),
   ("Is a capsule machine real espresso?","Not quite. Capsule machines like the VertuoPlus make espresso-style coffee, but not true pump espresso."),
  ],
  "sources": [
   ("Tom's Guide — Best espresso machines","https://www.tomsguide.com/home/coffee-makers/best-espresso-machines"),
   ("The Coffee Locator — Best espresso machines 2026","https://thecoffeelocator.com/espresso-machines/best-espresso-machines/"),
   ("Yahoo Shopping — Best espresso machines","https://shopping.yahoo.com/home-garden/kitchen/article/best-espresso-machines-185436615.html"),
  ],
 },

 {
  "slug": "best-wireless-earbuds", "icon": "earbuds", "tint": "tint-earbuds", "short": "Wireless Earbuds",
  "title": "The 10 Best Wireless Earbuds to Buy in 2026",
  "card": "Noise-cancelling, workout and budget earbuds for iPhone, Android and everyone else.",
  "lead": "From flagship noise cancelling to great-sounding pairs under $70, these are the earbuds reviewers rate highest right now.",
  "filters": [("anc","Noise cancelling"),("iphone","Best for iPhone"),("android","Best for Android"),("workout","Workouts"),("budget","Budget")],
  "products": [
   dict(name="Sony WF-1000XM6", badge="Best overall", price="$$", f=["anc","android","iphone"],
        tags=["Noise cancelling","Hi-res audio"],
        summary="Named the best wireless earbuds overall by both What Hi-Fi? and Digital Trends. They pair natural, detailed sound with excellent noise cancelling and good call quality, and work well with any phone.",
        pros=["Natural, detailed sound","Excellent noise cancelling","Clear calls and lots of customization"],
        cons=["Expensive","Bulky case and a larger fit that won't suit every ear"]),
   dict(name="Apple AirPods Pro 3", badge="Best for iPhone", price="$", f=["anc","iphone","workout"],
        tags=["Noise cancelling","Heart-rate sensing","IP57"],
        summary="Tom's Guide's top pick overall. Improved noise cancelling, a class-leading transparency mode and seamless iPhone features make these the easy choice for Apple users.",
        pros=["Strong, natural-feeling noise cancelling","Best-in-class transparency mode","Comfortable fit and IP57 water resistance"],
        cons=["Many features need an iPhone","No charging cable in the box"]),
   dict(name="Bose QuietComfort Ultra Earbuds (2nd Gen)", badge="Best noise cancelling", price="$", f=["anc","android","iphone"],
        tags=["Top-tier ANC","Wireless charging"],
        summary="Reviewers call Bose's noise cancelling the benchmark. If blocking out planes, trains and open offices is your priority, these are the ones to get.",
        pros=["Benchmark noise cancelling","Comfortable, secure fit","Clear voice calls"],
        cons=["Battery life is only average (about 6 hours)","Fairly large buds"]),
   dict(name="Apple AirPods 5", badge="Best affordable AirPods", price="$", f=["iphone"],
        tags=["Open fit","Noise cancelling"],
        summary="Digital Trends' pick for iPhone owners who want AirPods without paying Pro prices. The open fit is comfortable for all-day wear.",
        pros=["Comfortable open fit","Improved noise cancelling for an open design","Seamless with Apple devices"],
        cons=["Less isolation than in-ear models","Shorter battery life"]),
   dict(name="Samsung Galaxy Buds 4 Pro", badge="Best for Samsung phones", price="$", f=["anc","android"],
        tags=["Noise cancelling","Galaxy features"],
        summary="Rich sound, strong noise cancelling and deep integration with Galaxy phones make these the natural pick for Samsung owners.",
        pros=["Rich, customizable sound","Strong noise cancelling","Lots of extra features with Galaxy phones"],
        cons=["Best features need a Samsung phone","Modest battery life with ANC on"]),
   dict(name="Google Pixel Buds Pro 2", badge="Best for Pixel phones", price="$", f=["anc","android"],
        tags=["Noise cancelling","Gemini"],
        summary="Light, comfortable and great-sounding, with strong noise cancelling and Google's Gemini assistant built in — the best match for Pixel owners.",
        pros=["Light and comfortable","Strong noise cancelling","Connects to two devices at once"],
        cons=["No hi-res codecs like LDAC","Limited spatial audio"]),
   dict(name="Beats Powerbeats Pro 2", badge="Best for workouts", price="$", f=["workout","iphone","android"],
        tags=["Ear hooks","Heart-rate monitor"],
        summary="Secure ear hooks keep them in place through runs and lifts, and they work with both iPhone and Android. Physical buttons are easy to use mid-workout.",
        pros=["Very secure fit for exercise","Heart-rate monitoring","Works with iPhone and Android"],
        cons=["Bulky case","Noise cancelling trails the best"]),
   dict(name="Sony WF-C710N", badge="Best mid-price", price="$", f=["anc","budget","android","iphone"],
        tags=["Noise cancelling","Under $130"],
        summary="A What Hi-Fi? Award winner that delivers full, detailed sound and good noise cancelling for well under the price of flagships.",
        pros=["Musical, detailed sound","Good noise cancelling for the money","Great value"],
        cons=["Buds and case are a bit chunky","No hi-res codecs"]),
   dict(name="Soundcore Liberty 4 NC", badge="Best budget noise cancelling", price="$", f=["anc","budget","android","iphone"],
        tags=["Noise cancelling","Long battery"],
        summary="Digital Trends' best budget pick: impressive noise cancelling, good sound and long battery life at around $100 or less.",
        pros=["Impressive noise cancelling for the price","Long battery life","Connects to two devices"],
        cons=["Transparency mode is mediocre","Not as refined as premium pairs"]),
   dict(name="Sony WF-C510", badge="Best under $70", price="$", f=["budget","android","iphone"],
        tags=["Small & light","Long battery"],
        summary="Another What Hi-Fi? Award winner — small, light and comfortable, with musical sound and long battery life for very little money. No noise cancelling.",
        pros=["Very affordable","Small, light and comfortable","Great battery life"],
        cons=["No active noise cancelling","Build feels a bit cheap"]),
  ],
  "tips": [
   ("Match your phone","AirPods work best with iPhone, Galaxy Buds with Samsung and Pixel Buds with Pixel. Sony, Bose and Soundcore work well with anything."),
   ("Do you need noise cancelling?","ANC is worth it for commuting, flying and open offices. For workouts or casual listening, you can save money without it."),
   ("Fit is everything","Good sound and noise cancelling depend on a good seal. Try the different ear-tip sizes in the box."),
   ("Check battery life","Look at hours per charge (with ANC on) and total hours with the case. 6–8 hours per charge is typical."),
  ],
  "faq": [
   ("What are the best wireless earbuds overall?","The Sony WF-1000XM6 are the top pick at several major review sites for their sound and noise cancelling."),
   ("Are AirPods worth it on Android?","They work, but you lose many features. Android users are better off with Sony, Bose, Samsung or Google earbuds."),
   ("How much should I spend?","Excellent earbuds start around $60–$130. Flagships at $250–$330 add the best noise cancelling and extras."),
  ],
  "sources": [
   ("Tom's Guide — Best wireless earbuds","https://www.tomsguide.com/us/best-wireless-earbuds,review-6160.html"),
   ("What Hi-Fi? — Best wireless earbuds","https://www.whathifi.com/best-buys/best-wireless-earbuds-budget-and-premium"),
   ("Digital Trends — Best wireless earbuds","https://www.digitaltrends.com/home-theater/best-true-wireless-earbuds/"),
  ],
 },
 {
  "slug": "best-air-fryers", "icon": "airfryer", "tint": "tint-airfryer", "short": "Air Fryers",
  "title": "The 10 Best Air Fryers to Buy in 2026",
  "card": "Crispy food with less oil — compact, family-size and multi-cooker picks.",
  "lead": "Crispy fries, juicy chicken and fast weeknight dinners: these are the air fryers expert testers rate highest right now.",
  "filters": [("compact","Compact"),("family","Family-size"),("budget","Budget"),("multi","Multi-cooker"),("window","Viewing window")],
  "products": [
   dict(name="Ninja Air Fryer Max XL", badge="Best overall", price="$", f=["family"],
        tags=["5.5 qt","Max Crisp 450°F"],
        summary="Forbes Vetted's best air fryer overall. It crisps fast and consistently thanks to a high-heat Max Crisp setting, and it's easy to clean.",
        pros=["Fast, even crisping","Simple, tactile controls","Easy to clean"],
        cons=["Tall — needs cabinet clearance","Too big for one or two people"]),
   dict(name="Ninja AF101 Air Fryer", badge="Best value", price="$", f=["compact","budget"],
        tags=["4 qt","Dehydrate"],
        summary="Editors' Choice at both Reviewed and TechGearLab. It's affordable, crisps superbly and is great for reheating leftovers.",
        pros=["Excellent crisping for the price","Great for reheating","Dishwasher-safe basket"],
        cons=["No shake reminder","Can be noisy"]),
   dict(name="Cosori TurboBlaze", badge="Best for families", price="$", f=["family","budget"],
        tags=["6 qt","9-in-1"],
        summary="TechGearLab's top pick for families: exceptional crisping, accurate temperatures and a bigger basket that feeds a family.",
        pros=["Exceptional crisping","Accurate temperature control","Family-size basket"],
        cons=["Takes up counter space","Coated basket"]),
   dict(name="Instant Vortex Plus ClearCook", badge="Best with a window", price="$", f=["family","window"],
        tags=["6 qt","Viewing window"],
        summary="A see-through window lets you check food without opening the basket. Reviewers praise how well it crisps and how easy it is to use — great for beginners.",
        pros=["Watch food cook through the window","Crisps well","Simple, beginner-friendly controls"],
        cons=["Needs counter space","Odor-reduction feature doesn't do much"]),
   dict(name="Ninja Foodi DualZone 2-Basket", badge="Best dual-basket", price="$", f=["family"],
        tags=["8 qt","Two baskets"],
        summary="Two independent baskets let you cook a main and a side at different settings and finish at the same time — a weeknight-dinner hero for families.",
        pros=["Cook two foods at once","Huge 8-quart capacity","Quick cleanup"],
        cons=["Large footprint","Results can vary with some foods"]),
   dict(name="Ninja Speedi Rapid Cooker", badge="Best multi-cooker", price="$", f=["multi","family"],
        tags=["6 qt","12-in-1"],
        summary="Reviewed's best overall pick. Beyond air frying, it steams, bakes and slow-cooks, so it can make a complete meal in one pot.",
        pros=["Excellent frying","Full meals in one pot","Easy to use"],
        cons=["Bulky","Pot and tray lack handles"]),
   dict(name="Breville Smart Oven Air Fryer Pro", badge="Best toaster oven", price="$$", f=["multi","family"],
        tags=["Countertop oven","Air fry + convection"],
        summary="A countertop oven that air fries, bakes, roasts, dehydrates and more. It can replace a regular oven for many meals.",
        pros=["Extremely versatile","Large capacity","Even cooking"],
        cons=["Expensive and bulky","Not as crispy as basket air fryers"]),
   dict(name="Dreo ChefMaker Combi Fryer", badge="Best smart air fryer", price="$$", f=["family","window"],
        tags=["Cooking probe","App recipes"],
        summary="A built-in probe thermometer and guided app recipes take the guesswork out of cooking meat perfectly.",
        pros=["Built-in cooking probe","Guided app recipes and alerts","See-through basket"],
        cons=["Only three cooking modes","Overkill if you only make snacks"]),
   dict(name="Typhur Dome 2", badge="Best premium", price="$$", f=["family"],
        tags=["Wide flat basket","Quiet"],
        summary="Reviewed's large-capacity pick. A wide, flat basket cooks in a single layer, and testers found it fast, quiet and intuitive.",
        pros=["Fast and quiet","Wide basket for single-layer cooking","Intuitive controls"],
        cons=["Needs lots of counter space","No viewing window"]),
   dict(name="BLACK+DECKER Purifry 2-Quart", badge="Best compact", price="$", f=["compact","budget"],
        tags=["2 qt","Touchscreen"],
        summary="Forbes Vetted's best compact pick — a small square basket that makes good use of space, perfect for one or two people or tiny kitchens.",
        pros=["Small footprint","Even, crisp results","Easy touchscreen"],
        cons=["Too small for families","Some odor during first uses"]),
  ],
  "tips": [
   ("Pick the right size","2–4 quarts suits one or two people. 5–6 quarts feeds a family of four. 8+ quarts or dual baskets for bigger households."),
   ("Basket or oven-style?","Basket air fryers crisp best. Oven-style models do more (toast, bake, roast) but take more space."),
   ("Look for easy cleaning","Dishwasher-safe baskets and trays save a lot of hassle."),
   ("Measure your counter","Some air fryers are tall or wide. Check height under your cabinets."),
  ],
  "faq": [
   ("What size air fryer do I need?","For most households of 3–4 people, a 5–6 quart model is the sweet spot."),
   ("Are dual-basket air fryers worth it?","Yes, if you often cook a main and a side together — both finish at the same time."),
   ("Can an air fryer replace my oven?","An oven-style air fryer can for many meals. Basket models are best for crispy foods and reheating."),
  ],
  "sources": [
   ("Reviewed — Best air fryers","https://www.reviewed.com/cooking/best-right-now/the-best-air-fryers"),
   ("Forbes Vetted — Best air fryers","https://www.forbes.com/sites/forbes-personal-shopper/article/best-air-fryer/"),
   ("TechGearLab — Best air fryers","https://www.techgearlab.com/topics/kitchen/best-air-fryer"),
  ],
 },
 {
  "slug": "best-robot-vacuums", "icon": "vacuum", "tint": "tint-vacuum", "short": "Robot Vacuums",
  "title": "The 10 Best Robot Vacuums to Buy in 2026",
  "card": "Hands-free cleaning, from budget vacuums to self-emptying vacuum-and-mop combos.",
  "lead": "Let a robot handle the floors. These are the robot vacuums expert testers rate highest right now, for every home and budget.",
  "filters": [("mop","Vacuum + mop"),("pets","Pet hair"),("carpet","Carpet"),("selfempty","Self-emptying"),("budget","Budget")],
  "products": [
   dict(name="Dreame X60 Max Ultra Complete", badge="Best overall", price="$$$", f=["mop","selfempty"],
        tags=["Vacuum + mop","42,000 Pa"],
        summary="Tom's Guide's best robot vacuum overall. Very strong suction, excellent hard-floor cleaning and mopping, and a dock that empties the bin and washes and dries the mop pads.",
        pros=["Powerful suction and excellent mopping","Dock empties, washes and dries itself","Quick setup and easy app"],
        cons=["Bulky dock","Expensive"]),
   dict(name="Roborock Saros 10R", badge="Best tested by RTINGS", price="$$$", f=["mop","selfempty","pets"],
        tags=["Ultra slim","Obstacle avoidance"],
        summary="The best robot vacuum RTINGS has tested. Advanced sensors and obstacle recognition help it avoid cables and pet messes, and its low profile fits under furniture.",
        pros=["Excellent obstacle avoidance","Low profile reaches under furniture","Anti-tangle brush"],
        cons=["Premium price","Dock needs floor space"]),
   dict(name="Roborock Saros 20", badge="Best for pet hair", price="$$$", f=["mop","selfempty","pets"],
        tags=["36,000 Pa","Tangle-resistant"],
        summary="Tom's Guide's pick for pet owners and T3's best overall. Very strong suction and a tangle-resistant brush handle shedding pets with ease.",
        pros=["Excellent pet hair pickup","Tangle-resistant brush","Low-maintenance dock"],
        cons=["Very expensive","Mopping can leave streaks"]),
   dict(name="Shark PowerDetect UV Reveal", badge="Best for carpet", price="$$", f=["carpet","pets","selfempty","mop"],
        tags=["Bagless dock","UV stain reveal"],
        summary="Strong on carpets and hard floors with excellent pet hair pickup, plus a bagless base that holds up to 60 days of debris.",
        pros=["Great on carpet","Excellent pet hair pickup","No bags to buy"],
        cons=["No roller mop","Map editing in the app is clunky"]),
   dict(name="Dyson Spot+Scrub Ai", badge="Best for mopping", price="$$", f=["mop","selfempty"],
        tags=["Wet roller","Stain detection"],
        summary="A self-cleaning wet roller and hot-water washing make it the strongest mopper on this list — great for kitchens and hard floors.",
        pros=["Excellent mopping and stain removal","Accurate mapping","Self-emptying bagless dock"],
        cons=["Large and bulky","Noisy, slow drying cycle"]),
   dict(name="Roborock QV 35S", badge="Best value", price="$$", f=["mop","selfempty","budget"],
        tags=["Self-emptying","Long battery"],
        summary="Tom's Guide's best value pick: a self-emptying dock, reliable obstacle avoidance and strong suction at a mid-range price.",
        pros=["Self-emptying dock for the price","Reliable obstacle avoidance","Long battery life"],
        cons=["Struggles with high-pile carpet","Basic mopping"]),
   dict(name="Dreame L40 Ultra", badge="Best mid-range vacuum + mop", price="$$", f=["mop","selfempty"],
        tags=["11,000 Pa","Self-cleaning dock"],
        summary="Strong suction, versatile mopping and a dock that cleans and dries the mops — flagship features for far less than flagship prices.",
        pros=["Strong suction","Versatile mopping","Self-cleaning, self-drying dock"],
        cons=["Bulky dock","Cautious on carpet by default"]),
   dict(name="Shark Matrix Plus", badge="Best budget vacuum + mop", price="$$", f=["mop","selfempty","budget","pets"],
        tags=["2-in-1","Self-emptying"],
        summary="T3's best hybrid: a capable vacuum-and-mop combo with a self-emptying base and an excellent app at a good price.",
        pros=["Strong vacuum and mop combo","Self-emptying base","Excellent app"],
        cons=["Short power cable","Docking can be imprecise"]),
   dict(name="SwitchBot Mini K10+", badge="Best for small spaces", price="$$", f=["selfempty"],
        tags=["Mini size","Self-emptying"],
        summary="The smallest robot vacuum in T3's guide fits into tight spots other robots can't reach — ideal for apartments and cluttered rooms.",
        pros=["Fits tight spaces","Effective cleaning","Good mapping"],
        cons=["Too small for large homes","Weak mopping"]),
   dict(name="Dreame D10 Plus Gen 2", badge="Best budget", price="$", f=["budget","selfempty"],
        tags=["Under $300","Self-emptying"],
        summary="Tom's Guide's best budget robot vacuum — a self-emptying base and good hard-floor cleaning for under $300.",
        pros=["Very affordable","Good on hard floors","Easy-to-use app"],
        cons=["Basic mopping","Struggles on thick carpet"]),
  ],
  "tips": [
   ("Vacuum only, or vacuum + mop?","Combo robots save time on hard floors. If your home is mostly carpet, a strong vacuum-only robot is often enough."),
   ("Self-emptying is worth it","A self-emptying dock means you empty a bag every few weeks instead of a tiny bin every day."),
   ("Pets? Check the brush","Rubber or tangle-resistant brushes handle pet hair far better than bristle brushes."),
   ("Obstacle avoidance","Better models spot cables, socks and pet messes. Worth paying for if your floors are often cluttered."),
  ],
  "faq": [
   ("Do robot vacuums work on carpet?","Yes, but performance varies. Shark and Roborock models with strong suction do best on carpet."),
   ("How long do robot vacuums last?","Typically several years with regular brush and filter replacements."),
   ("Is Black Friday a good time to buy?","Yes — robot vacuums are among the most heavily discounted items during Black Friday sales."),
  ],
  "sources": [
   ("Tom's Guide — Best robot vacuums","https://www.tomsguide.com/best-picks/the-best-robot-vacuums"),
   ("RTINGS — Best robot vacuums","https://www.rtings.com/robot-vacuum/reviews/best/robot"),
   ("T3 — Best robot vacuum cleaner","https://www.t3.com/us/features/best-robot-vacuum-cleaner"),
  ],
 },

 {
  "slug": "best-standing-desks", "icon": "desk", "tint": "tint-desk", "short": "Standing Desks",
  "title": "The 10 Best Standing Desks to Buy in 2026",
  "card": "Sit-stand desks and converters for a healthier, more comfortable workday.",
  "lead": "Switching between sitting and standing is one of the easiest upgrades for a home office. These are the standing desks expert testers rate highest right now.",
  "filters": [("budget","Budget"),("stable","Extra stable"),("small","Small spaces"),("gaming","Gaming"),("premium","Premium")],
  "products": [
   dict(name="Branch Duo Standing Desk", badge="Best overall", price="$$", f=["small","premium"],
        tags=["Sit/stand reminders","Compact frame"],
        summary="Forbes Vetted's best standing desk overall. It offers lots of customization, built-in reminders to switch between sitting and standing, and optional accessories.",
        pros=["Many size and color options","Built-in reminders to sit or stand","Clean, frameless design"],
        cons=["Surface can show fingerprints","Top can chip with rough use"]),
   dict(name="FlexiSpot E7 Pro", badge="Best value", price="$$", f=["stable"],
        tags=["Dual motor","25–50.6 in range"],
        summary="TechRadar's Editor's Choice for best standing desk overall. A solid wood top, built-in cable management and a wide height range make it a great all-rounder.",
        pros=["Very stable and quiet","Wide height range for short and tall users","Cable management included"],
        cons=["Heavy to move","Pricier than basic desks"]),
   dict(name="Uplift V3", badge="Most customizable", price="$$", f=["premium","stable"],
        tags=["Many tops & sizes","Fast motor"],
        summary="Forbes Vetted's best customizable pick. Choose from a huge range of sizes, tops and accessories, and enjoy fast, quiet height changes.",
        pros=["Huge range of options","Fast, quiet movement","Optional solid wood tops"],
        cons=["Add-on accessory quality varies","Costs add up with extras"]),
   dict(name="Fully Jarvis Bamboo", badge="Best premium", price="$$", f=["premium","stable"],
        tags=["Bamboo top","4 memory presets"],
        summary="A durable desk with a sustainably sourced bamboo top, four height presets and a 350-pound weight limit.",
        pros=["Sustainable bamboo top","Four memory presets","High weight capacity"],
        cons=["Limited top color choices","Premium price"]),
   dict(name="FlexiSpot E7 Plus", badge="Most stable", price="$$", f=["stable"],
        tags=["Four legs","High capacity"],
        summary="TechRadar's pick for stability. A four-legged frame keeps it rock solid at standing height, even with heavy monitors.",
        pros=["Very stable four-leg frame","High lifting capacity","Great for multi-monitor setups"],
        cons=["Takes up more floor space","Heavy"]),
   dict(name="Secretlab Magnus Pro", badge="Best for gaming", price="$$", f=["gaming","premium"],
        tags=["All-metal","Built-in cable tray"],
        summary="TechRadar's best standing desk for gaming: an all-metal build with integrated cable management and a tall maximum height.",
        pros=["Sturdy all-metal build","Excellent cable management","Good for tall users"],
        cons=["Premium price","Can't screw accessories into the metal top"]),
   dict(name="ApexDesk Elite Pro (Curved)", badge="Best curved desk", price="$$", f=["gaming"],
        tags=["Curved top","Quiet motor"],
        summary="Forbes Vetted's best curved standing desk. Easy assembly, a spacious surface and a quiet motor.",
        pros=["Easy to assemble","Spacious curved surface","Quiet motor"],
        cons=["30-inch minimum height may be too tall for some"]),
   dict(name="FEZIBO Electric Standing Desk", badge="Best budget", price="$", f=["budget","small"],
        tags=["Under $150","Electric"],
        summary="TechRadar's cheapest pick does what most people need for very little money, and doesn't feel cheap.",
        pros=["Very affordable","Electric height adjustment","Simple setup"],
        cons=["Two-piece top is less stable","No cable management"]),
   dict(name="FlexiSpot M7 Desk Converter", badge="Best converter", price="$", f=["budget","small"],
        tags=["Sits on your desk","One-hand lift"],
        summary="Turns the desk you already have into a standing desk. Forbes Vetted's best converter lifts with one hand and comes in several sizes.",
        pros=["No new desk needed","One-hand lift","Several sizes"],
        cons=["Raises your work surface even when seated"]),
   dict(name="FlexiSpot H7 Mobile Table", badge="Best for small spaces", price="$", f=["budget","small"],
        tags=["On wheels","Slides under furniture"],
        summary="Forbes Vetted's small-space pick: a height-adjustable table on casters that slides under a couch or bed — great for laptops in apartments.",
        pros=["Rolls anywhere","Slides under furniture","Very affordable"],
        cons=["No motor (gas-spring lift)","Lower maximum height than full desks"]),
  ],
  "tips": [
   ("Check the height range","Make sure the desk goes low enough for sitting and high enough for standing at your height. Wider ranges suit more people."),
   ("Two motors and four legs = stability","Dual motors and four-leg frames wobble less, especially with big monitors."),
   ("Size your desktop","48 inches fits one monitor and a laptop. 55–60+ inches for two monitors."),
   ("Not ready for a full desk?","A desk converter turns your existing desk into a standing desk for much less."),
  ],
  "faq": [
   ("How long should I stand each day?","Alternating every 30–60 minutes is a common approach. Comfort matters more than a strict schedule."),
   ("Are cheap standing desks worth it?","Budget desks work well for light setups, but expect more wobble at full height."),
   ("Do I need an anti-fatigue mat?","It helps a lot if you stand for long periods."),
  ],
  "sources": [
   ("Forbes Vetted — Best standing desks","https://www.forbes.com/sites/forbes-personal-shopper/article/best-standing-desk/"),
   ("TechRadar — Best standing desks","https://www.techradar.com/en-ae/news/best-standing-desk"),
  ],
 },
 {
  "slug": "best-mattresses", "icon": "mattress", "tint": "tint-mattress", "short": "Mattresses",
  "title": "The 10 Best Mattresses to Buy in 2026",
  "card": "Mattress-in-a-box picks for every sleeping position, budget and body type.",
  "lead": "A great mattress is the best sleep upgrade you can make. These are the boxed mattresses expert testers rate highest — all available on Amazon.",
  "filters": [("side","Side sleepers"),("back","Back & stomach"),("cooling","Hot sleepers"),("couples","Couples"),("budget","Budget"),("firm","Firm")],
  "products": [
   dict(name="Helix Midnight Luxe", badge="Best overall", price="$$", f=["side","couples","cooling"],
        tags=["Hybrid","Medium-firm"],
        summary="Forbes Vetted's best mattress in a box. Its medium-firm feel suits side, back and combination sleepers, with strong edge support for couples.",
        pros=["Relieves pressure for most sleep positions","Strong edge support for couples","Copper-infused design sleeps cool"],
        cons=["Stomach sleepers may want firmer","Cooling cover costs extra"]),
   dict(name="DreamCloud Hybrid", badge="Best for back & stomach sleepers", price="$$", f=["back","firm","couples"],
        tags=["Hybrid","365-night trial"],
        summary="A firm, lifted feel with good edge support and a full-year trial — and often less expensive than many all-foam beds when on sale.",
        pros=["Supportive for back and stomach sleepers","Good edge support","365-night trial"],
        cons=["Likely too firm for side sleepers"]),
   dict(name="Nectar Premier", badge="Best memory foam", price="$$", f=["side","couples"],
        tags=["Memory foam","365-night trial"],
        summary="Classic contouring memory foam with great motion isolation — your partner's tossing and turning won't wake you.",
        pros=["Contouring pressure relief","Excellent motion isolation","365-night trial"],
        cons=["Sleeps warm for many people"]),
   dict(name="Tuft & Needle Mint Hybrid", badge="Best soft mattress", price="$$", f=["side","cooling"],
        tags=["Hybrid","Plush"],
        summary="A plush, pressure-relieving feel with bouncy coils and heat-wicking foam — ideal if you like sinking in a little.",
        pros=["Plush and pressure-relieving","Bouncy coil support","Heat-wicking foam"],
        cons=["Weaker motion isolation","Shorter 100-night trial"]),
   dict(name="Leesa Sapira Chill Hybrid", badge="Best hybrid", price="$$", f=["cooling","side","back"],
        tags=["Hybrid","3 firmness options"],
        summary="Temperature-regulating fibers in the cover and three firmness options let you match it to any sleeping position.",
        pros=["Cooling cover","Choose soft, medium-firm or firm","Works for all sleep positions"],
        cons=["120-night trial, not a full year"]),
   dict(name="Allswell Luxe", badge="Best budget", price="$", f=["budget","firm"],
        tags=["Hybrid","Under $450 (queen)"],
        summary="The most affordable pick in Forbes Vetted's guide — a durable hybrid for under $450 in a queen.",
        pros=["Lowest price on this list","Medium or extra-firm options","Durable for the price"],
        cons=["Not for people who want a soft bed","Shorter 90-night trial"]),
   dict(name="Nolah Evolution", badge="Best for side sleepers", price="$$", f=["side","couples"],
        tags=["Hybrid","Zoned support"],
        summary="Zoned support relieves pressure at the hips and shoulders — exactly where side sleepers need it.",
        pros=["Excellent hip and shoulder relief","Good edge support and motion isolation","Zoned support"],
        cons=["Tall — needs deep-pocket sheets","May run warm for some"]),
   dict(name="Plank Firm", badge="Best firm mattress", price="$$", f=["firm","back"],
        tags=["Flippable","Very firm"],
        summary="A very firm, two-sided mattress for back and stomach sleepers who want maximum support.",
        pros=["Very firm, flippable design","Optional cooling cover","Great for back and stomach sleepers"],
        cons=["Not suited to side sleepers"]),
   dict(name="Brooklyn Bedding Aurora Luxe", badge="Best for hot sleepers", price="$$", f=["cooling","couples"],
        tags=["Hybrid","Cooling layers"],
        summary="Cooling features in nearly every layer, three firmness levels and strong edge support make it the top pick if you sleep hot.",
        pros=["Cooling throughout","Three firmness levels","Strong edge support"],
        cons=["Less of a hug than memory foam"]),
   dict(name="Helix Plus", badge="Best for heavier people", price="$$", f=["back","firm","couples"],
        tags=["Hybrid","Reinforced coils"],
        summary="Reinforced coils and durable materials give a supportive, lifted feel built for heavier bodies.",
        pros=["Durable, reinforced support","Medium-firm suits many positions","Lifted feel"],
        cons=["Heavier side sleepers may want softer","120-night trial"]),
  ],
  "tips": [
   ("Match your sleeping position","Side sleepers need softer pressure relief; back and stomach sleepers need firmer support."),
   ("Hot sleeper? Go hybrid","Coils let air flow. Look for cooling covers and gel or copper-infused foams."),
   ("Sharing a bed?","Memory foam isolates motion best; good edge support gives you more usable space."),
   ("Use the trial","Most boxed mattresses offer 90–365-night trials. Give your body 2–4 weeks to adjust."),
  ],
  "faq": [
   ("Foam or hybrid?","Foam hugs and isolates motion; hybrids add bounce, edge support and cooler sleep."),
   ("Which size do the links show?","The buttons open the queen size. You can switch sizes on Amazon."),
   ("When is the best time to buy?","Big sales around Black Friday and holiday weekends often bring the best prices."),
  ],
  "sources": [
   ("Forbes Vetted — Best mattresses in a box","https://www.forbes.com/sites/forbes-personal-shopper/article/the-best-mattresses-in-a-box/"),
  ],
 },
 {
  "slug": "best-hair-dryers", "icon": "hairdryer", "tint": "tint-hairdryer", "short": "Hair Dryers & Stylers",
  "title": "The 10 Best Hair Dryers & Stylers to Buy in 2026",
  "card": "Fast, gentle hair dryers and all-in-one stylers like the Dyson Airwrap.",
  "lead": "From salon-grade dryers to all-in-one stylers, these are the hair tools beauty testers rate highest right now.",
  "filters": [("dryer","Hair dryers"),("styler","Multi-stylers & hot brushes"),("curly","Curly hair"),("fine","Fine hair"),("budget","Budget"),("luxury","Luxury")],
  "products": [
   dict(name="T3 AireLuxe", badge="Best overall", price="$", f=["dryer","fine"],
        tags=["5 heat / 3 speed","Frizz control"],
        summary="Forbes Vetted's best hair dryer overall: fast drying, smooth, frizz-free results and easy controls that suit beginners.",
        pros=["Fast drying","Reduces frizz","Easy for beginners"],
        cons=["No diffuser included","Controls on the back of the handle"]),
   dict(name="Dyson Supersonic Nural", badge="Best luxury dryer", price="$$", f=["dryer","luxury","curly"],
        tags=["Scalp protection","Smart attachments"],
        summary="Dyson's smartest dryer senses distance from your scalp to protect it from heat and recognizes each attachment automatically.",
        pros=["Heat-sensing scalp protection","Versatile, auto-recognized attachments","Quiet"],
        cons=["Expensive","Heavier, with a bulky cord"]),
   dict(name="BaBylissPRO Nano Titanium", badge="Best value", price="$", f=["dryer","budget"],
        tags=["1,875W","4-year warranty"],
        summary="Forbes Vetted's best value pick: a powerful, quiet salon-style dryer with a long warranty at a friendly price.",
        pros=["Affordable","Powerful and quiet","4-year warranty"],
        cons=["Only three heat settings","Gets very hot"]),
   dict(name="Dyson Airwrap Multi-Styler", badge="Best multi-styler", price="$$", f=["styler","luxury"],
        tags=["Dry, curl & smooth","No extreme heat"],
        summary="The iconic all-in-one styler dries, curls, waves and smooths using air instead of extreme heat — one of the most-wanted beauty gifts.",
        pros=["Dries and styles in one tool","Gentler air-based styling","Premium build and attachments"],
        cons=["Very expensive","Takes practice; curls can drop on straight hair"]),
   dict(name="Shark FlexStyle", badge="Best Airwrap alternative", price="$$", f=["styler","curly","dryer"],
        tags=["Dryer + styler","All hair types"],
        summary="Who What Wear's best hot brush for all hair types. It works as a regular dryer and twists into a multi-styler — for far less than a Dyson.",
        pros=["Works on all hair types","Converts from dryer to styler","Smooth, bouncy results"],
        cons=["Pricier than basic tools","Noisy"]),
   dict(name="Shark SpeedStyle Pro Flex", badge="Best for curly hair", price="$$", f=["dryer","curly"],
        tags=["Folds for travel","Scalp shield"],
        summary="Forbes Vetted's pick for curls and waves, with a scalp shield and a foldable design for travel.",
        pros=["Great for curls and waves","Folds for travel","Versatile styling"],
        cons=["Learning curve","More than a basic dryer needs"]),
   dict(name="Revlon One-Step Volumizer", badge="Best budget hot brush", price="$", f=["styler","budget"],
        tags=["Dryer brush","Under $60"],
        summary="The affordable classic: it dries and styles in one step for a salon-style blowout at home.",
        pros=["Very affordable","Dries and styles at once","Adds volume"],
        cons=["Barrel gets very hot","Only one attachment"]),
   dict(name="GA.MA iQ Perfetto", badge="Best professional", price="$", f=["dryer","fine"],
        tags=["Just over 10 oz","Brushless motor"],
        summary="A pro-level dryer that weighs just over 10 ounces — fast drying without arm fatigue.",
        pros=["Very lightweight","Fast drying","Memory function and safety lock"],
        cons=["Pricier","Louder than some","Only a 1-year warranty"]),
   dict(name="Bio Ionic PowerLight Pro", badge="Best for fine hair", price="$", f=["dryer","fine"],
        tags=["Lightweight","5-year warranty"],
        summary="Forbes Vetted's pick for fine hair: quiet, lightweight and long-lasting, with a 5-year warranty when registered.",
        pros=["Quiet","Lightweight","Long warranty"],
        cons=["Cool-shot button must be held down","No diffuser"]),
   dict(name="BondiBoost Blowout Brush Pro", badge="Best for volume", price="$", f=["styler","budget","fine"],
        tags=["Hot brush","Beginner-friendly"],
        summary="Who What Wear's best hot brush for volume — easy for beginners and great for smooth, lifted blowouts.",
        pros=["Beginner-friendly","Adds volume and smoothness","Long-lasting hold"],
        cons=["Somewhat noisy","Large to hold"]),
  ],
  "tips": [
   ("Dryer or multi-styler?","A good dryer is all most people need. Multi-stylers like the Airwrap replace several tools if you curl or smooth often."),
   ("Match your hair type","Curly hair loves a diffuser; fine hair does best with gentler, lighter dryers."),
   ("Weight matters","Lighter dryers (around 1 lb or less) are easier on your arms for long or thick hair."),
   ("Protect your hair","Use heat protectant and lower heat settings, especially with hot brushes."),
  ],
  "faq": [
   ("Is the Dyson Airwrap worth it?","If you style often and want one tool to dry and curl, many people think so. The Shark FlexStyle is a strong cheaper alternative."),
   ("Do expensive hair dryers really make a difference?","Pricier dryers are usually faster, lighter and quieter, and some protect your scalp from excess heat."),
   ("What's a hot brush?","A hot air brush dries and styles at the same time — great for quick, volumized blowouts."),
  ],
  "sources": [
   ("Forbes Vetted — Best hair dryers","https://www.forbes.com/sites/forbes-personal-shopper/article/best-hair-dryer/"),
   ("Who What Wear — Best hot brushes","https://whowhatwear.com/best-hot-brushes"),
   ("The Knot — Best gifts for your wife (Dyson Airwrap)","https://www.theknot.com/content/romantic-gifts-for-wife"),
  ],
 },

 {
  "slug": "best-office-chairs", "icon": "chair", "tint": "tint-chair", "short": "Office Chairs",
  "title": "The 10 Best Office Chairs to Buy in 2026",
  "card": "Ergonomic chairs for long workdays, from under $150 to Herman Miller.",
  "lead": "If you sit for hours a day, your chair matters more than almost anything on your desk. These are the office chairs expert testers rate highest right now.",
  "filters": [("budget","Budget"),("backpain","Back support"),("mesh","Breathable mesh"),("adjust","Highly adjustable"),("premium","Premium")],
  "products": [
   dict(name="Steelcase Series 2", badge="Best overall", price="$$", f=["backpain","adjust","premium"],
        tags=["12-year warranty","Weight-activated recline"],
        summary="TechRadar's best office chair overall: full ergonomic comfort, good back support and lots of adjustment at a much lower price than most premium chairs.",
        pros=["Great value for a premium-brand chair","Good back support and breathability","12-year warranty"],
        cons=["Recline doesn't lock","Not ideal for people over 6 feet"]),
   dict(name="Branch Verve Chair", badge="Best design", price="$$", f=["backpain"],
        tags=["3D knit back","7 colors"],
        summary="Tom's Guide's best office chair overall. A soft, breathable knit backrest, a comfortable contoured seat and a 7-year warranty in a stylish package.",
        pros=["Comfortable contoured seat","Breathable knit back","Stylish, in seven colors"],
        cons=["Armrests only adjust up and down"]),
   dict(name="Herman Miller Aeron", badge="Best premium", price="$$", f=["mesh","adjust","premium","backpain"],
        tags=["Iconic mesh","3 sizes"],
        summary="The iconic mesh chair: excellent weight distribution, three sizes and extensive adjustment, backed by a 12-year warranty.",
        pros=["Excellent support and weight distribution","Three sizes for a better fit","12-year warranty"],
        cons=["Big investment, especially with upgrades"]),
   dict(name="Steelcase Leap V2", badge="Best for posture", price="$$", f=["backpain","adjust","premium"],
        tags=["Deep lumbar adjustment","12-year warranty"],
        summary="TechRadar's pick for posture. An engineered backrest with deep lumbar adjustment and a firmness dial keeps you supported all day.",
        pros=["Engineered back support","Deep lumbar and firmness adjustment","Sturdy build"],
        cons=["Firm armrests","Can feel warm"]),
   dict(name="LiberNovo Omni", badge="Best for back pain", price="$$", f=["backpain","adjust","premium"],
        tags=["Motorized lumbar","Dynamic backrest"],
        summary="Tom's Guide's pick for back pain, with motorized lumbar adjustment, a dynamic backrest and a back-stretch feature.",
        pros=["Motorized lumbar adjustment","Very comfortable materials","Back-stretch feature"],
        cons=["Premium price","Electronics have a shorter warranty"]),
   dict(name="Autonomous ErgoChair Pro", badge="Best ergonomics for the price", price="$$", f=["adjust","mesh"],
        tags=["Mesh or foam","Many adjustments"],
        summary="Tom's Guide's best-ergonomics pick packs lots of adjustment points into a chair that costs far less than the big names.",
        pros=["Many adjustment points","Mesh or foam options","Strong features for the price"],
        cons=["Thin armrest padding","Less suited to tall users"]),
   dict(name="SIHOO Doro C300 Pro V2", badge="Most adjustable", price="$$", f=["adjust","mesh","backpain"],
        tags=["Adaptive support","8D armrests"],
        summary="TechRadar's pick for adjustability: very comfortable, breathable and quiet, with an excellent build for the money.",
        pros=["Extensive adjustments","Breathable and comfortable","Excellent build quality"],
        cons=["Bulky for small rooms","Back support may fall short for people over 6 feet"]),
   dict(name="FlexiSpot C7", badge="Best mid-range", price="$", f=["mesh","adjust","budget"],
        tags=["Dynamic lumbar","All-mesh"],
        summary="TechRadar's best mid-range chair: dynamic lumbar support, 4D armrests and all-mesh airflow at a friendly price.",
        pros=["Dynamic lumbar support","Breathable all-mesh design","Long warranty"],
        cons=["Some plastic rattle","4D armrests take time to learn"]),
   dict(name="Boulies EP200", badge="Best value", price="$", f=["budget","mesh","adjust"],
        tags=["Under $250","Breathable mesh"],
        summary="Named the best value chair by TechRadar and best budget chair by Tom's Guide: highly adjustable and comfortable for 8+ hour days.",
        pros=["Broad adjustability","Comfortable for long days","Easy assembly"],
        cons=["Firm seat","Not ideal for chronic back pain"]),
   dict(name="SIHOO M57", badge="Best budget", price="$", f=["budget","mesh"],
        tags=["Under $150","Adjustable lumbar"],
        summary="TechRadar's best budget pick: a breathable mesh chair with adjustable lumbar support at a very low price.",
        pros=["Very affordable","Breathable mesh","Adjustable lumbar"],
        cons=["Fiddly assembly","Limited adjustment for tall users"]),
  ],
  "tips": [
   ("Lumbar support first","Adjustable lower-back support makes the biggest difference for all-day comfort."),
   ("Fit matters","Check seat height, seat depth and the user height range, especially if you're very tall or petite."),
   ("Mesh vs foam","Mesh stays cooler; foam feels softer. Pick based on how warm your room gets."),
   ("Check the warranty","Premium chairs often come with 10–12-year warranties, which helps justify the price."),
  ],
  "faq": [
   ("Is an expensive office chair worth it?","If you sit 6+ hours a day, a well-built ergonomic chair is one of the best investments in your comfort."),
   ("What's the best chair for back pain?","Look for strong, adjustable lumbar support, like the LiberNovo Omni or Steelcase Leap V2."),
   ("What's a good budget office chair?","The SIHOO M57 and Boulies EP200 are well-rated options at low prices."),
  ],
  "sources": [
   ("TechRadar — Best office chairs","https://www.techradar.com/best/best-office-chairs"),
   ("Tom's Guide — Best office chairs","https://www.tomsguide.com/home/home-office/best-office-chairs"),
  ],
 },
 {
  "slug": "best-luggage", "icon": "luggage", "tint": "tint-luggage", "short": "Luggage",
  "title": "The 10 Best Luggage & Carry-Ons to Buy in 2026",
  "card": "Carry-ons, checked bags and travel backpacks that last.",
  "lead": "Whether you're a weekend traveler or a frequent flyer, these are the suitcases and travel bags experts recommend most right now.",
  "filters": [("carryon","Carry-on"),("checked","Checked"),("budget","Budget"),("business","Business travel"),("lightweight","Lightweight"),("soft","Bags & backpacks")],
  "products": [
   dict(name="Away Bigger Carry-On", badge="Best carry-on", price="$", f=["carryon"],
        tags=["Hardside","Compression system"],
        summary="Forbes Vetted's best carry-on: a roomy, durable polycarbonate shell, a compression system, quiet wheels and a lifetime warranty.",
        pros=["Roomy and durable","Built-in compression","Lifetime warranty"],
        cons=["Very common — less distinctive"]),
   dict(name="CALPAK Ambeur Carry-On", badge="Most stylish carry-on", price="$", f=["carryon"],
        tags=["Expandable","Quiet wheels"],
        summary="Yahoo Shopping's best carry-on overall: stylish, scratch-resistant, expandable and smooth-rolling.",
        pros=["Stylish and scratch-resistant","Expandable","Quiet, straight-rolling wheels"],
        cons=["No compression features"]),
   dict(name="Samsonite Freeform Carry-On", badge="Best value", price="$", f=["carryon","budget"],
        tags=["Expandable","10-year warranty"],
        summary="Forbes Vetted's best value pick: an affordable, expandable spinner from a trusted brand with smooth wheels.",
        pros=["Affordable","Expandable","10-year limited warranty"],
        cons=["Shell is less impact-resistant than polycarbonate"]),
   dict(name="Monos Carry-On Pro Plus", badge="Best for business travel", price="$$", f=["carryon","business"],
        tags=["Front laptop pocket","Quiet wheels"],
        summary="A front laptop pocket, ultra-quiet wheels and interior compression make this the frequent business traveler's pick.",
        pros=["Quick-access laptop pocket","Very quiet wheels","Interior compression"],
        cons=["Front pocket reduces interior space","Handle can stick when overpacked"]),
   dict(name="Samsonite Proxis Global Carry-On", badge="Best lightweight", price="$$", f=["carryon","lightweight"],
        tags=["Under 5 lbs","USB port"],
        summary="Forbes Vetted's lightest pick at about 4.6 pounds, so you can pack more without hitting weight limits.",
        pros=["Very light","Easy to maneuver","Built-in USB port"],
        cons=["Less packing space","Not for overpackers"]),
   dict(name="Briggs & Riley Baseline Essential", badge="Best softside", price="$$", f=["carryon","soft","business"],
        tags=["Expands ~30%","Lifetime warranty"],
        summary="A premium softside carry-on that expands about 30%, with shock-absorbing wheels and a lifetime warranty.",
        pros=["Big expansion","Shock-absorbing wheels","Lifetime warranty"],
        cons=["Utilitarian look","Heavier than hardside options"]),
   dict(name="CALPAK Ambeur Large", badge="Best large checked bag", price="$", f=["checked"],
        tags=["100L","Expandable"],
        summary="A spacious checked suitcase that expands up to 2 inches — relatively affordable for its size.",
        pros=["Huge capacity","Expandable","Comfortable handles"],
        cons=["No exterior pockets","Shorter warranty"]),
   dict(name="Osprey Sojourn Porter 46L", badge="Best travel backpack", price="$", f=["carryon","soft","lightweight"],
        tags=["Carry-on size","Laptop sleeve"],
        summary="Yahoo Shopping's best backpack pick: a carry-on-compliant travel pack for travelers who'd rather not roll a suitcase.",
        pros=["Carry-on compliant","Comfortable to carry","Padded laptop sleeve"],
        cons=["No wheels"]),
   dict(name="CALPAK Luka Duffel", badge="Best personal item", price="$", f=["soft","lightweight"],
        tags=["Shoe compartment","Lightweight"],
        summary="Forbes Vetted's best personal item: very light, with lots of pockets and a separate shoe compartment.",
        pros=["Very lightweight","Lots of pockets","Separate shoe compartment"],
        cons=["No wheels","Short warranty"]),
   dict(name="Amazon Basics 21\" Hardside Spinner", badge="Best budget", price="$", f=["carryon","budget","lightweight"],
        tags=["Under $70"],
        summary="Yahoo Shopping's best affordable pick: lightweight, roomy and reinforced at a very low price.",
        pros=["Very affordable","Lightweight","Large capacity for the price"],
        cons=["Wheels are noisy","Not as balanced as pricier bags"]),
  ],
  "tips": [
   ("Check airline size limits","Most U.S. carry-on limits are about 22 x 14 x 9 inches including wheels and handles. International limits are often smaller."),
   ("Hardside or softside?","Hardside protects better and resists rain; softside flexes and usually has outside pockets."),
   ("Look at the warranty","Lifetime and 10-year warranties are a good sign the bag is built to last."),
   ("Weight matters","A lighter suitcase leaves more of your airline weight allowance for your stuff."),
  ],
  "faq": [
   ("What's the best carry-on size?","Look for about 22 x 14 x 9 inches for most U.S. airlines."),
   ("Is expensive luggage worth it?","Pricier bags usually roll smoother, last longer and come with better warranties."),
   ("Do I need a checked bag too?","For trips over a week or family travel, a large checked bag plus a carry-on is the most flexible combo."),
  ],
  "sources": [
   ("Forbes Vetted — Best luggage","https://www.forbes.com/vetted/travel/article/best-luggage/"),
   ("Yahoo Shopping — Best carry-on luggage","https://shopping.yahoo.com/style/luggage/article/best-carry-on-luggage-200846622.html"),
  ],
 },
 {
  "slug": "best-cookware-sets", "icon": "cookware", "tint": "tint-cookware", "short": "Cookware Sets",
  "title": "The 10 Best Cookware Sets to Buy in 2026",
  "card": "Stainless, nonstick and ceramic pots and pans worth the investment.",
  "lead": "A good set of pots and pans lasts for years. These are the cookware sets expert test kitchens rate highest right now, from budget starter sets to heirloom stainless.",
  "filters": [("stainless","Stainless steel"),("nonstick","Nonstick"),("ceramic","Ceramic"),("induction","Induction-ready"),("budget","Budget"),("premium","Premium")],
  "products": [
   dict(name="All-Clad D3 Stainless 10-Piece", badge="Best stainless steel", price="$$", f=["stainless","induction","premium"],
        tags=["Tri-ply","Oven & broiler safe"],
        summary="A co-winner at America's Test Kitchen and Food Network's best stainless pick: sturdy, balanced tri-ply pans that heat evenly and brown beautifully.",
        pros=["Even heating and great browning","Sturdy, well-balanced build","Works on all cooktops"],
        cons=["Expensive","Stainless takes more effort to clean"]),
   dict(name="All-Clad HA1 Nonstick 10-Piece", badge="Best nonstick", price="$$", f=["nonstick","induction"],
        tags=["Hard-anodized","Oven safe to 500°F"],
        summary="Food Network's best nonstick and Reviewed's best overall nonstick set: durable, easy to clean, with tight-fitting lids.",
        pros=["Durable, scratch-resistant coating","Easy cleanup","Induction-ready"],
        cons=["Heavy","Takes storage space"]),
   dict(name="Made In 10-Piece Stainless", badge="Best premium", price="$$", f=["stainless","induction","premium"],
        tags=["5-ply","Crafted in Italy"],
        summary="America's Test Kitchen co-winner: browns and heats evenly, with a roomy 4-quart saucepan and a saucier, and handles that stay cool.",
        pros=["Excellent, even heating","Includes a saucier","Comfortable, cool handles"],
        cons=["Expensive","Skillet corners can trap food"]),
   dict(name="HexClad Hybrid 12-Piece", badge="Best hybrid", price="$$", f=["nonstick","induction","premium"],
        tags=["Stainless + nonstick","Dishwasher safe"],
        summary="Reviewed's best hybrid: a steel-and-nonstick surface that handles high heat while staying reliably nonstick.",
        pros=["Handles high heat","Reliably nonstick","Oven- and dishwasher-safe"],
        cons=["Can stain after high-heat cooking","Heavy"]),
   dict(name="GreenPan Valencia Pro 11-Piece", badge="Best ceramic", price="$$", f=["ceramic","nonstick","induction"],
        tags=["Ceramic nonstick","Metal-utensil safe"],
        summary="Reviewed's best ceramic set and Food Network's best professional-grade pick: sears well, cleans easily and is built to last.",
        pros=["Sears well for ceramic","Easy to clean","Durable coating"],
        cons=["Stockpot is on the small side"]),
   dict(name="Caraway 12-Piece Ceramic", badge="Best-looking set", price="$$", f=["ceramic","nonstick","premium"],
        tags=["Storage included","Many colors"],
        summary="Food Network's best nontoxic pick: very nonstick, comes in lots of colors and includes storage racks.",
        pros=["Very nonstick","Beautiful colors","Storage organizers included"],
        cons=["Needs gentle cleaning","Heavy"]),
   dict(name="Tramontina Tri-Ply Clad 10-Piece", badge="Best value stainless", price="$", f=["stainless","induction","budget"],
        tags=["Tri-ply","Dishwasher safe"],
        summary="Food Network's best value stainless set: reasonably priced, works on all cooktops and browns food nicely.",
        pros=["Great value for tri-ply","Works on all cooktops","Dishwasher-safe"],
        cons=["Some pieces run small","Can discolor over time"]),
   dict(name="Calphalon Ceramic 12-Piece", badge="Best value ceramic", price="$", f=["ceramic","nonstick","budget"],
        tags=["PFAS-free","Metal-utensil safe"],
        summary="Food Network's best ceramic pick: excellent food release and great value.",
        pros=["Excellent food release","Great value","Metal-utensil safe"],
        cons=["Not induction-compatible","Some lids fit loosely"]),
   dict(name="T-fal Advanced Nonstick 12-Piece", badge="Best budget nonstick", price="$", f=["nonstick","budget"],
        tags=["Heat indicator","Dishwasher safe"],
        summary="Reviewed's best value set: cooks eggs and sauces well, boils water fast and has comfortable handles.",
        pros=["Very affordable","Great for eggs and sauces","Comfortable handles"],
        cons=["Doesn't sear meat as well as stainless"]),
   dict(name="Tramontina PrimaWare 18-Piece", badge="Best starter set", price="$", f=["nonstick","budget"],
        tags=["18 pieces","Under $60"],
        summary="Food Network's best value nonstick: a big, lightweight set for very little money — perfect for a first apartment.",
        pros=["Lots of pieces","Very affordable","Lightweight"],
        cons=["Thin aluminum heats unevenly","Coating wears faster"]),
  ],
  "tips": [
   ("Stainless or nonstick?","Stainless lasts forever and browns food best. Nonstick and ceramic make eggs and cleanup easy. Many cooks own both."),
   ("Induction cooktop?","Check that the set is induction-ready — not all aluminum or ceramic sets are."),
   ("Fewer, better pieces","A 10-piece set with the sizes you'll use beats a giant set full of extras."),
   ("Care for nonstick","Use medium heat and wooden or silicone utensils to make nonstick coatings last."),
  ],
  "faq": [
   ("What's the best cookware material?","Tri-ply stainless steel is the most versatile and long-lasting; nonstick is easiest for everyday eggs and fish."),
   ("Is ceramic cookware safe?","Ceramic coatings are marketed as PFAS-free, which is why many people choose them."),
   ("How long does nonstick last?","Typically a few years with care. Stainless steel can last a lifetime."),
  ],
  "sources": [
   ("America's Test Kitchen — Best cookware sets","https://www.americastestkitchen.com/equipment_reviews/2045-cookware-sets"),
   ("Food Network — Best cookware sets","https://foodnetwork.com/how-to/packages/shopping/product-reviews/best-cookware-sets"),
   ("Reviewed — Best nonstick cookware sets","https://reviewed.com/cooking/best-right-now/the-best-nonstick-cookware-sets"),
  ],
 },
 {
  "slug": "gifts-for-him", "kind": "gift", "icon": "gift", "tint": "tint-gift-him", "short": "Gifts for Him",
  "title": "The 10 Best Gifts for Him in 2026 (Husband, Boyfriend & Men)",
  "card": "Gifts he'll actually use — for husbands, boyfriends and every guy on your list.",
  "lead": "Shopping for your husband, boyfriend or the guy who says he doesn't need anything? These are the gifts editors keep recommending — from under $50 to splurges.",
  "price_notes": GIFT_NOTES,
  "filters": [("tech","Tech"),("outdoors","Outdoors"),("kitchen","Cooking"),("grooming","Grooming")],
  "products": [
   dict(name="Therabody Theragun Pro", badge="Best splurge", price="$$$$", f=["tech"],
        tags=["Massage gun","Recovery"],
        summary="A percussive massage gun that eases sore muscles after workouts or long days. It appears in The Knot's gift guide for husbands.",
        pros=["Professional-grade muscle relief","Great for active guys","Feels like a real treat"],
        cons=["Expensive","Overkill for casual use"]),
   dict(name="Solo Stove Bonfire 2.0", badge="Best for the backyard", price="$$$", f=["outdoors"],
        tags=["Low-smoke fire pit","Portable"],
        summary="A low-smoke, portable fire pit for backyard hangs and camping trips — a gift the whole family enjoys.",
        pros=["Much less smoke than a regular fire pit","Portable","Easy cleanup with removable ash pan"],
        cons=["Pricey for a fire pit","Gets very hot — needs a safe spot"]),
   dict(name="Ooni Karu 12", badge="Best for foodies", price="$$$$", f=["outdoors","kitchen"],
        tags=["Pizza oven","Wood or gas"],
        summary="A portable pizza oven that cooks restaurant-style pizza in about a minute. A favorite for guys who love to grill.",
        pros=["Super-fast, crispy pizzas","Wood or gas (burner sold separately)","Portable"],
        cons=["Learning curve","Outdoor use only"]),
   dict(name="Apple AirPods Pro 3", badge="Best tech gift", price="$$$", f=["tech"],
        tags=["Noise cancelling","iPhone"],
        summary="Our top earbuds pick for iPhone users, with strong noise cancelling and a comfortable fit. See our earbuds list for Android picks.",
        pros=["Excellent noise cancelling","Comfortable fit","Seamless with iPhone"],
        cons=["Best features need an iPhone"]),
   dict(name="Braun Series 9 Pro+", badge="Best grooming gift", price="$$$$", f=["grooming"],
        tags=["Electric shaver","Wet & dry"],
        summary="The #1 pick on our electric shavers list — one of the closest, most comfortable shaves you can get.",
        pros=["Very close, comfortable shave","Wet or dry","Premium feel"],
        cons=["Expensive","Cleaning cartridges add cost"]),
   dict(name="LEGO Technic McLaren MCL39 F1 Car", badge="Best for car & F1 fans", price="$$$", f=["tech"],
        tags=["Build-and-display"],
        summary="A detailed, working replica of a McLaren F1 car — a relaxing build and an impressive display piece. A LEGO McLaren set appears in The Knot's guide for husbands.",
        pros=["Hours of satisfying building","Great display piece","Perfect for F1 fans"],
        cons=["Takes shelf space"]),
   dict(name="Leatherman ARC", badge="Best everyday carry", price="$$$", f=["outdoors"],
        tags=["20 tools","Premium steel"],
        summary="A 20-in-1 multi-tool with a premium MagnaCut steel blade — useful at home, at work and outdoors.",
        pros=["20 tools in one","Premium blade steel","Built to last"],
        cons=["Pricey for a multi-tool"]),
   dict(name="Cuisinart Griddler", badge="Best for the home cook", price="$$", f=["kitchen"],
        tags=["Grill + griddle + panini"],
        summary="ABC News' gift guide for husbands picks this indoor grill, griddle and panini press for pancakes, burgers and more.",
        pros=["Five cooking modes","Dishwasher-safe plates","Great value"],
        cons=["Takes counter space"]),
   dict(name="Ekster Leather Smart Wallet", badge="Best everyday upgrade", price="$$", f=["tech"],
        tags=["Pop-up cards","RFID blocking"],
        summary="A slim leather wallet with a pop-up card mechanism and anti-skimming protection.",
        pros=["Slim and sleek","Cards pop up with one click","RFID blocking"],
        cons=["Holds fewer cards than a bifold"]),
   dict(name="YETI Rambler 20 oz Travel Mug", badge="Best under $50", price="$", f=["outdoors"],
        tags=["Keeps drinks hot or cold"],
        summary="A tough, spill-resistant travel mug that keeps coffee hot for hours — a gift he'll use every single day.",
        pros=["Keeps drinks hot or cold for hours","Spill-resistant lid","Very durable"],
        cons=["Pricier than basic mugs"]),
  ],
  "tips": [
   ("Think about his routine","The best gifts improve something he does every day — coffee, commuting, workouts or weekend hobbies."),
   ("Upgrade what he already uses","A better version of something he loves (earbuds, shaver, wallet) is almost always a hit."),
   ("Experiences count too","Pair a gift like a pizza oven or fire pit with a planned night together."),
  ],
  "faq": [
   ("What do you get a man who has everything?","Upgrades and experiences work best: a premium version of something he uses daily, or a hobby gift like a pizza oven."),
   ("What's a good gift under $50?","The YETI Rambler travel mug is a crowd-pleaser he'll use every day."),
   ("When should I order holiday gifts?","Order by early December to be safe with shipping, and watch for Black Friday deals."),
  ],
  "sources": [
   ("The Knot — Gifts for your husband","https://www.theknot.com/content/gifts-for-husband"),
   ("ABC News — 2026 gift guide for your husband","https://abcnews.com/GMA/Shop/best-gifts-for-husband-2026/story?id=137606188"),
  ],
 },
 {
  "slug": "gifts-for-her", "kind": "gift", "icon": "gift", "tint": "tint-gift-her", "short": "Gifts for Her",
  "title": "The 10 Best Gifts for Her in 2026 (Wife, Girlfriend & Women)",
  "card": "Thoughtful gifts for your wife, girlfriend or any woman on your list.",
  "lead": "From cozy self-care to splurge-worthy beauty tech, these are the gifts editors recommend most for wives, girlfriends and the women in your life.",
  "price_notes": GIFT_NOTES,
  "filters": [("beauty","Beauty"),("cozy","Cozy & self-care"),("tech","Tech"),("home","Home")],
  "products": [
   dict(name="Dyson Airwrap Multi-Styler", badge="Best splurge", price="$$$$", f=["beauty"],
        tags=["Hair styler","Dry & curl"],
        summary="One of the most-wanted beauty gifts. It dries and curls with air instead of extreme heat — see our hair tools list for cheaper alternatives.",
        pros=["Dries and styles in one tool","Gentler on hair","Feels luxurious"],
        cons=["Very expensive","Takes practice"]),
   dict(name="Oura Ring 4", badge="Best tech gift", price="$$$$", f=["tech"],
        tags=["Smart ring","Sleep & health"],
        summary="A slim smart ring that tracks sleep, activity, heart rate and women's health — no bulky watch required.",
        pros=["Discreet, stylish design","Detailed sleep tracking","Long battery life"],
        cons=["Needs the right ring size","Some features need a subscription"]),
   dict(name="KitchenAid Artisan Stand Mixer", badge="Best for bakers", price="$$$$", f=["home"],
        tags=["5-quart","Iconic design"],
        summary="The classic stand mixer for anyone who loves to bake. It looks great on the counter and lasts for years.",
        pros=["Versatile and durable","Iconic, colorful design","Lots of add-on attachments"],
        cons=["Heavy","Takes counter space"]),
   dict(name="Omnilux Contour Face", badge="Best skincare tech", price="$$$$", f=["beauty","cozy"],
        tags=["LED light therapy mask"],
        summary="An at-home LED light therapy mask for fine lines and redness. Red-light masks are one of the hottest gift trends of recent holiday seasons.",
        pros=["Professional-style LED treatment at home","Flexible, comfortable mask","Relaxing routine"],
        cons=["Expensive","Results take consistent use"]),
   dict(name="Swarovski Matrix Tennis Bracelet", badge="Best jewelry", price="$$$", f=["beauty"],
        tags=["Crystal","Classic"],
        summary="A sparkly crystal tennis bracelet that delivers the look of fine jewelry at a friendlier price.",
        pros=["Classic, wearable style","Lots of sparkle for the price","Comes gift-ready"],
        cons=["Crystal, not diamonds"]),
   dict(name="Hatch Restore 3", badge="Best for better sleep", price="$$$", f=["cozy","tech"],
        tags=["Sunrise alarm","Sound machine"],
        summary="A sunrise alarm and sleep-sound machine that makes bedtime and wake-ups calmer.",
        pros=["Gentle sunrise wake-up","Soothing sleep sounds","Screen-free bedtime routine"],
        cons=["Some content needs a subscription"]),
   dict(name="Bearaby Cotton Weighted Blanket", badge="Best cozy gift", price="$$$", f=["cozy","home"],
        tags=["Chunky knit","Breathable"],
        summary="A beautiful chunky-knit weighted blanket that's calming without trapping heat.",
        pros=["Calming weight","Breathable knit stays cool","Looks great on a sofa or bed"],
        cons=["Pricey","Heavy to move around"]),
   dict(name="LEGO Botanicals Pretty Pink Bouquet", badge="Flowers that last", price="$$", f=["home"],
        tags=["Build-and-display"],
        summary="A build-it-yourself flower bouquet that never wilts — fun to build and lovely on display.",
        pros=["Never wilts","Relaxing build","Great date-night activity"],
        cons=["Not real flowers"]),
   dict(name="Capri Blue Volcano Candle", badge="Best under $50", price="$", f=["home","cozy"],
        tags=["Signature scent"],
        summary="A cult-favorite scent of tropical fruit and sugared citrus in a pretty, reusable glass jar.",
        pros=["Beloved signature scent","Reusable jar","Easy, crowd-pleasing gift"],
        cons=["Strong scent isn't for everyone"]),
   dict(name="Grace & Stella Under Eye Masks", badge="Best stocking stuffer", price="$", f=["beauty","cozy"],
        tags=["Self-care","Under $25"],
        summary="Cooling gel eye patches for puffiness and dark circles — a little self-care treat. Yahoo Shopping includes them in its gift guide for wives.",
        pros=["Inexpensive treat","Refreshing and cooling","Great add-on gift"],
        cons=["Results are temporary"]),
  ],
  "tips": [
   ("Listen for hints","The best gifts are often things she's mentioned wanting but wouldn't buy for herself."),
   ("Mix big and small","Pair a main gift with a small add-on like a candle or eye masks."),
   ("Comfort is always welcome","Sleep, self-care and cozy gifts are consistent favorites."),
  ],
  "faq": [
   ("What's a good gift for my wife?","Gifts that pamper her — a beauty tool, better sleep or a cozy blanket — are consistently popular."),
   ("What's a good gift under $50?","The Capri Blue Volcano candle or Grace & Stella eye masks are easy wins."),
   ("Is the Dyson Airwrap a good gift?","It's one of the most-wanted beauty gifts. If it's over budget, the Shark FlexStyle is a popular alternative."),
  ],
  "sources": [
   ("The Knot — Best gifts for your wife","https://www.theknot.com/content/romantic-gifts-for-wife"),
   ("Yahoo Shopping — Best gifts for your wife","https://shopping.yahoo.com/gift-ideas/article/best-wife-gift-ideas-180334098.html"),
   ("Google — Holiday 100 gift search trends","https://blog.google/products-and-platforms/products/shopping-payments/holiday-100-2025/"),
  ],
 },
 {
  "slug": "gifts-for-dad", "kind": "gift", "icon": "gift", "tint": "tint-gift-dad", "short": "Gifts for Dad",
  "title": "The 10 Best Gifts for Dad in 2026",
  "card": "Useful, fun and sentimental gifts for every kind of dad.",
  "lead": "Whether he's a tech guy, a traveler or a backyard birdwatcher, these are the dad gifts editors are recommending this year.",
  "price_notes": GIFT_NOTES,
  "filters": [("tech","Tech"),("travel","Travel"),("food","Food & drink"),("home","Home & hobbies")],
  "products": [
   dict(name="KODAK Luma 350 Projector", badge="Best for movie nights", price="$$$$", f=["tech","home"],
        tags=["Portable","Battery-powered"],
        summary="A portable smart projector for backyard or living-room movie nights. ABC News includes it in its 2026 gift guide for dads.",
        pros=["Big-screen movies anywhere","Built-in apps and battery","Compact"],
        cons=["Not as bright as home-theater projectors"]),
   dict(name="Aura Carver Digital Photo Frame", badge="Best sentimental gift", price="$$$", f=["home","tech"],
        tags=["Wi-Fi photo frame"],
        summary="The whole family can add photos from their phones, so the frame keeps filling with new pictures. Forbes Vetted recommends it for dads.",
        pros=["Family adds photos remotely","Easy setup","Beautiful display"],
        cons=["Needs Wi-Fi"]),
   dict(name="Breville Barista Express Impress", badge="Best for coffee lovers", price="$$$$", f=["food","home"],
        tags=["Espresso machine"],
        summary="The #1 pick on our espresso machine list — café-quality espresso at home with a built-in grinder.",
        pros=["Built-in grinder","Helps beginners get great shots","Café drinks at home"],
        cons=["Expensive","Takes counter space"]),
   dict(name="Birdsnap TUC Smart Bird Feeder", badge="Best for nature lovers", price="$$$", f=["tech","home"],
        tags=["Camera","AI bird ID"],
        summary="Forbes Vetted's pick for birding dads: a smart feeder that streams live video and identifies bird species automatically.",
        pros=["Live HD bird video","Automatic species ID","Fun for the whole family"],
        cons=["Needs Wi-Fi and charging"]),
   dict(name="TUMI Alpha Split Travel Kit", badge="Best for travelers", price="$$$", f=["travel"],
        tags=["Toiletry kit"],
        summary="A durable, well-organized toiletry kit from TUMI for the dad who's always on the road.",
        pros=["Premium, durable build","Smart split organization","Looks sharp"],
        cons=["Expensive for a toiletry bag"]),
   dict(name="Hoka Clifton 10", badge="Best for active dads", price="$$", f=["travel"],
        tags=["Running shoe","Cushioned"],
        summary="Comfortable, cushioned running shoes for walks, runs and all-day wear. Forbes Vetted picks them for active dads.",
        pros=["Very cushioned and comfortable","Great for walking and running","Popular, well-reviewed"],
        cons=["Need to know his shoe size"]),
   dict(name="Logitech MX Keys Mini", badge="Best for his desk", price="$$", f=["tech"],
        tags=["Wireless keyboard","Backlit"],
        summary="A compact, backlit wireless keyboard that makes typing a pleasure. ABC News recommends it for dads.",
        pros=["Comfortable, quiet typing","Backlit keys","Works with multiple devices"],
        cons=["No number pad"]),
   dict(name="Anker MagGo Power Bank", badge="Best tech accessory", price="$$", f=["tech","travel"],
        tags=["Magnetic","Qi2 fast charging"],
        summary="A magnetic power bank that snaps onto his phone for wireless top-ups on the go.",
        pros=["Snaps on magnetically","Fast wireless charging","Compact"],
        cons=["Magnetic charging works best with recent iPhones"]),
   dict(name="Harry & David Meat & Cheese Gift Box", badge="Best food gift", price="$$", f=["food"],
        tags=["Snack box"],
        summary="A crowd-pleasing box of smoked meats, cheeses and crackers. Forbes Vetted includes it for dads.",
        pros=["Easy, crowd-pleasing gift","Great for sharing","Ships ready to gift"],
        cons=["Perishable — check delivery timing"]),
   dict(name="YETI Rambler Colster", badge="Best under $50", price="$", f=["food","travel"],
        tags=["Can cooler"],
        summary="A tough can cooler that keeps drinks cold far longer than a foam koozie — perfect for game days and cookouts.",
        pros=["Keeps drinks cold for hours","Extremely durable","Affordable"],
        cons=["Pricier than a basic koozie"]),
  ],
  "tips": [
   ("Feed his hobby","Gifts tied to what he already loves — coffee, travel, birdwatching, movies — land best."),
   ("Sentimental wins","A digital photo frame filled with family pictures often becomes his favorite gift."),
   ("Practical is good","Dads often love useful upgrades they'd never buy themselves."),
  ],
  "faq": [
   ("What do you get a dad who has everything?","Sentimental gifts like a digital photo frame, or experiences like movie nights with a projector."),
   ("What's a good gift for dad under $50?","The YETI Rambler Colster is a practical favorite."),
   ("When should I order?","Order by early December for holiday delivery, and watch for Black Friday sales."),
  ],
  "sources": [
   ("Forbes Vetted — Best gifts for dads","https://www.forbes.com/sites/forbes-personal-shopper/article/best-gift-for-dads/"),
   ("ABC News — 2026 gift guide for dads","https://abcnews.com/GMA/Shop/best-gifts-dad/story?id=126887452"),
  ],
 },
 {
  "slug": "gifts-for-mom", "kind": "gift", "icon": "gift", "tint": "tint-gift-mom", "short": "Gifts for Mom",
  "title": "The 10 Best Gifts for Mom in 2026",
  "card": "Thoughtful, cozy and sentimental gifts she'll truly use.",
  "lead": "From keepsakes to kitchen upgrades and cozy self-care, these are the gifts for mom that editors recommend most this season.",
  "price_notes": GIFT_NOTES,
  "filters": [("home","Home & cozy"),("kitchen","Kitchen"),("beauty","Beauty & self-care"),("sentimental","Sentimental")],
  "products": [
   dict(name="Aura Carver Digital Photo Frame", badge="Best overall", price="$$$", f=["sentimental","home"],
        tags=["Wi-Fi photo frame"],
        summary="Family members add photos from their phones, so mom always has new pictures to enjoy. A top pick in GiftList's 2026 guide for moms.",
        pros=["Family adds photos remotely","Easy for any age to use","Beautiful display"],
        cons=["Needs Wi-Fi"]),
   dict(name="Kindle Paperwhite", badge="Best for readers", price="$$$", f=["home"],
        tags=["E-reader","Warm light"],
        summary="A glare-free e-reader with a warm light for comfortable night reading — holds thousands of books.",
        pros=["Easy on the eyes","Warm light for bedtime reading","Long battery life"],
        cons=["Books are bought separately"]),
   dict(name="Ember Mug 3", badge="Best for coffee & tea lovers", price="$$", f=["kitchen","home"],
        tags=["Smart mug","Keeps drinks hot"],
        summary="Keeps coffee or tea at her perfect temperature — no more reheating a forgotten cup.",
        pros=["Drinks stay at the perfect temperature","App-controlled","Elegant design"],
        cons=["Pricey for a mug","Hand wash only"]),
   dict(name="Shark FlexStyle", badge="Best beauty tool", price="$$$$", f=["beauty"],
        tags=["Dryer + styler"],
        summary="A hair dryer that converts into a multi-styler — a popular alternative to the Dyson Airwrap.",
        pros=["Dries and styles","Works on all hair types","Far cheaper than a Dyson"],
        cons=["Takes some practice"]),
   dict(name="Le Creuset Signature Dutch Oven (5.5 qt)", badge="Best for the cook", price="$$$$", f=["kitchen"],
        tags=["Enameled cast iron"],
        summary="An heirloom-quality Dutch oven with a lifetime warranty — perfect for soups, stews and holiday meals.",
        pros=["Lasts a lifetime","Beautiful colors","Goes from oven to table"],
        cons=["Expensive","Heavy"]),
   dict(name="TheraFace Mask Glo", badge="Best self-care splurge", price="$$$$", f=["beauty"],
        tags=["LED face mask"],
        summary="An LED light therapy mask from Therabody for a relaxing nightly skincare routine.",
        pros=["Spa-style treatment at home","Cordless","Relaxing"],
        cons=["Expensive","Needs consistent use"]),
   dict(name="Sunbeam Royal Luxe Heated Throw", badge="Best cozy gift", price="$", f=["home"],
        tags=["Heated blanket","Auto shut-off"],
        summary="A soft heated throw with several heat settings and auto shut-off — instant coziness for under $50.",
        pros=["Very affordable","Several heat settings","Auto shut-off for safety"],
        cons=["Needs to be near an outlet"]),
   dict(name="LEGO Botanicals Orchid", badge="Flowers that never wilt", price="$", f=["home"],
        tags=["Build-and-display"],
        summary="A lifelike orchid she can build and display — no watering required.",
        pros=["Never needs watering","Relaxing build","Lovely décor"],
        cons=["Not a real plant"]),
   dict(name="LANEIGE Lip Sleeping Mask", badge="Best stocking stuffer", price="$", f=["beauty"],
        tags=["Overnight lip treatment"],
        summary="A cult-favorite overnight lip mask that leaves lips soft by morning — a perfect small add-on gift.",
        pros=["Beloved by beauty fans","Affordable treat","Lasts a long time"],
        cons=["Small jar"]),
   dict(name="Tell Me Your Life Story, Mom", badge="Best keepsake", price="$", f=["sentimental"],
        tags=["Guided journal"],
        summary="A guided journal with questions for mom to answer in her own words — a keepsake the family will treasure.",
        pros=["Meaningful and personal","Very affordable","Creates a family keepsake"],
        cons=["Takes time to fill in"]),
  ],
  "tips": [
   ("Make it personal","Sentimental gifts like photo frames and memory journals are often the most treasured."),
   ("Help her relax","Cozy and self-care gifts are consistent favorites for moms."),
   ("Upgrade everyday moments","A better mug, a heated throw or a Kindle makes daily routines nicer."),
  ],
  "faq": [
   ("What's the best gift for mom this year?","A digital photo frame the whole family can add pictures to is a top pick."),
   ("What's a good gift for mom under $50?","The Sunbeam heated throw, LEGO orchid or Tell Me Your Life Story journal."),
   ("What do you get a mom who has everything?","Sentimental gifts and experiences — photos, keepsakes and time together."),
  ],
  "sources": [
   ("GiftList — Christmas gifts for mom (2026)","https://giftlist.com/gift-guides/christmas-gifts-for-mom"),
   ("The Knot — Best gifts for your wife","https://www.theknot.com/content/romantic-gifts-for-wife"),
  ],
 },
]

SOON = []

PRICE_NOTE = {"$":"Under ~$300","$$":"About $300–$1,500","$$$":"About $1,000–$2,500","$$$$":"$2,500+"}

e = html.escape

LISTS = [c for c in CATS if c.get("kind") != "gift"]
GIFTS = [c for c in CATS if c.get("kind") == "gift"]
for c in GIFTS:
    c["filters"] = [("under50","Under $50"),("under150","Under $150"),("splurge","Splurge")] + c["filters"]
    for p in c["products"]:
        extra = {"$":["under50","under150"],"$$":["under150"],"$$$":[],"$$$$":["splurge"]}[p["price"]]
        p["f"] = p["f"] + [x for x in extra if x not in p["f"]]

RANK = {}   # product name -> (list cat, rank) for product lists
for c in LISTS:
    for n, p in enumerate(c["products"], 1):
        RANK.setdefault(p["name"], (c, n))
IN_GIFTS = {}   # product name -> [gift cats]
for c in GIFTS:
    for p in c["products"]:
        IN_GIFTS.setdefault(p["name"], []).append(c)

RELATED = {
 "best-tvs": ["best-projectors","best-wireless-earbuds","best-robot-vacuums"],
 "best-projectors": ["best-tvs","best-wireless-earbuds","best-standing-desks"],
 "best-electric-shavers": ["best-hair-dryers","best-wireless-earbuds","best-luggage"],
 "best-espresso-machines": ["best-air-fryers","best-cookware-sets","best-robot-vacuums"],
 "best-wireless-earbuds": ["best-tvs","best-projectors","best-luggage"],
 "best-air-fryers": ["best-cookware-sets","best-espresso-machines","best-robot-vacuums"],
 "best-robot-vacuums": ["best-air-fryers","best-mattresses","best-tvs"],
 "best-standing-desks": ["best-office-chairs","best-wireless-earbuds","best-projectors"],
 "best-mattresses": ["best-robot-vacuums","best-office-chairs","best-standing-desks"],
 "best-hair-dryers": ["best-electric-shavers","best-luggage","best-mattresses"],
 "best-office-chairs": ["best-standing-desks","best-wireless-earbuds","best-mattresses"],
 "best-luggage": ["best-wireless-earbuds","best-electric-shavers","best-hair-dryers"],
 "best-cookware-sets": ["best-air-fryers","best-espresso-machines","best-mattresses"],
 "gifts-for-him": ["gifts-for-dad","best-wireless-earbuds","best-electric-shavers"],
 "gifts-for-her": ["gifts-for-mom","best-hair-dryers","best-mattresses"],
 "gifts-for-dad": ["gifts-for-him","best-espresso-machines","best-projectors"],
 "gifts-for-mom": ["gifts-for-her","best-hair-dryers","best-cookware-sets"],
}
BY_SLUG = {c["slug"]: c for c in CATS}

def label(c):
    return c["short"] if c.get("kind") == "gift" else "Best " + c["short"]

def notes(cat):
    return cat.get("price_notes", PRICE_NOTE)

# ---------------------------------------------------------------- layout
def nav(active=""):
    is_list = active.startswith("best-")
    is_gift = active.startswith("gifts-")
    links = [("index.html","Home", active=="index.html"),
             ("index.html#categories","Best-of lists", is_list),
             ("index.html#gifts","Gift guides", is_gift),
             ("about.html","About", active=="about.html")]
    return "\n".join(f'<a href="{h}"{" aria-current=\"page\"" if cur else ""}>{e(l)}</a>' for h,l,cur in links)

def trim_desc(t, n=155):
    t = " ".join(t.split())
    if len(t) <= n: return t
    cut = t[:n].rsplit(" ", 1)[0].rstrip(",;:—-")
    return cut + "…"

def og_image(key):
    ph = PHOTOS.get(key) or PHOTOS["tv"]
    return f"https://images.unsplash.com/photo-{ph['id']}?auto=format&fit=crop&w=1200&h=630&q=75"

def page(fname, title, desc, body, active="", jsonld=None, image_key=None, ptype="website", noindex=False):
    canonical = f"{DOMAIN}/{'' if fname=='index.html' else fname}"
    desc = trim_desc(desc)
    img = og_image(image_key)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (jsonld or []))
    robots = '<meta name="robots" content="noindex">\n' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">\n'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="google-site-verification" content="kcC7Zvdq113b5_QDND_9pNeT6ufAG4TuTtjXcTjrYko" />
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7203025563112136" crossorigin="anonymous"></script>
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#1b2559">
<meta property="og:site_name" content="{e(SITE)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{ptype}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{e(img)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{e(img)}">
{ld}<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="preload" href="assets/adventor-bold.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html"><span class="logo-mark" aria-hidden="true">10</span>{e(SITE)}</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav">
{nav(active)}
    </nav>
  </div>
  <div class="progress" aria-hidden="true"><span></span></div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="index.html"><span class="logo-mark" aria-hidden="true">10</span>{e(SITE)}</a>
        <p>Short, honest lists of the best things to buy — researched from trusted expert reviews and updated regularly.</p>
      </div>
      <div>
        <h4>Best of</h4>
        <ul>{''.join(f'<li><a href="{c["slug"]}.html">{e(c["short"])}</a></li>' for c in LISTS)}</ul>
      </div>
      <div>
        <h4>Gift guides</h4>
        <ul>{''.join(f'<li><a href="{c["slug"]}.html">{e(c["short"])}</a></li>' for c in GIFTS)}</ul>
      </div>
      <div>
        <h4>Site</h4>
        <ul>
          <li><a href="about.html">About &amp; how we pick</a></li>
          <li><a href="disclosure.html">Affiliate disclosure</a></li>
          <li><a href="privacy.html">Privacy policy</a></li>
        </ul>
      </div>
    </div>
    <p class="fine">As an Amazon Associate we earn from qualifying purchases. Prices and availability change often — always check the retailer for current details. &copy; <span id="yr">2026</span> {e(SITE)}.</p>
  </div>
</footer>
<a class="to-top" href="#" aria-label="Back to top">Top</a>
<script src="assets/config.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
"""


NOUN = {"best-tvs":"TV","best-projectors":"projector","best-electric-shavers":"electric shaver","best-espresso-machines":"espresso machine",
 "best-wireless-earbuds":"wireless earbuds","best-air-fryers":"air fryer","best-robot-vacuums":"robot vacuum","best-standing-desks":"standing desk",
 "best-mattresses":"mattress","best-hair-dryers":"hair dryer","best-office-chairs":"office chair","best-luggage":"carry-on","best-cookware-sets":"cookware set"}
PLURAL = {"best-wireless-earbuds"}
WHO = {"gifts-for-him":"him","gifts-for-her":"her","gifts-for-dad":"dad","gifts-for-mom":"mom"}
QOVERRIDE = {
 ("best-tvs","Best OLED deal"):"What's the best OLED TV deal?",
 ("best-tvs","Best big screen on a budget"):"What's the best big-screen TV on a budget?",
 ("best-tvs","Best budget pick"):"What's the best budget TV?",
 ("best-tvs","Best giant-screen flagship"):"What's the best giant-screen TV?",
 ("best-projectors","Best pocket portable"):"What's the best pocket-size portable projector?",
 ("best-electric-shavers","Best premium rotary value"):"What's the best value premium rotary shaver?",
 ("best-electric-shavers","Best mid-range rotary"):"What's the best mid-range rotary shaver?",
 ("best-electric-shavers","Best hybrid shaver & trimmer"):"What's the best hybrid shaver and trimmer?",
 ("best-electric-shavers","Best budget foil shaver"):"What's the best budget foil shaver?",
 ("best-electric-shavers","Best budget rotary"):"What's the best budget rotary shaver?",
 ("best-espresso-machines","Best guided experience"):"What's the best espresso machine with guided brewing?",
 ("best-espresso-machines","Easiest to use"):"What's the easiest espresso machine to use?",
 ("best-espresso-machines","Best splurge"):"What's the best high-end espresso machine?",
 ("best-wireless-earbuds","Best noise cancelling"):"What are the best noise-cancelling earbuds?",
 ("best-wireless-earbuds","Best affordable AirPods"):"What are the best affordable AirPods?",
 ("best-wireless-earbuds","Best budget noise cancelling"):"What are the best budget noise-cancelling earbuds?",
 ("best-air-fryers","Best with a window"):"What's the best air fryer with a viewing window?",
 ("best-air-fryers","Best smart air fryer"):"What's the best smart air fryer?",
 ("best-robot-vacuums","Best tested by RTINGS"):None,
 ("best-robot-vacuums","Best mid-range vacuum + mop"):"What's the best mid-range robot vacuum and mop?",
 ("best-robot-vacuums","Best budget vacuum + mop"):"What's the best budget robot vacuum and mop?",
 ("best-standing-desks","Most customizable"):"What's the most customizable standing desk?",
 ("best-standing-desks","Most stable"):"What's the most stable standing desk?",
 ("best-standing-desks","Best curved desk"):"What's the best curved standing desk?",
 ("best-standing-desks","Best converter"):"What's the best standing desk converter?",
 ("best-mattresses","Best soft mattress"):"What's the best soft mattress?",
 ("best-mattresses","Best firm mattress"):"What's the best firm mattress?",
 ("best-hair-dryers","Best luxury dryer"):"What's the best luxury hair dryer?",
 ("best-hair-dryers","Best multi-styler"):"What's the best hair multi-styler?",
 ("best-hair-dryers","Best Airwrap alternative"):"What's the best Dyson Airwrap alternative?",
 ("best-hair-dryers","Best budget hot brush"):"What's the best budget hot air brush?",
 ("best-hair-dryers","Best for volume"):"What's the best hot brush for volume?",
 ("best-office-chairs","Best design"):"What's the best-looking ergonomic office chair?",
 ("best-office-chairs","Best ergonomics for the price"):"What's the best ergonomic office chair for the price?",
 ("best-office-chairs","Most adjustable"):"What's the most adjustable office chair?",
 ("best-luggage","Best carry-on"):"What's the best carry-on suitcase?",
 ("best-luggage","Most stylish carry-on"):"What's the most stylish carry-on?",
 ("best-luggage","Best large checked bag"):"What's the best large checked suitcase?",
 ("best-luggage","Best travel backpack"):"What's the best carry-on travel backpack?",
 ("best-luggage","Best personal item"):"What's the best personal item bag for flights?",
 ("best-cookware-sets","Best value stainless"):"What's the best value stainless steel cookware set?",
 ("best-cookware-sets","Best-looking set"):"What's the best-looking cookware set?",
 ("best-cookware-sets","Best starter set"):"What's the best cookware set for a first apartment?",
}

def question(cat, p):
    key = (cat["slug"], p["badge"])
    if key in QOVERRIDE: return QOVERRIDE[key]
    b = p["badge"]
    if not b.startswith("Best "): return None
    n = NOUN[cat["slug"]]; rest = b[5:]
    lead = "What are the best" if cat["slug"] in PLURAL else "What's the best"
    if rest == "overall": return f"{lead} {n} overall?"
    if rest.split()[0] in ("for", "under"): return f"{lead} {n} {rest}?"
    return f"{lead} {rest} {n}?"

def budget_pick(cat):
    for n, p in enumerate(cat["products"], 1):
        if n > 1 and any(w in p["badge"].lower() for w in ("budget", "under $", "value", "cheap")):
            return n, p
    for n, p in enumerate(cat["products"], 1):
        if n > 1 and p["price"] == "$":
            return n, p
    return None

def quick_answer(cat):
    ps = cat["products"]
    if cat.get("kind") == "gift":
        who = WHO[cat["slug"]]
        picks = [(1, ps[0]), (2, ps[1]), (3, ps[2])]
        cheap = next(((n, p) for n, p in enumerate(ps, 1) if p["price"] == "$" and n > 3), None)
        text = f"Our top gift ideas for {who} in 2026 are the {ps[0]['name']}, the {ps[1]['name']} and the {ps[2]['name']}."
        if cheap: text += f" Under $50, we like the {cheap[1]['name']}."
        others = picks[1:] + ([cheap] if cheap else [])
    else:
        n = NOUN[cat["slug"]]
        verb = "are" if cat["slug"] in PLURAL else "is"
        text = f"The best {n} for most people in 2026 {verb} the {ps[0]['name']}."
        others = [(2, ps[1])]
        bp = budget_pick(cat)
        if bp and bp[0] != 2: others.append(bp)
        third = next(((k, p) for k, p in enumerate(ps, 1) if k > 2 and (not bp or k != bp[0])), None)
        if third and len(others) < 3: others.append(third)
        others.sort(key=lambda x: x[0])
        text += " " + " ".join(f"{p['badge']}: the {p['name']}." for _, p in others)
    return text, [(1, ps[0])] + others

def answer_box(cat):
    text, picks = quick_answer(cat)
    top = cat["products"][0]
    items = "".join(f'<li><a href="#{cat["slug"]}-{k}"><span class="mini-sticker" aria-hidden="true">{k}</span><span><span class="qa-badge">{e(p["badge"])}</span> {e(p["name"])}</span></a></li>' for k, p in picks[1:])
    return f'''<div class="answer-box" id="quick-answer">
      <div class="top-pick">
        <span class="sticker big" aria-hidden="true">1</span>
        <div class="top-pick-txt">
          <h2 class="answer-title">Our top pick</h2>
          <p class="top-name"><a href="#{cat["slug"]}-1">{e(top["name"])}</a></p>
          <p class="top-why">{e(top["summary"].split(". ")[0].rstrip(".") + ".")}</p>
          <a class="btn buy" data-amazon href="{amz(top["name"])}" target="_blank" rel="sponsored nofollow noopener">Check price on Amazon</a>
        </div>
      </div>
      <div class="quick">
        <h2 class="answer-title">Quick answer</h2>
        <p class="answer-text">{e(text)}</p>
        <ul class="answer-list">{items}</ul>
      </div>
    </div>''', text

def compare_table(cat):
    rows = "".join(f'''<tr>
        <td class="ct-rank"><span class="mini-sticker">{k}</span></td>
        <th scope="row"><a href="#{cat["slug"]}-{k}">{e(p["name"])}</a></th>
        <td>{e(p["badge"])}</td>
        <td>{e(" · ".join(p["tags"]))}</td>
        <td class="ct-price">{e(notes(cat)[p["price"]])}</td>
        <td><a class="btn ct-btn" data-amazon href="{amz(p["name"])}" target="_blank" rel="sponsored nofollow noopener">See price</a></td>
      </tr>''' for k, p in enumerate(cat["products"], 1))
    caption = f"Comparison of the {len(cat['products'])} {'gifts' if cat.get('kind')=='gift' else 'picks'} in this guide"
    return f'''<div class="table-wrap"><table class="compare">
      <caption>{e(caption)}</caption>
      <thead><tr><th scope="col">#</th><th scope="col">Product</th><th scope="col">Best for</th><th scope="col">Key features</th><th scope="col">Price</th><th scope="col"><span class="vh">Buy</span></th></tr></thead>
      <tbody>{rows}</tbody></table></div>'''

def qa_section(cat):
    if cat.get("kind") == "gift": return ""
    out = []
    for k, p in enumerate(cat["products"], 1):
        q = question(cat, p)
        if not q: continue
        ans = f"{p['pros'][0]}; {p['pros'][1][0].lower()}{p['pros'][1][1:]}."
        out.append(f'<div class="qa"><h3>{e(q)}</h3><p><a href="#{cat["slug"]}-{k}"><strong>{e(p["name"])}</strong></a> — {e(ans)}</p></div>')
    if not out: return ""
    return f'''<section>
  <div class="wrap">
    <div class="section-head"><div><h2>Best {e(cat["short"].lower() if cat["short"] not in ("TVs",) else "TVs")} by need</h2><p>Quick answers to the questions shoppers ask most.</p></div></div>
    <div class="qa-grid">{"".join(out)}</div>
  </div>
</section>'''

def xref(cat, p):
    bits = []
    if cat.get("kind") == "gift" and p["name"] in RANK:
        lc, n = RANK[p["name"]]
        bits.append(f'Ranked #{n} in our <a href="{lc["slug"]}.html#{lc["slug"]}-{n}">{e(label(lc))}</a> list')
    if cat.get("kind") != "gift" and p["name"] in IN_GIFTS:
        links = " and ".join(f'<a href="{g["slug"]}.html">{e(g["short"])}</a>' for g in IN_GIFTS[p["name"]])
        bits.append(f"Also a top pick in our {links} guide")
    return f'<p class="xref">{". ".join(bits)}.</p>' if bits else ""

def product_card(cat, i, p):
    pid = f"{cat['slug']}-{i}"
    pros = "".join(f"<li>{e(x)}</li>" for x in p["pros"])
    cons = "".join(f"<li>{e(x)}</li>" for x in p["cons"])
    tags = "".join(f'<span class="pill">{e(t)}</span>' for t in p["tags"])
    return f"""
<article class="product{' is-top' if i == 1 else ''}" id="{pid}" data-f="{' '.join(p['f'])}">
  <div class="p-rank"><span class="sticker" aria-label="Rank {i}">{i}</span></div>
  <div class="p-body">
    <p class="badge">{e(p['badge'])}</p>
    <h3>{e(p['name'])}</h3>
    <div class="tags">{tags}<span class="pill price-pill" title="{e(notes(cat)[p['price']])}">{p['price']}</span></div>
    <p class="summary">{e(p['summary'])}</p>{xref(cat, p)}
    <div class="proscons">
      <div class="pros"><h4>What we like</h4><ul>{pros}</ul></div>
      <div class="cons"><h4>Keep in mind</h4><ul>{cons}</ul></div>
    </div>
    <div class="cta-row">
      <a class="btn buy" data-amazon href="{amz(p['name'])}" target="_blank" rel="sponsored nofollow noopener">Check price on Amazon</a>
      <small>{e(notes(cat)[p['price']])}</small>
    </div>
  </div>
</article>"""

def rel_card(c):
    is_gift = c.get("kind") == "gift"
    media = (f'<div class="rel-photo">{photo(c["icon"], sizes="(max-width: 760px) 100vw, 360px")}</div>' if c["icon"] in PHOTOS
             else f'<div class="rel-photo {c["tint"]}"><span class="gift-ico">{ICONS["gift"]}</span></div>')
    return (f'<a class="rel-card" href="{c["slug"]}.html">{media}<span class="rel-body"><span class="rel-title">{e(label(c))}</span>'
            f'<span class="rel-sub">{"Top gift" if is_gift else "#1 pick"}: {e(c["products"][0]["name"])}</span></span></a>')

def guide(cat):
    quick = "".join(f"""
    <div class="quick-row"><span class="n">{i}</span>
      <div><a class="name" href="#{cat['slug']}-{i}">{e(p['name'])}</a><span class="bf">{e(p['badge'])}</span></div>
      <a class="btn" data-amazon href="{amz(p['name'])}" target="_blank" rel="sponsored nofollow noopener">See price</a></div>"""
        for i,p in enumerate(cat["products"],1))
    chips = '<button class="chip" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" data-filter="{k}" aria-pressed="false">{e(v)}</button>' for k,v in cat["filters"])
    cards = "".join(product_card(cat,i,p) for i,p in enumerate(cat["products"],1))
    tips = "".join(f'<div class="tip"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a,b in cat["tips"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q,a in cat["faq"])
    srcs = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{e(t)}</a></li>' for t,u in cat["sources"])
    is_gift = cat.get("kind") == "gift"
    kind_label = "Gift guide" if is_gift else "Buying guide"
    src_names = ", ".join(t.split(" — ")[0] for t, _ in cat["sources"])
    if is_gift:
        how_text = (f"We started with what shoppers search for most, then compared this year's gift guides from {src_names} "
                    "and kept the gifts that appear again and again. We favored gifts that are well-reviewed, easy to buy on Amazon, "
                    "and cover a range of budgets. Where a gift also appears in one of our product lists, we link to the full comparison.")
    else:
        how_text = (f"We compared the latest hands-on testing and buying guides from {src_names}, and kept the products "
                    "that consistently rank near the top. Then we grouped them by what each is best for — overall, budget, premium and specific needs — "
                    "and summarized the strengths and trade-offs in plain language. We haven't tested every product ourselves; our picks reflect the consensus of expert testers.")
    related = "".join(rel_card(BY_SLUG[r]) for r in RELATED.get(cat["slug"], []))
    more = "".join(f'<a class="chip-link" href="{c["slug"]}.html">{e(label(c))}</a>' for c in LISTS + GIFTS if c["slug"] != cat["slug"] and c["slug"] not in RELATED.get(cat["slug"], []))
    rail = "".join(f'<a href="#{cat["slug"]}-{k}" title="{e(p["name"])}">{k}</a>' for k, p in enumerate(cat["products"], 1))
    answer_html, answer_text = answer_box(cat)
    page_url = f"{DOMAIN}/{cat['slug']}.html"
    section_name = "Gift guides" if is_gift else "Best-of lists"
    ld = [
      {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":f"{DOMAIN}/"},
        {"@type":"ListItem","position":2,"name":section_name,"item":f"{DOMAIN}/#{'gifts' if is_gift else 'categories'}"},
        {"@type":"ListItem","position":3,"name":cat["short"],"item":page_url}]},
      {"@context":"https://schema.org","@type":"Article","headline":cat["title"],"description":cat["lead"],"abstract":answer_text,
        "datePublished":UPDATED_ISO,"dateModified":UPDATED_ISO,"mainEntityOfPage":page_url,"image":og_image(cat["icon"]),
        "author":{"@type":"Organization","name":f"{SITE} editors","url":f"{DOMAIN}/about.html"},
        "publisher":{"@type":"Organization","name":SITE,"url":f"{DOMAIN}/"}},
      {"@context":"https://schema.org","@type":"ItemList","name":cat["title"],"numberOfItems":len(cat["products"]),
        "itemListOrder":"https://schema.org/ItemListOrderAscending",
        "itemListElement":[{"@type":"ListItem","position":n,"name":p["name"],"url":f"{page_url}#{cat['slug']}-{n}"} for n,p in enumerate(cat["products"],1)]},
      {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in cat["faq"]]
        + ([{"@type":"Question","name":question(cat,p),"acceptedAnswer":{"@type":"Answer","text":f"The {p['name']}. {p['summary']}"}}
            for p in cat["products"] if cat.get("kind")!="gift" and question(cat,p)])},
    ]
    if cat["icon"] in PHOTOS:
        hero_media = f'<figure class="hero-photo {cat["tint"]}">{photo(cat["icon"], eager=True)}<figcaption>{credit(cat["icon"])}</figcaption></figure>'
    else:
        hero_media = f'<div class="hero-art {cat["tint"]}">{ICONS[cat["icon"]]}</div>'
    body = f"""
<section class="guide-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="index.html#{"gifts" if is_gift else "categories"}">{"Gift guides" if is_gift else "Best-of lists"}</a> / {e(cat['short'])}</div>
    <div class="guide-hero-inner">
      <div>
        <h1>{e(cat['title'])}</h1>
        <p class="lead">{e(cat['lead'])}</p>
        <p class="byline">{kind_label} by {e(SITE)} editors, based on {len(cat["sources"])} expert sources. Updated <time datetime="{UPDATED_ISO}">{UPDATED_LONG}</time>.</p>
      </div>
      {hero_media}
    </div>
    {answer_html}
    <p class="disclosure-note">We may earn a commission when you buy through links on this page, at no extra cost to you. <a href="disclosure.html">Learn more</a>.</p>
  </div>
</section>
<nav class="rank-rail" aria-label="Jump to a pick"><div class="wrap"><span class="rail-label">Jump to</span><div class="rail-links">{rail}</div></div></nav>
<section>
  <div class="wrap">
    <div class="section-head"><div><h2>Comparison at a glance</h2><p>All {len(cat["products"])} {"gifts" if is_gift else "picks"} side by side. Tap a name for the full details.</p></div></div>
    {compare_table(cat)}
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><div><h2>Our picks in detail</h2><p>Filter by what matters to you.</p></div></div>
    <div class="filters" role="group" aria-label="Filter picks">{chips}</div>
    <div class="products">{cards}</div>
  </div>
</section>
{qa_section(cat)}
<section>
  <div class="wrap">
    <div class="section-head"><div><h2>How to choose</h2></div></div>
    <div class="tips">{tips}</div>
  </div>
</section>
<section>
  <div class="wrap prose">
    <h2>Questions people ask</h2>
    {faq}
    <h2 id="how-we-picked">How we picked</h2>
    <p>{how_text}</p>
    <p class="sources">Main sources for this guide:</p>
    <ul class="sources">{srcs}</ul>
    <p class="sources">Prices change often, so always check the current price before you buy. Read our <a href="about.html">full method</a> and <a href="disclosure.html">affiliate disclosure</a>.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="section-head"><div><h2>Keep browsing</h2><p>More shortlists people read next.</p></div></div>
    <div class="related">{related}</div>
    <div class="more-links">{more}</div>
  </div>
</section>"""
    full = f"{cat['title']} | {SITE}"
    title = cat.get("seo_title") or (full if len(full) <= 65 else cat["title"])
    return page(cat["slug"]+".html", title, cat["lead"], body, active=cat["slug"]+".html",
                jsonld=ld, image_key=cat["icon"], ptype="article")

def home():
    cards = "".join(f"""
<a class="cat-card" href="{c['slug']}.html" data-k="{e(' '.join([c['short'], c['card']] + [p['name'] for p in c['products']]).lower())}">
  <div class="cat-photo">{photo(c['icon'], sizes="(max-width: 760px) 100vw, 360px")}</div>
  <div class="cat-body">
    <h3>Best {e(c['short'])}</h3><p>{e(c['card'])}</p>
    <span class="cat-top"><span class="mini-sticker" aria-hidden="true">1</span><span><span class="vh">Number one pick: </span>{e(c['products'][0]['name'])}</span></span>
  </div>
</a>""" for c in LISTS)
    gifts = "".join(f"""
<a class="gift-card {c['tint']}" href="{c['slug']}.html">
  <h3>{e(c['short'])}</h3><p>{e(c['card'])}</p>
  <ul class="gift-peek">{''.join(f'<li>{e(p["name"])}</li>' for p in c['products'][:3])}</ul>
  <span class="go">See all 10 gifts</span>
</a>""" for c in GIFTS)
    receipt = "".join(f"""
     <li><a href="{c['slug']}.html"><span class="r-cat">{e(c['short'])}</span><span class="r-dots" aria-hidden="true"></span><span class="r-pick">{e(c['products'][0]['name'])}</span></a></li>""" for c in LISTS)
    index = [{"t": label(c), "u": c["slug"] + ".html"} for c in LISTS + GIFTS]
    index += [{"t": p["name"], "u": f'{c["slug"]}.html#{c["slug"]}-{k}', "s": f'#{k} in {label(c)}'} for c in LISTS + GIFTS for k, p in enumerate(c["products"], 1)]
    popular = "".join(f'<a href="{c["slug"]}.html">{e(c["short"])}</a>' for c in [BY_SLUG[x] for x in ("best-tvs","best-wireless-earbuds","best-air-fryers","best-robot-vacuums","gifts-for-him","gifts-for-her")])
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
   <div class="hero-copy">
    <h1>The ten best of everything you’re about to buy.</h1>
    <p class="lead">We read the expert reviews and keep only the top 10 in each category, so you can choose in minutes instead of evenings.</p>
    <form class="search" role="search" action="#" onsubmit="return false">
      <label class="vh" for="q">Search products and guides</label>
      <input id="q" type="search" placeholder="Search products, like “earbuds”" autocomplete="off">
      <ul class="search-results" id="results" role="listbox" hidden></ul>
    </form>
    <p class="popular"><span>Popular:</span>{popular}</p>
   </div>
   <div class="receipt" aria-labelledby="receipt-title">
     <span class="sticker big slap" aria-hidden="true">1</span>
     <h2 id="receipt-title">This month’s #1 picks</h2>
     <ol class="receipt-list">{receipt}</ol>
     <p class="receipt-foot">Updated {UPDATED}</p>
   </div>
  </div>
  <script type="application/json" id="search-index">{json.dumps(index, ensure_ascii=False)}</script>
</section>
<section id="gifts" class="gifts-band">
  <div class="wrap">
    <div class="section-head"><div><h2>Holiday gift guides</h2><p id="countdown">The 10 best gifts for everyone on your list.</p></div></div>
    <div class="gift-grid">{gifts}</div>
  </div>
</section>
<section id="categories">
  <div class="wrap">
    <div class="section-head"><div><h2>Every top 10</h2><p>Pick a category. Each card shows our #1 pick.</p></div></div>
    <div class="cat-grid">{cards}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="trust">
      <div><h3>Researched, not guessed</h3><p>Every pick comes from the consensus of trusted, hands-on reviewers, and we link our sources on every list.</p></div>
      <div><h3>Every budget</h3><p>Each list mixes budget, mid-range and premium options, so there’s a pick for you.</p></div>
      <div><h3>Kept up to date</h3><p>We refresh lists as new models launch and add new guides every week.</p></div>
    </div>
  </div>
</section>"""
    home_ld = [
      {"@context":"https://schema.org","@type":"WebSite","name":SITE,"url":f"{DOMAIN}/"},
      {"@context":"https://schema.org","@type":"Organization","name":SITE,"url":f"{DOMAIN}/",
        "email":"amazonassociates9901@gmail.com"},
      {"@context":"https://schema.org","@type":"ItemList","name":f"{SITE} buying guides and gift guides",
        "itemListElement":[{"@type":"ListItem","position":n,"name":c["title"],"url":f"{DOMAIN}/{c['slug']}.html"} for n,c in enumerate(LISTS+GIFTS,1)]},
    ]
    return page("index.html", f"{SITE}: Best Products & Gift Guides for 2026",
                "Short, honest top-10 lists and holiday gift guides — the best TVs, earbuds, air fryers, gifts for him and her, and more, based on expert reviews.", body, "index.html", jsonld=home_ld, image_key="home")

def simple(fname, title, inner, desc):
    body = f'<section class="guide-hero"><div class="wrap prose"><div class="crumbs"><a href="index.html">Home</a> / {e(title)}</div><h1>{e(title)}</h1>{inner}</div></section>'
    return page(fname, f"{title} | {SITE}", desc, body, fname, noindex=(fname=="404.html"))

ABOUT = f"""
<p class="lead">{SITE} makes buying decisions easier. Instead of reading a dozen long reviews, you get one clear, short list.</p>
<h2>How we pick</h2>
<p>For each category, we study the latest buying guides and hands-on reviews from respected independent testers. We look for products that show up again and again near the top, then group them by what they're best for — overall, budget, gaming, bright rooms and so on.</p>
<p>We write every summary in our own words and link our sources at the bottom of each list so you can read more. When we haven't tested a product ourselves, we say so — the picks reflect expert consensus, not made-up hands-on claims.</p>
<h2>How we make money</h2>
<p>Some links on this site are affiliate links. If you buy through them, we may earn a small commission at no extra cost to you. This never changes which products we recommend. Read our <a href="disclosure.html">full disclosure</a>.</p>
<h2>Photo credits</h2>
<p>Category photos are from <a href="https://unsplash.com/?utm_source=the_shortlist&amp;utm_medium=referral">Unsplash</a> and used under the Unsplash License. Thank you to Prydumano Design, Valerion, F\u00e1bio Alves, Becca Tapert, atelierbyvineeth, Mitchell Luo, Onur Binay, ergonofis, Dina Makhmutova, Shubham Dhage, Giorgio Trovato, American Green Travel and Janko Ferli\u010d.</p>
<h2>Contact</h2>
<p>Questions, corrections or suggestions? Email us at <a href="mailto:amazonassociates9901@gmail.com">amazonassociates9901@gmail.com</a>.</p>
"""
DISCLOSURE = f"""
<p>{SITE} is reader-supported. Some links on this website are affiliate links, which means we may earn a commission if you click a link and make a purchase — at no additional cost to you.</p>
<p><strong>{SITE} is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate we earn from qualifying purchases.</strong></p>
<p>Commissions never influence which products we include or how we rank them. Our picks are based on research into independent expert reviews, as explained on our <a href="about.html">About page</a>.</p>
<p>Prices and availability change frequently. Always confirm the current price and details on the retailer's website before buying.</p>
"""
PRIVACY = f"""
<p><em>Last updated: {UPDATED}</em></p>
<h2>What we collect</h2>
<p>{SITE} does not require accounts and does not ask for personal information. Like most websites, our hosting provider may automatically log basic technical data such as your IP address, browser type and pages visited, for security and performance.</p>
<h2>Affiliate links and cookies</h2>
<p>When you click an affiliate link (for example, to Amazon), that retailer may place cookies in your browser to track the referral. Those cookies are controlled by the retailer and covered by their privacy policy, not ours.</p>
<h2>Advertising and cookies</h2>
<p>We use Google AdSense to show ads on this site. Google and its partners use cookies to serve ads based on your previous visits to this and other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to our site and/or other sites on the internet.</p>
<p>You can opt out of personalized advertising by visiting <a href="https://adssettings.google.com" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies for personalized advertising at <a href="https://www.aboutads.info/choices" target="_blank" rel="noopener">aboutads.info</a>. Learn more about <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from sites that use its services</a>.</p>
<p>Visitors in the European Economic Area, the UK and Switzerland will be asked for consent before personalized ads are shown.</p>
<h2>Analytics</h2>
<p>If we add analytics in the future to understand which pages are useful, we will update this policy to say which service we use and what it collects.</p>
<h2>Contact</h2>
<p>Questions about privacy? Email <a href="mailto:amazonassociates9901@gmail.com">amazonassociates9901@gmail.com</a>.</p>
"""

CONFIG_JS = """/* ============================================================
   EDIT THIS FILE to add your Amazon Associates tracking ID.
   Replace YOURTAG-20 with the tag Amazon gives you (keep the quotes).
   Every "Check price" button on the site will then use it.
   ============================================================ */
window.SITE_CONFIG = {
  amazonTag: "shortlisttop1-20"
};
"""
SITE_JS = """(function () {
  var doc = document;
  // Mobile menu
  var btn = doc.querySelector('.menu-btn'), nav = doc.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  // Affiliate tag
  var tag = (window.SITE_CONFIG || {}).amazonTag;
  if (tag && tag !== 'YOURTAG-20') {
    doc.querySelectorAll('a[data-amazon]').forEach(function (a) {
      try { var u = new URL(a.href); u.searchParams.set('tag', tag); a.href = u.toString(); } catch (e) {}
    });
  }
  // Filters
  var chips = doc.querySelectorAll('.chip');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.getAttribute('data-filter');
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      doc.querySelectorAll('.product').forEach(function (p) {
        p.hidden = !(f === 'all' || (' ' + p.getAttribute('data-f') + ' ').indexOf(' ' + f + ' ') > -1);
      });
    });
  });
  // Reading progress + back to top
  var bar = doc.querySelector('.progress span'), top = doc.querySelector('.to-top'), isGuide = !!doc.querySelector('.products');
  function onScroll() {
    var h = doc.documentElement, max = h.scrollHeight - h.clientHeight, y = h.scrollTop || doc.body.scrollTop;
    if (bar && isGuide) bar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    if (top) top.classList.toggle('show', y > 1400);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  // Rank rail: highlight the pick in view
  var rail = doc.querySelectorAll('.rail-links a');
  if (rail.length && 'IntersectionObserver' in window) {
    var map = {}; rail.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) {
          rail.forEach(function (a) { a.removeAttribute('aria-current'); });
          var a = map[en.target.id]; if (a) { a.setAttribute('aria-current', 'true'); }
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    doc.querySelectorAll('.product').forEach(function (p) { io.observe(p); });
  }
  // Holiday countdown
  var cd = doc.getElementById('countdown');
  if (cd) {
    var now = new Date(), xmas = new Date(now.getFullYear(), 11, 25);
    var days = Math.ceil((xmas - now) / 864e5);
    if (days > 1 && days < 70) cd.textContent = 'Christmas is ' + days + ' days away. Here are the 10 best gifts for everyone on your list.';
  }
  // Search
  var q = doc.getElementById('q'), out = doc.getElementById('results'), idxEl = doc.getElementById('search-index');
  if (q && out && idxEl) {
    var idx = JSON.parse(idxEl.textContent);
    function esc(t) { return t.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    q.addEventListener('input', function () {
      var v = q.value.trim().toLowerCase();
      if (v.length < 2) { out.hidden = true; out.innerHTML = ''; return; }
      var words = v.split(/\\s+/), hits = idx.filter(function (it) {
        var t = (it.t + ' ' + (it.s || '')).toLowerCase();
        return words.every(function (w) { return t.indexOf(w) > -1; });
      }).slice(0, 8);
      out.innerHTML = hits.length ? hits.map(function (it) {
        return '<li><a href="' + it.u + '"><strong>' + esc(it.t) + '</strong>' + (it.s ? '<span>' + esc(it.s) + '</span>' : '<span>Guide</span>') + '</a></li>';
      }).join('') : '<li class="none">No match yet. Try a category like “TV”, “coffee” or “gifts”.</li>';
      out.hidden = false;
    });
    q.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { var a = out.querySelector('a'); if (a) location.href = a.href; }
      if (e.key === 'Escape') { out.hidden = true; }
    });
  }
  var y = doc.getElementById('yr'); if (y) y.textContent = new Date().getFullYear();
})();
"""
FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#ffcf33"/><text x="32" y="42" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-size="28" font-weight="800" fill="#1b2559">10</text></svg>'

README = f"""THE SHORTLIST — YOUR AFFILIATE WEBSITE
======================================

1) ADD YOUR AMAZON TAG
   Open  assets/config.js  in any text editor (Notepad, TextEdit).
   Replace YOURTAG-20 with your Amazon Associates tracking ID. Save.

2) PUT THE SITE ONLINE (free, ~1 minute)
   - Go to https://app.netlify.com/drop
   - Drag this whole folder onto the page.
   - Netlify gives you a live web address. Create a free account to keep it.

3) BEFORE APPLYING TO AMAZON ASSOCIATES
   - If you move to a custom domain later, ask Claude to update the
     sitemap and canonical links to the new address.
   - Apply at https://affiliate-program.amazon.com using your live site address.

4) RENAMING THE SITE
   The name "{SITE}" appears in each .html file. Use your editor's
   Find & Replace across files, or ask Claude to regenerate with a new name.

5) ADDING NEW LISTS
   Ask Claude: "Add a top 10 headphones page to my site" and upload this folder.
"""

def main():
    keep = set()
    if os.path.exists(OUT):
        for n in os.listdir(OUT):
            if n in keep: continue
            fp = os.path.join(OUT, n)
            shutil.rmtree(fp) if os.path.isdir(fp) else os.remove(fp)
    os.makedirs(OUT+"/assets", exist_ok=True)
    shutil.copy(STYLE, OUT+"/assets/style.css")
    shutil.copy(os.path.join(HERE, "fonts", "adventor-bold.woff"), OUT+"/assets/adventor-bold.woff")
    w = lambda p,s: open(os.path.join(OUT,p),"w").write(s)
    w("index.html", home())
    for c in CATS: w(c["slug"]+".html", guide(c))
    w("about.html", simple("about.html","About us",ABOUT,f"How {SITE} researches and picks the products in our top-10 buying guides and gift guides, and how we make money."))
    w("disclosure.html", simple("disclosure.html","Affiliate disclosure",DISCLOSURE,f"How {SITE} earns money through affiliate links."))
    w("privacy.html", simple("privacy.html","Privacy policy",PRIVACY,f"How {SITE} handles your information, cookies and affiliate links. We don't require accounts or collect personal data."))
    w("assets/config.js", CONFIG_JS); w("assets/site.js", SITE_JS); w("assets/favicon.svg", FAVICON)
    pages = ["","about.html","disclosure.html","privacy.html"]+[c["slug"]+".html" for c in CATS]
    w("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{DOMAIN}/{p}</loc><lastmod>{UPDATED_ISO}</lastmod></url>\n" for p in pages)+"</urlset>\n")
    bots = ["Googlebot","Bingbot","OAI-SearchBot","ChatGPT-User","GPTBot","PerplexityBot","Perplexity-User",
            "Claude-SearchBot","Claude-User","ClaudeBot","Google-Extended","Applebot","DuckDuckBot"]
    robots = "# Search engines and AI assistants are welcome to read and cite this site.\n"
    robots += "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    robots += f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
    w("robots.txt", robots)
    llms = f"# {SITE}\n\n> Short, independent top-10 buying guides and holiday gift guides. Each guide summarizes the consensus of trusted expert reviewers, links its sources, and is updated regularly. Last updated {UPDATED_LONG}.\n\n"
    llms += "## Buying guides\n\n" + "".join(f"- [{c['title']}]({DOMAIN}/{c['slug']}.html): {quick_answer(c)[0]}\n" for c in LISTS)
    llms += "\n## Gift guides\n\n" + "".join(f"- [{c['title']}]({DOMAIN}/{c['slug']}.html): {quick_answer(c)[0]}\n" for c in GIFTS)
    llms += f"\n## About\n\n- [How we pick]({DOMAIN}/about.html)\n- [Affiliate disclosure]({DOMAIN}/disclosure.html)\n"
    w("llms.txt", llms)
    w("404.html", simple("404.html","Page not found",'<p>Sorry, that page doesn\'t exist. <a href="index.html">Go to the homepage</a>.</p>',"Page not found"))
    w("README.txt", README)
    w("ads.txt", "google.com, pub-7203025563112136, DIRECT, f08c47fec0942fa0\n")
    # Google Search Console file verification -- never remove
    w("google6a61f04b9d521fa6.html", "google-site-verification: google6a61f04b9d521fa6.html")
    print("built", sorted(os.listdir(OUT)))

main()
