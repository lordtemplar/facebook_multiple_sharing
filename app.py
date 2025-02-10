import streamlit as st
import requests
import time
import random
import json
import os

# โหลด Secrets (Access Token & Page IDs) จาก Streamlit Cloud
FB_ACCESS_TOKENS = json.loads(st.secrets["FB_ACCESS_TOKENS"])  # { "page_id1": "token1", "page_id2": "token2", ... }

# ฟังก์ชันสำหรับแชร์โพสต์ไปยังเพจ
def share_post_to_pages(post_url):
    shared_results = []
    
    for page_id, access_token in FB_ACCESS_TOKENS.items():
        try:
            api_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
            payload = {
                "link": post_url,
                "access_token": access_token
            }
            response = requests.post(api_url, data=payload)
            result = response.json()

            if "id" in result:
                shared_results.append((page_id, "✅ แชร์สำเร็จ", result["id"]))
            else:
                shared_results.append((page_id, "❌ แชร์ไม่สำเร็จ", result.get("error", {}).get("message", "Unknown error")))

            # หน่วงเวลาสุ่ม 10-30 วินาที
            time.sleep(random.randint(10, 30))

        except Exception as e:
            shared_results.append((page_id, "❌ แชร์ไม่สำเร็จ", str(e)))

    return shared_results

# UI หลักของ Streamlit
st.title("📢 Multiple Facebook Post Sharing")

post_url = st.text_input("📌 ใส่ลิงก์โพสต์ Facebook ที่ต้องการแชร์")

if st.button("แชร์ไปยังทุกเพจ"):
    if not post_url:
        st.error("กรุณาใส่ลิงก์โพสต์ก่อนแชร์")
    else:
        st.info("กำลังแชร์โพสต์ไปยังเพจทั้งหมด... กรุณารอ")
        results = share_post_to_pages(post_url)

        # แสดงผลลัพธ์
        st.write("## 📌 ผลการแชร์โพสต์")
        for page_id, status, detail in results:
            st.write(f"🔹 เพจ {page_id}: {status} ({detail})")
