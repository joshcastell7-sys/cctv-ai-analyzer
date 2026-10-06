# CCTV AI Log Analyzer 📷🤖

## Overview
An intelligent Python script that bridges traditional physical security hardware (DVRs/NVRs like Dahua, Hikvision, Honeywell) with Generative AI (Google Gemini). 

Traditional security systems generate raw, technical logs that are difficult to monitor at scale. This tool parses those raw events and converts them into actionable, executive-level security summaries with automated risk classification.

## Key Features
* **AI-Powered Analysis:** Leverages the Gemini REST API to interpret complex security events (e.g., line crossing, unauthorized motion detection).
* **Automated Risk Triage:** Instantly classifies physical security incidents into Low, Medium, or High risk based on context.
* **Enterprise Security Standards:** Implements strict credential management using environment variables (`.env`) to prevent API key leaks.
* **Hardware Agnostic:** Can process string-based logs from any major CCTV or intrusion alarm vendor.

## Setup & Installation

1. **Install dependencies:**
   Ensure you have Python installed, then run:
   ```bash
   pip install requests python-dotenv
   