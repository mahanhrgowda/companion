# companion
Mystic Companion Finder — A playful Streamlit companion app
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
