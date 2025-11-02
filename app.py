"""
Mystic Companion Finder — A playful Streamlit companion app (single-file)
- Minimal external libraries: streamlit, math, datetime, random, io, base64
- From-scratch, simplified astrological calculations for Sun/Moon longitudes and basic house placement (approximate)
- Features:
  - Spirit-animal / guardian matching using occult synastry heuristics + phonetic "vibration matching"
  - Bioregional folklore influence from latitude/longitude
  - Gallery of placeholder illustrations (simple Streamlit sketches + emojis)
  - Interactive chat simulation seeded by birth details; option to export chat logs
  - Harmony meter driven by moon illumination and phase
- Defaults as requested: Name, Birth Date, Birth Time, Latitude, Longitude
- Date inputs constrained to years 1900-2100
- Birth Time input step = 60 seconds
How to run:
1. Save this file as `mystic_companion_finder.py`
2. Install Streamlit: `pip install streamlit`
3. Run: `streamlit run mystic_companion_finder.py`
DISCLAIMER: Astronomical/astrological formulas are simplified and intended for playful companion use only, not professional charting.
"""
import streamlit as st
from datetime import date, datetime, time
import math
import random
import io
import base64
# ----------------------- Constants & Utilities -----------------------
ZODIAC = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
SPIRIT_POOL = {
    'fire': ["Phoenix 🔥", "Dragon 🔥", "Salamander 🔥"],
    'earth': ["Wolf 🐺", "Stag 🦌", "Tortoise 🐢"],
    'air': ["Raven 🪶", "Hawk 🦅", "Sphinx 🦁🪶"],
    'water': ["Otter 🦦", "Koi 🐟", "Selkie 🧜‍♀️"]
}
PHRASE_POOLS = {
    "fiery": [
        "Rise and blaze — start that streak you've been thinking of. 🔥",
        "Spark, don't scorch: channel your heat into clean action. 🔥",
        "A bold first step wins more than a perfect plan. 🚀",
        "Ignite your passion and let it guide you through the day. 🌟",
        "Embrace the fire within; it's your greatest ally. 🛡️"
    ],
    "airy": [
        "Playful curiosity will find you better doors today. 🌬️",
        "Breeze through clutter — ideas thrive in open spaces. 💨",
        "Share one story; you'll find the thread you need. 🧵",
        "Let your thoughts soar like the wind. 🕊️",
        "Connect the dots with a light-hearted approach. 🔗"
    ],
    "earthy": [
        "Small steady work adds up — plant one seed today. 🌱",
        "Organize a single corner of your life and watch momentum grow. 🪴",
        "Trust the slow, quiet progress underfoot. 🪨",
        "Ground yourself in nature's rhythm. 🌳",
        "Build foundations that last a lifetime. 🏰"
    ],
    "watery": [
        "Feel before you speak; your subtlety is your strength. 🌊",
        "Let intuition polish the edges of a choice tonight. 🌕",
        "A humane touch heals where logic cannot. 🤲",
        "Flow with the currents of emotion. 🌀",
        "Dive deep into your inner wisdom. 🐚"
    ]
}
# Expanded persona variations for spirits
PERSONA_VARIATIONS = {
    "Phoenix 🔥": {"persona": "Wise and reborn, offering guidance on transformation.", "style": "fiery"},
    "Dragon 🔥": {"persona": "Fierce protector, sharing secrets of power.", "style": "fiery"},
    "Salamander 🔥": {"persona": "Playful fire spirit, igniting creativity.", "style": "fiery"},
    "Wolf 🐺": {"persona": "Loyal pack leader, teaching unity and instinct.", "style": "earthy"},
    "Stag 🦌": {"persona": "Graceful wanderer, guiding through forests of life.", "style": "earthy"},
    "Tortoise 🐢": {"persona": "Patient sage, emphasizing endurance.", "style": "earthy"},
    "Raven 🪶": {"persona": "Mysterious messenger, revealing hidden truths.", "style": "airy"},
    "Hawk 🦅": {"persona": "Sharp visionary, helping focus on goals.", "style": "airy"},
    "Sphinx 🦁🪶": {"persona": "Enigmatic riddle-master, sparking intellect.", "style": "airy"},
    "Otter 🦦": {"persona": "Joyful swimmer, promoting play and adaptability.", "style": "watery"},
    "Koi 🐟": {"persona": "Resilient fish, symbolizing perseverance.", "style": "watery"},
    "Selkie 🧜‍♀️": {"persona": "Shape-shifting seal, exploring emotions.", "style": "watery"}
}
# Simple SVG placeholders
SVG_PLACEHOLDERS = {
    "Phoenix 🔥": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <path d="M50 10 L70 40 L90 30 L70 60 L80 90 L50 70 L20 90 L30 60 L10 30 L30 40 Z" fill="orange" stroke="red"/>
        <circle cx="50" cy="20" r="5" fill="yellow"/>
    </svg>
    """,
    "Dragon 🔥": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <path d="M20 50 Q40 20 60 50 Q80 80 100 50" fill="none" stroke="green" stroke-width="5"/>
        <polygon points="100,50 90,40 90,60" fill="green"/>
        <circle cx="20" cy="50" r="10" fill="red"/>
        <line x1="20" y1="40" x2="20" y2="30" stroke="black" stroke-width="2"/>
    </svg>
    """,
    "Salamander 🔥": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <rect x="20" y="40" width="60" height="20" rx="10" fill="orange"/>
        <circle cx="20" cy="50" r="10" fill="orange"/>
        <line x1="10" y1="50" x2="0" y2="50" stroke="orange" stroke-width="5"/>
        <line x1="80" y1="50" x2="100" y2="50" stroke="orange" stroke-width="5"/>
    </svg>
    """,
    "Wolf 🐺": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <polygon points="50,20 30,40 20,60 30,80 50,100 70,80 80,60 70,40" fill="gray"/>
        <circle cx="40" cy="30" r="3" fill="black"/>
        <circle cx="60" cy="30" r="3" fill="black"/>
    </svg>
    """,
    "Stag 🦌": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <rect x="40" y="40" width="20" height="40" fill="brown"/>
        <circle cx="50" cy="30" r="10" fill="brown"/>
        <path d="M40 20 L30 0 L20 10 M60 20 L70 0 L80 10" fill="none" stroke="brown" stroke-width="5"/>
    </svg>
    """,
    "Tortoise 🐢": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <ellipse cx="50" cy="50" rx="40" ry="30" fill="green"/>
        <circle cx="20" cy="50" r="10" fill="green"/>
        <rect x="10" y="40" width="20" height="20" fill="green"/>
    </svg>
    """,
    "Raven 🪶": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <polygon points="50,20 20,50 50,80 80,50" fill="black"/>
        <circle cx="50" cy="30" r="5" fill="white"/>
    </svg>
    """,
    "Hawk 🦅": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <path d="M20 50 L50 20 L80 50" fill="brown"/>
        <path d="M10 60 L50 80 L90 60" fill="brown"/>
        <circle cx="50" cy="40" r="5" fill="yellow"/>
    </svg>
    """,
    "Sphinx 🦁🪶": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <rect x="20" y="50" width="60" height="30" fill="gold"/>
        <circle cx="20" cy="40" r="10" fill="gold"/>
        <path d="M10 30 L0 10 L5 20 M30 30 L40 10 L35 20" fill="none" stroke="gold" stroke-width="3"/>
    </svg>
    """,
    "Otter 🦦": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <ellipse cx="50" cy="50" rx="30" ry="15" fill="brown"/>
        <circle cx="80" cy="50" r="10" fill="brown"/>
        <line x1="80" y1="60" x2="100" y2="70" stroke="brown" stroke-width="5"/>
    </svg>
    """,
    "Koi 🐟": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <path d="M20 50 Q50 30 80 50 Q50 70 20 50" fill="orange"/>
        <circle cx="80" cy="50" r="5" fill="black"/>
    </svg>
    """,
    "Selkie 🧜‍♀️": """
    <svg width="100" height="100" viewBox="0 0 100 100">
        <circle cx="50" cy="30" r="10" fill="blue"/>
        <path d="M40 40 L50 100 L60 40" fill="blue"/>
        <line x1="30" y1="50" x2="10" y2="60" stroke="blue" stroke-width="3"/>
        <line x1="70" y1="50" x2="90" y2="60" stroke="blue" stroke-width="3"/>
    </svg>
    """
}
# ----------------------- Astronomical helpers (simplified) -----------------------
def to_julian_day(dt: datetime) -> float:
    year = dt.year
    month = dt.month
    day = dt.day + (dt.hour + (dt.minute + dt.second / 60.0) / 60.0) / 24.0
    if month <= 2:
        year -= 1
        month += 12
    A = year // 100
    B = 2 - A + (A // 4)
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    return jd
def sun_ecliptic_longitude(jd: float) -> float:
    d = jd - 2451545.0
    L = (280.460 + 0.9856474 * d) % 360
    g = (357.528 + 0.9856003 * d) % 360
    lambda_sun = L + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g))
    return lambda_sun % 360
def moon_ecliptic_longitude(jd: float) -> float:
    d = jd - 2451545.0
    Lm = (218.316 + 13.176396 * d) % 360
    Mm = (134.963 + 13.064993 * d) % 360
    D = (297.850 + 12.190749 * d) % 360
    lon = Lm + 6.289 * math.sin(math.radians(Mm))
    lon += 1.274 * math.sin(math.radians(2 * D - Mm))
    lon += 0.658 * math.sin(math.radians(2 * D))
    lon += 0.213 * math.sin(math.radians(2 * Mm))
    return lon % 360
def moon_phase_illumination(jd: float) -> float:
    ls = sun_ecliptic_longitude(jd)
    lm = moon_ecliptic_longitude(jd)
    phase_angle = (lm - ls) % 360
    illum = (1 - math.cos(math.radians(phase_angle))) * 50.0
    return round(illum, 1)
# Improved sidereal time calculation for ascendant
def gmst(jd: float) -> float:
    d = jd - 2451545.0
    gmst = (280.46061837 + 360.98564736629 * d) % 360
    return gmst
def local_sidereal_time(jd: float, longitude: float) -> float:
    return (gmst(jd) + longitude) % 360
def obliquity_of_ecliptic(jd: float) -> float:
    t = (jd - 2451545.0) / 36525.0
    eps = 23 + (26 + (21.448 - t * (46.815 + t * (0.00059 - t * 0.001813))) / 60) / 60
    return eps
def approximate_ascendant_longitude(jd: float, latitude: float, longitude: float) -> float:
    lst_deg = local_sidereal_time(jd, longitude)
    lst = math.radians(lst_deg)
    lat_rad = math.radians(latitude)
    eps = math.radians(obliquity_of_ecliptic(jd))
    tan_asc = -math.cos(lst) / (math.sin(lst) * math.sin(eps) + math.tan(lat_rad) * math.cos(eps))
    asc = math.degrees(math.atan(tan_asc)) % 360
    # Adjust quadrant
    if math.cos(lst) > 0:
        asc += 180
    elif math.sin(lst) < 0:
        asc += 360
    return asc % 360
# ----------------------- Zodiac & house (very simplified) -----------------------
def zodiac_from_longitude(lon_deg: float) -> str:
    idx = int(lon_deg // 30) % 12
    return ZODIAC[idx]
def house_from_longitude(planet_lon: float, asc_lon: float) -> int:
    # Divide 360 into 12 houses starting from ascendant
    diff = (planet_lon - asc_lon) % 360
    house = int(diff // 30) + 1
    return house
# ----------------------- Matching logic -----------------------
def tone_seed_from_birth(birth_date: date) -> str:
    s = (birth_date.day + birth_date.month) % 4
    return ["fiery", "airy", "earthy", "watery"][s]
def phonetic_vibration(name: str) -> str:
    # Simple phonetic vibration: count vowels -> map to angelic/animal realms
    vowels = sum(1 for ch in name.lower() if ch in 'aeiou')
    return ['angelic', 'animal', 'spirit', 'elemental'][vowels % 4]
def bioregional_tone(latitude: float) -> str:
    # Near equator -> more tropical / water/fire suggestions
    lat_abs = abs(latitude)
    if lat_abs < 15:
        return 'tropical'
    elif lat_abs < 45:
        return 'temperate'
    else:
        return 'boreal'
def match_spirits(sun_sign: str, moon_sign: str, tone: str, vib: str, bio: str, rng: random.Random):
    # Combine signals to pick 2-3 companions
    element_map = {
        'Aries':'fire','Taurus':'earth','Gemini':'air','Cancer':'water','Leo':'fire','Virgo':'earth',
        'Libra':'air','Scorpio':'water','Sagittarius':'fire','Capricorn':'earth','Aquarius':'air','Pisces':'water'
    }
    picks = []
    primary_el = element_map.get(sun_sign, 'earth')
    secondary_el = element_map.get(moon_sign, 'water')
    # pick primary spirit
    sp = rng.choice(SPIRIT_POOL[primary_el])
    picks.append({'role':'Primary Familiar', 'spirit':sp, 'reason':f'Born under {sun_sign} ({primary_el})'})
    # pick secondary
    sp2 = rng.choice(SPIRIT_POOL[secondary_el])
    picks.append({'role':'Guardian', 'spirit':sp2, 'reason':f'Moon in {moon_sign} ({secondary_el})'})
    # add vibration-based pick
    vib_pick = rng.choice(sum(SPIRIT_POOL.values(), []))
    picks.append({'role':'Whisperer', 'spirit':vib_pick, 'reason':f'Phonetic vibe: {vib}, bioregion: {bio}'})
    return picks
# ----------------------- Chat generation & export -----------------------
def generate_alispar_response(name: str, sun_sign: str, moon_sign: str, tone: str, spirit: str, rng: random.Random) -> str:
    title = "Your Mystic Companion"
    greeting = f"{title} 🧚: Hello {name.split()[0]}!"
    persona = PERSONA_VARIATIONS.get(spirit, {"persona": "Mystic guide", "style": tone})
    phrase = rng.choice(PHRASE_POOLS[persona["style"]])
    flavor = f"With Sun in {sun_sign} and Moon in {moon_sign}, {phrase} As your {persona['persona']}, I say..."
    return greeting + " " + flavor
def make_chat_download(chat_log: list) -> tuple:
    txt = "\n".join(chat_log)
    b = txt.encode('utf-8')
    b64 = base64.b64encode(b).decode()
    href = f"data:file/txt;base64,{b64}"
    return href, txt
# ----------------------- Streamlit App -----------------------
def app():
    # Custom CSS for themed colors and animations, with dark mode support
    st.markdown("""
    <style>
    .stApp {
        /* Use Streamlit's default background */
    }
    .block-container {
        padding: 1rem;
        border-radius: 10px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    :root[data-theme="light"] .stButton > button {
        background-color: #4CAF50;
        color: white;
    }
    :root[data-theme="dark"] .stButton > button {
        background-color: #2E7D32;
        color: white;
    }
    :root[data-theme="dark"] .stButton > button:hover {
        background-color: #1B5E20;
        transform: scale(1.05);
    }
    .expander-header {
        color: #333;
        font-weight: bold;
    }
    :root[data-theme="dark"] .expander-header {
        color: #ccc;
        font-weight: bold;
    }
    .harmony-meter {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    /* Element-specific colors */
    :root[data-theme="light"] [data-element="fiery"] {
        background-color: #ffcccb;
        border: 1px solid #ff0000;
        color: #000000;
    }
    :root[data-theme="dark"] [data-element="fiery"] {
        background-color: #5c0a0a;
        border: 1px solid #ff0000;
        color: #ffffff;
    }
    :root[data-theme="light"] [data-element="airy"] {
        background-color: #e0ffff;
        border: 1px solid #00bfff;
        color: #000000;
    }
    :root[data-theme="dark"] [data-element="airy"] {
        background-color: #0a5c5c;
        border: 1px solid #00bfff;
        color: #ffffff;
    }
    :root[data-theme="light"] [data-element="earthy"] {
        background-color: #f5f5dc;
        border: 1px solid #8b4513;
        color: #000000;
    }
    :root[data-theme="dark"] [data-element="earthy"] {
        background-color: #5c5c3d;
        border: 1px solid #8b4513;
        color: #ffffff;
    }
    :root[data-theme="light"] [data-element="watery"] {
        background-color: #add8e6;
        border: 1px solid #0000ff;
        color: #000000;
    }
    :root[data-theme="dark"] [data-element="watery"] {
        background-color: #0a3d5c;
        border: 1px solid #0000ff;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.set_page_config(page_title="Mystic Companion Finder 🧭✨", layout="wide")
    st.title("Mystic Companion Finder — Find your spirit companion! 🧚‍♀️🦄🔥")
    st.markdown("A playful app that **matches** you with a spirit animal, guardian angel, or mythical familiar using simplified occult synastry, phonetic vibration matching, and bioregional folklore. 🌍✨")
    with st.sidebar:
        st.header("Birth & Location (defaults)")
        name = st.text_input("Name", value="Mahan H R Gowda")
        birth_date = st.date_input("Birth Date", value=date(1993,7,12), min_value=date(1900,1,1), max_value=date(2100,12,31))
        default_time = time(12,26)
        birth_time = st.time_input("Birth Time (HH:MM)", value=default_time, step=60)
        lat = st.number_input("Latitude (° N)", value=13.32, format="%.6f")
        lon = st.number_input("Longitude (° E)", value=75.77, format="%.6f")
        st.markdown("---")
        st.header("Target Date")
        target_date = st.date_input("Target Date", value=date(2025,11,1), min_value=date(1900,1,1), max_value=date(2100,12,31))
        if st.button("Match me! 🔮"):
            st.session_state['matched'] = True
            st.session_state['picks'] = None  # Reset picks
    # compute positions
    birth_dt = datetime.combine(birth_date, birth_time)
    jd = to_julian_day(birth_dt)
    sun_lon = sun_ecliptic_longitude(jd)
    moon_lon = moon_ecliptic_longitude(jd)
    moon_illum = moon_phase_illumination(jd)
    sun_sign = zodiac_from_longitude(sun_lon)
    moon_sign = zodiac_from_longitude(moon_lon)
    asc_lon = approximate_ascendant_longitude(jd, lat, lon)
    # seed RNG deterministically
    seed_val = birth_date.day + birth_date.month + birth_date.year + birth_time.hour + birth_time.minute
    rng = random.Random(seed_val)
    tone = tone_seed_from_birth(birth_date)
    vib = phonetic_vibration(name)
    bio = bioregional_tone(lat)
    # layout
    col1, col2 = st.columns([2,3])
    with col1:
        st.subheader("Astrological Snapshot ✨")
        st.write(f"**Sun (approx):** {sun_lon:.2f}° → **{sun_sign}**")
        st.write(f"**Moon (approx):** {moon_lon:.2f}° → **{moon_sign}**")
        st.write(f"**Ascendant (approx):** {asc_lon:.2f}° → **{zodiac_from_longitude(asc_lon)} (1st house cusp)**")
        st.write(f"**Moon illumination:** {moon_illum}% 🌙")
        st.write(f"**Phonetic vibration:** {vib} — vowels-based mapping 🎶")
        st.write(f"**Bioregion:** {bio} — latitude: {lat}° 🌎")
        st.markdown("---")
        st.subheader("Harmony Meter — Moon Sync 🌕")
        harmony_value = int(round(moon_illum))
        st.progress(harmony_value / 100.0, text=f"Harmony: {harmony_value}%")
        waxing = 'Waxing' if 0 < ((moon_lon - sun_lon) % 360) < 180 else 'Waning'
        st.caption(f"{waxing} phase. Your spirit's energy: {tone} tone.")
        st.markdown("---")
        st.subheader("Matching Logic 🧭")
        st.write("We combine Sun element, Moon element, phonetic vibration, and bioregional flavor to propose companions. This is playful and symbolic — enjoy! ✨")
        if st.button("Generate Match Now 🐾"):
            st.session_state['matched'] = True
            st.session_state['picks'] = match_spirits(sun_sign, moon_sign, tone, vib, bio, rng)
    with col2:
        st.subheader("Gallery of Matched Companions 🎨🖼️")
        if st.session_state.get('matched', False):
            picks = st.session_state.get('picks') or match_spirits(sun_sign, moon_sign, tone, vib, bio, rng)
            for i, p in enumerate(picks):
                element = PERSONA_VARIATIONS.get(p['spirit'], {"style": "fiery"})["style"]
                with st.expander(f"{p['role']}: {p['spirit']}"):
                    st.markdown(f'<div data-element="{element}">', unsafe_allow_html=True)
                    st.write(f"**Role:** {p['role']} — **Spirit:** {p['spirit']}")
                    st.write(f"**Reason:** {p['reason']}")
                    # SVG illustration
                    svg = SVG_PLACEHOLDERS.get(p['spirit'], "<svg width='100' height='100'></svg>")
                    st.markdown(svg, unsafe_allow_html=True)
                    st.write("A stylized portrait for your imagination. 🥰")
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Generate a match to populate the gallery! Click 'Generate Match Now' or 'Match me!' in the sidebar. ✨")
    st.markdown("---")
    st.subheader("Interactive Chat Simulation 💬")
    if 'chat_log' not in st.session_state:
        st.session_state['chat_log'] = []
    user_msg = st.text_input("You to your companion:", value="Hello, who are you?", key='chat_input')
    if st.button("Send Message ✉️"):
        if not st.session_state.get('matched', False):
            st.warning("Please generate a match first so your companion is ready to reply! 🌟")
        else:
            # user's message
            st.session_state['chat_log'].append(f"You: {user_msg}")
            # Select a random spirit for response
            picks = st.session_state.get('picks') or match_spirits(sun_sign, moon_sign, tone, vib, bio, rng)
            spirit = rng.choice([p['spirit'] for p in picks])
            # advance RNG deterministically
            rng.random(); rng.random()
            reply = generate_alispar_response(name, sun_sign, moon_sign, tone, spirit, rng)
            st.session_state['chat_log'].append(f"{spirit}: {reply}")
    # show chat log
    st.write("**Chat Log**")
    for line in st.session_state['chat_log']:
        if line.startswith('You:'):
            st.markdown(f"**{line}**")
        else:
            st.markdown(f":sparkles: {line}")
    # export chat
    if st.session_state['chat_log']:
        href, txt = make_chat_download(st.session_state['chat_log'])
        st.markdown(f"[Download chat log as TXT 📥]({href})")
    st.markdown("---")
    st.subheader("Extra Options & UI Play 🎭")
    st.write("- Use emojis throughout to set tone. ✨\n- Placeholder images are SVG-based for a lightweight app. 🎨\n- For prettier graphics we can add external images later. 🖼️")
    st.markdown("---")
    st.caption("Built with ❤️ for playful exploration. Not a substitute for professional astrology. 🌟")
if __name__ == '__main__':
    app()