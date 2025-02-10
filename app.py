import streamlit as st
import requests
import json

# Load Secrets (Access Token from Streamlit Secrets)
FB_ACCESS_TOKEN = st.secrets["FB_ACCESS_TOKEN"]  # A single user access token with "pages_read_engagement"
BASE_GRAPH_API = "https://graph.facebook.com/v19.0"

def get_latest_post_link(page_id_or_username):
    """Fetch the latest post link from a Facebook Page"""
    try:
        api_url = f"{BASE_GRAPH_API}/{page_id_or_username}/posts?fields=id,permalink_url&limit=1&access_token={FB_ACCESS_TOKEN}"
        response = requests.get(api_url)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            latest_post = data["data"][0]
            return latest_post["permalink_url"]
        else:
            return "⚠️ No posts found or insufficient permissions."

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit UI
st.title("🔍 Fetch Latest Facebook Post Link")

page_id = st.text_input("📌 Enter Facebook Page ID or Username:")

if st.button("Get Latest Post Link"):
    if not page_id:
        st.error("⚠️ Please enter a Facebook Page ID or username.")
    else:
        st.info("Fetching the latest post link...")
        post_link = get_latest_post_link(page_id)
        st.success(f"📌 Latest Post Link: [Click here]({post_link})" if "http" in post_link else post_link)
