#  ThreatScan — Message Vulnerability Detector

A browser-based tool that uses AI to analyze messages for scams, phishing attacks, and social engineering threats. Paste any suspicious SMS, email, or WhatsApp message and get an instant threat assessment.

---

##  Installation Instructions

No installs or packages required. Just two steps:

**1. Download the project**
- Download or clone this repository to your computer
- You will have a single file: `index.html`

**2. Open in VS Code with Live Server**
- Open VS Code
- Install the **Live Server** extension (by Ritwick Dey) from the Extensions tab
- Right-click `index.html` → click **Open with Live Server**
- The site opens at `http://127.0.0.1:5500/index.html`

**3. Add your API key**
- Sign up at [console.anthropic.com](https://console.anthropic.com) 
- Create an API key and copy it
- Open `index.html` and find this line:
  ```js
  const API_KEY = "YOUR_ANTHROPIC_API_KEY_HERE";
  ```
- Replace the placeholder with your actual key and save

---

##  Usage

1. Open the site in your browser via Live Server
2. Paste any suspicious message into the text box
3. Click **ANALYZE THREAT**
4. The tool returns:
   - A **risk score** from 0–100
   - A **risk level**: SAFE / LOW / MEDIUM / HIGH / CRITICAL
   - **Threat type badges** (Phishing, Malware, Financial Fraud, etc.)
   - **Red flags** found in the message
   - A plain-English **explanation**
   - A **recommended action** (e.g. delete, report, safe to open)

You can also click the example buttons — **Bank Phishing**, **Prize Scam**, **Legit Email**, **WhatsApp Malware** — to test the tool instantly without typing anything.

---

## Examples 

**Example 1 — Bank Phishing (HIGH RISK)**
```
URGENT: Your Barclays account has been suspended. Click here to verify 
your details: http://barclays-secure-verify.ru/login or your account 
will be permanently closed within 24 hours.
```
> Result: CRITICAL — Phishing + Urgency Tactic + Suspicious Link detected

**Example 2 — Legitimate Message (SAFE)**
```
Hi, your Amazon order #204-1234567 has been shipped and will arrive 
by Thursday. Track it at amazon.co.uk/orders. No action needed.
```
> Result: SAFE — No threats detected

**Example 3 — Prize Scam (HIGH RISK)**
```
Congratulations! You've won £5,000. Send £50 processing fee via bank 
transfer to sort code 20-45-67, account 12345678 to claim your prize.
```
> Result: HIGH — Financial Fraud + Social Engineering detected

---

## License

This project is open for personal and educational use. You are free to:
- Use it for yourself or your studies
- Modify the code however you like
- Share it with others

Please do not use it commercially or deploy it publicly with your API key exposed, as this could result in unauthorized usage charges.

---

## Contributors / Contact

**Built by:** Hasan Fahmee
**Project type:** University coursework / Personal project  
**Tech stack:** HTML, CSS, JavaScript, Bootstrap 5, Anthropic Claude API  

For questions or feedback, feel free to reach out or open an issue in the repository.
