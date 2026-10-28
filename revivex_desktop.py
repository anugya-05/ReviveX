import json
import threading
import urllib.request
import urllib.error
import customtkinter as ctk
from tkinter import messagebox

# REVIVEX desktop interface for the existing Flask API.
# Start your Flask backend first (default: http://127.0.0.1:5000).

API_BASE = "http://127.0.0.1:5000"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def api_request(path, method="GET", payload=None, timeout=20):
    url = API_BASE + path
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else {}


class RevivexApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("REVIVEX AI | Hardware Repair Assistant")
        self.geometry("1180x760")
        self.minsize(980, 640)
        self.configure(fg_color="#0b1120")

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#101a2d")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar, text="REVIVEX", font=ctk.CTkFont(size=27, weight="bold"),
            text_color="#64d8cb"
        ).pack(anchor="w", padx=22, pady=(28, 0))
        ctk.CTkLabel(
            self.sidebar, text="AI HARDWARE CARE", font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#8292aa"
        ).pack(anchor="w", padx=23, pady=(2, 24))

        self.nav_buttons = {}
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Device Lookup", self.show_devices),
            ("AI Triage", self.show_triage),
            ("AI Chatbot", self.show_chat),
            ("Repair Shops", self.show_shops),
            ("Community Reports", self.show_reports),
        ]
        for label, command in nav_items:
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w", height=42, corner_radius=10,
                fg_color="transparent", hover_color="#1b2b43", text_color="#d8e3f0",
                font=ctk.CTkFont(size=14), command=command
            )
            btn.pack(fill="x", padx=12, pady=4)
            self.nav_buttons[label] = btn

        ctk.CTkLabel(
            self.sidebar, text="LOCAL DESKTOP CLIENT\nAPI: 127.0.0.1:5000",
            justify="left", text_color="#6f8099", font=ctk.CTkFont(size=10)
        ).pack(side="bottom", anchor="w", padx=20, pady=20)

        self.main = ctk.CTkFrame(self, corner_radius=0, fg_color="#0b1120")
        self.main.pack(side="left", fill="both", expand=True)
        self.show_dashboard()

    def clear_main(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def heading(self, title, subtitle=""):
        top = ctk.CTkFrame(self.main, fg_color="transparent")
        top.pack(fill="x", padx=28, pady=(25, 18))
        ctk.CTkLabel(top, text=title, font=ctk.CTkFont(size=27, weight="bold"),
                     text_color="#f2f6fc").pack(anchor="w")
        if subtitle:
            ctk.CTkLabel(top, text=subtitle, font=ctk.CTkFont(size=13),
                         text_color="#91a2bb").pack(anchor="w", pady=(5, 0))

    def content_frame(self):
        frame = ctk.CTkScrollableFrame(self.main, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=22, pady=(0, 22))
        return frame

    def card(self, parent, title, value, detail=""):
        frame = ctk.CTkFrame(parent, fg_color="#142139", corner_radius=14)
        ctk.CTkLabel(frame, text=title.upper(), text_color="#8fa4bf",
                     font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=17, pady=(16, 5))
        ctk.CTkLabel(frame, text=str(value), text_color="#f2f6fc",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(anchor="w", padx=17)
        if detail:
            ctk.CTkLabel(frame, text=detail, text_color="#64d8cb",
                         font=ctk.CTkFont(size=11)).pack(anchor="w", padx=17, pady=(4, 16))
        else:
            ctk.CTkFrame(frame, height=12, fg_color="transparent").pack()
        return frame

    def run_async(self, task, on_success, status_label=None):
        if status_label:
            status_label.configure(text="Connecting to Flask API…", text_color="#f4c76b")

        def worker():
            try:
                result = task()
                self.after(0, lambda: on_success(result))
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", errors="replace")
                msg = f"API returned HTTP {e.code}: {detail[:500]}"
                self.after(0, lambda m=msg: self.show_error(m, status_label))
            except Exception as e:
                msg = f"Could not connect to {API_BASE}.\n\n{e}\n\nStart the Flask backend and try again."
                self.after(0, lambda m=msg: self.show_error(m, status_label))

        threading.Thread(target=worker, daemon=True).start()

    def show_error(self, message, status_label=None):
        if status_label:
            status_label.configure(text="Connection or request failed.", text_color="#ff8c8c")
        messagebox.showerror("REVIVEX API Error", message)

    def show_dashboard(self):
        self.clear_main()
        self.heading("Hardware Care Dashboard", "Repair intelligence, device verification and circular-tech support.")
        body = self.content_frame()
        stats = ctk.CTkFrame(body, fg_color="transparent")
        stats.pack(fill="x")
        for i in range(3):
            stats.grid_columnconfigure(i, weight=1)
        self.card(stats, "Registered devices", "6", "Sample hardware records").grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=5)
        self.card(stats, "Repair shops", "4", "Directory entries in API").grid(row=0, column=1, sticky="ew", padx=4, pady=5)
        self.card(stats, "Community reports", "3", "Initial sample reports").grid(row=0, column=2, sticky="ew", padx=(8, 0), pady=5)

        panel = ctk.CTkFrame(body, fg_color="#142139", corner_radius=14)
        panel.pack(fill="x", pady=(20, 12))
        ctk.CTkLabel(panel, text="QUICK ACTIONS", font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#f2f6fc").pack(anchor="w", padx=18, pady=(17, 10))
        row = ctk.CTkFrame(panel, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(0, 16))
        for label, command in [
            ("Look up a device", self.show_devices),
            ("Diagnose an issue", self.show_triage),
            ("Ask REVIVEX AI", self.show_chat),
        ]:
            ctk.CTkButton(row, text=label, command=command, height=38,
                          fg_color="#167e80", hover_color="#12696b").pack(side="left", padx=5, expand=True, fill="x")
        note = ctk.CTkFrame(body, fg_color="#17253a", corner_radius=12)
        note.pack(fill="x", pady=8)
        ctk.CTkLabel(note, text="Before you start", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#f4c76b").pack(anchor="w", padx=17, pady=(15, 5))
        ctk.CTkLabel(note, text="This desktop app uses your existing Flask API. Hardware records and shop listings in the supplied code are demo data, not independent verification. If a lithium battery is swollen, smoking or hot, stop using the device and seek qualified help.",
                     wraplength=850, justify="left", text_color="#c1ccdc").pack(anchor="w", padx=17, pady=(0, 16))

    def show_devices(self):
        self.clear_main()
        self.heading("Device Lookup", "Search registered device records by serial / identifier.")
        body = self.content_frame()
        row = ctk.CTkFrame(body, fg_color="transparent")
        row.pack(fill="x", pady=(0, 12))
        serial = ctk.CTkEntry(row, placeholder_text="e.g. SN-DELL-XPS15-9520", height=42)
        serial.pack(side="left", fill="x", expand=True, padx=(0, 10))
        status = ctk.CTkLabel(body, text="", text_color="#91a2bb")
        status.pack(anchor="w")
        output = ctk.CTkTextbox(body, height=430, corner_radius=12, fg_color="#111d31",
                                text_color="#dce7f5", font=ctk.CTkFont(family="Consolas", size=12))
        output.pack(fill="both", expand=True, pady=(8, 0))

        def render(data):
            output.delete("1.0", "end")
            output.insert("end", json.dumps(data, indent=2, ensure_ascii=False))
            status.configure(text="Device record loaded.", text_color="#64d8cb")

        def lookup():
            value = serial.get().strip()
            if not value:
                messagebox.showinfo("Enter device ID", "Enter a device serial / identifier first.")
                return
            self.run_async(lambda: api_request("/api/device/" + urllib.request.quote(value, safe="")), render, status)

        ctk.CTkButton(row, text="Search device", command=lookup, height=42,
                      fg_color="#167e80", hover_color="#12696b").pack(side="right")
        ctk.CTkButton(row, text="Load all", command=lambda: self.run_async(
            lambda: api_request("/api/devices-all"), render, status), height=42).pack(side="right", padx=(0, 8))
        ctk.CTkLabel(body, text="Tip: the API currently returns generated placeholder details for unknown IDs. Treat those as unverified.",
                     text_color="#f4c76b", wraplength=850, justify="left").pack(anchor="w", pady=8)

    def show_triage(self):
        self.clear_main()
        self.heading("AI Triage & Scanner", "Describe the symptoms to receive a safety-first assessment from your Flask API.")
        body = self.content_frame()
        form = ctk.CTkFrame(body, fg_color="#142139", corner_radius=14)
        form.pack(fill="x", pady=4)
        ctk.CTkLabel(form, text="Device category", text_color="#c7d5e7").pack(anchor="w", padx=18, pady=(15, 5))
        device = ctk.CTkComboBox(form, values=["Laptop", "Smartphone", "Smartwatch", "Headphones", "Bluetooth Speaker", "Other"], width=300)
        device.set("Laptop")
        device.pack(anchor="w", padx=18)
        ctk.CTkLabel(form, text="Model / serial (optional)", text_color="#c7d5e7").pack(anchor="w", padx=18, pady=(12, 5))
        model = ctk.CTkEntry(form, placeholder_text="Device model", width=450)
        model.pack(anchor="w", padx=18)
        ctk.CTkLabel(form, text="Symptoms / issue", text_color="#c7d5e7").pack(anchor="w", padx=18, pady=(12, 5))
        symptoms = ctk.CTkTextbox(form, height=110, width=700)
        symptoms.pack(fill="x", padx=18, pady=(0, 12))
        ctk.CTkLabel(form, text="Response language", text_color="#c7d5e7").pack(anchor="w", padx=18, pady=(0, 5))
        language = ctk.CTkComboBox(form, values=["English", "Hindi"], width=220)
        language.set("English")
        language.pack(anchor="w", padx=18, pady=(0, 16))
        status = ctk.CTkLabel(body, text="", text_color="#91a2bb")
        status.pack(anchor="w", pady=(10, 4))
        output = ctk.CTkTextbox(body, height=270, fg_color="#111d31", text_color="#dce7f5",
                                font=ctk.CTkFont(family="Consolas", size=12))
        output.pack(fill="both", expand=True)

        def render(data):
            output.delete("1.0", "end")
            output.insert("end", json.dumps(data, indent=2, ensure_ascii=False))
            status.configure(text="Assessment received. Follow the stop condition and safety guidance.", text_color="#64d8cb")

        def submit():
            symptom_text = symptoms.get("1.0", "end").strip()
            if not symptom_text:
                messagebox.showinfo("Describe the issue", "Enter a few symptoms first.")
                return
            payload = {"deviceType": device.get(), "model": model.get().strip(),
                       "symptoms": symptom_text, "language": language.get()}
            self.run_async(lambda: api_request("/api/triage", "POST", payload, timeout=35), render, status)

        ctk.CTkButton(form, text="Analyze issue", command=submit, height=40,
                      fg_color="#167e80", hover_color="#12696b").pack(anchor="w", padx=18, pady=(0, 18))

    def show_chat(self):
        self.clear_main()
        self.heading("REVIVEX AI Chatbot", "Ask about hardware symptoms, safe checks, repairs and e-waste.")
        body = self.content_frame()
        language = ctk.CTkSegmentedButton(body, values=["English", "Hindi"])
        language.set("English")
        language.pack(anchor="w", pady=(0, 12))
        chat_area = ctk.CTkTextbox(body, height=460, fg_color="#111d31", text_color="#e1eaf5",
                                   corner_radius=12, wrap="word", font=ctk.CTkFont(size=13))
        chat_area.pack(fill="both", expand=True)
        chat_area.insert("end", "REVIVEX AI: Hi! Describe your device issue. For a swollen, smoking or overheating battery, stop using and charging it and seek qualified help.\n\n")
        row = ctk.CTkFrame(body, fg_color="transparent")
        row.pack(fill="x", pady=(12, 0))
        entry = ctk.CTkEntry(row, placeholder_text="Type your question…", height=42)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        status = ctk.CTkLabel(body, text="", text_color="#91a2bb")
        status.pack(anchor="w", pady=(6, 0))

        def send():
            message = entry.get().strip()
            if not message:
                return
            entry.delete(0, "end")
            chat_area.insert("end", f"You: {message}\n")
            chat_area.see("end")
            lang = "hi" if language.get() == "Hindi" else "en"

            def render(data):
                chat_area.insert("end", f"REVIVEX AI: {data.get('reply', 'No reply returned.')}\n\n")
                chat_area.see("end")
                status.configure(text="Reply received.", text_color="#64d8cb")

            self.run_async(lambda: api_request("/api/chat", "POST", {"message": message, "language": lang}, timeout=35), render, status)

        ctk.CTkButton(row, text="Send", command=send, height=42, width=90,
                      fg_color="#167e80", hover_color="#12696b").pack(side="right")
        entry.bind("<Return>", lambda event: send())

    def show_shops(self):
        self.clear_main()
        self.heading("Repair Shop Directory", "Shop entries are loaded from /api/shops.")
        body = self.content_frame()
        status = ctk.CTkLabel(body, text="", text_color="#91a2bb")
        status.pack(anchor="w")
        listing = ctk.CTkScrollableFrame(body, fg_color="transparent")
        listing.pack(fill="both", expand=True)

        def render(items):
            for child in listing.winfo_children():
                child.destroy()
            for shop in items:
                card = ctk.CTkFrame(listing, fg_color="#142139", corner_radius=12)
                card.pack(fill="x", pady=6)
                ctk.CTkLabel(card, text=shop.get("name", "Repair shop"),
                             font=ctk.CTkFont(size=16, weight="bold"), text_color="#f2f6fc").pack(anchor="w", padx=16, pady=(13, 4))
                details = (
                    f"{shop.get('rating', 'Rating unavailable')}  •  {shop.get('city', '')}\n"
                    f"Specialty: {shop.get('specialty', 'Not listed')}\n"
                    f"Devices: {shop.get('supportedDevices', 'Not listed')}\n"
                    f"Address: {shop.get('address', 'Not listed')}\n"
                    f"Phone: {shop.get('phone', 'Not listed')}  •  Turnaround: {shop.get('turnaround', 'Not listed')}"
                )
                ctk.CTkLabel(card, text=details, justify="left", anchor="w", wraplength=850,
                             text_color="#aebed2").pack(fill="x", padx=16, pady=(0, 14))
            status.configure(text=f"Loaded {len(items)} directory entries. Verify details independently before visiting.", text_color="#64d8cb")

        self.run_async(lambda: api_request("/api/shops"), render, status)

    def show_reports(self):
        self.clear_main()
        self.heading("Community Repair Reports", "View existing reports or submit a new report to the Flask API.")
        body = self.content_frame()
        form = ctk.CTkFrame(body, fg_color="#142139", corner_radius=12)
        form.pack(fill="x", pady=(0, 12))
        fields = {}
        for label, key, placeholder in [
            ("Your name (optional)", "userName", "Name or Anonymous"),
            ("Device name", "deviceName", "e.g. Dell laptop"),
            ("Device history", "deviceHistory", "Age, usage, recent events"),
            ("Problem reported", "problemReported", "What went wrong?"),
            ("Repair attempted", "repairAttempted", "What have you tried?"),
            ("Cost", "cost", "e.g. ₹500 or unknown"),
            ("Tips for others", "tips", "Optional safety tip"),
        ]:
            ctk.CTkLabel(form, text=label, text_color="#c7d5e7").pack(anchor="w", padx=15, pady=(8, 3))
            entry = ctk.CTkEntry(form, placeholder_text=placeholder, height=34)
            entry.pack(fill="x", padx=15)
            fields[key] = entry
        status = ctk.CTkLabel(body, text="", text_color="#91a2bb")
        status.pack(anchor="w")
        output = ctk.CTkTextbox(body, height=250, fg_color="#111d31", text_color="#dce7f5",
                                font=ctk.CTkFont(family="Consolas", size=12))
        output.pack(fill="both", expand=True, pady=(5, 0))

        def render(data):
            output.delete("1.0", "end")
            output.insert("end", json.dumps(data, indent=2, ensure_ascii=False))
            status.configure(text=f"Loaded {len(data)} reports.", text_color="#64d8cb")

        def refresh():
            self.run_async(lambda: api_request("/api/reports"), render, status)

        def submit():
            payload = {key: entry.get().strip() for key, entry in fields.items() if entry.get().strip()}
            if not payload.get("deviceName") or not payload.get("problemReported"):
                messagebox.showinfo("Missing details", "Device name and problem reported are required.")
                return
            def done(result):
                messagebox.showinfo("Report submitted", "The API accepted the report.")
                refresh()
            self.run_async(lambda: api_request("/api/reports", "POST", payload), done, status)

        buttons = ctk.CTkFrame(form, fg_color="transparent")
        buttons.pack(fill="x", padx=15, pady=13)
        ctk.CTkButton(buttons, text="Submit report", command=submit, fg_color="#167e80",
                      hover_color="#12696b").pack(side="left", padx=(0, 8))
        ctk.CTkButton(buttons, text="Refresh reports", command=refresh).pack(side="left")
        refresh()


if __name__ == "__main__":
    app = RevivexApp()
    app.mainloop()
