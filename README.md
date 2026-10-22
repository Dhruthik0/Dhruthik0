<p align="center">
  <img src="assets/banner.svg" width="100%" alt="Dhruthik — self-hosted systems that connect Android phones, browsers and backends">
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/dhruthik-s-gowda-4643aa225"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:dhruthik2004@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://github.com/Dhruthik0?tab=repositories"><img src="https://img.shields.io/badge/Repositories-181717?style=for-the-badge&logo=github&logoColor=white" alt="Repositories"></a>
  <!-- TODO: add a portfolio link here once you have one -->
</p>

I build the plumbing: Android phones that work as SMS and call gateways, browser tools that plug into apps people already use, and the backends that hold it all together. Most of my projects are full systems, with a mobile client, an API, a dashboard and deployment.

## ⚡ What I work on

- 📡 **Telephony and messaging.** Routing real cellular calls and SMS through Android handsets, with Asterisk, SIP and WebSockets in between.
- 🧩 **Browser automation and extensions.** Manifest V3 extensions and Playwright/CDP tooling that work with existing web apps.
- 🧠 **Applied ML and AI.** URL-based phishing detection with classical and deep models, and speech-to-text, LLM and text-to-speech pipelines in production-style backends.
- 🔭 **Current focus:** extending [Telora](https://github.com/Dhruthik0/Telora) and prototyping [HistoWay](https://github.com/Dhruthik0/HistoWay), a travel companion that narrates the history of places as you pass them.

## 🛠️ Tech stack

**Languages**<br>
<img src="https://skillicons.dev/icons?i=java,py,js,ts,kotlin" height="40" alt="Java, Python, JavaScript, TypeScript, Kotlin">

**Mobile**<br>
<img src="https://skillicons.dev/icons?i=react,androidstudio" height="40" alt="React Native, Android Studio"><br>
<sub>React Native · native Android (Kotlin, Java)</sub>

**Backend**<br>
<img src="https://skillicons.dev/icons?i=nodejs,nestjs,express,fastapi" height="40" alt="Node.js, NestJS, Express, FastAPI">

**Frontend**<br>
<img src="https://skillicons.dev/icons?i=react,vite,tailwind" height="40" alt="React, Vite, Tailwind CSS">

**E-commerce**<br>
<img src="https://img.shields.io/badge/Shopify-7AB55C?style=for-the-badge&logo=shopify&logoColor=white" alt="Shopify">

**Data**<br>
<img src="https://skillicons.dev/icons?i=postgres,redis,mongodb,sqlite,prisma" height="40" alt="PostgreSQL, Redis, MongoDB, SQLite, Prisma">

**Tooling**<br>
<img src="https://skillicons.dev/icons?i=docker,vitest,jest" height="40" alt="Docker, Vitest, Jest"><br>
<sub>Also: Playwright, Asterisk (ARI / PJSIP), Turborepo, pnpm</sub>

**AI / ML**<br>
<img src="https://skillicons.dev/icons?i=pytorch,sklearn,tensorflow" height="40" alt="PyTorch, scikit-learn, TensorFlow"><br>
<sub>Also: Gemini, Deepgram, Google Cloud Text-to-Speech, sentence-transformers</sub>

## 🚀 Featured builds

<table>
<tr>
<td width="50%" valign="top">

### 📞 [Telora](https://github.com/Dhruthik0/Telora)
**Cellular calls and SMS through your own Android phones, run from one backend and one dashboard.**

- SMS over an authenticated device WebSocket with delivery acks. Inbound messages are buffered and replayed if the link drops.
- Voice over SIP through Asterisk ARI, and the handset places the real cellular call.
- Speech-to-text → LLM → text-to-speech pipeline for automated calls. API keys are stored only as SHA-256 hashes.

<sub>TypeScript · NestJS · React + Vite · Kotlin · Asterisk · PostgreSQL + Prisma · Redis + BullMQ · Docker · Turborepo</sub>

</td>
<td width="50%" valign="top">

### 🎣 [Phishing URL Detector](https://github.com/Dhruthik0/Website-Authentication-extension-)
**Two models, one verdict on whether a URL is phishing.**

- A Random Forest on engineered URL features plus a character-level CNN on the raw URL. The API averages both.
- A FastAPI `/predict` service ([phish-detector](https://github.com/Dhruthik0/phish-detector)) serves the models.
- A Manifest V3 extension checks the active tab, and a Streamlit UI is included for demos.

<sub>Python · scikit-learn · PyTorch · FastAPI · Streamlit · Chrome extension (MV3)</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🖼️ [Varoza](https://github.com/Dhruthik0/varoza)
**A poster marketplace with buyer, seller and admin sides.** · [Live site](https://varoza.vercel.app)

- Buyers browse, add to cart and check out. Sellers upload posters, track earnings and request withdrawals.
- Admins approve sellers, posters and payments, and manage margins, coupons and shipping.
- JWT auth with role-based route guards. Images are stored in Cloudinary.

<sub>React · Vite · Tailwind CSS · Node.js + Express · MongoDB · Cloudinary · Vercel</sub>

</td>
<td width="50%" valign="top">

### 🤖 [AI Bridge](https://github.com/Dhruthik0/ChatGPT-Gateway)
**Pipe prompts from your scripts and shell to your own ChatGPT web session.**

- Attaches to a real Chrome profile over CDP, and each request runs in a fresh temporary chat.
- Loopback-only, with a constant-time bearer token check, DNS-rebinding defense, request size caps and no prompt logging by default.
- Sync, async, poll and cancel job API, with unit, live and end-to-end tests.

<sub>Python · FastAPI · Playwright · pytest · systemd</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 💰 [FinLedger](https://github.com/Dhruthik0/FinLedger)
**Borrowers, loans, monthly interest and collections for a small lending business.**

- Generates monthly interest due dates and applies each payment to the oldest pending interest first (FIFO), so the user only enters an amount.
- Dashboard for due-today, overdue and next-7-days items, plus a due-date calendar, browser notifications and Excel export.
- One Docker Compose command runs PostgreSQL, the API and the Nginx-served frontend.

<sub>React · Vite · Tailwind CSS · Node.js + Express · Prisma · PostgreSQL · Docker</sub>

</td>
<td width="50%" valign="top">

### 📨 [sms-freebie](https://github.com/Dhruthik0/sms-freebie)
**A self-hosted SMS gateway on paired Android phones instead of a paid SMS API. It is the predecessor of Telora's SMS side.**

- An Android foreground service dispatches across multiple SIMs, stores messages in Room during network drops and restarts on boot.
- An Express server on SQLite (WAL mode) with JWT and API-key auth, a WebSocket device pool and live SSE dashboard updates.
- Ships with Docker and an end-to-end integration test script.

<sub>Kotlin · Node.js + Express · SQLite · WebSocket · SSE · Docker</sub>

</td>
</tr>
</table>

## 🧪 More experiments

- 🔗 [Chat-trace](https://github.com/Dhruthik0/Chat-trace): a Chrome extension that records which ChatGPT answer prompted each follow-up question, so you can jump back to it (WXT, React, TypeScript).
- 🔑 [OTP AutoFill Assistant](https://github.com/Dhruthik0/Helpyy-ext): a Manifest V3 extension that reads one-time codes from Outlook or Gmail and fills them into login forms (TypeScript, Vite).
- 📄 [resume-screen-agent](https://github.com/Dhruthik0/resume-screen-agent): ranks resumes against a job description with semantic search (Streamlit, sentence-transformers, FAISS).
- 🙂 [emotion-detection](https://github.com/Dhruthik0/emotion-detection): webcam emotion detection served over FastAPI (DeepFace, TensorFlow).

## 📊 GitHub activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=Dhruthik0&layout=compact&langs_count=6&hide_border=true&theme=github_dark">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Dhruthik0&layout=compact&langs_count=6&hide_border=true" alt="Most-used languages across Dhruthik0's public repositories">
</picture>

<sub>If the card doesn't load, browse the <a href="https://github.com/Dhruthik0?tab=repositories">repositories</a> directly.</sub>

## 📫 Get in touch

The easiest way to reach me is [LinkedIn](https://www.linkedin.com/in/dhruthik-s-gowda-4643aa225) or [email](mailto:dhruthik2004@gmail.com).
