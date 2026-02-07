import streamlit as st
import spacy
import pandas as pd
from geopy.geocoders import Nominatim
import time
import re

st.set_page_config(page_title="Chennai Dispatch Center", layout="wide")

@st.cache_resource
def load_nlp():
    try:
        return spacy.load("chennai_gazetteer_model")
    except:
        st.error("Model 'chennai_gazetteer_model' not found. Please run your training script first.")
        return None

nlp = load_nlp()
geolocator = Nominatim(user_agent="chennai_dispatch_web", timeout=10)

def analyze_text(text):
    text = text.lower()
    category = "GENERAL"
    is_emergency = False
    severity = 1
    victim_count = 0

   
    categories = {
        "ACCIDENT": ["accident", "crash", "collision", "hit", "flipped", "ambulance"],
        "FIRE": ["fire", "smoke", "burning", "explosion", "blast", "short circuit"],
        "MEDICAL": ["heart attack", "unconscious", "breathing", "bleeding", "sick", "injury"],
        "CRIME": ["robbery", "theft", "fight", "assault", "gun", "knife"],
        "DELIVERY": ["delivery", "package", "courier", "order", "parcel"],
        "MEETING": ["meeting", "interview", "discussion", "appointment"],
    }

    for cat, keywords in categories.items():
        if any(kw in text for kw in keywords):
            category = cat
            is_emergency = cat in ["ACCIDENT", "FIRE", "MEDICAL", "CRIME"]
            break

    
    num_match = re.search(r'(\d+)', text)
    word_nums = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    if num_match:
        victim_count = int(num_match.group(1))
    else:
        for word, val in word_nums.items():
            if f" {word} " in f" {text} ": victim_count = val

    
    if is_emergency:
        severity = 3
        if victim_count > 0: severity += 1
        if any(kw in text for kw in ["child", "kid", "children"]): severity += 1
    return category, min(5, severity), victim_count

st.title("🚨 Chennai Emergency Dispatch System")
st.markdown("Automated text-to-dispatch analysis for Chennai city.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Message")
    input_text = st.text_area("Paste the incoming message here:", 
                              placeholder="e.g., Accident of two children in OMR near the church",
                              height=150)
    process_btn = st.button("Analyze & Dispatch")

if process_btn and input_text:
    
    doc = nlp(input_text)
    street = next((ent.text for ent in doc.ents if ent.label_ == "STREET"), None)
    locality = next((ent.text for ent in doc.ents if ent.label_ == "LOCALITY"), None)
    
    
    cat, sev, victims = analyze_text(input_text)
    
    query = f"{street or ''} {locality or ''}, Chennai, India".strip()
    location = geolocator.geocode(query)
    
    with col2:
        st.subheader("Analysis Results")
        
    
        p_color = "inverse" if sev >= 4 else "normal"
        st.metric("Priority Level", f"{'HIGH' if sev >= 4 else 'MEDIUM' if sev >=3 else 'LOW'}", delta=f"Severity {sev}/5", delta_color=p_color)

    
        c1, c2, c3 = st.columns(3)
        c1.write(f"**Type**\n\n{cat}")
        c2.write(f"**Victims**\n\n{victims}")
        c3.write(f"**Location**\n\n{street or 'N/A'}")

        
        if location:
            df_map = pd.DataFrame({'lat': [location.latitude], 'lon': [location.longitude]})
            st.map(df_map)
            st.success(f"Pinned to: {location.address}")
            st.write(f"[Open in Google Maps](https://www.google.com/maps?q={location.latitude},{location.longitude})")
        else:
            st.warning("Could not pinpoint exact GPS coordinates. Fallback to Chennai center.")

st.sidebar.info("This system uses a custom Chennai Street Gazetteer (42k+ records) and a Rule-based Emergency Classifier.")
   