"""
ThreatScan - Local AI Backend
Bridges the HTML frontend to Ollama running on your machine.
Run this with: python server.py
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import json
import os

PORT = 8080
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

SYSTEM_PROMPT = """You are a cybersecurity expert specializing in detecting scams, phishing, and social engineering attacks. Analyze the given message and respond ONLY with a JSON object. No markdown, no explanation, no backticks. Just raw JSON.

Return this exact structure:
{
  "risk_level": "SAFE" or "LOW" or "MEDIUM" or "HIGH" or "CRITICAL",
  "risk_score": a number from 0 to 100,
  "summary": "One sentence verdict",
  "threats": ["phishing","malware","social_engineering","financial_fraud","impersonation","urgency_tactic","suspicious_link","safe"],
  "red_flags": ["specific red flag 1", "specific red flag 2"],
  "explanation": "2-3 sentence detailed explanation of why this is or is not dangerous",
  "advice": "What the person should do"
}

Only include relevant threat types in the threats array. If the message is safe, just use ["safe"]. Respond with ONLY the JSON object, nothing else."""


class ThreatScanHandler(SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == "/analyze":
            self._handle_analyze()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        # Serve index.html for root path
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
        return SimpleHTTPRequestHandler.do_GET(self)

    def _handle_analyze(self):
        try:
            # Read request body
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            message = data.get("message", "")

            if not message:
                self._send_json({"error": "No message provided"}, 400)
                return

            # Call Ollama
            prompt = f"{SYSTEM_PROMPT}\n\nAnalyze this message:\n\n{message}"
            ollama_payload = json.dumps({
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }).encode()

            req = urllib.request.Request(
                OLLAMA_URL,
                data=ollama_payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=60) as resp:
                ollama_data = json.loads(resp.read())
                raw_text = ollama_data.get("response", "")

            # Clean and parse the JSON response
            cleaned = raw_text.strip()
            # Strip markdown fences if model adds them anyway
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            cleaned = cleaned.strip()

            result = json.loads(cleaned)
            self._send_json(result)

        except urllib.error.URLError:
            self._send_json({
                "error": "Cannot connect to Ollama. Make sure it is running (run: ollama serve)"
            }, 503)
        except json.JSONDecodeError as e:
            self._send_json({
                "error": f"Could not parse AI response: {str(e)}"
            }, 500)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self._set_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def log_message(self, format, *args):
        # Clean up console output
        status = args[1] if len(args) > 1 else "?"
        path = args[0].split('"')[1] if '"' in args[0] else args[0]
        print(f"  [{status}] {path}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    server = HTTPServer(("localhost", PORT), ThreatScanHandler)
    print("=" * 45)
    print("  🛡  ThreatScan Server")
    print("=" * 45)
    print(f"  Running at:  http://localhost:{PORT}")
    print(f"  AI Model:    {MODEL}")
    print(f"  Press Ctrl+C to stop")
    print("=" * 45)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")
