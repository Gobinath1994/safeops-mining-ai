
# SafeOps-Mining-AI – Intelligent Safety Violation Monitoring System

## 🔍 Overview
SafeOps AI is a modular AI-powered safety monitoring system built for mining and construction sites. It combines real-time computer vision (YOLOv8), rule-based notifications, and LLM-based reasoning to detect, analyze, and respond to safety violations such as missing helmets, proximity to heavy machinery, or trip hazards.

## 🧠 Key Features
- YOLOv8-based CV detection for helmet compliance, PPE, posture, and hazards.
- LLM integration (Mistral 7B via LM Studio) for contextual escalation, policy suggestions, and action plans.
- Email alerts & logging system for real-time notifications to supervisors.
- Streamlit dashboard for visualizing detections, LLM logs, and plans.

---

## 📁 Project Structure
```
safeops_ai/
├── agents/
│   ├── llm_agent.py           # LLM calls (reasoning, action plans, policies)
│   └── notify_agent.py        # Notification rules and email alerts
├── data/
│   ├── dummy_frames/         # Sample input images
│   └── dummy_detections.json # Generated detection outputs
├── utils/
│   └── logger.py             # Logs actions and violations
├── vision/
│   ├── dummy_detector.py     # Simulates violations randomly
│   └── yolo_detector.py      # Real CV detection using YOLOv8 + OpenCV
├── yolov8n.pt                # YOLOv8 nano model weights
├── pipeline.py               # Main orchestration pipeline
├── streamlit_app.py          # Streamlit dashboard app
├── README.md                 # You're here
├── requirements.txt          # Python dependencies
├── *.txt                     # LLM outputs: logs, plans, and recommendations
```

---

## 🧪 Sample Workflow

### 1. Simulate or Run Detection
Run either the dummy simulator or real YOLOv8 detector:
```bash
# (A) Simulated detections
python vision/dummy_detector.py

# (B) Real object detection (YOLOv8 + OpenCV)
./safeops_ai_env/bin/python vision/yolo_detector.py
```

### 2. Run Inference Pipeline
This reads detection outputs, triggers LLMs, alerts, and logs actions:
```bash
./safeops_ai_env/bin/python pipeline.py
```

### 3. Launch Dashboard
```bash
./safeops_ai_env/bin/streamlit run streamlit_app.py
```
Access it at: http://localhost:8501

---

## 📦 Technologies Used
- Computer Vision: YOLOv8 (Ultralytics), OpenCV
- LLM: Mistral 7B (via LM Studio)
- Visualization: Streamlit
- Notifications: Yagmail (Gmail SMTP alerts)
- Python Environment: Conda virtualenv in `safeops_ai_env`

---

## 📌 Detected Violation Types
- `no_helmet`
- `too_close_to_excavator`
- `fatigue_posture`
- `trip_hazard`
- `no_safety_vest`
- `obstructed_exit`
- `unsafe_manual_handling`

Each triggers tailored responses, emails, and logs.

---

## 📬 Alerts & Escalation
The pipeline logs all actions in `logs.txt`, emails critical alerts to supervisors, and saves:
- Reasoning → `llm_logs.txt`
- Action Plans → `action_plan.txt`
- Policy Suggestions → `policy_recommendations.txt`

---

## 🧠 Example Output
```json
[Frame frame_005]
{
  "escalate": true,
  "notify_roles": ["Safety Officer", "Supervisor"],
  "shutdown_required": true,
  "summary": "Two workers are not wearing helmets near blast zone during day shift"
}
```

---

## 🛠️ Setup Guide
```bash
# Create conda environment
conda create -n safeops_ai_env python=3.10
conda activate safeops_ai_env
pip install -r requirements.txt
```

Ensure `yolov8n.pt` is in root. Update LLM endpoint in `llm_agent.py` if needed.

---

## 📧 Email Setup (Gmail)
- Use an app password (not your real Gmail password).
- Update credentials in `notify_agent.py`:
```python
yag = yagmail.SMTP("your@gmail.com", "your-app-password")
```

---

## 📍 Notes
- YOLOv8 Nano used for quick inference (<150ms avg/frame)
- OpenCV used for image processing, resizing, loading.
- Designed for local PoC use – can be dockerized or deployed on edge.

---

## ✨ Future Enhancements
- Integrate live CCTV stream feeds
- Add more object classes (gloves, goggles, signage)
- Replace dummy logic fully with real YOLOv8 + fine-tuned safety model
- Build user authentication and historical trend dashboard

---

## 🧑‍💼 Author
**Gobinath Sindhuja**  
*Last updated: June 27, 2025*
