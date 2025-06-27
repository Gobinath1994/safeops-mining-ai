import streamlit as st
import os
import json
import pandas as pd
import re

st.set_page_config(page_title="SafeOps AI Dashboard", layout="wide")

st.title("📊 SafeOps AI – Dashboard")

# ---------------- Frame Images ----------------
st.subheader("🖼️ Annotated Frame Preview (YOLOv8 + OpenCV)")

# ✅ NEW: Use annotated_frames instead of dummy_frames
image_dir = "data/annotated_frames"
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith((".png", ".jpg"))])

cols = st.columns(4)
for idx, img in enumerate(image_files):
    with cols[idx % 4]:
        st.image(os.path.join(image_dir, img), caption=img, use_container_width=True)

# ---------------- Frame Violation Summary ----------------
st.subheader("📌 Frame Violation Summary")

# ✅ Map back to original frame IDs (remove file extensions)
frame_ids = [f.replace(".png", "").replace(".jpg", "") for f in image_files]
frame_violations = {}

try:
    with open("data/dummy_detections.json") as f:
        data = json.load(f)
        for entry in data:
            fid = entry.get("frame_id")
            det_types = [d.get("type") for d in entry.get("detections", [])]
            frame_violations[fid] = ", ".join(det_types) if det_types else "Safe"
except Exception as e:
    st.error(f"Failed to load detection data: {e}")

summary_data = []
for fid in frame_ids:
    status = frame_violations.get(fid, "Safe")
    summary_data.append({"Frame": fid, "Violations": status})

df_summary = pd.DataFrame(summary_data)
st.dataframe(df_summary, use_container_width=True)

# ---------------- LLM Reasoning Summary ----------------
st.subheader("🧠 LLM Reasoning Summary")

try:
    with open("llm_logs.txt") as f:
        logs = f.read().strip().split("\n\n")

    if not logs:
        st.info("No reasoning logs yet.")
    else:
        displayed_frames = set()
        for block in logs:
            lines = block.strip().split("\n")
            if not lines:
                continue

            frame_line = lines[0].strip()
            if frame_line in displayed_frames:
                continue
            displayed_frames.add(frame_line)

            json_text = "\n".join(lines[1:]).strip()
            json_text = re.sub(r"```json|```", "", json_text).strip()

            try:
                parsed = json.loads(json_text)
                st.markdown(f"**{frame_line}**")
                st.markdown(f"""
- 🔁 **Escalate:** `{parsed.get("escalate", False)}`
- 📧 **Notify:** `{', '.join(parsed.get("notify_roles", []))}`
- ⛔ **Shutdown Required:** `{parsed.get("shutdown_required", False)}`
- 📝 **Summary:** {parsed.get("summary", 'N/A')}
""")
                st.markdown("---")
            except json.JSONDecodeError:
                continue
except FileNotFoundError:
    st.warning("llm_logs.txt not found.")

# ---------------- Action Plan ----------------
st.subheader("🛠️ LLM Action Plan Suggestions")
try:
    with open("action_plan.txt") as f:
        content = f.read().strip()
        seen = set()
        for section in content.split("[Frame"):
            section = section.strip()
            if not section:
                continue
            if section in seen:
                continue
            seen.add(section)
            st.markdown(f"[Frame {section}")
            st.markdown("---")
except FileNotFoundError:
    st.info("action_plan.txt not found.")

# ---------------- Policy Recommendations ----------------
st.subheader("📋 Policy Recommendations")
try:
    with open("policy_recommendations.txt") as f:
        content = f.read().strip()
        seen = set()
        for section in content.split("[Frame"):
            section = section.strip()
            if not section:
                continue
            if section in seen:
                continue
            seen.add(section)
            st.markdown(f"[Frame {section}")
            st.markdown("---")
except FileNotFoundError:
    st.info("policy_recommendations.txt not found.")