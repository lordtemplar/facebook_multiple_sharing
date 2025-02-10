import streamlit as st
import requests
import time
import random
import json

# Debug: Check if secrets are loaded
st.write("✅ Streamlit app started...")

# Try to load Facebook Access Tokens safely
FB_ACCESS_TOKENS = {}
try:
    if "FB_ACCESS_TOKENS" in st.secrets:
        FB_ACCESS_TOKENS = json.loads(st.secrets["FB_ACCESS_TOKENS"])
        st.write("🔍 Loaded Facebook Access Tokens successfully!")
    else:
        st.error("❌ `FB_ACCESS_TOKENS` is missing in Streamlit Secrets! Please check your settings.")
        st.stop()
except Exception as e:
    st.error(f"❌ Error loading secrets: {str(e)}")
    st.stop()

# Function to share a post link to multiple pages
def share_post_to_pages(post_link):
    shared_results = []
    for page_id, access_token in FB_ACCESS_TOKENS.items():
        try:
            api_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
            payload = {"link": post_link, "access_token": access_token}
            response = requests.post(api_url, data=payload)
            result = response.json()
            shared_results.append((page_id, "✅ Success", result.get("id", "No ID")))
            time.sleep(random.randint(10, 30))
        except Exception as e:
            shared_results.append((page_id, "❌ Failed", str(e)))
    return shared_results

# Streamlit UI
st.title("📢 Facebook Post Link Sharer")
post_link = st.text_input("📌 Facebook Post URL:")

if st.button("Share to All Pages"):
    if not post_link or "facebook.com" not in post_link:
        st.error("⚠️ Invalid Facebook post URL.")
    else:
        st.info("Sharing... Please wait.")
        results = share_post_to_pages(post_link)
        for page_id, status, detail in results:
            st.write(f"🔹 Page {page_id}: {status} ({detail})")
