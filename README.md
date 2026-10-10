# 🛡️ CASFER Sentry: AI-Powered CCTV Alert Analyzer

An asynchronous, AI-driven backend automation system designed to monitor, filter, and analyze CCTV email alerts in real-time. 

CASFER Sentry ingests unstructured email alerts from security cameras (Dahua, Hikvision, Imou), filters out commercial SPAM, and leverages **Google Gemini LLM** to generate structured, actionable security intelligence in strict JSON format. 

## 🚀 Engineering Highlights & Architecture

This project was built focusing on enterprise-grade reliability, data validation, and concurrent processing:

* **Asynchronous Batch Processing:** Implemented `asyncio` and Semaphores to process multiple CCTV alerts concurrently, achieving a **3.43x performance speedup** compared to sequential processing (reducing execution time from 283s to 82s for large batches).
* **Network Resilience & Retry Logic:** Integrated `tenacity` for exponential backoff. The system silently handles API rate limits (`429`), network timeouts (`10060`), and server errors without crashing.
* **Strict Schema Validation:** Utilized `pydantic` to enforce strict data contracts on the LLM output. Hallucinated or malformed data is automatically rejected before it can pollute the system.
* **Secure Integrations:** Implemented OAuth2 for secure Gmail API ingestion and SMTP for automated dispatch of consolidated executive reports.

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Core Libraries:** `asyncio`, `tenacity`, `pydantic`
* **AI & APIs:** `google-generativeai` (Gemini 1.5 Flash), Google Workspace API (Gmail OAuth2)

## ⚙️ System Workflow (Sentry Mode)

1. **Ingestion:** Polls the connected Gmail inbox via Google API for unread messages tagged as alerts.
2. **Concurrent Analysis:** Dispatches the unread alerts to the Gemini LLM engine using an `asyncio.Semaphore` (max 3 concurrent calls to respect API limits).
3. **Data Structuring:** The LLM evaluates the text, discards SPAM, and extracts the event type, severity, location, and timestamp into a strict Pydantic JSON schema.
4. **Dispatch:** Consolidates the validated JSON reports and sends a clean, executive summary to the client's email via SMTP.
5. **Sleep Cycle:** Enters a resource-efficient 60-second sleep cycle before the next polling iteration.

## 📊 Performance Benchmark

| Execution Mode | Time (Seconds) | Status |
| :--- | :--- | :--- |
| Sequential Processing | 283.07s | Baseline |
| **Concurrent Processing** | **82.61s** | **Optimized** |
| **Speedup Factor** | **3.43x** | 🚀 |

## 💻 Local Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your credentials:
   ```env
   GEMINI_API_KEY=your_google_ai_key
   EMAIL_USER=your_sender_email
   EMAIL_PASS=your_app_password
   