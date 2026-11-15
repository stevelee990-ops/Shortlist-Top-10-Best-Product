#!/usr/bin/env python3
"""Generates the static affiliate site into ./site"""
import html, os, shutil, urllib.parse, json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "public")   # what Netlify publishes
STYLE = os.path.join(HERE, "style.css")              # edit styles here
SITE = "The Shortlist"
DOMAIN = "https://the-shortlist-top10best.netlify.app"   # change after you buy a domain
UPDATED = "November 2026"
UPDATED_ISO = "2026-11-15"
UPDATED_LONG = "November 15, 2026"

ICONS = {
 "airpurifier": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="20" y="10" width="24" height="42" rx="6"/><path d="M26 30h12M26 36h12M26 42h12"/><circle cx="32" cy="19" r="3"/><path d="M10 14c3-2 5 2 8 0M8 24c3-2 5 2 8 0M48 14c3-2 5 2 8 0M50 24c3-2 5 2 8 0" stroke-width="2.5" opacity=".7"/></svg>',
 "gamingchair": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 4h20l-2 28H24z"/><path d="M28 8h8" stroke-width="2.5" opacity=".7"/><path d="M18 32h28v6H18z"/><path d="M14 22v10M50 22v10"/><path d="M32 38v8M20 52l12-6 12 6"/></svg>',
 "soundbar": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="30" width="56" height="12" rx="5"/><circle cx="14" cy="36" r="1.5" fill="currentColor"/><circle cx="50" cy="36" r="1.5" fill="currentColor"/><path d="M26 36h12" stroke-width="2.5" opacity=".7"/><path d="M24 20a12 12 0 0 1 16 0M19 14a19 19 0 0 1 26 0" stroke-width="2.5" opacity=".7"/></svg>',
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
 "stocking": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="22" y="3" width="24" height="9" rx="2"/><path d="M24 12v22L12 42c-5 4-2 12 5 11l10-2c6-1 10-5 13-10l4-7V12"/><path d="M26 22h16" stroke-width="2" opacity=".7"/></svg>',
 "heater": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="10" y="8" width="44" height="38" rx="6"/><path d="M20 16v22M28 16v22M36 16v22M44 16v22" stroke-width="2.5" opacity=".7"/><path d="M16 46v4M48 46v4"/></svg>',
 "humidifier": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 22h28l4 26a4 4 0 0 1-4 4H18a4 4 0 0 1-4-4z"/><path d="M24 22v-4h16v4"/><circle cx="32" cy="38" r="5"/><path d="M26 12c0-4 4-4 4-8M34 12c0-4 4-4 4-8" stroke-width="2.5" opacity=".7"/></svg>',
 "coffeemaker": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4h40v10H12zM12 14v38h40"/><path d="M20 14l4 8h16l4-8" stroke-width="2.5" opacity=".7"/><path d="M22 30h20v12a6 6 0 0 1-6 6h-8a6 6 0 0 1-6-6z"/><path d="M42 33h3a3 3 0 0 1 0 6h-3"/></svg>',
 "controller": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 14h24c8 0 13 6 15 16l2 10c1 6-6 10-11 5l-6-6H20l-6 6c-5 5-12 1-11-5l2-10c2-10 7-16 15-16z"/><path d="M18 24v10M13 29h10"/><circle cx="42" cy="26" r="2"/><circle cx="48" cy="32" r="2"/></svg>',
 "stickvac": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M40 4l-8 38"/><rect x="34" y="14" width="10" height="14" rx="3" transform="rotate(12 39 21)"/><path d="M16 44h26a4 4 0 0 1 4 4v2H12v-2a4 4 0 0 1 4-4z"/><path d="M38 4h6" stroke-width="2.5" opacity=".7"/></svg>',
 "knife": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 48L44 12c6 0 9 4 8 9L26 47z"/><path d="M26 47l-6 6"/><path d="M14 52l-6-4" stroke-width="2.5"/><path d="M8 52h48" stroke-width="2.5" opacity=".7"/></svg>',
 "mixer": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 52h40"/><path d="M14 52V18"/><path d="M10 10h30a10 10 0 0 1 10 10v2H10z"/><path d="M32 22v8" stroke-width="2.5" opacity=".7"/><path d="M22 32h22l-3 14H25z"/></svg>',
 "blender": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 4h24l-4 30H24z"/><path d="M44 10h6v14h-8" stroke-width="2.5"/><path d="M26 22l6-4 6 4" stroke-width="2.5" opacity=".7"/><rect x="18" y="34" width="28" height="16" rx="4"/><circle cx="32" cy="42" r="3"/></svg>',
 "smartwatch": '<svg viewBox="0 0 64 56" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M24 4h16l2 10H22zM24 52h16l2-10H22z"/><rect x="18" y="14" width="28" height="28" rx="7"/><path d="M32 22v6l5 3" stroke-width="2.5" opacity=".7"/><path d="M46 24h3v8h-3"/></svg>',
}

PHOTOS = {
 "airpurifier": dict(id="1730299789489-b55bf96b22bf", alt="A hand resting on top of a black and silver air purifier", by="Mat\u00fa\u0161 Gocman", user="matgocman", page="https://unsplash.com/photos/a-persons-hand-is-on-top-of-a-black-and-silver-air-puri-KNJW4jA6_JI"),
 "gamingchair": dict(id="1551033541-2075d8363c66", alt="A black and gray gaming chair at a desk with a desktop computer", by="Balkouras Nicos", user="ba1kouras", page="https://unsplash.com/photos/turned-on-desktop-computer-set-with-black-and-gray-leather-gaming-chair-ncOQxZe8Krw"),
 "soundbar": dict(id="1604914416956-38b08c516877", alt="A flat-screen TV on a wooden table in a living room", by="Jonas Leupe", user="jonasleupe", page="https://unsplash.com/photos/black-flat-screen-tv-on-brown-wooden-table-2RyHepsRFqE"),
 "smartwatch": dict(id="1659366100463-9e29a63adcc2", alt="A smartwatch showing a heart rate reading on a person's wrist", by="Nik", user="helloimnik", page="https://unsplash.com/photos/smartwatch-heart-rate-monitor-on-wrist-BR8MqYyOPiU"),
 "headphones": dict(id="1599669454699-248893623440", alt="Black wireless over-ear headphones on a dark surface", by="Jason Leung", user="ninjason", page="https://unsplash.com/photos/black-wireless-headphones-on-black-surface-xR4JHzr69Og"),
 "stickvac": dict(id="1631016042350-a3a5a5cdf2e0", alt="A black and red cordless stick vacuum cleaner", by="eMotion Tech", user="medias_emotiontech", page="https://unsplash.com/photos/black-and-red-stick-vacuum-cleaner-D971boKoaC8"),
 "knife": dict(id="1646754303099-e6249e0b0d71", alt="A set of kitchen knives in a wooden knife block", by="Ahmed Zalabany", user="amzmahmoud", page="https://unsplash.com/photos/a-set-of-knives-sitting-on-top-of-a-wooden-block-ToJf8f0v6U0"),
 "mixer": dict(id="1564940735784-b15466e8dc09", alt="A green stand mixer on a kitchen counter", by="Kaur Kristjan", user="badgerblack", page="https://unsplash.com/photos/green-stand-mixer-TpDFsRWfNsw"),
 "blender": dict(id="1622818426197-d54f85b88690", alt="A blender filled with fruit and greens for a smoothie", by="Nature Zen", user="nature_zen", page="https://unsplash.com/photos/a-blender-filled-with-ingredients-to-make-a-smoothie-oJzx58W1__M"),
 "chair": dict(id="1626379501846-0df4067b8bb9", alt="A black office chair in a bright room", by="Giorgio Trovato", user="giorgiotrovato", page="https://unsplash.com/photos/black-and-silver-office-rolling-chair-beside-mirror-gI9rvJK61L8"),
 "luggage": dict(id="1639597784714-4905e95de813", alt="Three pieces of white luggage in a room", by="American Green Travel", user="americangreentravel", page="https://unsplash.com/photos/three-pieces-of-white-luggage-sitting-in-a-room-Whnjjhi8OfQ"),
 "cookware": dict(id="1580929753603-10519c6e480a", alt="Stainless steel pots on a gas stove", by="Janko Ferli\u010d", user="itfeelslikefilm", page="https://unsplash.com/photos/stainless-steel-cooking-pots-on-gas-stove-KwU5Cl0LSXs"),
 "desk": dict(id="1623177623442-979c1e42c255", alt="Wooden standing desk in a home office", by="ergonofis", user="ergonofis", page="https://unsplash.com/photos/wooden-standing-desk-in-home-office-tdnYk4qOGhc"),
 "mattress": dict(id="1762199904138-d163fe89540a", alt="A neatly made bed with white linens", by="Dina Makhmutova", user="dinamakhmutova", page="https://unsplash.com/photos/a-neatly-made-bed-with-white-linens-and-pillows-ooDvIpnXkwo"),
 "hairdryer": dict(id="1727755868077-22f0d2ff8353", alt="A red hair dryer on a table", by="Shubham Dhage", user="theshubhamdhage", page="https://unsplash.com/photos/a-red-hair-dryer-sitting-on-top-of-a-table-a5Ekb8Q3q-0"),
 "earbuds": dict(id="1770292170233-5d9e235ec739", alt="White wireless earbuds and charging case", by="atelierbyvineeth", user="atelierbyvineeth", page="https://unsplash.com/photos/white-wireless-earbuds-and-charging-case-on-dark-background-rN1hLIGV4gE"),
 "airfryer": dict(id="1630384060421-cb20d0e0649d", alt="A basket of crispy french fries", by="Mitchell Luo", user="mitchel3uo", page="https://unsplash.com/photos/a-basket-of-french-fries-sitting-on-top-of-a-wooden-table-ChXHveqrb28"),
 "vacuum": dict(id="1653990480360-31a12ce9723e", alt="A robot vacuum on a wooden floor", by="Onur Binay", user="onurbinay", page="https://unsplash.com/photos/a-black-robot-vacuum-on-a-wooden-floor-uhJgh4FHi6I"),
 "heater": dict(id="1547186577-a3f4fa07c2ef", alt="A glowing electric heater in a dark room", by="Achudh Krishna", user="biworks", page="https://unsplash.com/photos/turned-on-heater-39mlECY8VkU"),
 "humidifier": dict(id="1768471569643-717e823b5f9a", alt="A white humidifier giving off mist on a wooden desk", by="zeliang xiao", user="xiaozeliang", page="https://unsplash.com/photos/a-white-humidifier-emits-mist-on-a-wooden-desk-tqIaIls1eJY"),
 "coffeemaker": dict(id="1705233244114-7625c14b2e74", alt="A drip coffee maker with a glass carafe", by="Amr Taha\u2122", user="amr_taha", page="https://unsplash.com/photos/a-coffee-maker-with-a-glass-carafe-on-top-of-it-X9rFVk0iW1A"),
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

ASIN = {'Winix 5530': 'B0GVLNG9DZ', 'Levoit Core 400S': 'B0B93SJ2XT', 'Blueair Blue Signature': 'B08KTH125D', 'Coway Airmega AP-1512HH Mighty': 'B01728NLRG', 'Blueair Blue Pure 211i Max': 'B0BN2MGV5H', 'Dyson HushJet Purifier Compact': 'B0FJPYSFRH', 'Windmill Air Purifier': 'B0GP2JG37Q', 'Secretlab Titan Evo': 'B0B3RH59X8', 'Razer Iskur V2': 'B0CPGW5W9Q', 'Corsair TC100 Relaxed': 'B0BN6RRD5V', 'AndaSeat Kaiser 3 XL': 'B0CXJ4P9VB', 'Razer Iskur V2 X': 'B0DP5SY554', 'AndaSeat Novis': 'B0F8BWPNRR', 'Sonos Arc Ultra': 'B0DFK4GS4D', 'Samsung HW-Q990H': 'B0GL1Q8P1P', 'Sonos Beam Ultra': 'B0HBRH363Z', 'Samsung HW-QS750F': 'B0FMKL2KJ6', 'Sony BRAVIA Theater Bar 7': 'B0GSBYNNX1', 'Sony HT-S2000': 'B0BWLCLZPS', 'Samsung HW-Q600F': 'B0DY1Z31MC', 'Bose Smart Soundbar': 'B0D6W8XQ6J', 'Creative Stage Pro': 'B0FC6CCHFQ', 'Sony HT-S100F': 'B0797MY6JB', 'Apple Watch Series 12': 'B0HJ9YNRW7', 'Google Pixel Watch 5': 'B0H7X25DRT', 'Samsung Galaxy Watch 9': 'B0H1DG7XRW', 'Apple Watch SE 3': 'B0FQFW7M9H', 'Garmin Venu 4': 'B0FRG19TD4', 'Amazfit Active 3 Premium': 'B0GK246NH3', 'Garmin Forerunner 165': 'B0CT3SGHXL', 'OnePlus Watch 3': 'B0DYQ1QKF3', 'Amazfit Active 2': 'B0DT3YNMBX', 'Sony WH-1000XM6': 'B0F3PQHWTZ', 'Bose QuietComfort Ultra Headphones (2nd Gen)': 'B0FDKR293G', 'Sennheiser HDB 630': 'B0FK4K5Z37', 'Sonos Ace Ultra': 'B0H8TBGMBJ', 'Sony WH-CH730N': 'B0HFB6FS8K', 'Nothing Headphone (a)': 'B0G6LCC42J', 'Sony ULT Wear': 'B0CYR5Y96M', 'Røde NTH-100': 'B09NCNQCY1', 'Dyson V15 Detect': 'B0C2J8KJH9', 'Shark PowerDetect Clean & Empty': 'B0DBVW1RFW', 'Dreame R20': 'B0BXD5L1M5', 'Bissell PowerClean FurFinder': 'B0DQJV5D9K', 'Tineco Pure ONE S11': 'B0G39SD4XZ', 'Levoit LVAC-200': 'B0DMVWXJN3', 'Tineco Pure ONE Station 5': 'B0D8J2RPV9', 'Dyson Gen5detect': 'B0C2JD5H7D', 'Wüsthof Classic 9-Piece Knife Block Set': 'B09JFQ5227', 'Ginsu Gourmet Chikara 8-Piece Knife Set': 'B0016J4230', 'Zwilling Pro 7-Piece Knife Block Set': 'B07CX5J723', 'Mercer Culinary Genesis 6-Piece Forged Knife Block Set': 'B000IBU9FW', 'Mercer Culinary Millennia 3-Piece Starter Set': 'B0B5YNT915', 'Vitamix Explorian E310': 'B0758JHZM3', 'Ninja Professional Blender (BL610)': 'B00NGV4506', 'Breville Fresh & Furious': 'B07GJ24VXV', 'Vitamix Ascent X2': 'B0D9ZR58T1', 'Braun TriForce Power Blender (JB9040)': 'B093CPKV4Y', 'Ninja Compact Kitchen System (AMZ493BRN)': 'B08QJSDBY4', 'BlendJet 2': 'B0D3VPR9WJ', 'Technivorm Moccamaster KBGV Select': 'B093DYPBYR', 'OXO Brew 8-Cup Coffee Maker': 'B07H9G93WK', 'Cuisinart PerfecTemp 14-Cup Programmable Coffee Maker': 'B00MVWGQX0', 'Breville Precision Brewer Thermal': 'B078RQVQF1', 'Ninja Specialty Coffee Maker': 'B07PFLM2LK', 'Café Specialty Drip Coffee Maker': 'B09648KFJ4', 'Keurig K-Duo': 'B07ZHYJDCN', 'Café Specialty Grind and Brew Coffee Maker': 'B0CG2KZDB2', 'Levoit LV600HH': 'B08FHZTYJB', 'Levoit Superior 6000S': 'B0CGR1N9T6', 'Carepod One': 'B0916J478T', 'Dreo HM713S': 'B0CB4CK3ZS', 'Levoit Classic 300S': 'B09C24TYGQ', 'Everlasting Comfort Ultrasonic Cool Mist Humidifier': 'B077Z2QCS5', 'Levoit Sprout Evaporative Humidifier': 'B0DLGDRRXY', 'Vornado Evap40': 'B00O0WOO74', 'Lasko FH500': 'B07QHG97RZ', 'Dyson Purifier Hot+Cool HP1': 'B0F468V6BW', "De'Longhi SlimStyle Digital Convection Panel Heater": 'B0777K9SJ5', 'Apple AirTag (2nd Generation)': 'B0GJTFXNRX', 'Twelve South AirFly SE': 'B0BQZBMXD4', 'Anker Nano 3-in-1 Power Bank (10,000mAh)': 'B0CX4992Z8', 'Fly By Jing Original Sichuan Chili Crisp': 'B0849Q133Y', 'Loop Quiet 2 Earplugs': 'B0D3V6Y38G', 'Theragun Mini Plus': 'B0FKCSFVLQ', 'Baratza Encore': 'B007F183LK', 'AeroPress Original': 'B0047BIWSK', 'Fellow Atmos Vacuum Canister (0.7 L)': 'B07PY4WXXV', 'LG C6 OLED': 'B0GRK5D3RW', 'Samsung S95H QD-OLED': 'B0H5G3H55T', 'TCL QM8L': 'B0GPSYT2KN', 'Hisense U7SG': 'B0GR9BLPJ8', 'Vizio Mini LED Quantum 4K': 'B0GVV3NXPV', 'TCL X11L': 'B0GFDJGFG7', 'Hisense C2 Ultra': 'B0DHLH7VPH', 'Epson Home Cinema LS11000': 'B09TS2M1ZS', 'Hisense PX4-Pro': 'B0H6DDBCNQ', 'AWOL Vision Aetherion Max': 'B0GN3XX19L', 'BenQ W2720i': 'B0DPJDK31N', 'Hisense M2 Pro': 'B0F6ZV1367', 'Sony Bravia Projector 8': 'B0DGRCB57X', 'JVC DLA-NZ800': 'B0D45ZGZ4N', 'Aurzen ZIP Tri-Fold': 'B0DYJP2JY6', 'Braun Series 9 Pro+': 'B0FGLF3SDT', 'Philips Norelco i9000 Prestige Ultra': 'B0F1P4RZMK', 'Panasonic Arc5 (ES-LV67-K)': 'B07W7XK55Q', 'Braun Series 8': 'B0CFBV91YQ', 'Philips Norelco 7800': 'B0BPZR1MBC', 'Philips Norelco 5400': 'B0BF9QHHLJ', 'Philips Norelco OneBlade 360': 'B0BZDPFH45', 'Remington F5-5800': 'B00BB5YHEI', 'Philips Norelco Shaver 3600': 'B0CLWDF9NK', 'Philips Norelco Head Shaver Pro 7000': 'B0FHJ55R4L', 'Breville Barista Express Impress': 'B0BBYNPV33', "De'Longhi La Specialista Touch": 'B0F6DY1DGR', 'Breville Bambino Plus': 'B07JVD78TT', 'Breville Bambino': 'B0B1JPPG2L', 'Gaggia Classic E24': 'B07RQ3NL76', "De'Longhi Stilosa": 'B08C96BG9H', 'Ninja Luxe Café Premier': 'B0D45PK5V4', 'Terra Kaffe Demi': 'B0FGWSD63C', 'Nespresso VertuoPlus': 'B01N7GO468', 'Sony WF-1000XM6': 'B0G6HLWS6Q', 'Apple AirPods Pro 3': 'B0FQFB8FMG', 'Bose QuietComfort Ultra Earbuds (2nd Gen)': 'B0F7M3HPBD', 'Samsung Galaxy Buds 4 Pro': 'B0G1PJLWLZ', 'Google Pixel Buds Pro 2': 'B0D79ND3N7', 'Beats Powerbeats Pro 2': 'B0DT2344N3', 'Sony WF-C710N': 'B0DWHPBK42', 'Soundcore Liberty 4 NC': 'B0BZV4QFP8', 'Sony WF-C510': 'B0D9R4GYTN', 'Ninja Air Fryer Max XL': 'B07S6529ZZ', 'Ninja AF101 Air Fryer': 'B07FDJMC9Q', 'Cosori TurboBlaze': 'B0C33CHG99', 'Instant Vortex Plus ClearCook': 'B096N3FTZP', 'Ninja Foodi DualZone 2-Basket': 'B089TQWJKK', 'Ninja Speedi Rapid Cooker': 'B0B3QT6H7H', 'Breville Smart Oven Air Fryer Pro': 'B01N5UPTZS', 'Dreo ChefMaker Combi Fryer': 'B0C5JHKGFP', 'Typhur Dome 2': 'B0CKP6Y6KB', 'BLACK+DECKER Purifry 2-Quart': 'B0D384TSVC', 'Dreame X60 Max Ultra Complete': 'B0G5X4H4PS', 'Roborock Saros 10R': 'B0DHCJ571Z', 'Roborock Saros 20': 'B0G64MM1HM', 'Shark PowerDetect UV Reveal': 'B0GJFVJGXL', 'Dyson Spot+Scrub Ai': 'B0GKC52QZP', 'Roborock QV 35S': 'B0FB419PLY', 'Dreame L40 Ultra': 'B0D6VS4SLX', 'Shark Matrix Plus': 'B0B8B6N2G4', 'SwitchBot Mini K10+': 'B0CHBC7BW1', 'Dreame D10 Plus Gen 2': 'B0D6TTRTPL', 'Branch Duo Standing Desk': 'B0C3WS16XP', 'FlexiSpot E7 Pro': 'B08B3X9CKH', 'Uplift V3': 'B07HYGZXP7', 'Fully Jarvis Bamboo': 'B07GVQF5HM', 'Secretlab Magnus Pro': 'B0G1S75G2K', 'ApexDesk Elite Pro (Curved)': 'B09CJJHJSJ', 'FEZIBO Electric Standing Desk': 'B0F8MHPVPH', 'FlexiSpot M7 Desk Converter': 'B078HGW7FP', 'FlexiSpot H7 Mobile Table': 'B0B2VZZQVG', 'Helix Midnight Luxe': 'B0D3SJ2FXN', 'DreamCloud Hybrid': 'B0DP3F2RWH', 'Nectar Premier': 'B0DCXHY632', 'Tuft & Needle Mint Hybrid': 'B0BV5CS62W', 'Leesa Sapira Chill Hybrid': 'B0F7B18GGP', 'Nolah Evolution': 'B0CDJ9RZ2T', 'Brooklyn Bedding Aurora Luxe': 'B0GQH4CL4L', 'Helix Plus': 'B0D54YMPNT', 'T3 AireLuxe': 'B09SPBNKGR', 'Dyson Supersonic Nural': 'B0DMXJPM4T', 'BaBylissPRO Nano Titanium': 'B091KB6H1F', 'Dyson Airwrap Multi-Styler': 'B0B61XH5YT', 'Shark FlexStyle': 'B0B89P16MC', 'Shark SpeedStyle Pro Flex': 'B0DDYDWVD1', 'Revlon One-Step Volumizer': 'B097CNMZF5', 'GA.MA iQ Perfetto': 'B092RD44N3', 'Therabody Theragun Pro': 'B0B6RL7NQJ', 'Solo Stove Bonfire 2.0': 'B0B7BFJ5Y6', 'Ooni Karu 12': 'B083WGMTGZ', 'LEGO Technic McLaren MCL39 F1 Car': 'B0FMZRRYFP', 'Leatherman ARC': 'B0D7JTK4KM', 'Cuisinart Griddler': 'B002YD99Y4', 'Ekster Leather Smart Wallet': 'B0F3P42YK1', 'KitchenAid Artisan Stand Mixer': 'B01H424IU4', 'Swarovski Matrix Tennis Bracelet': 'B0FG49S9N5', 'Hatch Restore 3': 'B0DLLSCVZW', 'Bearaby Cotton Weighted Blanket': 'B0C1F9MFH1', 'LEGO Botanicals Pretty Pink Bouquet': 'B0DHLJ6TR9', 'Capri Blue Volcano Candle': 'B07H14RYTV', 'Grace & Stella Under Eye Masks': 'B01DZ7C502', 'KODAK Luma 350 Projector': 'B07RB7P439', 'Aura Carver Digital Photo Frame': 'B0CBQRVL7H', 'TUMI Alpha Split Travel Kit': 'B09J1Q6F6B', 'Logitech MX Keys Mini': 'B098JPSVKY', 'Anker MagGo Power Bank': 'B0CFDSMNT7', 'Harry & David Meat & Cheese Gift Box': 'B07D19J4J1', 'YETI Rambler Colster': 'B0BVGF1DJG', 'Sunbeam Royal Luxe Heated Throw': 'B008BF2OF0', 'LEGO Botanicals Orchid': 'B09Q4L157D', 'LANEIGE Lip Sleeping Mask': 'B07XXPHQZK', 'TheraFace Mask Glo': 'B0FKD3826X', 'Tell Me Your Life Story, Mom': '1952568099', 'Steelcase Series 2': 'B08L8GCCDV', 'Branch Verve Chair': 'B0CK3NSMM6', 'Herman Miller Aeron': 'B007WU4NFO', 'Steelcase Leap V2': 'B00TYE4SKG', 'LiberNovo Omni': 'B0FYCKPWP9', 'Autonomous ErgoChair Pro': 'B0FL2JGMK5', 'SIHOO Doro C300 Pro V2': 'B0GSFPTKD5', 'FlexiSpot C7': 'B0DPQQ2L22', 'SIHOO M57': 'B07BDFW1Y7', 'CALPAK Ambeur Carry-On': 'B0HLSB3PGC', 'CALPAK Ambeur Large': 'B0HNNP4JWZ', 'Osprey Sojourn Porter 46L': 'B0CB6YWXNJ', 'CALPAK Luka Duffel': 'B0GKV9M82F', 'All-Clad D3 Stainless 10-Piece': 'B008PLB15Y', 'All-Clad HA1 Nonstick 10-Piece': 'B016SJHAOA', 'Made In 10-Piece Stainless': 'B09HR6MV21', 'HexClad Hybrid 12-Piece': 'B0CVH8FXKB', 'GreenPan Valencia Pro 11-Piece': 'B071HVQL76', 'Caraway 12-Piece Ceramic': 'B08XM1B6ZX', 'Tramontina Tri-Ply Clad 10-Piece': 'B00JDL0TA8', 'Calphalon Ceramic 12-Piece': 'B0GS7KS6MB', 'T-fal Advanced Nonstick 12-Piece': 'B076682L7W', 'Tramontina PrimaWare 18-Piece': 'B01M5H9UCV'}
QUERY = {'Levoit Core 300': 'LEVOIT Core 300 True HEPA air purifier', 'Levoit Vital 200S': 'LEVOIT Vital 200S air purifier', 'Oneisall Pet Air Purifier': 'oneisall pet air purifier HEPA', 'DXRacer Craft': 'DXRacer Craft gaming chair', 'Herman Miller x Logitech G Vantum': 'Herman Miller x Logitech G Vantum gaming chair', 'Herman Miller x Logitech G Embody': 'Herman Miller x Logitech G Embody gaming chair', 'Withings ScanWatch 2': 'Withings ScanWatch 2 hybrid smartwatch 42mm', 'Apple AirPods Max 2': 'Apple AirPods Max 2 wireless over-ear headphones', 'Soundcore Life Q30': 'Soundcore Life Q30 hybrid active noise cancelling headphones', 'Levoit LVAC-300': 'LEVOIT LVAC-300 cordless vacuum', 'Dyson V15 Detect Submarine': 'Dyson V15s Detect Submarine wet and dry vacuum', 'Victorinox Fibrox 4-Piece Knife Set': 'Victorinox 4-piece knife set Fibrox handles chef bread utility paring', 'Henckels Classic Precision 15-Piece Self-Sharpening Set': 'Henckels Classic Precision 15-piece self-sharpening knife block set', 'Shun Classic 5-Piece Starter Block Set': 'Shun Classic 5 piece starter block set', 'Shun Premier 5-Piece In-Drawer Set': 'Shun Premier 5 piece in-drawer knife set', 'Material The Knives + Stand': 'Material Kitchen The Knives + Stand magnetic', 'Cuisinart Precision Master SM-50': 'Cuisinart SM-50 Precision Master 5.5 quart stand mixer', 'KitchenAid Classic Series 4.5-Quart Stand Mixer': 'KitchenAid Classic Series 4.5 quart tilt-head stand mixer K45SS', 'Ankarsrum Assistent Original': 'Ankarsrum Assistent Original stand mixer AKM 6230', 'Ooni Halo Pro Spiral Mixer': 'Ooni Halo Pro spiral mixer', 'KitchenAid 7-Quart Bowl-Lift Stand Mixer': 'KitchenAid 7 quart bowl-lift stand mixer KSM70', 'Bosch Universal Plus Stand Mixer': 'Bosch Universal Plus stand mixer', 'KitchenAid Artisan Mini 3.5-Quart Stand Mixer': 'KitchenAid Artisan Mini 3.5 quart tilt-head stand mixer', 'Costway Stand Mixer': 'COSTWAY stand mixer 6 speed tilt-head', 'Hamilton Beach All-Metal Stand Mixer': 'Hamilton Beach All-Metal stand mixer 4.5 quart', 'Ninja Detect Power Blender Pro': 'Ninja Detect Power Blender Pro BlendSense', 'Ninja BlendBoss': 'Ninja BlendBOSS personal blender', 'Oster Master Series Blender with Texture Select': 'Oster Master Series blender Texture Select glass jar Blend-N-Go cup', 'BLACK+DECKER 12-Cup Programmable Coffee Maker': 'BLACK+DECKER 12-cup programmable coffee maker', 'Mr. Coffee 5-Cup Coffee Maker': 'Mr. Coffee 5-cup coffee maker', 'Levoit Dual 100': 'LEVOIT Dual 100 ultrasonic top fill cool mist humidifier 1.8L', 'Canopy Humidifier': 'Canopy evaporative humidifier 2.5L', 'Dr. Infrared Heater DR-968': 'Dr Infrared Heater DR-968 portable space heater 1500 watt', 'Dreo Tower Heater 718': 'Dreo tower heater 718', 'Amazon Basics Portable Radiator Heater': 'Amazon Basics portable radiator heater oil filled manual control 1500W', 'Morento Space Heater': 'MORENTO space heater 1500W ceramic portable', 'Dreo Whole Room Heater 714': 'Dreo whole room heater 714', 'Lasko CD08200 Bathroom Heater': 'Lasko CD08200 bathroom heater ALCI', 'Shark TurboBlade Cool + Heat': 'Shark TurboBlade Cool + Heat tower fan heater', 'Body Restore Shower Steamers (6-Pack)': 'Body Restore shower steamers aromatherapy 6 pack', 'Bombas Marl Calf Socks (4-Pack)': 'Bombas marl calf socks 4-pack', 'Nintendo Switch 2 Mario Kart World Bundle': 'Nintendo Switch 2 Mario Kart World bundle', 'Steam Deck OLED': 'Steam Deck OLED handheld', 'Meta Quest 3S': 'Meta Quest 3S', 'Turtle Beach Stealth Pro II': 'Turtle Beach Stealth Pro II wireless gaming headset', 'PlayStation DualSense Edge': 'DualSense Edge wireless controller PS5', 'Logitech G502 HERO': 'Logitech G502 HERO wired gaming mouse', 'LEGO Game Boy': 'LEGO Game Boy 72046', 'Evercade Nexus': 'Evercade Nexus handheld', 'KontrolFreek FPS Freek Galaxy': 'KontrolFreek FPS Freek Galaxy thumbsticks', 'The Elder Scrolls: The Official Cookbook': 'The Elder Scrolls Official Cookbook Chelsea Monroe-Cassel', 'Cosori Gooseneck Electric Kettle': 'COSORI gooseneck electric kettle temperature control', 'Fellow Aiden': 'Fellow Aiden precision coffee maker', 'Chemex Pour-Over Glass Coffeemaker': 'Chemex pour-over glass coffeemaker classic', 'Takeya Deluxe Cold Brew Coffee Maker': 'Takeya Deluxe cold brew coffee maker', 'Frank Body Original Coffee Scrub': 'frank body original coffee scrub', 'JBL Go 4': 'JBL Go 4 portable Bluetooth speaker', 'Apple AirTag': 'Apple AirTag', 'Bialetti Moka Express (3-Cup)': 'Bialetti Moka Express 3 cup stovetop espresso maker', 'Warmies Microwavable Slippers': 'Warmies microwavable slippers', 'Kosterina Olive Oil & Balsamic Duo': 'Kosterina olive oil balsamic vinegar duo', 'Nodpod Gentle Pressure Sleep Mask': 'Nodpod gentle pressure sleep mask', 'Q-Less Crossword Dice Game': 'Q-Less crossword dice game', 'LG G6 OLED': 'LG G6 OLED evo 2026 TV', 'Sony Bravia 9 II': 'Sony BRAVIA 9 II Mini LED TV', 'Hisense UR9': 'Hisense UR9 RGB MiniLED TV', 'LG C5 OLED (2025)': 'LG C5 OLED evo TV 2025', 'Nebula Capsule 3 GTV': 'NEBULA Capsule 3 GTV projector', 'Breville Oracle': 'Breville Oracle dual boiler espresso machine', 'Apple AirPods 5': 'Apple AirPods 5', 'FlexiSpot E7 Plus': 'FlexiSpot E7 Plus standing desk', 'Allswell Luxe': 'Allswell Luxe hybrid mattress', 'Plank Firm': 'Plank Firm mattress Brooklyn Bedding', 'Bio Ionic PowerLight Pro': 'Bio Ionic PowerLight Pro hair dryer', 'BondiBoost Blowout Brush Pro': 'BondiBoost Blowout Brush Pro', 'YETI Rambler 20 oz Travel Mug': 'YETI Rambler 20 oz travel mug', 'Oura Ring 4': 'Oura Ring 4', 'Omnilux Contour Face': 'Omnilux Contour Face LED mask', 'Birdsnap TUC Smart Bird Feeder': 'Birdsnap TUC smart bird feeder', 'Hoka Clifton 10': 'Hoka Clifton 10 men', 'Ember Mug 3': 'Ember Mug 3 10 oz', 'Kindle Paperwhite': 'Kindle Paperwhite', 'Le Creuset Signature Dutch Oven (5.5 qt)': 'Le Creuset Signature round Dutch oven 5.5 qt', 'Boulies EP200': 'boulies EP200 ergonomic office chair', 'Away The Bigger Carry-On': 'Away The Bigger Carry-On', 'Away Bigger Carry-On': 'Away The Bigger Carry-On', 'Samsonite Freeform Carry-On': 'Samsonite Freeform carry-on spinner', 'Monos Carry-On Pro Plus': 'Monos Carry-On Pro Plus', 'Samsonite Proxis Global Carry-On': 'Samsonite Proxis Global carry-on spinner', 'Briggs & Riley Baseline Essential': 'Briggs & Riley Baseline Essential carry-on expandable spinner', 'Amazon Basics 21" Hardside Spinner': 'Amazon Basics 21 inch hardside carry-on spinner'}

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
  "slug": "best-space-heaters", "icon": "heater", "tint": "tint-heater", "short": "Space Heaters",
  "title": "The 10 Best Space Heaters of 2026",
  "price_notes": GIFT_NOTES,
  "card": "Safe, quiet heaters for large rooms, small rooms, bathrooms and basements.",
  "lead": "The Dr. Infrared DR-968 is the best space heater for most people: quiet, 1,500W and a top large-room pick. Plus small-room, bathroom and budget picks.",
  "filters": [("large","Large rooms"),("small","Small rooms"),("budget","Budget"),("quiet","Quiet"),("fan","Doubles as a fan")],
  "products": [
   dict(name="Dr. Infrared Heater DR-968", badge="Best overall", price="$$", f=["large","quiet"],
        tags=["1,500W infrared","Casters + remote"],
        summary="The one heater that shows up across our sources: Bob Vila's top energy-efficient pick, and both Bob Vila's and HGTV's choice for large rooms. It's an infrared cabinet heater with an eco mode, a 12-hour timer and a remote.",
        pros=["Very quiet (Bob Vila measured 39 dB)","Even heat in large rooms","Built-in casters and a three-year warranty"],
        cons=["Heavy, roughly 19–24 lb","Dated cabinet look"]),
   dict(name="Dreo Tower Heater 718", badge="Best tower for large rooms", price="$$", f=["large"],
        tags=["5 heat settings","Tower + remote"],
        summary="HGTV's best space heater overall. Testers found its heat powerful and even across a large room and singled out its remote as the best of the group. Tip-over and overheat protection, a child lock and a cool-touch housing are built in.",
        pros=["Powerful, even heat","Excellent remote","Child lock and cool-touch housing"],
        cons=["Only a one-year warranty"]),
   dict(name="Amazon Basics Portable Radiator Heater", badge="Best oil-filled radiator", price="$", f=["large","quiet","budget"],
        tags=["1,500W oil-filled","Manual dials"],
        summary="Bob Vila's best space heater overall: a simple 1,500-watt oil-filled radiator that's nearly silent and gives off plenty of steady heat, with tip-over and overheat shutoff.",
        pros=["Nearly silent","Easy to set up and use","Tip-over and overheat protection"],
        cons=["Slow: about 2 hours to warm a living room from 60°F to 70°F","No display, remote or timer"]),
   dict(name="Morento Space Heater", badge="Best budget", price="$", f=["small","budget"],
        tags=["1,500W ceramic","4 lb"],
        summary="Tom's Guide's best budget space heater: a 4-pound ceramic heater that puts out more heat than its size suggests, with an Eco mode, a timer and tip-over and overheat protection.",
        pros=["Compact and light","Strong heat for its size","Three-year warranty"],
        cons=["Best for small spaces only","Auto shut-off waits a full 24 hours"]),
   dict(name="Dreo Whole Room Heater 714", badge="Best safety features", price="$$", f=["small","quiet","fan"],
        tags=["3D oscillation","Child lock"],
        summary="Tom's Guide names it the safest space heater it tested and the best under $100. A child lock and a cool-touch, flame-retardant housing sit on top of tip-over and overheat shutoff, and it oscillates up and down as well as side to side.",
        pros=["Heats up quickly","Quiet in everyday use","Fan-only mode for summer"],
        cons=["Remote is slow to respond","Airflow is very concentrated"]),
   dict(name="Lasko FH500", badge="Best ceramic tower", price="$$", f=["fan"],
        tags=["42-in tower","Fan + heater"],
        summary="Tom's Guide's best space heater overall. This 42-inch ceramic tower heats a room evenly, has an eco mode with a digital thermostat, stays cool to the touch and works as a fan in summer.",
        pros=["Even, effective heat","Eco mode and digital thermostat","Three-year warranty"],
        cons=["Controls are a bit confusing"]),
   dict(name="Lasko CD08200 Bathroom Heater", badge="Best for bathrooms", price="$", f=["small","budget"],
        tags=["ALCI safety plug","1-hour timer"],
        summary="HGTV's and Bob Vila's pick for bathrooms. Its ALCI safety plug is designed for damp rooms and cut the power in Bob Vila's water-spray test. One-button controls keep it simple.",
        pros=["ALCI plug for damp rooms","One-button operation","Three-year warranty"],
        cons=["No tip-over shutoff","No remote"]),
   dict(name="De'Longhi SlimStyle Digital Convection Panel Heater", badge="Best for basements", price="$$", f=["quiet"],
        tags=["Floor or wall","Freeze protection"],
        summary="Bob Vila's basement pick in two separate roundups. The slim panel stands on the floor or mounts on a wall, and a freeze-protection mode helps keep pipes from freezing.",
        pros=["Nearly silent in most modes","Freeze-protection mode","Wall brackets included"],
        cons=["No remote control"]),
   dict(name="Shark TurboBlade Cool + Heat", badge="Best fan and heater combo", price="$$$", f=["fan"],
        tags=["Bladeless tower","180° oscillation"],
        summary="HGTV's best fan/heater combo and Tom's Guide's pick for heating and cooling. It's a powerful bladeless tower fan in summer that heats quickly in winter, with a magnetic remote that has its own readout.",
        pros=["Powerful summer fan","Heats quickly","Great remote"],
        cons=["Heavy (about 21.5 lb) and bulky","Expensive unless on sale"]),
   dict(name="Dyson Purifier Hot+Cool HP1", badge="Best with an air purifier", price="$$$$", f=["fan"],
        tags=["HEPA + carbon filter","Heat, cool, purify"],
        summary="The pick from both HGTV and Tom's Guide if you want one machine that heats, cools and cleans the air. It monitors air quality, has no exposed heating elements and shuts off if tipped.",
        pros=["Heater, fan and purifier in one","Tip-over shutoff and sleep timer","Two-year warranty"],
        cons=["Very expensive","Replacement filters add yearly cost"]),
  ],
  "tips": [
   ("Size it to your room","Plan on about 10 watts per square foot. A 1,500-watt heater, the most a standard household outlet can supply, covers roughly 150 sq ft. High ceilings, drafty windows and poor insulation call for more heat, so err on the powerful side and turn it down."),
   ("Pick the right type","Ceramic fan heaters warm quickly and cost less but are louder and can make air feel dry. Oil-filled radiators are slow but nearly silent and hold steady heat. Infrared heaters warm the people and objects in front of them and run quietly."),
   ("Insist on automatic shutoff","Choose a heater that turns itself off if it tips over or overheats, carries a UL, ETL or CSA safety mark, and has a cord at least 6 ft long."),
   ("Plug it in safely","Plug straight into a wall outlet, never an extension cord or power strip. Set it on a hard, level surface (not carpet), at least 3 ft from curtains, bedding and furniture."),
   ("Extras that save energy","A thermostat or eco mode cycles the heater off once the room is warm. A timer, remote and oscillation make it easier to heat only when and where you need it."),
  ],
  "faq": [
   ("What is the safest space heater?","The safest space heaters shut off automatically if they tip over or overheat and carry a UL, ETL or CSA mark. Tom's Guide names the Dreo Whole Room Heater 714 the safest it tested, adding a child lock and a cool-touch, flame-retardant housing to tip-over and overheat protection."),
   ("What is the most energy-efficient space heater?","Bob Vila's top energy-efficient pick is the Dr. Infrared Heater DR-968. It notes that infrared heaters use up to 10% less energy than coil-and-fan models and that oil-filled radiators are among the most efficient; space heaters aren't Energy Star rated, so a thermostat or eco mode is the best way to save power."),
   ("Can you leave a space heater on overnight?","No. HGTV and Tom's Guide both say not to run a space heater while you sleep: warm the room, then turn the heater off before bed. Bob Vila notes the exception is an oil-filled radiator whose manual says overnight use is allowed."),
   ("What size space heater do I need?","Allow about 10 watts per square foot: a 10 x 12 ft room (120 sq ft) needs about 1,200 watts, and a 1,500-watt heater covers about 150 sq ft. Ceiling height, windows and insulation change the math."),
   ("Is an oil-filled or ceramic space heater better?","Ceramic heaters warm a room faster and cost less but are louder and can dry the air; oil-filled radiators are nearly silent and give steady heat but are slow (Bob Vila's top oil-filled pick took about 2 hours to warm a living room 10°F). Choose ceramic for quick spot heat and oil-filled for quiet, all-evening warmth."),
   ("Can you plug a space heater into an extension cord?","No. Bob Vila and Tom's Guide both say to plug a space heater directly into a wall outlet and never use an extension cord or power strip, and to keep it 3 ft away from anything that can burn."),
  ],
  "sources": [
   ("Bob Vila — The best space heaters of 2026, tested (updated November 2026)","https://www.bobvila.com/reviews/best-space-heaters/"),
   ("Bob Vila — The best energy-efficient space heaters of 2026 (October 2026)","https://www.bobvila.com/reviews/best-energy-efficient-space-heaters/"),
   ("HGTV — 7 best space heaters of 2026, tested (September 2026)","https://www.hgtv.com/shopping/product-reviews/best-space-heaters"),
   ("Tom's Guide — Best space heaters (May 2026)","https://tomsguide.com/best-picks/best-space-heaters"),
   ("Tom's Guide — Dreo Whole Room Heater 714 review","https://www.tomsguide.com/home/home-appliances/dreo-whole-room-heater-714-review"),
  ],
 },
 {
  "slug": "best-humidifiers", "icon": "humidifier", "tint": "tint-humidifier", "short": "Humidifiers",
  "title": "The 10 Best Humidifiers of 2026",
  "price_notes": GIFT_NOTES,
  "card": "Quiet humidifiers for bedrooms, large rooms and whole homes, from warm mist to easy-clean picks.",
  "lead": "The Levoit LV600HH is the best humidifier for most people: a 6L warm or cool mist model with auto mode. Plus bedroom, large-room and budget picks.",
  "filters": [("large","Large rooms"),("bedroom","Bedrooms"),("budget","Budget"),("warm","Warm mist"),("clean","Easy to clean")],
  "products": [
   dict(name="Levoit LV600HH", badge="Best overall", price="$$", f=["large","bedroom","warm"],
        tags=["6L tank","Warm + cool mist"],
        summary="The humidifier that turns up most across our sources: HGTV's pick for large rooms and Live Science's pick for bedrooms. Its 6-liter tank is rated for up to 753 sq ft, and a built-in humidity sensor adjusts the mist output on its own.",
        pros=["Warm or cool mist","Remote, timer and a display you can switch off","Very quiet (Live Science lists up to 31 dB)"],
        cons=["Bulky and hard to tuck out of sight","Humidity sensor can be oversensitive"]),
   dict(name="Levoit Superior 6000S", badge="Best for large rooms", price="$$$", f=["large","clean"],
        tags=["6-gallon evaporative","Up to 3,000 sq ft"],
        summary="Bob Vila's best overall in both its 2026 evaporative and large-room roundups. The 6-gallon tank rolls on wheels and refills from an included faucet hose, and its wick filter means plain tap water is fine. On auto at about 50% humidity, a tester went roughly a week between refills.",
        pros=["Humidifies open-plan spaces up to 3,000 sq ft","Tap water is fine thanks to the filter","Quiet sleep mode and app control"],
        cons=["Tall, and the tank is heavy when full","Wick filters need replacing"]),
   dict(name="Carepod One", badge="Best easy-to-clean", price="$$$", f=["bedroom","clean"],
        tags=["Stainless steel tank","3 parts, no filter"],
        summary="RTINGS calls it the best humidifier, and the best bedroom humidifier, it has tested, pointing to quiet running, strong humidification and an easy-clean design. It comes apart into just three pieces, and the stainless steel tank and inner lid go in the dishwasher.",
        pros=["Only three parts to clean and no filters to buy","4-liter tank rated for up to 30 hours and 500 sq ft","Quiet enough for a bedroom"],
        cons=["Expensive for a cool-mist-only model","The ultrasonic wand must be washed by hand"]),
   dict(name="Dreo HM713S", badge="Best smart humidifier", price="$$", f=["bedroom","warm"],
        tags=["6L warm + cool mist","App + Alexa"],
        summary="Live Science's best humidifier overall and Bob Vila's best smart pick. It offers warm or cool mist, a humidistat with auto mode, app and Alexa control and a 6-liter top-fill tank, and Bob Vila confirmed its claimed 60-hour runtime on low.",
        pros=["Verified 60-hour runtime on low","Warm mist plus app and voice control","Easy top-fill refills"],
        cons=["Bulky footprint","Mostly plastic build"]),
   dict(name="Levoit Classic 300S", badge="Best tabletop humidifier", price="$$", f=["bedroom","clean"],
        tags=["6L top-fill","VeSync app"],
        summary="Bob Vila's best tabletop humidifier and Live Science's pick for easy cleaning. The see-through 6-liter tank fills from the top and runs up to 60 hours, and the VeSync app adds schedules, auto mode and a sleep mode. Bob Vila measured it just under 30 dB on high.",
        pros=["Low-maintenance top-fill tank","App schedules, auto and sleep modes","Very quiet"],
        cons=["Can leave white dust with tap water (no demineralization cartridge)","Humidity sensor can be oversensitive"]),
   dict(name="Everlasting Comfort Ultrasonic Cool Mist Humidifier", badge="Best budget", price="$", f=["budget","bedroom"],
        tags=["6L, up to 50 hours","Essential-oil tray"],
        summary="Bob Vila's best bang for the buck in its 2026 large-room test, and its quietest pick in a 2025 test. It's a simple 6-liter ultrasonic unit rated for up to 500 sq ft and 50 hours; on low it raised humidity 11% over 8 hours in a 750 sq ft test room.",
        pros=["Nearly silent","Long runtime from a 6L tank","Easy to set up and clean"],
        cons=["No humidistat or auto mode","No filter, so it needs frequent cleaning"]),
   dict(name="Levoit Dual 100", badge="Best for small rooms", price="$", f=["budget","bedroom"],
        tags=["1.8L top-fill","Diffuser tray"],
        summary="HGTV's best humidifier overall. This compact ultrasonic model fills from the top, runs up to 20 hours, covers about 260 sq ft and has a night mode that stops room humidity from climbing past 60%. Two buttons run everything.",
        pros=["Quiet and simple","Top-fill tank is easy to clean","Low price"],
        cons=["No remote or timer","Small tank for big rooms"]),
   dict(name="Levoit Sprout Evaporative Humidifier", badge="Best quiet", price="$$", f=["bedroom","clean"],
        tags=["Evaporative, 1 gallon","20 dB sleep mode"],
        summary="Bob Vila's quietest evaporative pick: sleep mode drops it to about 20 dB while it keeps humidifying. It adds an air filter, a dimmable night light, a dry mode that helps limit mold and a top-fill tank rated for up to 36 hours in rooms up to 219 sq ft.",
        pros=["Whisper-quiet sleep mode","Dry mode helps limit mold","Easy top-fill refills"],
        cons=["Pricey for a 1-gallon tank","Tank lid rests on top instead of screwing on"]),
   dict(name="Vornado Evap40", badge="Best budget whole-home", price="$$", f=["large"],
        tags=["4 gallons, two tanks","Up to 1,000 sq ft"],
        summary="Bob Vila's large-room pick in its evaporative test and its small-home pick in its large-room test. Two 2-gallon tanks and a strong fan cover up to 1,000 sq ft; testers got about 36 hours on max, beating Vornado's 24-hour claim, and it held a basement near 45%.",
        pros=["Big output for the price","Ran about 36 hours on high in testing","No installation needed"],
        cons=["No digital humidistat or auto mode","Occasional glugging, and narrow spouts are hard to clean"]),
   dict(name="Canopy Humidifier", badge="Best anti-mold design", price="$$", f=["clean"],
        tags=["2.5L evaporative","UV light + aroma puck"],
        summary="HGTV's best humidifier and diffuser combo. It's an evaporative model built to fight mold: UV LEDs and a run-until-empty design keep water from sitting, parts are dishwasher-safe and a light tells you when to change the filter. It's rated for 500 sq ft and 36 hours.",
        pros=["Designed to prevent mold","Dishwasher-safe parts","Attractive, in several colors"],
        cons=["Expensive for its size","Ongoing filter costs"]),
  ],
  "tips": [
   ("Match the tank to the room","HGTV suggests a tank under 3 liters for rooms below about 200 sq ft and roughly 6 liters for spaces around 500 sq ft. Open doors, high ceilings and drafty rooms need more, so buy a unit rated for a little more space than you have."),
   ("Ultrasonic or evaporative?","Ultrasonic models are the quietest and put out plenty of mist, but minerals in tap water can settle as white dust. Evaporative models blow air through a wet wick, leave little residue and handle tap water, but the wick needs replacing every few months."),
   ("Warm mist or cool mist?","Warm mist can feel soothing in cold weather, but the water gets very hot, so cool mist is the safer choice around kids and pets. Mist temperature barely changes the temperature of the room."),
   ("Get a humidistat or auto mode","Aim for 30–50% indoor humidity (the EPA says stay below 60%). A built-in humidity sensor or auto mode stops the mist once it hits your target, which saves water and helps prevent mold; without one, use an inexpensive hygrometer."),
   ("Plan for cleaning","Rinse and refill the tank daily and clean it at least weekly, usually with white vinegar (check the manual). Top-fill tanks, wide openings and dishwasher-safe parts make this far easier, and distilled water or a demineralization cartridge cuts mineral buildup."),
  ],
  "faq": [
   ("Is a warm mist or cool mist humidifier better?","Cool mist is the better choice for most homes, especially with kids or pets, because warm-mist models heat the water until it's very hot. HGTV and Bob Vila say warm mist can feel nicer in cold climates and may ease winter congestion, and Bob Vila notes mist temperature rarely changes the room's temperature."),
   ("What size humidifier do I need?","Match the tank and coverage rating to the room: HGTV suggests a tank under 3 liters for spaces under 200 sq ft and about 6 liters for roughly 500 sq ft. For open-plan areas or a whole floor, look at large evaporative models such as the Levoit Superior 6000S (up to 3,000 sq ft) or the Vornado Evap40 (up to 1,000 sq ft)."),
   ("Should I use distilled water in a humidifier?","Use distilled water in ultrasonic humidifiers if you see white dust, because minerals in tap water come out with the mist and settle on nearby surfaces. Evaporative humidifiers trap minerals in their wick, so tap water is fine; Bob Vila says the Levoit Superior 6000S works with tap water for that reason."),
   ("What humidity should my house be in winter?","Keep indoor humidity between 30% and 50%. Live Science cites EPA guidance to stay below 60%, and Bob Vila recommends staying under 50% to limit mold and mildew, so a humidifier with a humidistat or auto mode is worth having."),
   ("Where should I put a humidifier in my bedroom?","Put it at least 3 ft from the bed, at least 1 ft from walls, furniture and curtains, and about 1 ft off the floor, with the mist pointed toward the middle of the room, as Live Science advises. A quiet ultrasonic or evaporative model with a sleep mode works best at night."),
   ("Is an ultrasonic or evaporative humidifier better?","Ultrasonic humidifiers are quieter and need less upkeep, which is why HGTV's top pick is ultrasonic; evaporative humidifiers avoid white dust and are happy with tap water but need replacement wicks. Bob Vila adds that ultrasonic units push out more moisture, while evaporative ones need regular cleaning to keep bacteria away."),
  ],
  "sources": [
   ("HGTV — 6 best humidifiers of 2026, tested and reviewed (September 2026)","https://www.hgtv.com/shopping/product-reviews/best-humidifiers"),
   ("Bob Vila — The best humidifiers for large rooms, tested (February 2026)","https://www.bobvila.com/reviews/best-humidifiers-for-large-rooms/"),
   ("Bob Vila — The best evaporative humidifiers of 2026, tested (January 2026)","https://www.bobvila.com/reviews/best-evaporative-humidifiers-2026/"),
   ("Bob Vila — The best room humidifiers, tested (October 2025)","https://www.bobvila.com/reviews/best-room-humidifiers-2025/"),
   ("Live Science — Best humidifiers 2026 (January 2026)","https://www.livescience.com/best-humidifiers"),
   ("RTINGS — The best humidifiers and best humidifiers for bedrooms (November 2026)","https://www.rtings.com/humidifier/reviews/best/humidifiers"),
   ("Carepod — Carepod One specifications","https://hellocarepod.com/products/carepod-one"),
  ],
 },
 {
  "slug": "best-coffee-makers", "icon": "coffeemaker", "tint": "tint-coffeemaker", "short": "Coffee Makers",
  "title": "The 10 Best Coffee Makers of 2026",
  "price_notes": GIFT_NOTES,
  "card": "Drip coffee makers for every kitchen, from $30 basics to SCA-certified brewers, thermal carafes and grind-and-brew.",
  "lead": "The Technivorm Moccamaster KBGV Select is the best coffee maker for most people: a fast, SCA-certified 10-cup drip brewer. Plus budget and thermal picks.",
  "filters": [("budget","Budget"),("small","Small kitchens"),("thermal","Thermal carafe"),("sca","SCA-certified"),("programmable","Programmable")],
  "products": [
   dict(name="Technivorm Moccamaster KBGV Select", badge="Best overall", price="$$$$", f=["sca"],
        tags=["10 cups, glass carafe","SCA-certified"],
        summary="The top drip pick at Tom's Guide and Reviewed, NBC Select's tested favorite and Food Network's best for craft coffee, where testers rated its coffee highest. Its copper heating element reaches 196–205°F in under a minute, and a full pot brews in about 4 to 6 minutes.",
        pros=["Consistently great-tasting coffee","Brews a full or half carafe, with an automatic drip-stop","5-year warranty and a metal build made to last"],
        cons=["Not programmable (no delayed start)","Expensive"]),
   dict(name="OXO Brew 8-Cup Coffee Maker", badge="Best thermal carafe", price="$$$", f=["thermal","sca","small"],
        tags=["8 cups, thermal carafe","Single-cup mode"],
        summary="Tom's Guide's best budget drip pick. This compact, SCA-certified brewer uses a rainshower head to wet the grounds evenly, has separate 2–4 and 5–8 cup settings, can brew a single cup, and pours into a double-walled thermal carafe that keeps coffee hot for hours.",
        pros=["Extremely easy to use","Consistent coffee, cup after cup","Compact for its capacity"],
        cons=["Water tank isn't removable","Not programmable"]),
   dict(name="Cuisinart PerfecTemp 14-Cup Programmable Coffee Maker", badge="Best for large batches", price="$$", f=["programmable"],
        tags=["14 cups, glass carafe","3 brew strengths"],
        summary="Food Network's best overall drip coffee maker and HGTV's pick for large batches. The 14-cup pot holds about nine mugs, you can set it to start up to 24 hours ahead, and it offers three brew strengths, a ready alert, a self-clean function and a 2-hour keep-warm plate.",
        pros=["Big capacity at a mid-range price","Programmable start and auto-shutoff","Three-year warranty"],
        cons=["Carafe lid doesn't flip open, so pouring takes two hands","Machine lid may not clear upper cabinets"]),
   dict(name="BLACK+DECKER 12-Cup Programmable Coffee Maker", badge="Best budget", price="$", f=["budget","programmable"],
        tags=["12 cups","Sneak-A-Cup pause"],
        summary="Food Network's best basic coffee maker, and a Black+Decker 12-cup programmable model is also Reviewed's best value pick. It keeps things simple: a removable brew basket, one-touch programming, measurement marks on the carafe and a Sneak-A-Cup feature for pouring mid-brew.",
        pros=["Very low price","Programmable clock and auto shutoff after 2 hours","Easy to use"],
        cons=["Only one brew strength","Less durable than pricier machines"]),
   dict(name="Breville Precision Brewer Thermal", badge="Best customizable", price="$$$", f=["thermal","sca"],
        tags=["12 cups, thermal carafe","6 presets"],
        summary="Food Network's best splurge and an NBC Select editors' pick. You can adjust brew temperature, bloom time and flow rate, choose from six presets (including one built to SCA standards), and use the Steep & Release valve to brew a single cup without the carafe. Testers liked its cold brew too.",
        pros=["Fine control over temperature, bloom and flow","SCA certified","Comes with flat-bottom and cone filter baskets"],
        cons=["Expensive","Large footprint"]),
   dict(name="Ninja Specialty Coffee Maker", badge="Best for iced coffee", price="$$$", f=["programmable"],
        tags=["10 cups + single serve","Fold-away frother"],
        summary="HGTV's best overall and Food Network's pick for hot and cold coffee. The Ninja CM401 has four brew styles, six sizes from a single cup to a full 10-cup carafe, a programmable timer and a fold-away milk frother. HGTV found it fits under upper cabinets and brews a full pot in about 8 minutes.",
        pros=["Hot, iced and specialty-style coffee in one machine","All removable parts are dishwasher-safe","Built-in milk frother"],
        cons=["The frother doesn't heat milk","More settings than a casual coffee drinker needs"]),
   dict(name="Café Specialty Drip Coffee Maker", badge="Best smart coffee maker", price="$$$", f=["thermal","sca","programmable"],
        tags=["10 cups, thermal carafe","Wi-Fi + voice control"],
        summary="HGTV's best splurge and NBC Select's smart brewer. It's SCA-certified, lets you set the brew temperature from 185°F to 205°F, and connects to the SmartHQ app, Alexa and Google Home for scheduling and strength control. HGTV's tester preferred its flavor to the other machines tested.",
        pros=["Precise temperature control","App and voice scheduling","Built-in water filter"],
        cons=["All parts must be hand-washed","May not fit under low cabinets"]),
   dict(name="Mr. Coffee 5-Cup Coffee Maker", badge="Best for small kitchens", price="$", f=["budget","small"],
        tags=["5 cups (25 oz)","Pause and pour"],
        summary="HGTV's best compact coffee maker. It measures about 10 x 8.8 x 6.4 inches, brews roughly two 12-oz mugs, pauses when you pull out the carafe and shuts itself off after two hours. A good fit for one or two coffee drinkers, dorms and small apartments.",
        pros=["Very small footprint","Simple to use","Cheapest pick on this list"],
        cons=["Parts aren't dishwasher-safe","Too small for a household of coffee drinkers"]),
   dict(name="Keurig K-Duo", badge="Best pod and carafe combo", price="$$$", f=["programmable"],
        tags=["12-cup carafe + K-Cups","Removable tank"],
        summary="HGTV's most versatile coffee maker. One side brews a 12-cup carafe of ground coffee and the other brews single K-Cup pods, sharing one removable water tank. You get programmable brewing, adjustable strength and pause-and-pour in a low-profile body.",
        pros=["Full pots and single pods in one machine","Adjustable strength and batch size","Programmable carafe brewing"],
        cons=["Carafe isn't dishwasher-safe","Reusable filters are sold separately"]),
   dict(name="Café Specialty Grind and Brew Coffee Maker", badge="Best with grinder", price="$$$", f=["programmable"],
        tags=["10 cups + single serve","Built-in grinder"],
        summary="Reviewed's best coffee maker with a grinder. It grinds whole beans right before brewing, can make a single cup or a full 10-cup carafe, and is programmable, so you can wake up to freshly ground coffee without a separate grinder taking up counter space.",
        pros=["Fresh-ground coffee with no extra appliance","Single cups or full carafes","Stylish design"],
        cons=["Prone to splashing","Large footprint"]),
  ],
  "tips": [
   ("Know what a 'cup' means","Coffee makers count 5-oz cups, so a 12-cup machine makes about seven 8-oz mugs and a 5-cup machine about two 12-oz mugs. One or two drinkers are fine with 5–8 cups; households and offices want 10–14."),
   ("Look for SCA certification","The Specialty Coffee Association certifies home brewers that hit its targets for water temperature (about 195–205°F), brew time (roughly 4–8 minutes) and even saturation. Testers at Food Network and HGTV found SCA-certified machines tended to taste better."),
   ("Thermal or glass carafe?","A glass carafe costs less and lets you see how much is left, but it sits on a hot plate that can make coffee taste scorched over time. A double-walled thermal carafe keeps coffee hot for hours without a hot plate, though it's harder to clean."),
   ("Programmable or not?","A programmable start (up to 24 hours ahead on the Cuisinart PerfecTemp) means coffee is ready when you wake up. Some of the best-tasting brewers, like the Moccamaster KBGV Select and OXO Brew 8-Cup, skip timers entirely, so decide which matters more."),
   ("Measure your counter and cabinets","Check the height under your upper cabinets before you buy: HGTV notes tall machines such as the Cuisinart PerfecTemp and Café Specialty Drip may not clear them. Removable water tanks and dishwasher-safe parts make daily use easier."),
  ],
  "faq": [
   ("What is the best coffee maker in 2026?","The Technivorm Moccamaster KBGV Select is the best coffee maker for most coffee lovers in 2026: it's the top drip pick at Tom's Guide and Reviewed, and Food Network testers rated its coffee highest. On a budget, the BLACK+DECKER 12-Cup Programmable is Food Network's best basic pick."),
   ("Is a Moccamaster worth it?","Yes, if you drink drip coffee every day and care about flavor: the KBGV Select is SCA-certified, heats water to 196–205°F in under a minute, brews a full pot in about 4 to 6 minutes and carries a 5-year warranty. It isn't programmable, so pick something like the Cuisinart PerfecTemp if you want a timer."),
   ("What does SCA certified mean on a coffee maker?","It means the Specialty Coffee Association has tested the brewer and confirmed it meets its standards for water temperature, brew time and how evenly the grounds are soaked. Picks here with SCA certification include the Moccamaster KBGV Select, OXO Brew 8-Cup, Breville Precision Brewer and Café Specialty Drip."),
   ("Is a thermal carafe better than glass?","For flavor, usually yes: a thermal carafe keeps coffee hot without a warming plate, while a glass carafe's hot plate can scorch coffee the longer it sits. Glass carafes are cheaper and easier to clean, and thermal carafes are harder to see into and to scrub."),
   ("How often should you clean a coffee maker?","Rinse or wash the carafe and brew basket after every use, and descale the machine every one to three months depending on how hard your water is. Use the self-clean cycle if it has one, or a vinegar-and-water mix or descaling solution, following the manufacturer's instructions."),
   ("What is the best coffee maker with a grinder?","The Café Specialty Grind and Brew is Reviewed's best coffee maker with a grinder; it grinds whole beans before brewing and makes anything from a single cup to a 10-cup carafe. Reviewed notes a built-in grinder adds cost and cleaning, so a separate burr grinder can be the better long-term setup."),
  ],
  "sources": [
   ("Tom's Guide — Best coffee maker 2026: we tested over 90 machines (November 2026)","https://www.tomsguide.com/home/coffee-makers/best-coffee-makers"),
   ("Reviewed — The best drip coffee makers of 2026 (March 2026)","https://reviewed.com/cooking/best-right-now/best-drip-coffee-makers"),
   ("HGTV — 5 best automatic drip coffeemakers of 2026, tested and reviewed (February 2026)","https://www.hgtv.com/shopping/product-reviews/best-drip-coffeemakers"),
   ("Food Network — 6 best drip coffeemakers of 2026, tested and reviewed (February 2026)","https://www.foodnetwork.com/how-to/packages/shopping/product-reviews/best-drip-coffee-makers"),
   ("NBC Select — The best coffee makers of 2026","https://www.nbcnews.com/shopping/kitchen/best-coffee-makers-brewers-grinders-n1172991"),
  ],
 },
 {
  "slug": "best-blenders", "icon": "blender", "tint": "tint-blender", "short": "Blenders",
  "title": "The 10 Best Blenders of 2026",
  "price_notes": GIFT_NOTES,
  "card": "Blenders for smoothies, soups and frozen drinks, from a $40 portable to Vitamix, Ninja and personal single-serve picks.",
  "lead": "The Vitamix Explorian E310 is the best blender for most people: powerful, easy to clean and great at smoothies. Plus budget, personal and portable picks.",
  "filters": [("budget","Budget"),("smoothies","Smoothies"),("single","Single-serve"),("ice","Crushing ice"),("hot","Hot soups"),("quiet","Quiet"),("small","Small kitchens")],
  "products": [
   dict(name="Vitamix Explorian E310", badge="Best overall", price="$$$$", f=["smoothies","hot","small"],
        tags=["48 oz container","1,400 W, 10 speeds"],
        summary="Food Network's best overall blender after testing more than 21 models, and the best smoothie blender RTINGS has tested. It pairs a 1,400-watt motor with 10 speeds and a pulse setting, can blend hot liquids for soups, and its squat 48 oz container may fit under upper cabinets.",
        pros=["Strong, consistent blending, from smoothies to nut butter","Dishwasher-safe parts","Handles hot liquids"],
        cons=["Expensive","Smaller container than many rivals"]),
   dict(name="Ninja Professional Blender (BL610)", badge="Best budget", price="$$", f=["budget","smoothies","ice"],
        tags=["72 oz pitcher","1,000 W"],
        summary="Food Network's best value pick, HGTV's best value and Food Network's best overall blender for smoothies. The big 72 oz pitcher and 1,000-watt motor crush ice and frozen fruit well, and the blade assembly lifts out so the parts can go in the dishwasher.",
        pros=["Large capacity at a low price","Strong at crushing ice","Removable, dishwasher-safe blades and a pour spout"],
        cons=["Louder than the other blenders Food Network tested","Not suited to hot soups (HGTV)"]),
   dict(name="Ninja Detect Power Blender Pro", badge="Best Vitamix alternative", price="$$$", f=["single","smoothies"],
        tags=["72 oz pitcher","BlendSense auto mode"],
        summary="Tom's Guide's runner-up, which it found came close to Vitamix performance for far less money. It has a 72 oz pitcher, an 1,800-watt motor, three speeds, three chop settings and a BlendSense auto mode; the version Tom's Guide tested also came with a 24 oz single-serve cup, and it made peanut butter in about three minutes.",
        pros=["Near-Vitamix results at a mid-range price","Removable blades for easy cleaning","Powerful enough for nut butter"],
        cons=["No tamper","BlendSense auto mode felt gimmicky to Tom's Guide"]),
   dict(name="Ninja BlendBoss", badge="Best for smoothies", price="$$", f=["budget","smoothies","single","ice","small"],
        tags=["Single-serve tumbler","3 auto programs"],
        summary="TechRadar's best blender for smoothies and Tom's Guide's best budget pick. This personal blender blends straight into the tumbler you drink from, has Smoothie, Ice Crush and Blend programs, and takes up little counter space. Tom's Guide found it crushes ice quickly and handles dips too.",
        pros=["Fast, powerful smoothies","Blends in the cup you drink from","Easy cleanup and a small footprint"],
        cons=["Needs a good amount of liquid","Only one cup included, and the lid doesn't lock"]),
   dict(name="Braun TriForce Power Blender (JB9040)", badge="Best for everyday cooking", price="$$$", f=["smoothies"],
        tags=["2 L (about 2 qt) jug","10 speeds + 6 presets"],
        summary="TechRadar's best blender overall, which it also recommends for cooking. The triangular 2-liter jug pulls ingredients into the blades efficiently, and you get 10 speeds plus pulse, six presets and a built-in cleaning mode, with dishwasher-safe parts.",
        pros=["Fast, powerful blending","Lots of presets","Cleaning mode and dishwasher-safe parts"],
        cons=["Noisy on high settings","Few color options"]),
   dict(name="Breville Fresh & Furious", badge="Best quiet blender", price="$$$", f=["smoothies","ice","quiet","small"],
        tags=["1.5 L jug","Smoothie + ice crush presets"],
        summary="HGTV's best blender for quiet blending and TechRadar's best medium-capacity pick. It's quieter than many blenders, compact for a jug model, and has one-touch presets for smoothies, green smoothies and crushing ice. TechRadar found it especially good with nuts.",
        pros=["Quieter than most full-size blenders","Compact footprint for a jug blender","Handy presets, including ice crush"],
        cons=["Inner lid can leak a little when filled to the max (TechRadar)"]),
   dict(name="Vitamix Ascent X2", badge="Best splurge", price="$$$$", f=["smoothies","hot"],
        tags=["48 oz container","1,500 W, 10-year warranty"],
        summary="Tom's Guide's best blender overall. The 1,500-watt Ascent X2 adds three one-touch programs, including a smoothie setting, to Vitamix's variable speed dial, chews through hard ingredients, cleans up easily and comes with a full 10-year warranty.",
        pros=["Excellent with hard and frozen ingredients","Smoothie program plus variable speed","Long 10-year warranty"],
        cons=["Very expensive","Loud"]),
   dict(name="Ninja Compact Kitchen System (AMZ493BRN)", badge="Best blender and food processor combo", price="$$$", f=["single"],
        tags=["72 oz pitcher + 40 oz bowl","18 oz single-serve cup"],
        summary="Food Network's best blender-food processor combo. One 1,200-watt base drives a 72 oz blender pitcher, a 40 oz food processor bowl and an 18 oz single-serve cup, and its Auto-iQ controls only show the programs that suit the container you've attached.",
        pros=["Blender, food processor and personal blender in one","Auto-iQ programs adapt to each container","Covers smoothies, chopping and dough"],
        cons=["Extra containers take up storage space","More than you need if you only make smoothies"]),
   dict(name="Oster Master Series Blender with Texture Select", badge="Best with a glass jar", price="$$", f=["budget","single"],
        tags=["6-cup glass jar","24 oz Blend-N-Go cup"],
        summary="HGTV's best blender for beginners. It uses a six-cup shatter-resistant glass jar instead of plastic, includes a 24 oz Blend-N-Go cup for drinks on the go, and has one-touch texture settings for thin, medium or thick results alongside manual controls.",
        pros=["Glass jar instead of plastic","Simple one-touch texture settings","Dishwasher-safe jar"],
        cons=["Less powerful than the full-size Ninja and Vitamix picks"]),
   dict(name="BlendJet 2", badge="Best portable", price="$", f=["budget","single","quiet","small"],
        tags=["16 oz, rechargeable","About 15 blends per charge"],
        summary="Food Network's best portable blender. It's a cordless 16 oz blender that weighs about 1.3 pounds, recharges by USB-C, manages roughly 15 blends per charge and has a lock mode so it can't switch on in your bag. Testers found it relatively quiet.",
        pros=["Light and easy to take anywhere","Lock mode prevents accidental blending","Relatively quiet"],
        cons=["Small capacity","No sipping opening in the cap, and not dishwasher-safe"]),
  ],
  "tips": [
   ("Pick the right size","Single-serve blenders (about 16–26 oz) suit one or two drinks you take with you. Full-size jugs of 48–72 oz are better for families, batch smoothies, soups and nut butter; the Ninja BL610's 72 oz pitcher is the largest pick here."),
   ("Wattage is a guide, not a guarantee","HGTV suggests about 1,000 watts or more for easy, reliable blending, but Food Network and Tom's Guide note wattage alone doesn't measure performance: motor design and container size matter too. A smaller single-serve blender can do well with less power than a big jug."),
   ("Check before blending hot soup","Only blend hot ingredients in a blender made for it, such as the Vitamix Explorian E310, and use a vented lid so pressure can't build up. HGTV says the Ninja BL610 isn't suited to hot soups."),
   ("Plastic or glass?","Most high-speed blenders use BPA-free Tritan plastic because glass could shatter at those speeds. If you'd rather avoid plastic, the Oster Master Series uses a shatter-resistant glass jar; glass jars are heavier."),
   ("Load it the right way","Put liquids and tough greens like kale at the bottom, then frozen and hard ingredients on top. Don't run every task on the top speed: Food Network notes that loading incorrectly or always blending on high can strain the motor."),
   ("Make cleanup easy","Look for dishwasher-safe parts or removable blades (both Ninja jug picks have them). The quickest clean: add a little dish soap and warm water and run the blender on high for 30–60 seconds, then rinse."),
  ],
  "faq": [
   ("What is the best blender in 2026?","The Vitamix Explorian E310 is the best blender for most people in 2026: it's Food Network's best overall after testing more than 21 blenders and the best smoothie blender RTINGS has tested. On a budget, the Ninja Professional Blender (BL610) is Food Network's and HGTV's best value pick at around $80."),
   ("Is a Vitamix worth it?","A Vitamix is worth it if you blend often and want one machine that handles smoothies, nut butter and hot soups for years: the Explorian E310 has a 1,400-watt motor and handles hot liquids, and the Ascent X2 carries a 10-year warranty. If you mostly make smoothies, the Ninja Detect Power Blender Pro came close to Vitamix performance in Tom's Guide's tests for much less."),
   ("What is the best blender for smoothies?","The Vitamix Explorian E310 is RTINGS' best blender for smoothies, and the Ninja Professional Blender (BL610) is Food Network's best overall smoothie blender for the price. For single servings you drink from the cup, TechRadar's pick is the Ninja BlendBoss."),
   ("How many watts should a good blender have?","Aim for about 1,000 watts or more for a full-size blender that crushes ice and frozen fruit easily, HGTV advises. Tom's Guide notes a single-serve blender can work well with less, around 900 watts, because wattage depends on motor type and container size."),
   ("Can you put hot liquids in a blender?","Yes, but only in a blender designed for it and with a vented lid, because steam can build pressure and push the lid off. The Vitamix Explorian E310 is made to handle hot liquids, while HGTV says the Ninja BL610 isn't suited to hot soups."),
   ("How do you clean a blender?","Add a couple of drops of dish soap and some warm water, run the blender on high for 30 seconds to a minute, then drain and rinse. For stuck-on residue, TechRadar suggests a paste of one tablespoon of baking soda and one teaspoon of white vinegar, scrubbed with a brush."),
  ],
  "sources": [
   ("Food Network — 6 best blenders of 2026, tested and reviewed (February 2026)","https://foodnetwork.com/how-to/packages/shopping/product-reviews/best-blenders"),
   ("Food Network — 6 best blenders for smoothies of 2026, tested and reviewed (July 2026)","https://www.foodnetwork.com/how-to/packages/shopping/product-reviews/best-blenders-for-smoothies"),
   ("TechRadar — The best blender 2026 (October 2026)","https://www.techradar.com/best/best-blenders"),
   ("Tom's Guide — Best blenders, reviewed by appliance experts (August 2026)","https://www.tomsguide.com/best-picks/best-blenders"),
   ("HGTV — 9 best blenders of 2026 for smoothies and shakes (February 2026)","https://www.hgtv.com/shopping/product-reviews/best-blenders-for-smoothies"),
   ("RTINGS — The best blenders for smoothies (October 2026)","https://www.rtings.com/blender/reviews/best/smoothies"),
  ],
 },
 {
  "slug": "best-stand-mixers", "icon": "mixer", "tint": "tint-mixer", "short": "Stand Mixers",
  "title": "The 10 Best Stand Mixers of 2026",
  "price_notes": GIFT_NOTES,
  "card": "Stand mixers for cookies, cakes and bread dough, from a budget tilt-head to the KitchenAid Artisan, Ankarsrum and Ooni spiral mixers.",
  "lead": "The KitchenAid Artisan is the best stand mixer for most home bakers. Plus budget, compact, bread-dough and big-batch picks from Cuisinart, Ooni and Bosch.",
  "filters": [("budget","Budget"),("bread","Bread dough"),("big","Big batches"),("small","Small kitchens"),("beginners","Beginners"),("quiet","Quiet")],
  "products": [
   dict(name="KitchenAid Artisan Stand Mixer", badge="Best overall", price="$$$$", f=["beginners","quiet"],
        tags=["Artisan Series 5 qt tilt-head (KSM150)","325 W, 10 speeds"],
        summary="The best overall pick at Food Network, Tom's Guide and BestReviews. The 5-quart Artisan Series tilt-head comes with a flat beater, dough hook, wire whip and pouring shield, and its front hub takes optional attachments such as pasta makers. Food Network found it excellent with cookie dough, egg whites and whipped cream, and it comes in more colors than any rival.",
        pros=["Reliable with cookies, cakes, egg whites and whipped cream","Quiet motor; hub for optional attachments","Huge choice of colors"],
        cons=["Bounced on the counter with heavy bread dough at higher speeds (Food Network)","Costs about $150 more than the KitchenAid Classic for similar results (America's Test Kitchen)"]),
   dict(name="Cuisinart Precision Master SM-50", badge="Best KitchenAid alternative", price="$$$", f=["budget","beginners","quiet"],
        tags=["5.5 qt tilt-head","500 W, 12 speeds + pulse"],
        summary="Tom's Guide's best budget stand mixer and BestReviews' best bang for the buck. It has a bigger 5.5-quart bowl and a more powerful 500-watt motor than the KitchenAid Artisan, 12 speeds plus pulse, a splash guard and a three-year limited warranty, and it's often on sale for about $200.",
        pros=["Bigger bowl and more speeds for much less money","Quiet and easy to use, even for beginners","Three-year limited warranty"],
        cons=["Not the strongest at kneading dough (Tom's Guide)","Struggled with egg whites and stiff doughs in America's Test Kitchen's tests"]),
   dict(name="KitchenAid Classic Series 4.5-Quart Stand Mixer", badge="Best entry-level KitchenAid", price="$$$$", f=["budget","beginners"],
        tags=["4.5 qt tilt-head (K45SS)","Adjustable beater height"],
        summary="America's Test Kitchen's Best Buy. It made billowy egg whites and handled a double batch of pizza dough, putting in strong all-round results for less than the Artisan. It's pared down: no splash guard, no handle on the bowl and coated rather than stainless steel beaters.",
        pros=["Strong all-round performance for the price","Adjustable beater height","Much cheaper than the Artisan Series"],
        cons=["No splash guard or bowl handle","Coated beaters; the tilt head broke in ATK's extreme abuse test"]),
   dict(name="Ankarsrum Assistent Original", badge="Best for serious bakers", price="$$$$", f=["bread","big"],
        tags=["Motor-in-base design","Steel bowl + plastic bowl"],
        summary="America's Test Kitchen's winning stand mixer. Its motor sits in the base, and ATK found it aced every test, from whipping just two egg whites to kneading pizza and bagel doughs, with no speed limit when kneading. It comes with a large steel bowl (about 5.25 quarts usable, per ATK) and a smaller plastic bowl.",
        pros=["Top results in every America's Test Kitchen test","Kneads heavy dough at any speed","Sturdy, with a clear view into the bowl"],
        cons=["Steep learning curve and lots of parts to store","Open-top bowl means keeping fingers clear"]),
   dict(name="Ooni Halo Pro Spiral Mixer", badge="Best for bread dough", price="$$$$", f=["bread","big"],
        tags=["Spiral dough hook","750 W, 5-year warranty"],
        summary="Tom's Guide's best stand mixer for bread. A spiral dough hook develops gluten like a bakery mixer, and it handles very large batches; America's Test Kitchen found it very fast at kneading big batches and stable on the counter, with a bright bowl light, a digital timer dial and a five-year warranty.",
        pros=["Fast, excellent kneading for big batches of bread and pizza dough","Stable, with a bowl light and timer","Five-year warranty"],
        cons=["Expensive (about $799 at Tom's Guide's check)","Struggled with small amounts, like whipping two egg whites (ATK)"]),
   dict(name="KitchenAid 7-Quart Bowl-Lift Stand Mixer", badge="Best for big batches", price="$$$$", f=["big","bread"],
        tags=["7 qt bowl-lift (KSM70)","11 speeds"],
        summary="Recommended by America's Test Kitchen for big batches. The bowl-lift design has 11 speeds, uncoated stainless steel attachments and adjustable tool height, and it handled large batches well in ATK's tests. Bowl-lift mixers have wide bases suited to large, heavy loads, Food Network notes.",
        pros=["Handles large batches well","Uncoated stainless steel attachments","Adjustable tool height"],
        cons=["Heavy and bulky (about 25.6 lb, per ATK)","KitchenAid's speed-2 limit for kneading makes dough take longer"]),
   dict(name="Bosch Universal Plus Stand Mixer", badge="Best lightweight", price="$$$$", f=["bread"],
        tags=["About 12.7 lb (ATK)","Whips cream in ~45 seconds"],
        summary="Recommended by America's Test Kitchen. It's light for its power, yet ATK found it sturdy: it kneaded bagel bread and pizza dough well and whipped cream in about 45 seconds.",
        pros=["Light enough to move around easily","Kneads bread and pizza dough well","Very fast at whipping cream"],
        cons=["You have to switch attachments mid-recipe","A bit loud at high speed; the metal bowl has no handle"]),
   dict(name="KitchenAid Artisan Mini 3.5-Quart Stand Mixer", badge="Best for small kitchens", price="$$$$", f=["small","beginners"],
        tags=["3.5 qt tilt-head","10 speeds, flex-edge beater"],
        summary="Food Network's best compact stand mixer. It excelled in all of Food Network's tests, whipping egg whites and cream with little splatter, and comes with a coated dough hook, wire whisk and a flex-edge silicone beater that scrapes the bowl. It's easy to move, clean and store.",
        pros=["Smaller and lighter than full-size mixers","Flex-edge beater scrapes the bowl as it mixes","Simple controls and lots of colors (ATK)"],
        cons=["Rocked at top speed with sticky brioche dough (Food Network)","Too small for double batches (ATK)"]),
   dict(name="Costway Stand Mixer", badge="Best budget", price="$$", f=["budget","beginners"],
        tags=["6 speeds","About $110 when tested"],
        summary="Food Network's best budget stand mixer, at about $110 when tested. It creamed butter and sugar in 45 seconds and got through every one of Food Network's tests, including the toughest bread test, without walking across the counter.",
        pros=["Very low price","Passed every Food Network test, including bread dough","Quick at creaming butter and sugar"],
        cons=["Light and doesn't feel very sturdy","Few extras"]),
   dict(name="Hamilton Beach All-Metal Stand Mixer", badge="Best value", price="$$$", f=["budget"],
        tags=["4.5 qt tilt-head","Beater, dough hook and whisk"],
        summary="Food Network's best value pick. It comes with the same three attachments as the KitchenAid and handled whipped cream, egg whites and cookie dough well for much less money.",
        pros=["Good results with egg whites, whipped cream and cookie dough","All-metal build","Much cheaper than a KitchenAid"],
        cons=["Struggled with heavy brioche dough at higher speeds","Clumsy tilt head; you may need to lift the beater to scrape the bowl"]),
  ],
  "tips": [
   ("Tilt-head or bowl-lift?","Tilt-head mixers like the KitchenAid Artisan are easier to use and usually cheaper, and are ideal for cookies, cakes and single batches; check that your cabinets clear the head when it's raised. Bowl-lift mixers such as the KitchenAid 7-Quart have wider bases and bigger bowls for large, heavy batches."),
   ("A 5-quart bowl suits most kitchens","Food Network calls 5 quarts a good size for home baking; BestReviews suggests 4 to 4.5 quarts for one or two people and about 6 quarts for a large family. America's Test Kitchen measured usable capacity well below the label on many mixers, so size up if you bake double batches."),
   ("Torque matters more than watts","America's Test Kitchen calls torque the true measure of a stand mixer: a good mixer doesn't slow down or strain in heavy dough. The 325-watt KitchenAid Artisan and 500-watt Cuisinart SM-50 show that wattage alone doesn't predict results."),
   ("Bake bread often? Check the kneading rules","KitchenAid recommends kneading on speed 2, which ATK found makes heavy dough slower. Mixers with no kneading speed limit, like the Ankarsrum Assistent Original, or a spiral hook, like the Ooni Halo Pro, are built for frequent bread and pizza dough."),
   ("Look at the attachments","At minimum you want a flat beater, dough hook and wire whisk. A flex-edge beater saves scraping, a pouring shield cuts splatter, and ATK prefers uncoated stainless steel tools because coated ones can chip."),
   ("Heavier is steadier","Light, cheap mixers can shake or walk across the counter with stiff dough. If you'll store the mixer in a cupboard, weigh that against how often you'll lift it: the KitchenAid 7-Quart weighs about 25.6 lb, the Bosch Universal Plus about 12.7 lb (ATK)."),
  ],
  "faq": [
   ("What is the best stand mixer in 2026?","The KitchenAid Artisan Stand Mixer (5-quart, KSM150) is the best stand mixer for most people in 2026: it's the best overall pick at Food Network, Tom's Guide and BestReviews. For less money, the Cuisinart Precision Master SM-50 is Tom's Guide's best budget pick, with a 5.5-quart bowl and a 500-watt motor."),
   ("Is a KitchenAid stand mixer worth it?","A KitchenAid is worth it if you bake regularly: the Artisan handles cookie dough, egg whites and whipped cream reliably, and its hub takes optional attachments like pasta makers. To save money, America's Test Kitchen found the KitchenAid Classic 4.5-quart performs similarly for about $150 less and named it its Best Buy."),
   ("Which is better, a tilt-head or bowl-lift stand mixer?","A tilt-head mixer is better for most home bakers because it's easier to use, usually cheaper and fine for cookies and cakes. A bowl-lift mixer is better if you often make large or heavy batches, because it has a wider base and a bigger bowl."),
   ("What size stand mixer do I need?","A 5-quart stand mixer is the right size for most home bakers, according to Food Network. BestReviews suggests 4 to 4.5 quarts for one or two people and around 6 quarts for a large family; a 3.5-quart mini like the KitchenAid Artisan Mini suits small kitchens but can't handle double batches."),
   ("What is the best stand mixer for bread dough?","The Ankarsrum Assistent Original is the best stand mixer for bread dough in America's Test Kitchen's testing: it aced pizza and bagel doughs and has no speed limit for kneading. Tom's Guide's pick for bread is the Ooni Halo Pro Spiral Mixer, whose spiral hook gives excellent gluten development in large batches."),
   ("How many watts should a stand mixer have?","Wattage isn't a reliable guide to stand mixer performance: America's Test Kitchen says torque is what counts, and BestReviews notes a well-engineered lower-wattage mixer can beat a cheaper high-wattage one. For example, the 325-watt KitchenAid Artisan is a top pick over many more powerful models."),
  ],
  "sources": [
   ("Food Network — 5 best stand mixers of 2026, tested and reviewed (October 2026)","https://foodnetwork.com/how-to/packages/shopping/product-reviews/best-stand-mixer"),
   ("America's Test Kitchen — The best stand mixers (October 2026)","https://www.americastestkitchen.com/equipment_reviews/2593-the-best-mixers"),
   ("BestReviews — Best stand mixers (October 2026)","https://bestreviews.com/best-stand-mixers"),
   ("Tom's Guide — Best stand mixers (May 2026)","https://www.tomsguide.com/uk/best-picks/best-stand-mixers"),
  ],
 },
 {
  "slug": "best-knife-sets", "icon": "knife", "tint": "tint-knife", "short": "Knife Sets",
  "title": "The 10 Best Knife Sets of 2026",
  "price_notes": GIFT_NOTES,
  "card": "Kitchen knife sets with and without a block, from a Victorinox starter set to Wüsthof, Shun and self-sharpening Henckels picks.",
  "lead": "The Wüsthof Classic 9-Piece is the best knife set for most home cooks. Plus budget, beginner, Japanese and self-sharpening picks from Victorinox and Shun.",
  "filters": [("budget","Budget"),("beginners","Beginners"),("small","Small kitchens"),("japanese","Japanese-style"),("steak","With steak knives"),("gift","Gifts & registries")],
  "products": [
   dict(name="Wüsthof Classic 9-Piece Knife Block Set", badge="Best overall", price="$$$$", f=["beginners","gift"],
        tags=["Forged, full-tang German knives","7 knives + shears, steel, acacia block"],
        summary="Food Network's best overall knife set. The forged, full-tang knives are well balanced and sharp out of the box, and the set covers nearly every job: 8-inch cook's, 8-inch bread, 8-inch carving, 6-inch utility and two paring knives, plus kitchen shears, a honing steel and an acacia block.",
        pros=["Well balanced, sharp and sturdy","Covers every core task, including carving","Honing steel and shears included"],
        cons=["Expensive (about $580 to $685 at Food Network's check)","Heavy: America's Test Kitchen found the Wüsthof Classic chef's knife tiring on tough squash"]),
   dict(name="Victorinox Fibrox 4-Piece Knife Set", badge="Best value", price="$$", f=["budget","beginners","small"],
        tags=["8\" chef's, 10.25\" bread, 6\" utility, 4\" paring","Model 5.1193.4-X1"],
        summary="America's Test Kitchen's winning knife set. Every blade passed ATK's tests, and the four knives are the ones most cooks actually use: a light 8-inch chef's knife (about 5.9 oz), a long 10.25-inch bread knife, a 6-inch utility knife and a 4-inch paring knife, all with Fibrox handles.",
        pros=["Every knife passed America's Test Kitchen's tests","Long bread knife handles big crusty loaves","Light chef's knife (about 5.9 oz)"],
        cons=["No block, steel or shears","Paring knife handle is bulky for small hands (ATK suggests adding a Swiss Classic paring knife)"]),
   dict(name="Henckels Classic Precision 15-Piece Self-Sharpening Set", badge="Best self-sharpening", price="$$$", f=["beginners","steak"],
        tags=["Slots hone the blades","Includes 8 steak knives"],
        summary="Food Network's best self-sharpening set. The block's slots hone each knife as you pull it out and put it back, and the slots are labeled. You get an 8-inch chef's, 7-inch santoku, 5.5-inch prep, 5-inch serrated utility and 4-inch paring knife, eight 4.5-inch steak knives, shears and an ash block.",
        pros=["Block keeps the edges honed automatically","Large assortment, including steak knives","Labeled slots"],
        cons=["Somewhat lightweight knives","No carving knife"]),
   dict(name="Ginsu Gourmet Chikara 8-Piece Knife Set", badge="Best budget", price="$$", f=["budget","beginners","japanese"],
        tags=["Forged Japanese stainless steel","About $100 at Food Network's check"],
        summary="Food Network's best value pick at about $100. The knives were sharp out of the box, held their edge and felt well balanced, and the chef's knife could cut through chicken bones. The set has 8-inch chef's, 7-inch santoku, 5-inch utility, 5-inch serrated utility and 3.5-inch paring knives, a sharpening steel, shears and a bamboo block.",
        pros=["Low price for a forged set","Sharp and well balanced","Light, a good fit for smaller hands (CNN Underscored)"],
        cons=["No long bread knife"]),
   dict(name="Shun Classic 5-Piece Starter Block Set", badge="Best Japanese", price="$$$$", f=["japanese","small","gift"],
        tags=["Damascus-clad steel blades","8\" chef's, 6\" utility, 3.5\" paring"],
        summary="Food Network's best Asian knife set. The handcrafted, Damascus-clad blades are very sharp, thin and smooth, with Pakkawood handles. It's a compact set: 8-inch chef's, 6-inch utility and 3.5-inch paring knives, a honing steel and a bamboo block.",
        pros=["Very sharp, thin blades for precise slicing","Compact block","Beautiful enough to give as a gift"],
        cons=["Expensive (about $400 to $440)","No bread knife; thin blades aren't meant for bones or crusty bread"]),
   dict(name="Zwilling Pro 7-Piece Knife Block Set", badge="Best for large hands", price="$$$$", f=["gift"],
        tags=["8\" chef's, 8\" bread, 5.5\" prep, 4\" paring","Shears, hone and block"],
        summary="Recommended by America's Test Kitchen, which found the paring and prep knives precise and the set comfortable for larger hands, with the biggest savings versus buying the pieces separately (about 38%). CNN Underscored named it runner-up and called the chef's knife the standout; its sloped bolster suits a pinch grip.",
        pros=["Excellent chef's knife (CNN Underscored)","Comfortable for larger hands","Big savings over buying knives one by one"],
        cons=["Heavy chef's knife (about 9.7 oz, per ATK) and a short bread knife","Shears feel lightly built"]),
   dict(name="Mercer Culinary Genesis 6-Piece Forged Knife Block Set", badge="Best under $150", price="$$", f=["budget"],
        tags=["Forged blades, 5 knives","Tempered glass block"],
        summary="Reviewed's best value knife set, at about $139. Reviewed found it performs as well as sets costing about three times as much, with good balance, comfortable grips and a favorite serrated knife. It includes 8-inch chef's, 8-inch bread, 6-inch boning, 5-inch utility and 3.5-inch paring knives.",
        pros=["Performs like much pricier sets (Reviewed)","Well balanced","Includes a boning knife"],
        cons=["No honing steel or shears","CNN Underscored found knives awkward to pull from the glass block"]),
   dict(name="Mercer Culinary Millennia 3-Piece Starter Set", badge="Best for beginners", price="$$", f=["budget","beginners","small"],
        tags=["8\" chef's, 10\" bread, 3.5\" paring","Model M4CKDM3PCSS"],
        summary="America's Test Kitchen's Best Buy. It's just the three knives ATK says cover most kitchen tasks, a chef's knife, a long bread knife and a paring knife, and all three are strong performers, which makes it a simple first set for a new cook or first apartment.",
        pros=["The three essential knives and nothing you won't use","Long 10-inch bread knife","Low price"],
        cons=["ATK found buying these three knives separately was cheaper","No block; bulky paring knife handle"]),
   dict(name="Shun Premier 5-Piece In-Drawer Set", badge="Best for small kitchens", price="$$$$", f=["japanese","small","gift"],
        tags=["4 knives + 7-slot in-drawer tray","Free lifetime mail-in sharpening"],
        summary="America's Test Kitchen's upgrade pick. The knives are very sharp and well balanced, and they live in a compact wooden tray inside a drawer, so the set takes no counter space. It includes 8-inch chef's, 9-inch bread, 6.5-inch utility and 4-inch paring knives, and Shun sharpens them for free by mail for as long as you own them.",
        pros=["Very sharp, well-balanced knives","In-drawer tray frees up the counter","Free mail-in sharpening for life"],
        cons=["Bread knife is shorter than ATK's testers wanted, with slightly slippery scalloped teeth","Pricey"]),
   dict(name="Material The Knives + Stand", badge="Best with a magnetic stand", price="$$$$", f=["small","gift"],
        tags=["8\" chef's, 6\" serrated, 4\" paring","Magnetic wooden stand"],
        summary="Food Network's best design-statement set. Three sharp, balanced knives with sloped bolsters for a comfortable pinch grip stand on an attractive magnetic stand that takes less room than a block, and the paring knife has a rounded tip.",
        pros=["Sharp, balanced knives","Slim magnetic stand looks good on the counter","Nice packaging for a gift"],
        cons=["Short 6-inch serrated knife","No honing steel or shears"]),
  ],
  "tips": [
   ("Start with the big three","A chef's knife, a bread knife and a paring knife cover most cooking, according to America's Test Kitchen. Aim for an 8-inch chef's knife, a bread knife of at least 10 inches for big loaves, and a 3- to 4-inch paring knife; Food Network adds a utility knife as the third essential."),
   ("Don't pay for pieces you won't use","Big sets can pad the piece count with steak knives, extra paring knives, blocks and shears. ATK warns that mediocre extras inflate the price, and sets aren't always cheaper: the Mercer Culinary Millennia 3-Piece cost more than its knives bought separately."),
   ("Forged or stamped?","Forged blades, like the Wüsthof Classic, are sturdier, hold an edge longer and usually have a bolster and full tang, but they're heavier and cost more. Stamped blades are lighter and easier to maneuver, and usually cheaper."),
   ("Western or Japanese style?","German and other Western knives are thicker and heavier, good for squash and chicken. Japanese knives such as the Shun Classic are thinner, harder and sharper but need more careful handling; Food Network says the Shun Classic isn't suited to crusty bread or bone-heavy jobs."),
   ("Pick storage for your counter","A block protects the blades but takes counter space. A magnetic stand (Material), magnetic wall strip or in-drawer tray (Shun Premier) saves room; never store knives loose in a drawer without blade guards."),
   ("Plan to hone and sharpen","Hand wash and dry knives right away; Reviewed and CNN Underscored both advise against the dishwasher. Hone often, and resharpen about once a year (Food Network) or whenever a blade no longer slices cleanly through paper or tomato skin."),
  ],
  "faq": [
   ("What is the best knife set in 2026?","The Wüsthof Classic 9-Piece Knife Block Set is the best knife set for most people in 2026: it's Food Network's best overall pick, with forged, well-balanced knives for every job. For much less money, America's Test Kitchen's winner is the Victorinox Fibrox 4-Piece Knife Set."),
   ("Is it better to buy a knife set or individual knives?","Buying individual knives is better if you want the best knife for each job or you're still learning what you need, America's Test Kitchen says. A set usually costs less than its knives bought separately (savings of up to about 38% in ATK's lineup) but not always, so compare before you buy."),
   ("What knives should a good knife set include?","A good knife set should include a chef's knife, a serrated bread knife and a paring or utility knife. A honing steel and kitchen shears are useful extras; boning, carving and steak knives are optional."),
   ("Are self-sharpening knife blocks worth it?","A self-sharpening block is worth it if you don't want to hone knives yourself: in sets like the Henckels Classic Precision 15-Piece, each slot hones the blade every time you remove or return the knife. You'll still need a full sharpening now and then."),
   ("Are forged knives better than stamped?","Forged knives are sturdier and hold an edge longer, but stamped knives are lighter, easier to maneuver and usually cheaper. Forged sets like the Wüsthof Classic usually have a bolster and full tang, which add weight and cost, Food Network notes."),
   ("Can you put a knife set in the dishwasher?","No, most knife sets should be washed by hand and dried right away. Reviewed and CNN Underscored both advise hand washing to protect the edges and finish."),
  ],
  "sources": [
   ("Food Network — 6 best kitchen knife sets of 2026, according to experts (September 2026)","https://foodnetwork.com/how-to/packages/shopping/product-reviews/best-knife-block-sets"),
   ("America's Test Kitchen — The best knife sets of 2026 (October 2026)","https://www.americastestkitchen.com/equipment_reviews/1331-knife-block-sets"),
   ("Reviewed — The best knife sets","https://reviewed.com/cooking/best-right-now/the-best-knife-sets"),
   ("CNN Underscored — Best kitchen knife sets","https://amp.cnn.com/cnn/cnn-underscored/reviews/best-kitchen-knife-set"),
  ],
 },
 {
  "slug": "best-cordless-vacuums", "icon": "stickvac", "tint": "tint-stickvac", "short": "Cordless Vacuums",
  "title": "The 10 Best Cordless Vacuums of 2026",
  "seo_title": "The 10 Best Cordless Stick Vacuums of 2026",
  "price_notes": GIFT_NOTES,
  "card": "Cordless stick vacuums for every home, from Dyson and Shark to budget Levoit and Dreame picks, plus pet hair, self-emptying and vacuum-mop options.",
  "lead": "The Dyson V15 Detect is the best cordless vacuum for most people: strong suction and up to 60 minutes per charge. Plus Shark, pet hair and budget picks.",
  "filters": [("budget","Budget"),("pets","Pet hair"),("light","Lightweight"),("selfempty","Self-emptying"),("carpet","Carpet"),("mop","Vacuum + mop")],
  "products": [
   dict(name="Dyson V15 Detect", badge="Best overall", price="$$$$", f=["pets","carpet"],
        tags=["Up to 60 min","About 6.8 lb, 0.2-gallon bin"],
        summary="The best cordless vacuum RTINGS has tested, and the top pick at Engadget and HGTV. It cleans bare floors and carpet well and is outstanding on pet hair (RTINGS). The Fluffy Optic head lights up fine dust, and a hair screw tool handles long hair on upholstery. Rated for up to 60 minutes on a charge.",
        pros=["Excellent on hard floors, carpet and pet hair","Light on the Fluffy Optic head reveals fine dust","Converts to a handheld with useful tools"],
        cons=["Expensive (about $750 list)","You have to hold the trigger the whole time; no lock button"]),
   dict(name="Shark PowerDetect Clean & Empty", badge="Best self-emptying", price="$$$", f=["pets","carpet","selfempty"],
        tags=["Auto-empty dock","Up to 70 min, 0.7 L bin"],
        summary="Forbes Vetted's best cordless vacuum and TechGearLab's pick for most people. Shark's model IP3251 has strong suction, LED headlights, a flexible wand for reaching under furniture and a dock that empties the bin for you. TechRadar rated the PowerDetect top for cleaning hard floors, carpet and pet hair.",
        pros=["Dock empties the bin automatically","Top cleaning scores, including pet hair (TechRadar)","Up to 70 minutes of runtime"],
        cons=["Heavy (about 8.4 to 8.8 lb) and less nimble on carpet","Limited storage for accessories"]),
   dict(name="Levoit LVAC-300", badge="Best value", price="$$$", f=["budget","pets","carpet"],
        tags=["Up to 60 min","Stands on its own, mini motorized brush"],
        summary="The best budget pick at both Engadget and TechGearLab. It cleans well on carpet and hard floors for the money, has a one-button start so you don't hold a trigger, stands upright by itself and comes with a mini motorized brush that TechGearLab found great for stairs.",
        pros=["Strong cleaning for the price","One-button start, no trigger to hold","Stands upright; good on stairs"],
        cons=["Turbo mode drains the battery quickly","TechGearLab flagged longevity concerns and weak pet hair results on shag rugs"]),
   dict(name="Dreame R20", badge="Best under $200", price="$$", f=["budget","light","pets"],
        tags=["Up to 90 min (standard mode)","About 6 lb, 0.6 L bin"],
        summary="TechRadar's best cordless vacuum overall, at about $150. It scored well across every test, is light and easy to steer, and its battery lasts a long time: up to 90 minutes in standard mode on hard floors.",
        pros=["Very long battery life","Light and maneuverable","Low price"],
        cons=["Not the strongest cleaner in TechRadar's group","Few smart features"]),
   dict(name="Bissell PowerClean FurFinder", badge="Best for pet hair", price="$$", f=["pets","budget","light"],
        tags=["Lights on floor and upholstery tools","Up to 40 min (about 13 on Turbo)"],
        summary="Forbes Vetted's best cordless vacuum for pet hair and TechGearLab's best buy for small spaces. It lifts pet hair well, has lights on both the floor head and the upholstery tool, stands on its own and includes a motorized brush tool that's handy on stairs. Model 4052.",
        pros=["Strong on pet hair","Lights on floor and upholstery tools","Stands upright; easy on stairs"],
        cons=["Short runtime on Turbo (about 13 minutes)","Dustbin is tricky to empty (TechGearLab)"]),
   dict(name="Tineco Pure ONE S11", badge="Best lightweight", price="$$", f=["light","budget"],
        tags=["About 5.7 lb","Up to 40 min, auto-adjusting suction"],
        summary="NBC Select's best lightweight cordless vacuum and HGTV's best budget pick. At about 5.7 pounds it's easy to carry around the house, a sensor adjusts suction to how dirty the floor is, an LED panel shows battery and mode, and it has a HEPA filter and a removable battery.",
        pros=["Light and easy to carry","Suction adjusts automatically","HEPA filter; removable battery"],
        cons=["Struggles on thick carpet (NBC Select)","Long hair tangles on the brush (HGTV)"]),
   dict(name="Levoit LVAC-200", badge="Best budget", price="$$", f=["budget","light"],
        tags=["Up to 50 min","About $200, 0.75 L bin"],
        summary="NBC Select's best budget cordless vacuum and Engadget's budget runner-up. It's affordable, light, runs up to 50 minutes, starts with one button and comes apart easily for storage, which makes it a good fit for apartments and hard floors.",
        pros=["Low price","Long runtime for the money","One-button start; easy to store"],
        cons=["Not the best on carpet","Small dustbin and no storage base (Engadget)"]),
   dict(name="Tineco Pure ONE Station 5", badge="Best self-cleaning", price="$$$", f=["selfempty","pets","carpet"],
        tags=["2.5 L auto-empty base","Up to 70 min"],
        summary="Forbes Vetted's best self-cleaning cordless vacuum and an Engadget honorable mention. Its charging base empties the bin into a 2.5-liter container and cleans the vacuum's path, and smart sensors adjust suction as you go. Forbes found it strong on both hard floors and carpet.",
        pros=["Base empties the bin and cleans the vacuum","Strong on hard floors and carpet","One-button start (Engadget)"],
        cons=["Large dock footprint","No upholstery tool (Forbes Vetted)"]),
   dict(name="Dyson V15 Detect Submarine", badge="Best vacuum and mop", price="$$$$", f=["mop","pets"],
        tags=["Wet roller head included","Up to 60 min"],
        summary="Engadget's best cordless vacuum and mop. It's the V15 Detect with an added Submarine wet head, so one machine vacuums and then mops hard floors and wet spills. You get the same strong suction and up to 60 minutes of runtime.",
        pros=["Vacuums and mops with one machine","Same strong suction as the V15 Detect","Good battery life"],
        cons=["Very expensive (about $950 to $1,050)","Small water tank; no one-button start"]),
   dict(name="Dyson Gen5detect", badge="Best splurge", price="$$$$", f=["pets","carpet"],
        tags=["Push-button power","HEPA filtration, up to about 60 to 70 min"],
        summary="TechGearLab's best-of-the-best pick and TechRadar's best premium cordless vacuum. It has the highest suction TechGearLab measured, cleans every floor type well, uses a power button instead of a trigger, and its screen and dirt detection were the most advanced TechRadar tested.",
        pros=["Highest suction in TechGearLab's tests","Excellent on all floor types and pet hair","Power button instead of a trigger"],
        cons=["Very expensive (about $1,000 list)","Heavy and top-heavy; hard to push on carpet"]),
  ],
  "tips": [
   ("Check real runtime, not the box","Rated runtimes such as 60 or 70 minutes are measured in eco mode. On max or Turbo, TechGearLab measured as little as 7 to 16 minutes, so for a whole-house clean look for at least 40 minutes on standard power or a swappable battery."),
   ("Weight matters more than you think","Most stick vacuums weigh about 5 to 9 pounds. Lighter models like the Tineco Pure ONE S11 (about 5.7 lb) are easier on stairs and overhead; heavier ones like the Shark PowerDetect (about 8.4 to 8.8 lb) tend to clean deeper but tire your arm sooner."),
   ("Trigger or button?","Dyson V-series models make you hold a trigger the whole time, which testers at Forbes Vetted and TechGearLab found tiring. The Levoit LVAC-300, Tineco Station 5 and Dyson Gen5detect use a one-press power button."),
   ("Pet hair needs the right head","For pet hair, look for an anti-tangle or comb-style brush roll, strong suction and a motorized mini tool for furniture and stairs, like the Bissell FurFinder. A bin of at least 0.5 liters saves trips to the trash."),
   ("Self-emptying docks save a messy job","Docks on the Shark PowerDetect Clean & Empty and Tineco Station 5 empty the bin for you, which helps with allergies and pet hair, but they need floor space and cost more."),
   ("Keep it clean","Empty the bin often, rinse washable filters and let them dry fully, and cut hair off the brush roll. Engadget also suggests wiping sensors and charging contacts so the vacuum keeps running at full power."),
  ],
  "faq": [
   ("What is the best cordless vacuum in 2026?","The Dyson V15 Detect is the best cordless vacuum for most people in 2026: it's the top pick at RTINGS, Engadget and HGTV, with strong suction on every floor type and up to 60 minutes of runtime. Forbes Vetted's top pick, the Shark PowerDetect Clean & Empty, is the best alternative if you want a self-emptying dock."),
   ("Is a Dyson cordless vacuum worth it?","A Dyson is worth it if you want top cleaning and pet hair performance; the V15 Detect and Gen5detect lead several 2026 tests. But Dysons cost the most, and Shark, Levoit, Tineco and Dreame models clean well for far less: TechRadar's best overall, the Dreame R20, costs about $150."),
   ("How long do cordless vacuum batteries last on a charge?","Most cordless vacuums run about 30 to 40 minutes per charge, and some reach 60 to 70 minutes, Engadget says. Those numbers are for the lowest power setting; on max power TechGearLab measured only about 7 to 16 minutes."),
   ("Can a cordless vacuum replace a regular vacuum?","Yes, a good cordless vacuum can replace a corded one in many homes, but in larger homes it often works best as a second vacuum for quick cleanups. Cordless models trade some suction and runtime for convenience, though pricier models come close to corded power."),
   ("What is the best cordless vacuum for pet hair?","The Bissell PowerClean FurFinder is Forbes Vetted's best cordless vacuum for pet hair, and the Dyson V15 Detect is outstanding on pet hair in RTINGS' tests. Look for strong suction, an anti-tangle brush roll and a motorized mini tool for furniture."),
   ("Shark or Dyson: which cordless vacuum is better?","Dyson usually wins on light weight, dust detection and premium features, while Shark offers self-emptying docks and strong cleaning for less money. In 2026 tests, the Dyson V15 Detect is RTINGS' and Engadget's top pick, and the Shark PowerDetect is Forbes Vetted's and TechGearLab's."),
  ],
  "sources": [
   ("RTINGS — The 5 best cordless vacuums of 2026 (October 2026)","https://www.rtings.com/vacuum/reviews/best/cordless"),
   ("Forbes Vetted — The best cordless vacuums (August 2026)","https://www.forbes.com/sites/forbes-personal-shopper/article/best-cordless-vacuums/"),
   ("TechGearLab — Best cordless stick vacuums (October 2026)","https://www.techgearlab.com/topics/floor-cleaning/best-cordless-stick-vacuum"),
   ("TechRadar — The best cordless vacuums 2026 (October 2026)","https://techradar.com/home/vacuums/best-cordless-vacuum-cleaners"),
   ("NBC Select — The best cordless vacuums of 2026 (November 2026)","https://www.nbcnews.com/select/shopping/best-cordless-vacuums-rcna242135"),
   ("Engadget — The best cordless vacuums for 2026","https://www.engadget.com/best-cordless-vacuum-130007125.html"),
   ("HGTV — Best cordless vacuums of 2026","https://www.hgtv.com/shopping/product-reviews/best-cordless-vacuums"),
  ],
 },
 {
  "slug": "best-over-ear-headphones", "icon": "headphones", "tint": "tint-headphones", "short": "Over-Ear Headphones",
  "title": "The 10 Best Over-Ear Headphones of 2026",
  "price_notes": GIFT_NOTES,
  "card": "Noise-cancelling, budget, wired and long-battery over-ear headphones from Sony, Bose, Sennheiser, Apple, Sonos and more, for travel, work and home.",
  "lead": "The Sony WH-1000XM6 are the best over-ear headphones for most people, with top noise cancelling and great sound. Plus Bose, iPhone, budget and wired picks.",
  "filters": [("budget","Budget"),("anc","Noise cancelling"),("travel","Travel"),("battery","Long battery"),("iphone","iPhone"),("wired","Wired")],
  "products": [
   dict(name="Sony WH-1000XM6", badge="Best overall", price="$$$$", f=["anc","travel"],
        tags=["30 hr with ANC (40 hr off)","About 9 oz, folds flat"],
        summary="The best overall pick at NBC Select, TechRadar and Engadget, and the best headphones RTINGS has tested. Sony moved to a new processor and 12 noise-cancelling mics (up from 8), so noise cancelling improved, the sound is detailed and open, and the headphones now fold for travel. Battery is rated at 30 hours with ANC on.",
        pros=["Class-leading noise cancelling and great sound","Light, foldable and comfortable","10-band EQ and automatic noise settings in the app"],
        cons=["Pricey (about $450 list)","Average battery for the price; no water resistance (TechRadar)"]),
   dict(name="Bose QuietComfort Ultra Headphones (2nd Gen)", badge="Best noise cancelling", price="$$$$", f=["anc","travel"],
        tags=["30 hr battery","About 9 oz, lossless audio over USB-C"],
        summary="The noise-cancelling pick at NBC Select, TechRadar and Engadget. Its ANC copes better with sudden noise than the first generation, and Tom's Guide found it blocks more noise than the Sony WH-1000XM6 after six months with both. Battery rises to about 30 hours, it plays lossless audio over USB-C and it folds into its case.",
        pros=["Best-in-class noise cancelling","Very comfortable fit","Foldable, with lossless USB-C audio"],
        cons=["Touch controls can be finicky (NBC Select)","Fewer EQ options and no hi-res certification"]),
   dict(name="Sennheiser HDB 630", badge="Best sound quality", price="$$$$", f=["anc","battery"],
        tags=["60 hr battery","USB-C hi-res dongle included"],
        summary="What Hi-Fi?'s award-winning best wireless over-ear headphones and Engadget's pick for sound quality. The natural, detailed sound gets a boost from the included USB-C dongle, which carries up to 24-bit/96kHz audio from phones and laptops. It adds a detailed EQ, a crossfeed option and a 60-hour battery (about 45 hours using the dongle).",
        pros=["Natural, detailed, dynamic sound","Dongle improves audio from phones and laptops","Very long 60-hour battery"],
        cons=["Noise cancelling is weaker than Sony and Bose","Needs battery power even for wired listening; plain design"]),
   dict(name="Apple AirPods Max 2", badge="Best for iPhone", price="$$$$", f=["iphone","anc"],
        tags=["20 hr with ANC","About 13.6 oz, replaceable ear cushions"],
        summary="NBC Select's best Apple headphones and TechRadar's recommendation for iPhone owners. They work smoothly with Apple devices and offer great sound and noise cancelling, and the ear cushions are easy to replace. NBC notes they are the only top pick that doesn't work equally well with every type of device.",
        pros=["Great sound and noise cancelling","Seamless with iPhone, iPad and Mac","Easily replaceable ear cushions"],
        cons=["Expensive (about $549 list) and heavy","Short 20-hour battery; soft cover instead of a hard case"]),
   dict(name="Sonos Ace Ultra", badge="Best for movies", price="$$$$", f=["anc"],
        tags=["35 hr with ANC","Dolby Atmos, adaptive ANC"],
        summary="TechRadar's best mid-range over-ear headphones, praised for strong Dolby Atmos with movies, a rich feature set and detailed EQ options. It sounds more musical than the original Sonos Ace, uses adaptive noise cancelling and is rated for 35 hours with ANC on.",
        pros=["Excellent Dolby Atmos for films and shows","Detailed EQ and lots of features","35-hour battery with ANC"],
        cons=["Some rivals deliver more detail","Doesn't fold fully; case feels less premium (TechRadar)"]),
   dict(name="Sony WH-CH730N", badge="Best under $200", price="$$$", f=["budget","anc","battery"],
        tags=["Up to 50 hr with ANC","About 7.3 oz (207 g), foldable"],
        summary="A What Hi-Fi? Award winner as the best cheap noise-cancelling over-ear headphones and TechRadar's best affordable Sony. It's light, foldable and well built for the money, with clear, entertaining sound, strong bass and outstanding battery life: up to 50 hours with ANC on and 75 hours off, per TechRadar.",
        pros=["Outstanding battery life","Light, foldable and comfortable","Customizable EQ"],
        cons=["Sounds best after some EQ tweaking","Noise cancelling is middling; mostly plastic build"]),
   dict(name="Nothing Headphone (a)", badge="Best battery life", price="$$$", f=["budget","battery","anc"],
        tags=["Up to 135 hr (ANC off)","About 75 hr with ANC on"],
        summary="TechRadar's pick for battery life: up to 135 hours with noise cancelling off and about 75 hours with it on, far more than any premium pair. TechRadar also rates its sound as strong and its app as excellent, and praises the physical on-ear controls. List price is $199, and it's often sold for less.",
        pros=["Huge battery life","Strong sound for the price","Excellent app and physical controls"],
        cons=["Heavy, boxy design","No auto-pause and no case (TechRadar)"]),
   dict(name="Soundcore Life Q30", badge="Best budget", price="$$", f=["budget","anc","travel","battery"],
        tags=["40 hr with ANC (60 hr off)","Hard travel case"],
        summary="NBC Select's best budget over-ear headphones. For well under $100 you get working noise cancelling, a transparency mode, the Soundcore app, a hard carrying case and long battery life: 40 hours with ANC on and 60 hours off.",
        pros=["Great value","Excellent battery life","Hard case and companion app included"],
        cons=["Plastic-feeling build","No noise cancelling over a wired connection"]),
   dict(name="Sony ULT Wear", badge="Best for bass", price="$$$", f=["budget","anc"],
        tags=["30 hr with ANC (50 hr off)","ULT bass-boost button"],
        summary="NBC Select's best over-ear headphones for bass. The ULT button adds heavy low end on demand, the on-ear controls are easy to use, and battery life is rated at 30 hours with ANC on and 50 hours with it off. Model WH-ULT900N.",
        pros=["Big, punchy bass at the press of a button","Good battery life","Competitive price"],
        cons=["ULT mode can distort audio (NBC Select)"]),
   dict(name="Røde NTH-100", badge="Best wired", price="$$$", f=["wired","budget"],
        tags=["Wired, closed-back","No battery to charge"],
        summary="What Hi-Fi?'s award-winning best wired over-ear headphones. The closed-back design keeps sound in, the sound is revealing and articulate, and the build is solid and comfortable for hours. A good choice for home listening or a desk setup where you don't need Bluetooth or noise cancelling.",
        pros=["Revealing, detailed sound for the price","Well made and comfortable for long sessions","No battery or pairing to worry about"],
        cons=["Can sound analytical to some ears","No wireless or noise cancelling; ears can get warm"]),
  ],
  "tips": [
   ("Decide how much noise cancelling you need","If you fly or commute, the Bose QuietComfort Ultra (2nd Gen) and Sony WH-1000XM6 lead for active noise cancelling (ANC). Sound-first pairs like the Sennheiser HDB 630 cancel less noise, and wired pairs like the Røde NTH-100 rely only on closed-back ear cups."),
   ("Compare battery life with ANC on","Rated battery ranges from 20 hours (AirPods Max 2) to 30 hours (Sony WH-1000XM6, Bose QC Ultra 2nd Gen), 60 hours (Sennheiser HDB 630) and about 75 hours with ANC on for the Nothing Headphone (a). Check the ANC-on number, since that's how most people listen."),
   ("Weight affects comfort","Over-ear headphones in this list run from about 7.3 oz (Sony WH-CH730N, 207 g) to about 13.6 oz (AirPods Max 2). Heavier pairs press more on the head over long flights; reviewers call the AirPods Max 2 and Nothing Headphone (a) heavy."),
   ("Match your phone","AirPods Max 2 work best with iPhone, iPad and Mac and have no companion app. NBC Select notes the other top picks work equally well with iPhone and Android, so they're the safer choice for mixed households."),
   ("Closed-back or open-back?","Every pick here is closed-back, which keeps sound in and outside noise out: right for travel, offices and shared rooms. Open-back headphones sound airier but leak sound, so they're best kept for quiet listening at home."),
   ("Check the case and wired options","The Sony, Bose and Soundcore pairs come with hard cases; AirPods Max 2 ship with a soft cover and the Nothing Headphone (a) with no case. The Bose and Sennheiser can play audio over USB-C, but the HDB 630 needs charge even when wired, and the Soundcore Life Q30 can't use ANC over a cable."),
  ],
  "faq": [
   ("What are the best over-ear headphones in 2026?","The Sony WH-1000XM6 are the best over-ear headphones for most people in 2026: they're the top pick at NBC Select, TechRadar and Engadget, with class-leading noise cancelling, detailed sound and 30 hours of battery with ANC on. The Bose QuietComfort Ultra Headphones (2nd Gen) are the best alternative if blocking noise matters most."),
   ("Sony WH-1000XM6 or Bose QuietComfort Ultra (2nd Gen): which is better?","The Sony WH-1000XM6 is the better all-rounder, while the Bose QuietComfort Ultra (2nd Gen) has stronger noise cancelling. After six months with both, Tom's Guide picked the Sony for its 10-band EQ (Bose offers 3 bands), better spatial audio and simpler design, but found the Bose blocks more noise."),
   ("Are the AirPods Max 2 worth it?","The AirPods Max 2 are worth it mainly for iPhone owners who want seamless Apple features with great sound and noise cancelling. For everyone else they're hard to justify: they list at $549, weigh about 13.6 oz, last about 20 hours with ANC on and come with a soft cover instead of a hard case."),
   ("What are the best budget over-ear headphones?","The Soundcore Life Q30 are the best budget over-ear headphones, NBC Select's pick, with noise cancelling, a hard case and 40 hours of battery with ANC on for well under $100. For a step up under $200, the Sony WH-CH730N won a What Hi-Fi? Award for best cheap noise-cancelling headphones."),
   ("Which over-ear headphones have the longest battery life?","The Nothing Headphone (a) have the longest battery life here: up to 135 hours with noise cancelling off and about 75 hours with it on, per TechRadar. The Sennheiser HDB 630 last about 60 hours and the Sony WH-CH730N up to 50 hours with ANC on."),
   ("Are noise-cancelling headphones bad for your ears?","No, noise-cancelling headphones are not bad for your ears. TechRadar notes that ANC can actually help protect your hearing, because with less background noise you can listen at a lower volume."),
  ],
  "sources": [
   ("NBC Select — The 7 best over-ear headphones of 2026 (May 2026)","https://www.nbcnews.com/select/shopping/best-over-ear-headphones-rcna206591"),
   ("What Hi-Fi? — Best over-ear headphones 2026 (October 2026)","https://www.whathifi.com/best-buys/headphones/best-over-ear-headphones"),
   ("TechRadar — Best headphones in 2026 (October 2026)","https://www.techradar.com/best/best-headphones"),
   ("TechRadar — Our top over-ear headphones of 2026 so far (October 2026)","https://www.techradar.com/audio/headphones/our-top-over-ear-headphones-of-2026-so-far"),
   ("Engadget — Best wireless headphones for 2026 (July 2026)","https://www.engadget.com/best-headphones-wireless-bluetooth-120543205.html"),
   ("Tom's Guide — Sony WH-1000XM6 vs Bose QuietComfort Ultra 2 after six months (January 2026)","https://www.tomsguide.com/audio/headphones/i-tested-the-sony-wh-1000xm6-vs-bose-quietcomfort-ultra-2-for-6-months-and-theres-a-clear-winner"),
   ("RTINGS — The best headphones of 2026 (October 2026)","https://www.rtings.com/headphones/reviews/best/by-price/under-400"),
  ],
 },
 {
  "slug": "best-smartwatches", "icon": "smartwatch", "tint": "tint-smartwatch", "short": "Smartwatches",
  "title": "The 10 Best Smartwatches of 2026",
  "price_notes": {"$":"Under $150","$$":"About $150–$300","$$$":"About $300–$500","$$$$":"$500+"},
  "card": "The best smartwatches for iPhone and Android, from Apple, Google, Samsung, Garmin, Amazfit and more, including budget, fitness and long-battery picks.",
  "lead": "The Apple Watch Series 12 is the best smartwatch for iPhone, and the Google Pixel Watch 5 is the best for Android. Plus Garmin, Samsung and budget picks.",
  "filters": [("iphone","Works with iPhone"),("android","Works with Android"),("budget","Budget"),("fitness","Fitness & running"),("battery","Long battery"),("health","Health tracking")],
  "products": [
   dict(name="Apple Watch Series 12", badge="Best overall", price="$$$", f=["iphone","health"],
        tags=["Up to 24 hr battery","42mm or 46mm, iPhone only"],
        summary="The best smartwatch overall at Engadget and TechRadar, and Tom's Guide's pick for iPhone. Apple's S11 chip powers new health features: a daily Readiness score with no subscription, heart rate variability tracking, hypertension alerts and sleep apnea detection. The ceramic case option returns, and the 42mm GPS model lists at $399, the same as last year.",
        pros=["Best app support and smart features for iPhone","Upgraded health sensors and free Readiness score","Comfortable, polished design in two sizes"],
        cons=["Works only with iPhone; battery still about 24 hours","Same design and display as the Series 11"]),
   dict(name="Google Pixel Watch 5", badge="Best for Android", price="$$$", f=["android","health","battery"],
        tags=["30 hr (41mm) / 40 hr (45mm)","Loss of Pulse Detection"],
        summary="Engadget's best smartwatch for Android users. Tom's Guide calls it the best watch for on-wrist safety thanks to Loss of Pulse Detection, and its 45mm model lasted about 48 hours in testing, past its 40-hour rating. GPS is more accurate than before, Gemini handles voice requests, and it charges from 5% to full in just under an hour. Starts at $399 (41mm).",
        pros=["Top safety features and good sleep reports","Long battery for a full-featured watch","Fast charging and works with any Android phone"],
        cons=["Prices went up from the Pixel Watch 4","Breathing Emergency Detection not yet available in the U.S."]),
   dict(name="Samsung Galaxy Watch 9", badge="Best for health tracking", price="$$$", f=["android","health"],
        tags=["30 hr (40mm) / 40 hr (44mm)","FDA-cleared sleep apnea detection"],
        summary="TechRadar's best smartwatch for health tracking and Android Central's best Android watch overall. A new Vitals dashboard combines heart rate, HRV, blood oxygen, skin temperature and breathing rate, and a Heart Health score and Fitness Index turn the data into advice without a subscription. Prices start at $379 (40mm Bluetooth).",
        pros=["Deep health and fitness insights, no paywall","Light, thin and comfortable day and night","Gemini voice assistant works well"],
        cons=["ECG and blood pressure need a Samsung phone","Slow charging (about 90 minutes); price went up"]),
   dict(name="Apple Watch SE 3", badge="Best affordable Apple Watch", price="$$", f=["iphone","budget"],
        tags=["Up to 18 hr battery","Always-on display, S10 chip"],
        summary="NBC Select's best budget smartwatch for iPhone, and TechRadar calls it the best Apple Watch for most people. For $249 (40mm) it gets an always-on display for the first time, the same S10 chip as last year's flagship, tougher glass, a Sleep Score and fast charging. It skips ECG, blood oxygen, hypertension and sleep apnea features.",
        pros=["Great value for iPhone owners","Always-on display and fast performance","Fast charging"],
        cons=["Shorter 18-hour battery","Older design with thicker bezels; fewer health sensors"]),
   dict(name="Garmin Venu 4", badge="Best for fitness", price="$$$$", f=["fitness","battery","iphone","android","health"],
        tags=["Up to 12 days (about 5 with always-on)","41mm or 45mm, built-in flashlight"],
        summary="NBC Select's best smartwatch for fitness and Android Central's pick for athletes. It brings Garmin's full set of training tools, accurate GPS and heart rate, and up to 12 days of battery (about 5 with the always-on display) in a slim AMOLED watch that works with both iPhone and Android. Lists at $549.99.",
        pros=["Extensive training and recovery tools","Days of battery, not hours","Works with iPhone and Android; flashlight and speaker"],
        cons=["Expensive","No offline maps; fewer reply and app options than Apple or Google"]),
   dict(name="Amazfit Active 3 Premium", badge="Best budget", price="$$", f=["budget","fitness","battery","iphone","android"],
        tags=["12-day rated battery (about 8 in testing)","1.3-inch AMOLED, 5 ATM"],
        summary="Tom's Guide's top smartwatch pick and its best budget smartwatch. For $169.99 you get a bright touchscreen, extensive fitness and sleep tracking with no subscription for core features, and battery that lasted about eight days in testing (12 days claimed). It works with both Android phones and iPhones.",
        pros=["Strong value for the price","Lots of fitness and sleep features, no subscription","Works with iPhone and Android"],
        cons=["Fewer smart features and apps than Apple or Google watches","Limited style options"]),
   dict(name="Garmin Forerunner 165", badge="Best for running", price="$$", f=["fitness","battery","iphone","android"],
        tags=["Up to 11 days smartwatch mode","43mm AMOLED"],
        summary="Engadget's best smartwatch for running. It's light and accurate, with an AMOLED screen, Garmin Coach training plans, a Race Predictor, wrist-based running power, Morning Report recovery guidance and up to 11 days of battery in smartwatch mode. TechRadar calls it a very good first running watch; list price is $249.99.",
        pros=["Accurate GPS and lots of training features","Bright AMOLED screen and long battery","Light and comfortable to sleep in"],
        cons=["Plastic build; music storage costs extra (Music model)","Missing some advanced metrics serious marathoners want"]),
   dict(name="OnePlus Watch 3", badge="Best battery life", price="$$$", f=["android","battery"],
        tags=["Up to 120 hr (about 5 days)","Wear OS with Google Play apps"],
        summary="The battery-life pick at both TechRadar and Android Central: up to 120 hours on the 47mm model, about five days, which is the longest of any Wear OS watch. You still get Google's apps, a working rotating crown, a bright display and fast charging, for $329.99. Android phones only.",
        pros=["Longest battery life of any Wear OS watch","Full Google Play app support","Fast charging and a classic look"],
        cons=["47mm model is big and heavy","No LTE or ECG in the U.S."]),
   dict(name="Amazfit Active 2", badge="Best under $100", price="$", f=["budget","battery","iphone","android","fitness"],
        tags=["Rated 10 days (about 5 typical)","Works with iPhone and Android"],
        summary="TechRadar's best cheap smartwatch at $99. It has a classic round design, strong health tracking and multi-day battery: rated at 10 days, with TechRadar's review getting about five days of normal use or more. It pairs with both Android phones and iPhones.",
        pros=["Very low price","Strong health tracking","Multi-day battery"],
        cons=["NFC payments only on the pricier Premium model","Strength-workout tracking feels clunky"]),
   dict(name="Withings ScanWatch 2", badge="Best hybrid", price="$$$", f=["battery","health","iphone","android"],
        tags=["Up to 35 days battery","Analog hands, ECG"],
        summary="Android Central's best hybrid smartwatch, and Engadget names the ScanWatch line as a stylish alternative. It looks like a classic analog watch but tracks heart rate, blood oxygen, sleep and a one-lead ECG, shows notifications on a small display and lasts up to about 35 days per charge. List price is $369.95.",
        pros=["Looks like a regular watch","About a month of battery","ECG and broad health tracking"],
        cons=["Tiny grayscale display; no apps","No built-in GPS (uses your phone's); basic fitness tracking"]),
  ],
  "tips": [
   ("Start with your phone","An Apple Watch works only with an iPhone. The Pixel Watch 5, Galaxy Watch 9 and OnePlus Watch 3 need an Android phone, and the Galaxy Watch 9's ECG and blood pressure features need a Samsung phone. Garmin, Amazfit and Withings watches work with both."),
   ("Smartwatch or fitness watch?","Apple, Google and Samsung watches have the best apps, payments, voice assistants and replies, but last about 18–48 hours. Fitness-first watches like the Garmin Venu 4 (up to 12 days) and Forerunner 165 (up to 11 days) trade some smart features for much longer battery and deeper training data."),
   ("Compare battery in hours vs. days","Rated battery ranges from 18 hours (Apple Watch SE 3) and 24 hours (Series 12) to 30–40 hours (Pixel Watch 5, Galaxy Watch 9), 120 hours (OnePlus Watch 3) and up to about 35 days (Withings ScanWatch 2). Turning on an always-on display cuts these numbers."),
   ("Pick the right case size","Most watches come in a small and large size: 40/44mm (SE 3, Galaxy Watch 9), 41/45mm (Pixel Watch 5, Venu 4) or 42/46mm (Series 12). The larger size usually has a bigger battery, like the Pixel Watch 5's 40 hours vs. 30 for the 41mm."),
   ("Check which health features you'll get","Sleep apnea detection is on the Apple Watch Series 12 and Galaxy Watch 9, while the Pixel Watch 5 adds Loss of Pulse Detection. The Apple Watch SE 3 skips ECG, blood oxygen and sleep apnea features, so pay up if those matter."),
   ("Decide on cellular (LTE)","GPS/Bluetooth models need your phone nearby for calls and data. LTE versions cost about $50–$100 more (for example $429 vs. $379 for the Galaxy Watch 9 40mm) plus a monthly carrier fee."),
  ],
  "faq": [
   ("What is the best smartwatch in 2026?","The Apple Watch Series 12 is the best smartwatch in 2026 for iPhone owners: Engadget and TechRadar both rank it best overall, with a new S11 chip, a free daily Readiness score, hypertension alerts and up to 24 hours of battery. Android users should get the Google Pixel Watch 5, Engadget's best smartwatch for Android."),
   ("What is the best smartwatch for Android?","The Google Pixel Watch 5 is the best smartwatch for most Android phones, with Loss of Pulse Detection, better GPS and 30–40 hours of rated battery. If you have a Samsung phone, the Samsung Galaxy Watch 9 is TechRadar's best for health tracking and unlocks ECG and blood pressure features."),
   ("Can you use an Apple Watch with an Android phone?","No, an Apple Watch only works with an iPhone. Pixel and Galaxy watches need an Android phone, while Garmin, Amazfit and Withings watches work with both iPhone and Android."),
   ("What is the best cheap smartwatch?","The Amazfit Active 3 Premium ($169.99) is Tom's Guide's best budget smartwatch, with about eight days of battery in testing and no subscription for core features. Under $100, the Amazfit Active 2 ($99) is TechRadar's best cheap watch; for iPhone, the Apple Watch SE 3 starts at $249."),
   ("Which smartwatch has the longest battery life?","The Withings ScanWatch 2 lasts the longest here, up to about 35 days, because it's a hybrid with analog hands. Among touchscreen watches, the Garmin Venu 4 (up to 12 days) and Garmin Forerunner 165 (up to 11 days) last longest, and the OnePlus Watch 3 (up to 120 hours) is the longest-lasting Wear OS watch."),
   ("Is a Garmin better than an Apple Watch?","A Garmin is better for training and battery life, while an Apple Watch is better for smart features on iPhone. The Garmin Venu 4 lasts up to 12 days and has Garmin's full training tools, compared with about 24 hours for the Apple Watch Series 12, but Apple has far more apps, replies and payment support."),
  ],
  "sources": [
   ("Engadget — Best smartwatches for 2026 (October 2026)","https://www.engadget.com/best-smartwatches-153013118.html"),
   ("TechRadar — The best smartwatches 2026 (October 2026)","https://www.techradar.com/best/best-smartwatch"),
   ("Tom's Guide — The best smartwatches (September 2026)","https://www.tomsguide.com/best-picks/best-smartwatches"),
   ("Tom's Guide — Apple Watch 12 vs Galaxy Watch 9 vs Pixel Watch 5 (November 2026)","https://www.tomsguide.com/wellness/smartwatches/ive-tested-the-apple-watch-12-galaxy-watch-9-and-pixel-watch-5-here-is-the-smartwatch-id-buy-with-my-own-money"),
   ("NBC Select — The best smartwatches (March 2026)","https://www.nbcnews.com/select/shopping/best-smartwatches-rcna248847"),
   ("Android Central — The best Android smartwatches 2026 (August 2026)","https://www.androidcentral.com/best-android-smartwatch"),
   ("Tom's Guide — Google Pixel Watch 5 review (August 2026)","https://www.tomsguide.com/wellness/smartwatches/google-pixel-watch5-review"),
   ("Tom's Guide — Samsung Galaxy Watch 9 review (August 2026)","https://www.tomsguide.com/wellness/smartwatches/i-wore-the-samsung-galaxy-watch-9-for-a-month-the-new-health-tools-impress-but-that-doesnt-mean-you-should-upgrade"),
   ("TechRadar — Apple Watch SE 3 review","https://www.techradar.com/health-fitness/smartwatches/apple-watch-se-3-review"),
   ("TechRadar — Garmin Forerunner 165 review","https://www.techradar.com/health-fitness/smartwatches/garmin-forerunner-165"),
  ],
 },
 {
  "slug": "best-soundbars", "icon": "soundbar", "tint": "tint-soundbar", "short": "Soundbars",
  "title": "The 10 Best Soundbars of 2026",
  "price_notes": {"$":"Under $200","$$":"About $200–$600","$$$":"About $600–$1,000","$$$$":"$1,000+"},
  "card": "The best soundbars for your TV from Sonos, Samsung, Sony, Bose and more, including Dolby Atmos, surround sound, small-room and budget picks.",
  "lead": "The Sonos Arc Ultra is the best soundbar of 2026 for most TVs. Plus Dolby Atmos, surround, small-room and budget picks under $500, $200 and $100.",
  "filters": [("budget","Budget"),("atmos","Dolby Atmos"),("sub","Subwoofer included"),("surround","Rear speakers included"),("small","Small TVs & rooms"),("dialogue","Clear dialogue")],
  "products": [
   dict(name="Sonos Arc Ultra", badge="Best overall", price="$$$$", f=["atmos","dialogue"],
        tags=["Dolby Atmos, HDMI eARC","About 4 ft long, for TVs over 55 in"],
        summary="The best soundbar overall at both What Hi-Fi? and Tom's Guide. On its own it delivers precise, spacious Dolby Atmos with convincing 3D placement, clear dialogue and punchy bass from its Sound Motion woofer, and new top-panel controls make it easy to use. It lists at $1,099; Sonos's Sub 4 and rear speakers can be added later.",
        pros=["Excellent movie sound and clear dialogue from a single bar","Punchy, tuneful bass without a subwoofer","Expandable with a Sonos sub and rear speakers"],
        cons=["No HDMI passthrough and no DTS:X","A full Sonos setup gets expensive; setup needs the Sonos app"]),
   dict(name="Samsung HW-Q990H", badge="Best for Dolby Atmos", price="$$$$", f=["atmos","sub","surround"],
        tags=["11.1.4 channels","Wireless sub + 2 rear speakers included"],
        summary="TechRadar's best soundbar for Dolby Atmos and What Hi-Fi?'s best package. The box includes the soundbar, a wireless subwoofer and two wireless rear speakers for a full 11.1.4 setup with Dolby Atmos and DTS:X, plus HDMI eARC and two HDMI 2.1 inputs. It's often seen around $1,100, and RTINGS rates its predecessor, the HW-Q990F, as the best soundbar it has tested.",
        pros=["Immersive, well-placed height and surround effects","Full-bodied, detailed sound","Lots of connections, including two HDMI 2.1 inputs"],
        cons=["Expensive","Familiar design and a hard-to-read display; last year's model is much cheaper"]),
   dict(name="Sonos Beam Ultra", badge="Best mid-range", price="$$$", f=["atmos","small","dialogue"],
        tags=["7.1.2 with up-firing drivers","About 30 in wide, for TVs up to ~55 in"],
        summary="TechRadar's best soundbar overall, What Hi-Fi?'s best mid-range pick and Tom's Guide's best compact soundbar. Two up-firing drivers give it real Dolby Atmos height, it fills a room with tight, controlled bass for its size, and a speech enhancement tool keeps voices clear. It sells for $699.",
        pros=["Room-filling Atmos from a compact bar","Speech enhancement for clear dialogue","Easy to add Sonos surrounds later"],
        cons=["No HDMI passthrough, no DTS:X and no remote","Pricey for its size; stereo music is weaker"]),
   dict(name="Samsung HW-QS750F", badge="Best surround sound package", price="$$$", f=["atmos","sub","surround"],
        tags=["5.1.2 channels","Wireless sub + rear speakers included"],
        summary="Tom's Guide's best-value soundbar: a 5.1.2 Dolby Atmos system with a powerful wireless subwoofer and rear speakers that delivers cinematic sound for well under $1,000 (listed at $899.99, often seen for $599–$799). The 46-inch bar suits TVs 55 inches and up, and its smart features add to the value.",
        pros=["Powerful subwoofer and wide soundstage","Good balance of detail and bass","Rear speakers included at a mid-range price"],
        cons=["Height effects are less impressive than the width","The left rear speaker still needs a power outlet"]),
   dict(name="Sony BRAVIA Theater Bar 7", badge="Best for movies", price="$$$", f=["atmos","dialogue"],
        tags=["5.1.2 with optional Sub 7","37.5 in wide, Dolby Atmos"],
        summary="Tom's Guide's best soundbar for movies, which it calls a no-brainer recommendation. It has very clear dialogue, good room calibration, controlled bass and immersive true Dolby Atmos. The bar alone is $869 (Tom's Guide saw it at $718), or $1,099 with Sony's Sub 7, which can also be added later for $329.",
        pros=["Very clear dialogue","Immersive Atmos with good room calibration","Can add a sub later"],
        cons=["Music performance is only okay","At 37.5 inches it can look small under very large TVs"]),
   dict(name="Sony HT-S2000", badge="Best without a subwoofer", price="$$", f=["atmos","dialogue","budget"],
        tags=["3.1 channels, built-in woofers","Dolby Atmos & DTS:X (virtual)"],
        summary="TechRadar's best budget soundbar and What Hi-Fi?'s best step-up pick. It's a simple plug-in-and-play 3.1 bar with built-in woofers, clear dialogue and solid dynamics, and it supports both Dolby Atmos and DTS:X using virtual height rather than up-firing speakers. It lists at $499.99 and TechRadar has seen it around $349.",
        pros=["Clear dialogue and easy setup","Supports both Atmos and DTS:X","No separate subwoofer to place"],
        cons=["Limited bass weight","Bluetooth is the only wireless streaming; one HDMI port"]),
   dict(name="Samsung HW-Q600F", badge="Best under $500", price="$$", f=["atmos","sub","budget"],
        tags=["3.1.2 channels","Wireless subwoofer included"],
        summary="The Tom's Guide soundbar writer's go-to mid-range recommendation, with clear dialogue, strong bass from its included wireless subwoofer and immersive Dolby Atmos sound. It was $499 (down from $699) when Tom's Guide recommended it. There's no Wi-Fi, which keeps it simple but means no smart features.",
        pros=["Clear dialogue and strong bass","Wireless subwoofer in the box","Atmos for a mid-range price"],
        cons=["No Wi-Fi or smart features","No rear speakers included"]),
   dict(name="Bose Smart Soundbar", badge="Best small soundbar", price="$$", f=["atmos","small"],
        tags=["3.0.2 with up-firing drivers","27 in long"],
        summary="TechRadar's best small soundbar and a Tom's Guide pick for smaller TVs. At just 27 inches long it still has up-firing speakers for real Dolby Atmos, wide streaming support and a Personal Surround Sound feature that can use compatible Bose earbuds as rear speakers. Tom's Guide listed it at $549, and it's often discounted.",
        pros=["Compact, attractive design","Real Atmos height from a small bar","Wide streaming and voice support"],
        cons=["Limited bass and a narrow soundstage","Only one HDMI port; subwoofer sold separately"]),
   dict(name="Creative Stage Pro", badge="Best under $200", price="$", f=["budget","sub","small"],
        tags=["2.1 with slim separate subwoofer","HDMI ARC, optical, Bluetooth 5.3"],
        summary="What Hi-Fi?'s best compact soundbar, priced around $161. The small bar and slim subwoofer give clear, emotive dialogue and surprisingly strong bass, and flexible connections (HDMI ARC, optical, aux, USB-C and Bluetooth 5.3) mean it works with a TV or a computer. It uses Dolby Audio rather than Atmos.",
        pros=["Subwoofer included for under $200","Clear dialogue and strong bass for the size","Works with TVs and PCs"],
        cons=["No Dolby Atmos; sound stays close to the bar","Wide Sound mode loses definition"]),
   dict(name="Sony HT-S100F", badge="Best under $100", price="$", f=["budget","small","dialogue"],
        tags=["2-channel, HDMI ARC","35 in long, for 32–48 in TVs"],
        summary="Tom's Guide's best soundbar under $100 (about $98) and What Hi-Fi?'s best cheap soundbar. It's a simple, well-made upgrade over TV speakers, mainly for clearer dialogue, with balanced sound for the price and a good remote. Its 35-inch length suits 32- to 48-inch TVs.",
        pros=["Very low price","Clearer dialogue than TV speakers","Premium look and feel"],
        cons=["No surround or Dolby Atmos; light bass","Sometimes doesn't turn on with the TV; can sound a bit thin"]),
  ],
  "tips": [
   ("Match the bar to your TV size","A bar should be roughly as wide as your TV or a little narrower. Tom's Guide pairs 27–30-inch bars like the Bose Smart Soundbar and Sonos Beam Ultra with TVs around 55 inches and smaller, and longer bars like the 46-inch Samsung HW-QS750F or the roughly 4-foot Sonos Arc Ultra with 55-inch-plus TVs."),
   ("Read the channel numbers","In 5.1.2, the first number is the main speaker channels, the second is the subwoofer and the third is the up-firing height channels used for Dolby Atmos. A 2.0 bar like the Sony HT-S100F has no sub or height channels; an 11.1.4 system like the Samsung HW-Q990H adds rear speakers and four height channels."),
   ("Connect with HDMI eARC","Plugging into your TV's HDMI ARC or eARC port lets your TV remote control the soundbar's volume and carries Dolby Atmos from the TV's apps. If you're short on TV ports, look for HDMI inputs (passthrough): the Samsung HW-Q990H has two HDMI 2.1 inputs, while the Sonos Arc Ultra and Beam Ultra have none."),
   ("Real vs. virtual Atmos","Bars with up-firing drivers (Sonos Beam Ultra, Bose Smart Soundbar, Samsung 3.1.2 and 5.1.2 models) bounce height effects off the ceiling. Virtual Atmos bars like the Sony HT-S2000 process the effect without up-firing speakers, which costs less but sounds less overhead."),
   ("Decide on a subwoofer now or later","For TV shows and news, clear dialogue matters most and a subwoofer isn't needed. For movies, a sub adds weight: the Samsung HW-Q600F and HW-QS750F include one, while Sony's Bar 7 can add a Sub 7 later for $329 and Sonos bars pair with the Sonos Sub 4."),
   ("Keep it simple if you want to","Wi-Fi and apps add streaming and room calibration but more setup. The Sony HT-S100F, Sony HT-S2000 and Samsung HW-Q600F work without Wi-Fi; Sonos bars need the Sonos app for setup."),
  ],
  "faq": [
   ("What is the best soundbar in 2026?","The Sonos Arc Ultra is the best soundbar in 2026 for most people: What Hi-Fi? and Tom's Guide both rank it best overall for its precise Dolby Atmos, clear dialogue and punchy bass from a single bar ($1,099). For a full surround system in one box, the Samsung HW-Q990H includes a wireless subwoofer and two rear speakers."),
   ("Is a soundbar worth it?","Yes, a soundbar is worth it for most flat-screen TVs because their thin built-in speakers make dialogue hard to hear. Even the roughly $98 Sony HT-S100F is a clear step up from TV speakers according to Tom's Guide and What Hi-Fi?, and mid-range bars like the Samsung HW-Q600F add a subwoofer and Dolby Atmos."),
   ("Do I need a subwoofer with a soundbar?","No, you don't need a subwoofer for everyday TV: Tom's Guide says clear dialogue matters most for TV shows and a sub and surrounds aren't needed. For movies, a subwoofer adds much more bass; the Samsung HW-Q600F and HW-QS750F include one, and the Sony HT-S2000 has built-in woofers if you don't want a separate box."),
   ("What size soundbar do I need for a 65-inch TV?","For a 65-inch TV, choose a soundbar about 40 inches or longer, such as the 46-inch Samsung HW-QS750F or the roughly 4-foot Sonos Arc Ultra. Compact 27–30-inch bars like the Bose Smart Soundbar and Sonos Beam Ultra suit TVs around 55 inches and smaller."),
   ("What does 5.1.2 mean on a soundbar?","5.1.2 means five main speaker channels, one subwoofer channel and two up-firing height channels for Dolby Atmos. For example, the Samsung HW-QS750F is a 5.1.2 system with a wireless subwoofer and rear speakers, while the Sonos Beam Ultra is rated 7.1.2 from a single bar."),
   ("Sonos Arc Ultra vs. Sonos Beam Ultra: which should I buy?","Buy the Sonos Arc Ultra ($1,099) for a TV over 55 inches and the best single-bar sound, and the Sonos Beam Ultra ($699) for TVs around 55 inches and smaller. The Beam Ultra is about 30 inches wide with up-firing Atmos drivers; the Arc Ultra is about 4 feet long with deeper bass. Neither has HDMI passthrough or DTS:X."),
  ],
  "sources": [
   ("Tom's Guide — The best soundbars (November 2026)","https://www.tomsguide.com/us/best-soundbar-speakers,review-2004.html"),
   ("TechRadar — The best soundbars (October 2026)","https://www.techradar.com/news/best-soundbars-5-soundbars-that-kick-bass/"),
   ("What Hi-Fi? — Best soundbars 2026 (October 2026)","https://www.whathifi.com/us/best-buys/soundbars"),
   ("RTINGS — The 5 best soundbars of 2026 (October 2026)","https://www.rtings.com/soundbar/reviews/best/by-usage/tv"),
   ("Tom's Guide — Top 6 soundbar recommendations for every budget (April 2026)","https://www.tomsguide.com/audio/soundbars/i-struggled-to-hear-movie-dialogue-until-i-got-a-soundbar-heres-my-top-6-recommendations-for-every-budget"),
   ("Tom's Guide — Sony Bravia Theater Bar 7 review","https://www.tomsguide.com/audio/soundbars/sony-bravia-theater-bar-7-review"),
  ],
 },
 {
  "slug": "best-gaming-chairs", "icon": "gamingchair", "tint": "tint-gamingchair", "short": "Gaming Chairs",
  "title": "The 10 Best Gaming Chairs of 2026",
  "price_notes": {"$":"Under $300","$$":"About $300–$700","$$$":"About $700–$1,200","$$$$":"$1,200+"},
  "card": "The best gaming chairs from Secretlab, Razer, AndaSeat, Corsair and Herman Miller, with budget, back pain, big and tall and mesh picks.",
  "lead": "The Secretlab Titan Evo is the best gaming chair of 2026 for most people. Plus picks for back pain, big and tall gamers, mesh fans and budgets under $300.",
  "filters": [("budget","Budget (under $300)"),("back","Back pain & lumbar"),("bigtall","Big & tall"),("recline","Deep recline"),("breathable","Breathable mesh & fabric"),("office","Office-style look")],
  "products": [
   dict(name="Secretlab Titan Evo", badge="Best overall", price="$$", f=["back","bigtall","recline"],
        tags=["Small, Regular and XL sizes (XL up to 395 lb)","165° recline, 4D armrests"],
        summary="The best gaming chair overall at PC Gamer, Tom's Guide and TechRadar. Three sizes cover people from about 5'6\" and under (Small) up to 6'9\" and 395 lb (XL), and every size gets a 4-way adjustable lumbar built into the backrest, a magnetic memory-foam head pillow, 4D armrests and recline to 165°. Choose SoftWeave Plus fabric or Neo Hybrid leatherette; the regular model is about $549, and the NanoGen edition starts around $799.",
        pros=["Three sizes plus adjustable built-in lumbar support","Magnetic memory-foam head pillow and 4D armrests","Durable build; TechRadar assembled it in about 15 minutes"],
        cons=["Not a budget chair, and special editions cost more","Firm seat that takes time to break in"]),
   dict(name="Razer Iskur V2", badge="Best for back pain", price="$$", f=["back","recline"],
        tags=["6D adjustable lumbar support","152° recline, 4D armrests, up to 299 lb"],
        summary="Tom's Guide's best gaming chair for back pain. Its adaptive lumbar support adjusts in six directions to fit the curve of your lower back, and it adds 4D armrests, a 152° recline and a 299 lb weight limit in PU leather or dark gray fabric. It lists at $649, and Tom's Guide found it very easy to assemble.",
        pros=["Highly adjustable lumbar support for lower backs","Sturdy build and very easy assembly","Attractive design"],
        cons=["Awkwardly shaped headrest pillow","Premium price"]),
   dict(name="Corsair TC100 Relaxed", badge="Best budget", price="$", f=["budget","recline"],
        tags=["About $270 list, often about $200","90–160° recline, up to 265 lb"],
        summary="The best budget gaming chair at both TechRadar and GamesRadar+. It has plush padding and soft armrests, comes with headrest and lumbar pillows, reclines from 90 to 160° and suits people up to about 6'2\" and 265 lb. It lists at $269.99, and TechRadar has seen it for $199.99.",
        pros=["Plush, comfortable cushioning for the price","Lumbar and neck pillows included","Understated look that suits a home office"],
        cons=["Frustrating build and some cheap-feeling parts","Only black or gray; 2D armrests and firm lumbar pillow"]),
   dict(name="AndaSeat Kaiser 3 XL", badge="Best for big and tall", price="$$", f=["bigtall","back","recline"],
        tags=["XL fits up to 6'9\" and 395 lb","165° recline, 4-way lumbar"],
        summary="The big-and-tall pick at TechRadar, Tom's Guide and Tom's Hardware. The XL version is rated for people up to 6'9\" and 395 lb, with a steel frame, a 4-way adjustable built-in lumbar, a magnetic memory-foam neck pillow and up to 165° of recline, plus rocking and tilt. Choose PVC leather in several colors or linen fabric; it sells for about $499.",
        pros=["Roomy, very comfortable seat","Great built-in lumbar support","Lots of recline, rock and tilt options"],
        cons=["Big and heavy; takes up a lot of room","Noisy armrest adjustment and so-so stitching"]),
   dict(name="DXRacer Craft", badge="Best value", price="$$", f=["back","recline"],
        tags=["4D armrests, adjustable lumbar","135° recline, up to 275 lb"],
        summary="Tom's Guide's best-value gaming chair at $449 for the standard size and $499 for XL. It comes in woven fabric or EPU leatherette with a big choice of colors and themed designs, and adds a memory-foam headrest, 4D armrests, adjustable lumbar support and a 135° recline. TechRadar likes its wide, comfortable seat and head pillow.",
        pros=["Comfortable, wide seat","Great build quality","Many colors and themed designs"],
        cons=["Headrest is awkward to adjust","Padding may feel too firm for some"]),
   dict(name="Herman Miller x Logitech G Vantum", badge="Best mesh", price="$$$", f=["breathable","back","office"],
        tags=["Knit back, up to 350 lb","12-year warranty, arrives nearly assembled"],
        summary="Tom's Hardware's best gaming chair overall and Tom's Guide's best mesh pick. This office-style chair is built for gaming with a forward-leaning posture, adjustable lumbar plus thoracic pads for the upper back, and a 12-year warranty. It weighs under 40 lb and ships nearly assembled. It launched at $995, and both sites have listed it at $795.",
        pros=["Lumbar and upper-back support","Light, sturdy and almost no assembly","Long 12-year warranty"],
        cons=["Doesn't recline like a racing chair; forward-leaning posture isn't for everyone","Expensive, and the armpads don't lock"]),
   dict(name="LiberNovo Omni", badge="Best ergonomic", price="$$$", f=["back","recline"],
        tags=["Motorized lumbar with massage","Up to 160° recline, up to 300 lb"],
        summary="GamesRadar+'s best gaming chair overall, PC Gamer's best high-end pick and Tom's Hardware's best ergonomic chair. The backrest moves with you and keeps your back supported as you recline (up to 160° in four positions), and it has motorized lumbar support with a 5-minute spinal massage, 4D armrests and a 300 lb limit. It costs about $1,099, with a 5-year warranty (2 years on the electronics).",
        pros=["Very comfortable with little fiddling","Stays supportive when you recline","Built-in massage"],
        cons=["Expensive, from a young brand","Lumbar adjusts in only one direction; shorter warranty on electronics"]),
   dict(name="Razer Iskur V2 X", badge="Best under $300", price="$", f=["budget","breathable","recline"],
        tags=["Breathable fabric, 22 in wide seat","152° recline, up to 300 lb"],
        summary="Tom's Hardware's best budget gaming chair. It keeps the build quality of the pricier Iskur V2 with a wide 22-inch seat, a full 152° recline and a 300 lb limit, and its multi-layer fabric is cooler than faux leather. To hit the price, the lumbar curve is built in rather than adjustable and the armrests are 2D. It lists at $299.99, and Tom's Hardware has seen it for about $190.",
        pros=["Quality build for the price","Breathable fabric stays cooler than faux leather","Wide seat and full 152° recline"],
        cons=["Lumbar isn't adjustable; 2D armrests only","Fabric is harder to clean"]),
   dict(name="AndaSeat Novis", badge="Best under $250", price="$", f=["budget"],
        tags=["About $249","Up to 265 lb, 17.5–21.5 in seat height"],
        summary="GamesRadar+'s best-value gaming chair at about $249. It borrows materials from AndaSeat's pricier chairs and keeps things simple, with a comfortable main cushion, a 21.7-inch-deep seat and a 265 lb limit. The trade-offs are a very stiff tilt and fewer adjustments than racing chairs that cost twice as much.",
        pros=["Low price for a well-made chair","Comfortable main cushion","No gimmicks"],
        cons=["Very stiff tilt","Limited adjustability and customization"]),
   dict(name="Herman Miller x Logitech G Embody", badge="Best splurge", price="$$$$", f=["back","office"],
        tags=["12-year warranty, arrives assembled","Up to 300 lb; no headrest"],
        summary="The premium pick at TechRadar and GamesRadar+ and Tom's Hardware's best splurge. It's an office-style ergonomic chair tuned for gaming, with BackFit spinal support, cooling foam in the seat, adjustable seat depth and height- and width-adjustable armrests. It arrives fully assembled with a 12-year warranty, and lists at about $2,395 (GamesRadar+ has seen it near $1,677).",
        pros=["Extremely comfortable and adjustable","No assembly needed","12-year warranty"],
        cons=["Very expensive","No headrest, and it doesn't recline like a racing chair"]),
  ],
  "tips": [
   ("Pick the right size first","Check the height and weight range before anything else. Secretlab sizes the Titan Evo Small for people up to 5'6\" and 200 lb, Regular for 5'7\"–6'2\" and under 220 lb, and XL for 5'11\"–6'9\" and up to 395 lb. TechRadar suggests an XL model if you're taller than 6'2\" or heavier than 200 lb, and Tom's Hardware says to check both ends of the range if several people will share the chair."),
   ("Get real lumbar support","PC Gamer calls lumbar support a must and a headrest optional. Built-in adjustable lumbar (4-way on the Secretlab Titan Evo and AndaSeat Kaiser 3 XL, 6D on the Razer Iskur V2) fits more backs than a strap-on pillow like the Corsair TC100 Relaxed's."),
   ("Choose fabric, mesh or leatherette","Mesh and fabric stay cooler in long sessions; TechRadar says they're also more comfortable over time than leatherette but harder to keep free of pet hair. If you're prone to spills, PC Gamer suggests leatherette or mesh, which wipe clean more easily than fabric."),
   ("Know your armrests and recline","4D armrests move up/down, forward/back, side to side and rotate; budget chairs like the Razer Iskur V2 X have 2D arms. Racing-style chairs recline to 152–165°, while office-style gaming chairs like the Herman Miller x Logitech G Vantum and Embody only tilt. Tom's Hardware notes many 4D arms don't lock by design; if they wobble at the base, tighten the bolts underneath."),
   ("Budget about $300–$700","Tom's Guide calls $300–$700 the sweet spot. Budget chairs start around $200, racing-style chairs from Secretlab and AndaSeat run about $450–$650, and Herman Miller office-style chairs cost much more but carry 12-year warranties versus the 2–5 years typical of gaming chairs (Tom's Hardware). TechRadar suggests waiting for sales like Black Friday."),
   ("Set it up properly","PC Gamer's posture checklist: knees at about 90°, feet flat on the floor, elbows level with the desk, about two inches between the seat edge and the back of your knees, and the top of your monitor at eye level. Stand up or move every 30–60 minutes."),
  ],
  "faq": [
   ("What is the best gaming chair in 2026?","The Secretlab Titan Evo is the best gaming chair in 2026 for most people: PC Gamer, Tom's Guide and TechRadar all rank it best overall. It comes in three sizes (XL holds up to 395 lb), has a 4-way adjustable built-in lumbar, a magnetic head pillow and a 165° recline, and costs about $549 for the regular model."),
   ("Are gaming chairs good for your back?","A gaming chair can be good for your back if it fits your size and has adjustable lumbar support. PC Gamer says lumbar support is a must and that adjustability and movement matter most. Tom's Guide's pick for back pain is the Razer Iskur V2, whose lumbar adjusts in six directions; whatever you sit in, get up every 30–60 minutes."),
   ("Is a gaming chair or an office chair better?","Neither is better for everyone: gaming chairs usually have taller backrests, headrests, more padding and deeper recline, while office chairs look more subdued and often have longer warranties (12 years for Herman Miller vs. 2–5 years for most gaming chairs, per Tom's Hardware). If you work and game at the same desk, a gaming-focused office chair like the Herman Miller x Logitech G Vantum is a good middle ground."),
   ("How much should I spend on a gaming chair?","Plan on about $300–$700, the sweet spot according to Tom's Guide. Good budget chairs like the Corsair TC100 Relaxed and Razer Iskur V2 X cost about $200–$300, racing-style chairs from Secretlab and AndaSeat run about $450–$650, and premium ergonomic chairs like the LiberNovo Omni and Herman Miller x Logitech G Embody cost $1,000 or more."),
   ("What size Secretlab Titan Evo should I get?","Get the Small if you're up to 5'6\" and under 200 lb, the Regular if you're 5'7\"–6'2\" and under 220 lb, and the XL if you're 5'11\"–6'9\" and up to 395 lb, according to Secretlab's sizing guide. If you fall between sizes, compare weight as well as height."),
   ("How long does a gaming chair last?","A good gaming chair should last at least two to three years of daily use, according to Tom's Guide, and better ones last much longer: PC Gamer's reviewer has used a Secretlab Titan Evo since 2021 and it's still in excellent condition. Warranties are a good guide, from 2 years on budget chairs to 12 years on Herman Miller models."),
  ],
  "sources": [
   ("PC Gamer — Best gaming chair in 2026 (October 2026)","https://www.pcgamer.com/best-gaming-chairs/"),
   ("Tom's Hardware — Best gaming chairs 2026 (October 2026)","https://www.tomshardware.com/best-picks/best-gaming-chairs"),
   ("GamesRadar+ — Best gaming chair (October 2026)","https://www.gamesradar.com/best-gaming-chair"),
   ("TechRadar — Best gaming chair in 2026 (September 2026)","https://www.techradar.com/gaming/best-gaming-chairs"),
   ("Tom's Guide — Best gaming chairs of 2026 (August 2026)","https://www.tomsguide.com/best-picks/best-gaming-chairs"),
   ("Secretlab — How to find the right chair size","https://blog.secretlab.co/stories/how-to-find-the-right-secretlab-chair-size-for-you/"),
  ],
 },
 {
  "slug": "best-air-purifiers", "icon": "airpurifier", "tint": "tint-airpurifier", "short": "Air Purifiers",
  "title": "The 10 Best Air Purifiers of 2026",
  "price_notes": GIFT_NOTES,
  "card": "HEPA air purifiers for allergies, pets, smoke, bedrooms and large rooms, from under $100 to whisper-quiet picks.",
  "lead": "The Winix 5530 is the best air purifier for most people: RTINGS' top pick, with True HEPA and a 23.5 dB low speed. Plus pet, bedroom and budget picks.",
  "filters": [("allergies","Allergies"),("pets","Pets"),("large","Large rooms"),("bedroom","Bedrooms"),("quiet","Quiet"),("budget","Budget")],
  "products": [
   dict(name="Winix 5530", badge="Best overall", price="$$$", f=["allergies","pets","large","bedroom","quiet"],
        tags=["True HEPA + carbon","AHAM: 392 sq ft"],
        summary="RTINGS' best air purifier for most people in its October 2026 update, and also its top pick for allergies, bedrooms, large rooms and budget buyers. Winix lists a smoke CADR of 253, AHAM-verified coverage of 392 sq ft, five fan speeds, Wi-Fi app and Alexa control, and a 23.5 dB lowest setting.",
        pros=["Strong filtration for a mid-range price, per RTINGS","Washable pre-filter plus 12-month carbon and True HEPA filters","Quiet 23.5 dB low speed for bedrooms"],
        cons=["Includes Winix's PlasmaWave ionizer (Winix rates its ozone output at 0.22 ppb)","At 13.3 lbs, bulkier than small-room models"]),
   dict(name="Levoit Core 400S", badge="Best smart", price="$$$", f=["allergies","large"],
        tags=["Pre + carbon + HEPA","App, auto + sleep modes"],
        summary="Engadget's best air purifier overall (March 2026 update). It reliably improved air quality in Engadget's testing, cleans about 1,000 sq ft in 30 minutes by Engadget's figures, and has easy onboard controls, so you don't have to use the VeSync app. Replacement filters run about $50.",
        pros=["Reliable air cleaning in testing","Powerful high speed that isn't overly loud","Inexpensive replacement filters"],
        cons=["Companion app is cluttered","Plain design"]),
   dict(name="Blueair Blue Signature", badge="Best for smoke and odors", price="$$$$", f=["allergies","large","quiet"],
        tags=["CADR 445 smoke","Pre + carbon + HEPA"],
        summary="Tom's Guide's best air purifier overall (June 2026) and Live Science's pick for bad smells. It posted the highest CADR Tom's Guide has tested (445 smoke, 434 dust, 450 pollen), cleared grill and candle smoke in about five minutes, and its carbon layer and odor-neutralizing tech target smells.",
        pros=["Highest CADR in Tom's Guide's testing","Stylish design that doubles as a footstool, with a color-coded air-quality light","Quiet for its power"],
        cons=["Heavy, with no wheels","Fabric pre-filters need regular cleaning and can be damaged by cats"]),
   dict(name="Coway Airmega AP-1512HH Mighty", badge="Best for medium rooms", price="$$$", f=["allergies","bedroom"],
        tags=["HEPA, 12-month filter","CADR 234 smoke"],
        summary="NBC Select's best air purifier for medium rooms (April 2026). The long-running Coway Mighty covers 361 sq ft at 4.8 air changes per hour, with a smoke CADR of 234, an auto mode with an air-quality light, and a HEPA filter that lasts about 12 months. It runs from 24 to 53 dB.",
        pros=["Powerful filtration for its size","Simple controls and auto mode","12-month filter life"],
        cons=["No app or Wi-Fi","Tom's Guide found it loud and heavy"]),
   dict(name="Levoit Core 300", badge="Best for small rooms", price="$$", f=["budget","bedroom","quiet"],
        tags=["AHAM verified","Sleep mode, 24 dB"],
        summary="NBC Select's best air purifier for small rooms. The compact, 7.9-lb Core 300 covers 222 sq ft at 4.8 air changes per hour, with a pollen CADR of 167, three speeds and a sleep mode that drops to about 24 dB. Its HEPA filter lasts about 6 to 8 months.",
        pros=["Strong filtration for its size","Competitive price, often under $100","Compact enough for a nightstand corner"],
        cons=["No smart features (the Wi-Fi Core 300S version costs more)","Filters need replacing more often than some rivals"]),
   dict(name="Levoit Vital 200S", badge="Best for pets", price="$$$", f=["pets","allergies"],
        tags=["Washable pre-filter","Pet mode"],
        summary="Live Science's best air purifier for pet owners (March 2026). It pairs a washable pre-filter that catches hair with an H13 True HEPA filter and activated carbon for odors, adds a dedicated pet mode, and has a CADR of 245 for rooms up to 380 sq ft. It runs from 24 to 54 dB and works with the VeSync app.",
        pros=["Washable pre-filter for pet hair","Dedicated pet mode plus app and voice control","Good value for its performance"],
        cons=["Too large for small spaces","Chunky design"]),
   dict(name="Blueair Blue Pure 211i Max", badge="Best for large rooms", price="$$$", f=["large","pets","allergies"],
        tags=["CADR 410","Up to 635 sq ft"],
        summary="NBC Select's best air purifier for large rooms. Its CADR of 410 for smoke, dust and pollen covers 635 sq ft at 4.8 air changes per hour, it pulls air in from all sides so it can sit almost anywhere, and its HEPA filter lasts about 12 months behind a washable fabric pre-filter.",
        pros=["Very powerful filtration","Long-lasting filters plus a washable pre-filter","360-degree intake makes placement easy"],
        cons=["Large, at 16.2 lbs"]),
   dict(name="Dyson HushJet Purifier Compact", badge="Best quiet", price="$$$$", f=["quiet","bedroom"],
        tags=["24 dB sleep mode","Filter lasts up to 5 years"],
        summary="Tom's Guide's quietest air purifier and Engadget's pick for small rooms. Tom's Guide measured 24 dB in sleep mode and saw it ramp up within seconds of cooking fumes. Its electrostatic filter lasts up to five years, so replacements are rare, but it's rated for only about 200 sq ft.",
        pros=["Whisper-quiet in sleep mode","Long-lasting filter keeps running costs low","Responsive auto mode and a strong app"],
        cons=["Low CADR (131) for medium and large rooms","Expensive for its size"]),
   dict(name="Oneisall Pet Air Purifier", badge="Best under $100", price="$$", f=["budget","pets"],
        tags=["Pre + HEPA + carbon","About 220 sq ft"],
        summary="Tom's Guide's best air purifier under $100 and Live Science's runner-up for pet owners. It's a simple set-and-forget unit with three-stage filtration and two speeds; Live Science found it effective on pet dander, hair and dust, though Tom's Guide expected it to trap more pet hair.",
        pros=["Very affordable","Simple to run, no app needed","Compact and portable"],
        cons=["Touch buttons can be hard to press and can't be muted","No smart features or real-time air-quality data"]),
   dict(name="Windmill Air Purifier", badge="Best design", price="$$$$", f=["quiet","bedroom"],
        tags=["CADR 286 smoke","AHAM verified"],
        summary="Engadget's most attractive pick, NBC Select's runner-up for medium rooms and Tom's Guide's pick for large rooms. Behind the bamboo-slat front is a HEPA filter with a smoke CADR of 286 (442 sq ft at 4.8 air changes per hour), plus app, Alexa and Google Home control and a lifetime warranty.",
        pros=["Attractive design that blends in","Quiet in testing (Tom's Guide measured 38.4 dBA)","Lifetime warranty"],
        cons=["Heavy (21 lbs) with no wheels or handle","Filters last about 6 months"]),
  ],
  "tips": [
   ("Match CADR to your room","CADR (clean air delivery rate) is how many cubic feet of clean air a purifier puts out per minute. NBC Select and Tom's Guide suggest a CADR of at least two-thirds of the room's square footage, so a 300 sq ft bedroom needs about 200. CADR tests assume 8-ft ceilings, so size up for taller rooms."),
   ("Insist on True HEPA","A True HEPA filter captures 99.97% of particles at 0.3 microns, the U.S. Department of Energy standard. 'HEPA-type' or 'HEPA-like' filters aren't certified. AHAM Verified ratings and CARB certification are good signs a maker's claims hold up."),
   ("Add carbon for smells and smoke","HEPA filters trap particles such as dust, pollen and dander but do little for odors. For cooking smells, pets or wildfire smoke, look for an activated carbon layer, as on the Blueair Blue Signature, Levoit Vital 200S and Winix 5530."),
   ("Budget for filters","Most filters need replacing every 6 to 12 months, so check the price before you buy: Engadget lists about $50 for Levoit Core 400S filters, while the Dyson HushJet's filter lasts up to five years. A washable pre-filter catches hair and helps the main filter last."),
   ("Check noise and modes","For bedrooms, choose at least three fan speeds plus a sleep mode; several picks here run at 24 dB or less on low. An auto mode with an air-quality sensor turns the fan up only when the air gets dirty, so you can leave the purifier on all day."),
  ],
  "faq": [
   ("Do air purifiers really work?","Yes, for airborne particles: a True HEPA filter captures 99.97% of particles at 0.3 microns, and in Tom's Guide's tests the Blueair Blue Signature cleared smoke in about five minutes. They can't remove carbon dioxide or dust already settled on carpets and bedding, so Engadget and Live Science say to keep ventilating and vacuuming."),
   ("What size air purifier do I need?","Pick one with a CADR of at least two-thirds of your room's square footage, so a 300 sq ft room needs a CADR of about 200. NBC Select notes AHAM recommends 4.8 air changes per hour (the CDC says 5), and rooms with ceilings above 8 ft need a higher CADR."),
   ("Should I run my air purifier all the time?","Yes, leaving it on low or auto mode is the practical approach. Engadget suggests running it on low most of the time and turning it up when the air gets murky, such as after cooking; auto mode does this for you with an air-quality sensor."),
   ("Where should I put an air purifier?","Put it in the room where you spend the most time, usually the bedroom, with clear space around it: Engadget suggests about a foot from walls and furniture, with one-sided intakes facing the middle of the room. Live Science adds keeping it away from stoves, fireplaces, humidifiers and damp bathrooms."),
   ("What's the best air purifier for allergies?","The Winix 5530 is RTINGS' top pick for allergies in 2026. In general, choose a True HEPA purifier with a high pollen CADR, as Tom's Guide advises, and size it for the bedroom, since Live Science cites EPA-referenced studies suggesting a purifier where you sleep may work better than one in a central spot."),
   ("Is an air purifier the same as a humidifier?","No. An air purifier filters particles and odors out of the air, but it doesn't change humidity, as Live Science points out. For dry winter air you need a humidifier, and for damp rooms or mold a dehumidifier, which tackles the moisture an air purifier can't."),
  ],
  "sources": [
   ("RTINGS — The best air purifiers, best for allergies, bedrooms, large rooms and budget (September–October 2026)","https://www.rtings.com/air-purifier/reviews/best/air-purifiers"),
   ("Tom's Guide — Best air purifiers, tested (June 2026)","https://www.tomsguide.com/best-picks/best-air-purifier"),
   ("NBC Select — Best air purifiers of 2026 (April 2026)","https://www.nbcnews.com/select/shopping/best-air-purifier-ncna1294453"),
   ("Engadget — The best air purifier for 2026 (March 2026)","https://www.engadget.com/best-air-purifier-120040002.html"),
   ("Live Science — Best air purifiers 2026 (March 2026)","https://www.livescience.com/air-purifiers-deals.html"),
   ("Winix — 5530 air purifier specifications","https://winixamerica.com/product/5530/"),
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
        cons=["Pricey for a mug","Charging coaster isn't dishwasher safe"]),
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
 {
  "slug": "gifts-under-50", "kind": "gift", "icon": "gift", "tint": "tint-gift-50", "short": "Gifts Under $50",
  "title": "The 10 Best Gifts Under $50 in 2026",
  "card": "Crowd-pleasing gifts that feel bigger than their price tag.",
  "lead": "Cozy, useful and fun gifts that all come in around $50 or less — picked from this season's most-trusted gift guides, for almost anyone on your list.",
  "price_notes": {"$":"Under $25","$$":"About $25–$50"},
  "no_price_filters": True,
  "filters": [("home","Home & cozy"),("tech","Tech"),("food","Food & drink"),("selfcare","Self-care"),("fun","Games & hobbies")],
  "products": [
   dict(name="Sunbeam Royal Luxe Heated Throw", badge="Best overall", price="$$", f=["home","selfcare"],
        tags=["Heated blanket","Auto shut-off"],
        summary="A soft electric throw with several warmth settings and an automatic shut-off — an easy winter win for parents, partners, friends or coworkers.",
        pros=["Useful for almost anyone","Several heat settings","Shuts itself off"],
        cons=["Has to sit near an outlet"]),
   dict(name="JBL Go 4", badge="Best tech gift", price="$$", f=["tech"],
        tags=["Bluetooth speaker","Waterproof"],
        summary="A palm-size Bluetooth speaker that shrugs off water and dust and plays for up to about seven hours per charge, according to BestReviews.",
        pros=["Tiny enough for a bag or pocket","Water- and dust-resistant","Several colors to choose from"],
        cons=["Small speaker, modest bass"]),
   dict(name="Apple AirTag", badge="Best for iPhone owners", price="$$", f=["tech"],
        tags=["Item tracker"],
        summary="A coin-size tracker that helps Apple users locate keys, bags or luggage through the Find My app — a practical pick highlighted by NBC Select.",
        pros=["Finds lost keys and bags","Long-lasting replaceable battery","Great for travelers"],
        cons=["Only works with Apple devices","Holder or keyring sold separately"]),
   dict(name="Bialetti Moka Express (3-Cup)", badge="Best for coffee lovers", price="$$", f=["food","home"],
        tags=["Stovetop coffee maker"],
        summary="The classic Italian stovetop pot that brews strong, rich coffee with no electricity or pods — a gift BestReviews singles out for coffee fans.",
        pros=["Simple and long-lasting","No pods or filters to buy","Iconic design"],
        cons=["Hand wash only","Takes a little practice"]),
   dict(name="Warmies Microwavable Slippers", badge="Best practical gift", price="$$", f=["home","selfcare"],
        tags=["Heatable slippers"],
        summary="Plush slippers you warm up in the microwave for toasty feet on cold mornings — Forbes Vetted's pick for a practical gift.",
        pros=["Cozy and comforting","No cords or batteries","Fun twist on a classic gift"],
        cons=["Warmth fades after a while","Check the size range"]),
   dict(name="Kosterina Olive Oil & Balsamic Duo", badge="Best food gift", price="$$", f=["food"],
        tags=["Greek olive oil","Gift set"],
        summary="A pairing of Greek extra virgin olive oil and balsamic vinegar in good-looking bottles — Forbes Vetted's favorite food gift under $50.",
        pros=["Great host or hostess gift","Gets used up — no clutter","Attractive packaging"],
        cons=["Set contents vary by retailer"]),
   dict(name="LEGO Botanicals Orchid", badge="Best for crafty adults", price="$$", f=["fun","home"],
        tags=["Build-and-display"],
        summary="A lifelike orchid built from LEGO bricks that makes a relaxing project and then a no-watering-needed decoration.",
        pros=["Relaxing build","Looks great on a shelf","Never wilts"],
        cons=["Not a real plant","Usually near the top of this budget"]),
   dict(name="Nodpod Gentle Pressure Sleep Mask", badge="Best for better sleep", price="$$", f=["selfcare"],
        tags=["Weighted eye mask"],
        summary="A sleep mask with softly weighted pods that block light without straps pressing on the face; BestReviews notes it suits any sleeping position.",
        pros=["Blocks light well","Comfortable for side sleepers","Light, gentle pressure"],
        cons=["Pricey for an eye mask"]),
   dict(name="Q-Less Crossword Dice Game", badge="Best game", price="$", f=["fun"],
        tags=["Word game","Solo or group"],
        summary="A quick crossword-style dice game you can play solo or with friends — NBC Select recommends it as a portable brain teaser.",
        pros=["Fast to learn","Small enough to travel","Great for word-game fans"],
        cons=["Best for people who like puzzles"]),
   dict(name="LANEIGE Lip Sleeping Mask", badge="Best stocking stuffer", price="$", f=["selfcare"],
        tags=["Overnight lip treatment"],
        summary="A cult-favorite overnight lip treatment that leaves lips soft by morning — an inexpensive add-on that rarely misses.",
        pros=["Beloved by beauty fans","Affordable treat","One jar lasts a long time"],
        cons=["Small jar"]),
  ],
  "tips": [
   ("Pick something they'll use up or use daily","Food, coffee gear and self-care treats feel generous without adding clutter."),
   ("Lean cozy in winter","Heated throws and warm slippers are easy wins from November through February."),
   ("Check compatibility","Tech gifts like AirTag need the right phone — make sure it fits what they already own."),
  ],
  "faq": [
   ("What's a good gift under $50 for almost anyone?","A heated throw blanket is a safe bet — it's useful, cozy and works for nearly any age or relationship."),
   ("What are good tech gifts under $50?","A small Bluetooth speaker like the JBL Go 4, or an Apple AirTag for iPhone owners."),
   ("What's a good gift under $25?","A word game like Q-Less or the LANEIGE Lip Sleeping Mask both usually come in under $25."),
   ("Are prices guaranteed to stay under $50?","No — prices change often, especially around Black Friday. Always check the current price before you buy."),
  ],
  "sources": [
   ("Forbes Vetted — Best gifts under $50 (updated 2026)","https://www.forbes.com/sites/forbes-personal-shopper/2025/11/03/best-gifts-under-50/"),
   ("BestReviews — Best gifts under $50 (October 2026)","https://bestreviews.com/gift-guides/holiday/christmas/best-gifts-under-50"),
   ("NBC Select — Best holiday gifts under $50","https://nbcnews.com/select/shopping/best-gifts-under-50-rcna242155"),
  ],
 },
 {
  "slug": "gifts-for-coffee-lovers", "kind": "gift", "icon": "espresso", "tint": "tint-gift-coffee", "short": "Gifts for Coffee Lovers",
  "title": "The 10 Best Gifts for Coffee Lovers in 2026",
  "card": "Smart mugs, grinders and brewers that upgrade every morning cup.",
  "price_notes": GIFT_NOTES,
  "lead": "The best gift for a coffee lover in 2026 is the Ember Mug 3, a smart mug that keeps coffee hot. See 10 expert-backed coffee gifts from under $20 to $400.",
  "filters": [("brewers","Coffee makers"),("gear","Grinders & gear"),("travel","Travel & office"),("fun","Fun extras")],
  "products": [
   dict(name="Ember Mug 3", badge="Best overall", price="$$", f=["travel"],
        tags=["Smart mug","Dishwasher safe"],
        summary="Ember's heated smart mug is a staple of this year's coffee gift guides, and the new Mug 3 adds on-mug buttons for five preset temperatures (125°F to 145°F) and, for the first time, top-rack dishwasher cleaning.",
        pros=["Keeps coffee at a set temperature","About 90 minutes per charge (10 oz) or all day on its coaster","Comes in 10 oz and 14 oz sizes"],
        cons=["Pricey for a mug","Charging coaster isn't dishwasher safe"]),
   dict(name="Fellow Atmos Vacuum Canister (0.7 L)", badge="Best under $50", price="$", f=["gear"],
        tags=["Coffee storage","Vacuum seal"],
        summary="A coffee canister with a twist-to-pump vacuum lid that pulls air out to keep beans fresher for longer; the 0.7-liter size holds up to about 11 ounces of beans.",
        pros=["Looks good on a counter","Seals out air and moisture","Glass, matte black or matte white"],
        cons=["Need to twist the lid to re-seal each time"]),
   dict(name="Baratza Encore", badge="Best coffee grinder", price="$$", f=["gear"],
        tags=["Burr grinder","40 grind settings"],
        summary="A compact electric burr grinder with 40 settings, from fine for espresso-style brews to coarse for French press; Baratza says it can last around 10 years of home use with proper care.",
        pros=["Biggest flavor upgrade for whole-bean drinkers","Simple one-switch operation","Repairable, long-lived design"],
        cons=["Not fine enough for serious espresso (look at the Encore ESP)"]),
   dict(name="AeroPress Original", badge="Best for travel", price="$", f=["brewers","travel"],
        tags=["Manual brewer","Portable"],
        summary="A light, nearly unbreakable press that brews a smooth single cup in a couple of minutes using air pressure and microfilters — easy to pack for trips, camping or the office.",
        pros=["Small and durable","Versatile — concentrated shots or full mugs","Inexpensive"],
        cons=["Makes one or two cups at a time"]),
   dict(name="Cosori Gooseneck Electric Kettle", badge="Best for pour-over fans", price="$$", f=["gear"],
        tags=["Gooseneck kettle","Temperature presets"],
        summary="A stainless-steel gooseneck kettle with five temperature presets and a keep-warm setting, so pour-over fans can pour slowly and precisely at the right temperature.",
        pros=["Precise, slow pour","Five presets plus hold-temperature","Also great for tea"],
        cons=["Smaller capacity than a standard kettle"]),
   dict(name="Breville Bambino Plus", badge="Best espresso machine gift", price="$$$$", f=["brewers"],
        tags=["Espresso machine","Auto milk frothing"],
        summary="A compact espresso machine that's ready in about three seconds and textures milk automatically, making café-style lattes and cappuccinos simple for beginners.",
        pros=["Very fast heat-up","Automatic steam wand for milk","Simple buttons, small footprint"],
        cons=["Needs a good grinder or pre-ground espresso","A big-ticket gift"]),
   dict(name="Fellow Aiden", badge="Best splurge", price="$$$$", f=["brewers"],
        tags=["Smart drip coffee maker","Single cup or full pot"],
        summary="A high-end drip brewer that makes either a single cup or a full carafe, with roast-specific presets and custom brew profiles you can download — a dream gift for the coffee nerd.",
        pros=["Brews a single cup or a full pot","Presets for different roasts","Sleek, modern design"],
        cons=["Expensive for a drip machine"]),
   dict(name="Chemex Pour-Over Glass Coffeemaker", badge="Best classic pour-over", price="$", f=["brewers"],
        tags=["Pour-over","Borosilicate glass"],
        summary="The iconic hourglass-shaped glass brewer that makes clean, bright coffee and doubles as a serving carafe — a timeless gift that usually costs under $50.",
        pros=["Beautiful on the counter","Non-porous glass doesn't hold flavors","Brews several cups at once"],
        cons=["Needs Chemex-style paper filters","Glass can break"]),
   dict(name="Takeya Deluxe Cold Brew Coffee Maker", badge="Best for cold brew fans", price="$", f=["brewers"],
        tags=["Cold brew","Airtight pitcher"],
        summary="An airtight pitcher with a fine mesh filter for making cold brew in the fridge; it keeps a batch fresh for up to two weeks and fits most fridge doors.",
        pros=["Easy overnight cold brew","Airtight lid keeps it fresh","Fits in a fridge door"],
        cons=["Takes about a day to steep"]),
   dict(name="Frank Body Original Coffee Scrub", badge="Best stocking stuffer", price="$", f=["fun"],
        tags=["Coffee body scrub","Under $20"],
        summary="A cult-favorite exfoliating body scrub made with ground coffee plus almond oil and vitamin E — a fun, coffee-themed extra that shows up in multiple 2026 gift guides.",
        pros=["Fun coffee-themed treat","Usually under $20","Great add-on to a bigger gift"],
        cons=["Can be messy in the shower"]),
  ],
  "tips": [
   ("Match the gift to how they brew","Pour-over fans get the most from a gooseneck kettle or a Chemex; latte lovers from an espresso machine with automatic milk like the Bambino Plus; travelers from an AeroPress."),
   ("A burr grinder is the biggest upgrade","Freshly ground beans taste noticeably better. A burr grinder like the Baratza Encore (40 settings) gives a more even grind than a blade grinder."),
   ("Keep beans fresh","Air, light and moisture make coffee go stale. A vacuum canister such as the Fellow Atmos 0.7 L holds about an 11-ounce bag."),
   ("Check sizes and what they already own","The Ember Mug 3 comes in 10 oz and 14 oz; ask yourself if they drink pods, drip or espresso before buying a machine."),
  ],
  "faq": [
   ("What do you get a coffee lover who has everything?","A smart mug like the Ember Mug 3 is a safe bet — most coffee lovers don't own one, and it keeps every cup at their favorite temperature. A vacuum canister or a gooseneck kettle are other upgrades people rarely buy for themselves."),
   ("What are good coffee gifts under $50?","The Fellow Atmos vacuum canister, AeroPress Original, Chemex pour-over, Takeya cold brew maker and Frank Body coffee scrub all usually cost under $50."),
   ("Is the Ember Mug worth it as a gift?","Yes, for anyone who lets coffee go cold. The Ember Mug 3 holds drinks at 125°F to 145°F for about 90 minutes per charge (10 oz) or all day on its coaster, and launched at $129.95 (10 oz) and $149.95 (14 oz)."),
   ("What is the best coffee grinder to give as a gift?","The Baratza Encore is the go-to gift grinder: a burr grinder with 40 settings that Baratza says lasts around 10 years with care. For espresso, choose the Encore ESP version."),
   ("What's a good gift for someone who wants to make espresso at home?","The Breville Bambino Plus. It heats up in about three seconds and froths milk automatically, so beginners can make lattes and cappuccinos with simple buttons."),
   ("Is a coffee subscription a good gift?","Yes — a subscription brings fresh beans from different roasters every month. Good Morning America lists Trade Coffee plans at roughly $17 to $22 per delivery; they're bought from the roaster, not Amazon."),
  ],
  "sources": [
   ("Forbes Vetted — Best gifts for coffee lovers (updated October 2026)","https://www.forbes.com/sites/forbes-personal-shopper/article/gifts-for-coffee-lovers/"),
   ("Good Morning America — The coffee lover's gift guide (November 2026)","https://www.goodmorningamerica.com/shop/story/best-coffee-gifts-2026-138083898"),
   ("Engadget — The best gifts for coffee lovers in 2026","https://www.engadget.com/best-gifts-for-coffee-lovers-130018731.html"),
   ("9to5Toys — Ember Mug 3 launch details (October 2026)","https://9to5toys.com/2026/10/13/ember-dishwasher-safe-smart-mug-3-hits-amazon/"),
  ],
 },
 {
  "slug": "gifts-for-gamers", "kind": "gift", "icon": "controller", "tint": "tint-gift-gamer", "short": "Gifts for Gamers",
  "title": "The 10 Best Gifts for Gamers in 2026",
  "card": "Consoles, handhelds, headsets and fun extras for every kind of player.",
  "lead": "The best gift for a gamer in 2026 is the Nintendo Switch 2, which plays on a TV or on the go. See 10 expert-backed gamer gifts, from $17 add-ons to VR.",
  "price_notes": GIFT_NOTES,
  "filters": [("consoles","Consoles & VR"),("pc","PC gamers"),("accessories","Controllers & headsets"),("retro","Retro & fun")],
  "products": [
   dict(name="Nintendo Switch 2 Mario Kart World Bundle", badge="Best overall", price="$$$$", f=["consoles"],
        tags=["Console","TV or handheld"],
        summary="Nintendo's newest console is the gift that shows up in nearly every 2026 gamer guide: it plays docked on a TV or as a handheld, and Tom's Guide highlights this bundle, which adds Mario Kart World and three months of Nintendo Switch Online.",
        pros=["Plays on the TV or on the go","Bundle includes Mario Kart World and 3 months of Switch Online","Joy-Con controllers detach for two-player games"],
        cons=["No OLED screen","A big-ticket gift (Tom's Guide listed the bundle at $549)"]),
   dict(name="Steam Deck OLED", badge="Best for PC gamers", price="$$$$", f=["consoles","pc"],
        tags=["Handheld gaming PC","OLED screen"],
        summary="Valve's handheld PC lets a PC gamer take their Steam library to the couch or on a trip. The OLED model has a better screen and longer battery life than the original, and Engadget notes that more than 22,000 Steam games are rated Verified or Playable on it.",
        pros=["Plays the Steam games they already own","Better screen and battery than the LCD model","Huge library of verified games"],
        cons=["Demanding games drain the battery quickly","Valve sells it on Steam — check the seller and condition on Amazon"]),
   dict(name="Meta Quest 3S", badge="Best VR gift", price="$$$$", f=["consoles"],
        tags=["Standalone VR","Mixed reality"],
        summary="Tom's Guide calls the Quest 3S one of the best VR headsets for gamers, with many Quest 3 features for less money. It runs on its own with no PC or console, uses the same Snapdragon XR2 Gen 2 chip as the Quest 3, and has full-color passthrough for mixed reality.",
        pros=["No PC or console needed","Same chip and 8GB RAM as the pricier Quest 3","128GB or 256GB storage"],
        cons=["Lower-resolution screens and narrower view than the Quest 3","Battery lasts up to about 2.5 hours"]),
   dict(name="Turtle Beach Stealth Pro II", badge="Best gaming headset", price="$$$", f=["accessories","pc"],
        tags=["Wireless headset","Noise cancelling"],
        summary="Game Informer's headset pick for 2026: a wireless gaming headset that switches between devices, with active noise cancellation, Dolby Atmos and large 60mm drivers.",
        pros=["Switches between devices","Active noise cancellation","Dolby Atmos and 60mm drivers"],
        cons=["About $300","Xbox and PlayStation/PC versions are sold separately — pick the right one"]),
   dict(name="PlayStation DualSense Edge", badge="Best pro controller", price="$$$", f=["accessories"],
        tags=["PS5 controller","Back buttons"],
        summary="Sony's pro controller for PS5 adds mappable back buttons, adjustable trigger lengths and swappable stick caps and modules, and saves quick-swap control profiles. Which? suggests the Xbox Elite Series 2 instead for Xbox players.",
        pros=["Two styles of remappable back buttons","Adjustable triggers and swappable sticks","Carrying case and locking braided cable included"],
        cons=["About $199","Replacement stick modules cost extra"]),
   dict(name="Logitech G502 HERO", badge="Best gaming mouse", price="$$", f=["pc","accessories"],
        tags=["Wired gaming mouse","11 programmable buttons"],
        summary="A Which? members' favorite, Logitech's wired G502 HERO uses the HERO 25K sensor (up to 25,600 DPI) and has 11 programmable buttons plus repositionable weights, so a PC gamer can tune how it feels.",
        pros=["Precise HERO 25K sensor","11 programmable buttons","Adjustable weights"],
        cons=["Wired — the wireless G502 Lightspeed costs more"]),
   dict(name="LEGO Game Boy", badge="Best for retro fans", price="$$", f=["retro"],
        tags=["LEGO set for adults","421 pieces"],
        summary="A near life-size brick replica of the original Game Boy, made as a build for adults, with swappable Game Paks for The Legend of Zelda: Link's Awakening and Super Mario Land and a display stand. GamesRadar includes it in its 2026 gamer gifts.",
        pros=["Fun, nostalgic build","Swappable cartridges with lenticular screens","Comes with a display stand"],
        cons=["Display piece only — no lights, sound or play"]),
   dict(name="Evercade Nexus", badge="Best retro handheld", price="$$$", f=["consoles","retro"],
        tags=["Retro handheld","Physical cartridges"],
        summary="A retro handheld that plays officially licensed game cartridges (with manuals) and comes with Banjo-Kazooie and Banjo-Tooie. It has a 5.89-inch screen and dual analog sticks, works with existing Evercade cartridges, and two units can share one cartridge for local multiplayer.",
        pros=["Comes with Banjo-Kazooie and Banjo-Tooie","Largest Evercade screen yet","Plays the existing Evercade cartridge library"],
        cons=["Extra games are cartridges sold separately"]),
   dict(name="KontrolFreek FPS Freek Galaxy", badge="Best stocking stuffer", price="$", f=["accessories"],
        tags=["Thumbstick grips","Under $20"],
        summary="A pair of clip-on thumbstick toppers — a mid-rise for the left stick and a high-rise for the right — with grippy rubber for shooters. They fit PS5/PS4 and Xbox controllers, and GamesRadar lists KontrolFreek sticks among its under-$20 gifts.",
        pros=["Cheap, useful add-on","Extra height and grip for aiming","Versions for PlayStation and Xbox"],
        cons=["Buy the version for their console"]),
   dict(name="The Elder Scrolls: The Official Cookbook", badge="Best for gamers who cook", price="$", f=["retro"],
        tags=["Cookbook","Hardcover"],
        summary="A 192-page hardcover with more than 60 recipes inspired by the Elder Scrolls games — sweetrolls included — and a fun under-$50 pick from GamesRadar's gamer gift guide.",
        pros=["Great for Skyrim fans","60+ recipes","Usually well under $50"],
        cons=["Best for fans of the series"]),
  ],
  "tips": [
   ("Check which console they own","Controllers, headsets and games are often platform-specific: the DualSense Edge is for PS5, the Turtle Beach Stealth Pro II comes in Xbox and PlayStation/PC versions, and KontrolFreek sticks come in PlayStation and Xbox versions."),
   ("Match the gift to how they play","PC gamers get the most from a Steam Deck OLED or a Logitech G502 HERO; couch and family players from a Nintendo Switch 2; anyone curious about VR from a Meta Quest 3S, which needs no PC or console."),
   ("For the gamer who has everything, go retro or collectible","Nostalgic gifts like the LEGO Game Boy (421 pieces) or the Evercade Nexus with Banjo-Kazooie are things most players don't buy for themselves."),
   ("Under $50, upgrade what they already use","Thumbstick grips such as the KontrolFreek FPS Freek Galaxy (about $17) or a game-themed cookbook make easy stocking stuffers; a Steam, PlayStation, Xbox or Nintendo gift card is the safe choice if you're unsure."),
  ],
  "faq": [
   ("What is the best gift for a gamer in 2026?","The Nintendo Switch 2 is the best all-round gamer gift in 2026: it plays on a TV or as a handheld, and Tom's Guide highlights the Mario Kart World Bundle, which includes the game and three months of Nintendo Switch Online."),
   ("What do you get a gamer who has everything?","Get something they wouldn't buy themselves, like the LEGO Game Boy display set, the Evercade Nexus retro handheld or a pro controller such as the DualSense Edge. A gift card for their platform is the fallback when you're not sure what they own."),
   ("What are good gifts for gamers under $50?","The KontrolFreek FPS Freek Galaxy thumbsticks (about $17) and The Elder Scrolls: The Official Cookbook are both under $50, and the Logitech G502 HERO mouse is often on sale near $40. Steam and console gift cards come in any amount."),
   ("What should I get a PC gamer?","A Steam Deck OLED lets a PC gamer play their Steam library anywhere, with more than 22,000 games rated Verified or Playable. For their desk, the Logitech G502 HERO mouse (11 programmable buttons) is a Which? members' favorite."),
   ("Is the Meta Quest 3S a good gift?","Yes, for anyone curious about VR: Tom's Guide calls it one of the best VR headsets for gamers, and it works on its own with no PC or console. The trade-offs versus the Quest 3 are lower-resolution screens and a narrower field of view."),
   ("Is the PS5 DualSense Edge worth it?","It's worth it for serious PS5 players who want back buttons and adjustable triggers. It costs about $199 and includes swappable stick caps, two kinds of back buttons, a carrying case and a locking braided cable."),
  ],
  "sources": [
   ("Game Informer — Holiday Gift Guide 2026 (November 2026)","https://gameinformer.com/gear/2026/11/03/holiday-gift-guide-2026"),
   ("Tom's Guide — The best tech gifts for everyone on your list (October 2026)","https://www.tomsguide.com/tech/the-best-tech-gifts-for-everyone-on-your-list-and-every-budget"),
   ("GamesRadar+ — The best gifts for gamers in 2026 (October 2026)","https://www.gamesradar.com/hardware/the-best-gifts-for-gamers-in-2026/"),
   ("Which? — Best gifts for gamers (September 2026)","https://www.which.co.uk/reviews/gifts/article/best-gifts-for-gamers-aGmSm1f7RAgF"),
   ("Engadget — The best gifts for gamers","https://www.engadget.com/best-gaming-gifts-for-gamers-150008483.html"),
   ("Tom's Hardware — Meta Quest 3S review","https://tomshardware.com/virtual-reality/meta-quest-3s-review"),
  ],
 },
 {
  "slug": "stocking-stuffers-for-adults", "kind": "gift", "icon": "stocking", "tint": "tint-gift-stocking", "short": "Stocking Stuffers for Adults",
  "title": "The 10 Best Stocking Stuffers for Adults in 2026",
  "card": "Small, useful gifts for grown-ups: trackers, travel tech, treats and self-care.",
  "lead": "The best stocking stuffer for adults in 2026 is Apple's new AirTag, a $29 tracker for keys and bags. See 10 useful, expert-picked ideas, most under $50.",
  "price_notes": GIFT_NOTES,
  "no_price_filters": True,
  "filters": [("under50","Under $50"),("useful","Useful"),("tech","Tech gadgets"),("travel","Travel"),("selfcare","Self-care & sleep")],
  "products": [
   dict(name="Apple AirTag (2nd Generation)", badge="Best overall", price="$", f=["under50","useful","tech","travel"],
        tags=["Item tracker","For iPhone users"],
        summary="Forbes Vetted names the AirTag its best stocking stuffer overall, and Apple's 2026 version is better: Engadget reports Precision Finding reaches up to 50% farther and the speaker is 50% louder, for the same $29 price.",
        pros=["Finds keys, bags and luggage in the Find My app","Louder speaker and longer Precision Finding range than the original","Battery is user-replaceable"],
        cons=["Needs an iPhone or iPad (iOS 26 or later)","Precision Finding needs an iPhone 15 or newer; keyring sold separately"]),
   dict(name="Twelve South AirFly SE", badge="Best for travelers", price="$", f=["under50","tech","travel"],
        tags=["Bluetooth transmitter","20-hour battery"],
        summary="Forbes Vetted's top travel stocking stuffer plugs into a plane's headphone jack so AirPods or other wireless headphones work with seatback entertainment. Engadget lists it at about $40 with up to 20 hours of battery.",
        pros=["Use your own wireless headphones on flights","Up to 20 hours per charge","Also works with gym equipment and other 3.5mm jacks"],
        cons=["Only useful where there's a 3.5mm headphone jack"]),
   dict(name="Anker Nano 3-in-1 Power Bank (10,000mAh)", badge="Best phone charger", price="$", f=["under50","useful","tech","travel"],
        tags=["10,000mAh","Built-in USB-C cable"],
        summary="Engadget's charger pick combines three things in one: a 10,000mAh battery, a wall charger with fold-out prongs, and a built-in USB-C cable, with up to 30W fast charging.",
        pros=["No separate cable or wall block to pack","Up to 30W fast charging","Foldable AC plug"],
        cons=["Built-in cable is USB-C, so older Lightning iPhones need a different version"]),
   dict(name="JBL Go 4", badge="Best Bluetooth speaker", price="$", f=["under50","tech"],
        tags=["Portable speaker","Waterproof"],
        summary="NBC Select's pocket-size speaker pick is waterproof and dustproof, plays for up to about 7 hours per charge and has a built-in loop for clipping to a bag; it was listed around $40.",
        pros=["Waterproof and dustproof","Built-in loop for bags","Small enough for a stocking"],
        cons=["About 7 hours of battery","Small speaker, modest bass"]),
   dict(name="LANEIGE Lip Sleeping Mask", badge="Best beauty stocking stuffer", price="$", f=["under50","selfcare"],
        tags=["Overnight lip mask","About $24"],
        summary="Good Morning America's November 2026 stocking stuffer guide includes this overnight lip mask at $24 — a cult-favorite treat that leaves lips soft by morning.",
        pros=["Popular, recognizable beauty gift","Under $25","One jar lasts a long time"],
        cons=["Small jar for the price"]),
   dict(name="Body Restore Shower Steamers (6-Pack)", badge="Best value", price="$", f=["under50","selfcare"],
        tags=["Aromatherapy","6 steamers"],
        summary="Forbes Vetted's best-value stocking stuffer: six essential-oil tablets that release scent in a hot shower, with variety packs including eucalyptus and lavender. TODAY also lists a six-pack at about $17.",
        pros=["Spa-like treat for under $20","Six individually wrapped steamers","Several scent packs to choose from"],
        cons=["Single-use — each tablet gets used up"]),
   dict(name="Fly By Jing Original Sichuan Chili Crisp", badge="Best food stocking stuffer", price="$", f=["under50"],
        tags=["6 oz jar","Vegan"],
        summary="Forbes Vetted's top food stocking stuffer and an NBC Select pick: a 6 oz jar of chili crisp with crunchy garlic and shallots and numbing Sichuan pepper heat, vegan and sugar-free, for about $10.",
        pros=["About $10","Vegan and sugar-free","Great for anyone who cooks or loves spicy food"],
        cons=["Too spicy for some — a mild version exists"]),
   dict(name="Loop Quiet 2 Earplugs", badge="Best for light sleepers", price="$", f=["under50","useful","travel","selfcare"],
        tags=["Reusable earplugs","Travel case"],
        summary="Reusable soft-silicone earplugs from NBC Select's adult stocking stuffer list, made for sleep and noisy flights. They come with several tip sizes and a travel case, and were listed around $21.",
        pros=["Reusable, soft silicone","Several tip sizes for a good fit","Travel case included"],
        cons=["Some people find any earplug uncomfortable for side sleeping"]),
   dict(name="Bombas Marl Calf Socks (4-Pack)", badge="Most practical", price="$$", f=["useful"],
        tags=["Cotton socks","Arch support"],
        summary="Forbes Vetted's most practical stocking stuffer: a four-pack of extra-long-staple cotton calf socks with honeycomb arch support.",
        pros=["Comfortable, everyday upgrade","Honeycomb arch support","Four pairs in one gift"],
        cons=["Pricier than regular socks","Check men's or women's sizing"]),
   dict(name="Theragun Mini Plus", badge="Best splurge", price="$$$", f=["selfcare"],
        tags=["Heated massage gun","Travel size"],
        summary="Forbes Vetted's luxury stocking stuffer: a compact massage gun with a heated attachment. Therabody lists it at $279.99 with up to 120 minutes of battery and a travel pouch.",
        pros=["Heat plus percussive massage","Small enough to travel","Up to 120 minutes per charge"],
        cons=["About $280 — a big stocking stuffer","Cold attachment costs extra"]),
  ],
  "tips": [
   ("Aim for useful things they'll use every week","The stocking stuffers editors repeat most solve small daily problems: a tracker for keys (AirTag), a charger that replaces a cable and wall block (Anker Nano 3-in-1), or good socks."),
   ("Check their phone before buying tech","The AirTag (2nd Generation) needs an iPhone or iPad on iOS 26 or later, and its Precision Finding needs an iPhone 15 or newer. For a USB-C power bank, make sure their phone charges over USB-C."),
   ("Think small enough to fit","A standard stocking holds items about the size of a speaker like the JBL Go 4 or a 6 oz jar of chili crisp; save bigger gifts like the Theragun Mini Plus for under the tree or the top of the stocking."),
   ("Mix one 'real' gift with consumables","A good stocking for an adult pairs one gadget (an AirFly SE for a frequent flyer) with things that get used up, like shower steamers, a lip mask or a hot sauce — so nothing feels like clutter."),
   ("Budget about $10–$50 per item","Most picks here cost under $50, from about $10 for Fly By Jing chili crisp to about $40 for the AirFly SE or JBL Go 4."),
  ],
  "faq": [
   ("What are good stocking stuffers for adults?","Good stocking stuffers for adults are small, useful gifts: an Apple AirTag (2nd Generation) for keys and bags, a Twelve South AirFly SE for flights, a 3-in-1 power bank, a JBL Go 4 speaker, plus treats like Fly By Jing chili crisp, a LANEIGE lip mask or aromatherapy shower steamers."),
   ("What is the most popular stocking stuffer?","The Apple AirTag is one of the most recommended: Forbes Vetted names it the best stocking stuffer overall, and NBC Select and Good Morning America also include it. The 2026 model costs $29 and has a louder speaker and longer finding range."),
   ("What are good stocking stuffers for men?","Practical gear works well for men: the AirTag for keys, an Anker Nano 3-in-1 power bank, a JBL Go 4 speaker, Bombas socks or a jar of Fly By Jing chili crisp."),
   ("What are good stocking stuffers for women?","Self-care treats are favorites for women, like the LANEIGE Lip Sleeping Mask (about $24), Body Restore shower steamers (six for under $20) and Loop Quiet 2 earplugs; the Theragun Mini Plus is the splurge."),
   ("How much should you spend on stocking stuffers?","Most adult stocking stuffers cost about $10–$50 each. In this guide, eight of the 10 picks are under $50, from about $10 (Fly By Jing chili crisp) to about $40 (AirFly SE and JBL Go 4)."),
   ("What are useful stocking stuffers for travelers?","The Twelve South AirFly SE lets wireless headphones work with in-flight entertainment (up to 20 hours of battery), and an AirTag in a checked bag helps track luggage. Loop Quiet 2 earplugs and a 10,000mAh power bank round out a travel stocking."),
  ],
  "sources": [
   ("Forbes Vetted — The best stocking stuffers (updated September 2026)","https://www.forbes.com/sites/forbes-personal-shopper/article/best-stocking-stuffer/"),
   ("Good Morning America — Best stocking stuffers (November 2026)","https://goodmorningamerica.com/shop/story/best-stocking-stuffers-126903766"),
   ("NBC Select — The best stocking stuffers for adults","https://www.nbcnews.com/select/shopping/adult-stocking-stuffer-ideas-rcna239348"),
   ("Engadget — The best stocking stuffer ideas for $50 or less","https://www.engadget.com/best-gifts-under-50-holiday-stocking-stuffers-130049028.html"),
   ("TODAY — Best stocking stuffers","https://www.today.com/shop/best-stocking-stuffers-rcna125737"),
   ("Engadget — Apple AirTag (2026) review","https://engadget.com/computing/accessories/apple-airtag-2026-review-143000427.html"),
   ("Therabody — Theragun Mini Plus","https://therabody.com/products/theragun-mini-plus-massage-gun"),
  ],
 },
]

SOON = []

PRICE_NOTE = {"$":"Under ~$300","$$":"About $300–$1,500","$$$":"About $1,000–$2,500","$$$$":"$2,500+"}

e = html.escape

LISTS = [c for c in CATS if c.get("kind") != "gift"]
GIFTS = [c for c in CATS if c.get("kind") == "gift"]
for c in GIFTS:
    if c.get("no_price_filters"): continue
    c["filters"] = [("under50","Under $50"),("under150","Under $150"),("splurge","Splurge")] + c["filters"]
    for p in c["products"]:
        extra = {"$":["under50","under150"],"$$":["under150"],"$$$":[],"$$$$":["splurge"]}[p["price"]]
        p["f"] = p["f"] + [x for x in extra if x not in p["f"]]

RANK = {}   # product name -> (list cat, rank) for product lists
for c in LISTS:
    for n, p in enumerate(c["products"], 1):
        RANK.setdefault(p["name"], (c, n))
LIST_RANKS = {}   # product name -> [(list cat, rank)] for products on more than one list
for c in LISTS:
    for n, p in enumerate(c["products"], 1):
        LIST_RANKS.setdefault(p["name"], []).append((c, n))
IN_GIFTS = {}   # product name -> [gift cats]
for c in GIFTS:
    for p in c["products"]:
        IN_GIFTS.setdefault(p["name"], []).append(c)

RELATED = {
 "best-tvs": ["best-soundbars","best-projectors","best-wireless-earbuds"],
 "best-projectors": ["best-tvs","best-soundbars","best-wireless-earbuds"],
 "best-electric-shavers": ["best-hair-dryers","best-wireless-earbuds","best-luggage"],
 "best-espresso-machines": ["gifts-for-coffee-lovers","best-coffee-makers","best-air-fryers"],
 "best-wireless-earbuds": ["best-over-ear-headphones","best-smartwatches","best-tvs"],
 "best-air-fryers": ["best-cookware-sets","best-blenders","best-coffee-makers"],
 "best-robot-vacuums": ["best-cordless-vacuums","best-air-purifiers","best-humidifiers"],
 "best-standing-desks": ["best-office-chairs","best-gaming-chairs","gifts-for-gamers"],
 "best-mattresses": ["best-air-purifiers","best-humidifiers","best-space-heaters"],
 "best-hair-dryers": ["best-electric-shavers","best-luggage","best-mattresses"],
 "best-office-chairs": ["best-standing-desks","best-gaming-chairs","gifts-for-gamers"],
 "best-luggage": ["best-wireless-earbuds","best-over-ear-headphones","stocking-stuffers-for-adults"],
 "best-cookware-sets": ["best-knife-sets","best-stand-mixers","best-air-fryers"],
 "best-space-heaters": ["best-humidifiers","best-mattresses","best-robot-vacuums"],
 "best-humidifiers": ["best-air-purifiers","best-space-heaters","best-cordless-vacuums"],
 "best-coffee-makers": ["best-espresso-machines","best-blenders","gifts-for-coffee-lovers"],
 "best-blenders": ["best-stand-mixers","best-air-fryers","best-coffee-makers"],
 "best-stand-mixers": ["best-blenders","best-cookware-sets","best-knife-sets"],
 "best-knife-sets": ["best-cookware-sets","best-stand-mixers","best-air-fryers"],
 "best-cordless-vacuums": ["best-robot-vacuums","best-humidifiers","best-space-heaters"],
 "best-over-ear-headphones": ["best-wireless-earbuds","best-smartwatches","best-soundbars"],
 "best-smartwatches": ["best-wireless-earbuds","best-over-ear-headphones","gifts-for-him"],
 "best-soundbars": ["best-tvs","best-projectors","best-over-ear-headphones"],
 "best-gaming-chairs": ["best-office-chairs","gifts-for-gamers","best-standing-desks"],
 "best-air-purifiers": ["best-humidifiers","best-cordless-vacuums","best-robot-vacuums"],
 "gifts-for-him": ["gifts-for-dad","best-smartwatches","best-over-ear-headphones"],
 "gifts-for-her": ["gifts-for-mom","stocking-stuffers-for-adults","best-hair-dryers"],
 "gifts-for-dad": ["gifts-for-him","gifts-for-coffee-lovers","best-espresso-machines"],
 "gifts-for-mom": ["gifts-for-her","best-stand-mixers","best-knife-sets"],
 "gifts-under-50": ["stocking-stuffers-for-adults","gifts-for-him","gifts-for-her"],
 "gifts-for-coffee-lovers": ["best-espresso-machines","best-coffee-makers","gifts-under-50"],
 "gifts-for-gamers": ["best-gaming-chairs","gifts-for-him","gifts-under-50"],
 "stocking-stuffers-for-adults": ["gifts-under-50","gifts-for-her","best-wireless-earbuds"],
}
BY_SLUG = {c["slug"]: c for c in CATS}

def label(c):
    return c["short"] if c.get("kind") == "gift" else "Best " + c["short"]

def notes(cat):
    return cat.get("price_notes", PRICE_NOTE)

# ---------------------------------------------------------------- layout
def nav(active=""):
    is_list = active.startswith("best-")
    is_gift = active.startswith("gifts-") or active[:-5] in {c["slug"] for c in GIFTS}
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
 "best-mattresses":"mattress","best-hair-dryers":"hair dryer","best-office-chairs":"office chair","best-luggage":"carry-on","best-cookware-sets":"cookware set","best-space-heaters":"space heater","best-humidifiers":"humidifier","best-coffee-makers":"coffee maker","best-blenders":"blender","best-stand-mixers":"stand mixer","best-knife-sets":"knife set","best-cordless-vacuums":"cordless vacuum","best-over-ear-headphones":"over-ear headphones","best-smartwatches":"smartwatch","best-soundbars":"soundbar","best-gaming-chairs":"gaming chair","best-air-purifiers":"air purifier"}
PLURAL = {"best-wireless-earbuds","best-over-ear-headphones"}
WHO = {"stocking-stuffers-for-adults":"adults","gifts-under-50":"anyone on your list","gifts-for-gamers":"gamers","gifts-for-coffee-lovers":"coffee lovers","gifts-for-him":"him","gifts-for-her":"her","gifts-for-dad":"dad","gifts-for-mom":"mom"}
QA_LEAD = {"gifts-under-50":"Our top gift ideas under $50","stocking-stuffers-for-adults":"Our top stocking stuffers for adults"}
QOVERRIDE = {
 ("best-air-purifiers","Best design"):"What's the best-looking air purifier?",
 ("best-air-purifiers","Best quiet"):"What's the quietest air purifier?",
 ("best-gaming-chairs","Best under $250"):"What's the best cheap gaming chair under $250?",
 ("best-gaming-chairs","Best splurge"):"What's the best high-end gaming chair?",
 ("best-gaming-chairs","Best mesh"):"What's the best mesh gaming chair?",
 ("best-gaming-chairs","Best for big and tall"):"What's the best gaming chair for big and tall people?",
 ("best-soundbars","Best surround sound package"):"What's the best soundbar with a subwoofer and rear speakers?",
 ("best-soundbars","Best without a subwoofer"):"What's the best soundbar without a subwoofer?",
 ("best-soundbars","Best small soundbar"):"What's the best small soundbar?",
 ("best-soundbars","Best mid-range"):"What's the best mid-range soundbar?",
 ("best-smartwatches","Best affordable Apple Watch"):"What's the best affordable Apple Watch?",
 ("best-smartwatches","Best battery life"):"Which smartwatch has the longest battery life?",
 ("best-smartwatches","Best hybrid"):"What's the best hybrid smartwatch that looks like a regular watch?",
 ("best-over-ear-headphones","Best noise cancelling"):"What are the best noise-cancelling over-ear headphones?",
 ("best-over-ear-headphones","Best sound quality"):"Which over-ear headphones have the best sound quality?",
 ("best-over-ear-headphones","Best battery life"):"Which over-ear headphones have the longest battery life?",
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
 ("best-space-heaters","Best tower for large rooms"):"What's the best tower space heater for large rooms?",
 ("best-space-heaters","Best oil-filled radiator"):"What's the best oil-filled radiator heater?",
 ("best-space-heaters","Best safety features"):"What's the safest space heater?",
 ("best-space-heaters","Best ceramic tower"):"What's the best ceramic tower heater?",
 ("best-space-heaters","Best for bathrooms"):"What's the best space heater for a bathroom?",
 ("best-space-heaters","Best for basements"):"What's the best space heater for a basement?",
 ("best-space-heaters","Best fan and heater combo"):"What's the best fan and space heater combo?",
 ("best-space-heaters","Best with an air purifier"):"What's the best space heater with an air purifier?",
 ("best-humidifiers","Best smart humidifier"):"What's the best smart humidifier?",
 ("best-humidifiers","Best tabletop humidifier"):"What's the best tabletop humidifier?",
 ("best-humidifiers","Best easy-to-clean"):"What's the easiest humidifier to clean?",
 ("best-humidifiers","Best quiet"):"What's the quietest humidifier?",
 ("best-humidifiers","Best budget whole-home"):"What's the best budget whole-house humidifier?",
 ("best-humidifiers","Best anti-mold design"):"What's the best humidifier for preventing mold?",
 ("best-coffee-makers","Best thermal carafe"):"What's the best coffee maker with a thermal carafe?",
 ("best-coffee-makers","Best customizable"):"What's the most customizable coffee maker?",
 ("best-coffee-makers","Best smart coffee maker"):"What's the best smart coffee maker?",
 ("best-coffee-makers","Best pod and carafe combo"):"What's the best coffee maker for K-Cups and a full pot?",
 ("best-coffee-makers","Best with grinder"):"What's the best coffee maker with a grinder?",
 ("best-blenders","Best Vitamix alternative"):"What's the best Vitamix alternative blender?",
 ("best-blenders","Best for everyday cooking"):"What's the best blender for everyday cooking?",
 ("best-blenders","Best quiet blender"):"What's the best quiet blender?",
 ("best-blenders","Best splurge"):"What's the best high-end blender?",
 ("best-blenders","Best blender and food processor combo"):"What's the best blender and food processor combo?",
 ("best-blenders","Best with a glass jar"):"What's the best blender with a glass jar?",
 ("best-stand-mixers","Best KitchenAid alternative"):"What's the best alternative to a KitchenAid stand mixer?",
 ("best-stand-mixers","Best entry-level KitchenAid"):"What's the best cheaper KitchenAid stand mixer?",
 ("best-stand-mixers","Best value"):"What's the best value stand mixer?",
 ("best-cookware-sets","Best starter set"):"What's the best cookware set for a first apartment?",
 ("best-cordless-vacuums","Best self-emptying"):"What's the best self-emptying cordless vacuum?",
 ("best-cordless-vacuums","Best vacuum and mop"):"What's the best cordless vacuum and mop combo?",
 ("best-cordless-vacuums","Best splurge"):"What's the best high-end cordless vacuum?",
 ("best-knife-sets","Best with a magnetic stand"):"What's the best knife set with a magnetic stand?",
 ("best-knife-sets","Best for large hands"):"What's the best knife set for large hands?",
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
        if cat["slug"] in QA_LEAD:
            cheap = None
            text = f"{QA_LEAD[cat['slug']]} in 2026 are the {ps[0]['name']}, the {ps[1]['name']} and the {ps[2]['name']}."
        else:
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
    if cat.get("kind") != "gift":
        for lc, n in LIST_RANKS.get(p["name"], []):
            if lc is not cat:
                bits.append(f'Also ranked #{n} in our <a href="{lc["slug"]}.html#{lc["slug"]}-{n}">{e(label(lc))}</a> list')
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
