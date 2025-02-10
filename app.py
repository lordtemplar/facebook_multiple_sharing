import streamlit as st
import requests
import time
import random
import json

# Load Secrets (Page Access Tokens)
FB_ACCESS_TOKENS = json.loads(st.secrets["FB_ACCESS_TOKENS"])  # { "page_id1": "token1", "page_id2": "token2", ... }

# Function to share a post link to multiple pages
def share_post_to_pages(post_link):
    shared_results = []
    
    for page_id, access_token in FB_ACCESS_TOKENS.items():
        try:
            api_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
            payload = {
                "link": post_link,
                "access_token": access_token
            }
            response = requests.post(api_url, data=payload)
            result = response.json()

            if "id" in result:
                shared_results.append((page_id, "✅ Success", result["id"]))
            else:
                shared_results.append((page_id, "❌ Failed", result.get("error", {}).get("message", "Unknown error")))

            # Random delay (10-30 sec)
            time.sleep(random.randint(10, 30))

        except Exception as e:
            shared_results.append((page_id, "❌ Failed", str(e)))

    return shared_results

# Streamlit UI
st.title("📢 Facebook Post Link Sharer")

post_link = st.text_input("📌 Enter Facebook Post Link:")

if st.button("Share to Pages"):
    if not post_link or "facebook.com" not in post_link:
        st.error("⚠️ Please enter a valid Facebook post link.")
    else:
        st.info("Sharing post link to all pages... Please wait.")
        results = share_post_to_pages(post_link)

        # Display results
        st.write("## 📌 Sharing Results")
        for page_id, status, detail in results:
            st.write(f"🔹 Page {page_id}: {status} ({detail})")
