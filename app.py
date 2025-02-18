import streamlit as st
import requests
import json
import time
import random

# Load Facebook Page Access Tokens from Streamlit Secrets
FB_ACCESS_TOKENS = {}
try:
    if "FB_ACCESS_TOKENS" in st.secrets:
        FB_ACCESS_TOKENS = json.loads(st.secrets["FB_ACCESS_TOKENS"])
        st.write("🔍 Facebook Access Tokens Loaded Successfully!")
    else:
        st.error("❌ `FB_ACCESS_TOKENS` is missing in Streamlit Secrets! Check your settings.")
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

            if "id" in result:
                shared_results.append((page_id, "✅ Success", result["id"]))
            else:
                shared_results.append((page_id, "❌ Failed", result.get("error", {}).get("message", "Unknown error")))

            # Random delay (10-30 sec) to avoid Facebook rate limits
            time.sleep(random.randint(10, 30))

        except Exception as e:
            shared_results.append((page_id, "❌ Failed", str(e)))

    return shared_results

# Streamlit UI
st.title("📢 Facebook Post Link Sharer")
st.write("Enter a Facebook post link and share it to multiple fan pages.")

# Single input field for the post URL
post_link = st.text_input("📌 Facebook Post URL:")

# Single button to trigger sharing
if st.button("Share to All Pages"):
    if not post_link or "facebook.com" not in post_link:
        st.error("⚠️ Invalid Facebook post URL.")
    else:
        st.info("Sharing... Please wait.")
        results = share_post_to_pages(post_link)
        
        # Display results
        st.write("## 📌 Sharing Results")
        for page_id, status, detail in results:
            st.write(f"🔹 Page {page_id}: {status} ({detail})")
