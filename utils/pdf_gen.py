from fpdf import FPDF
import datetime

class IncidentReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CyberSentinel - Security Incident Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(log_entry, analysis_text):
    pdf = IncidentReport()
    pdf.add_page()
    
    # 1. Metadata
    pdf.set_font("Arial", size=12)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, txt=f"Generated On: {timestamp}", ln=True)
    pdf.cell(200, 10, txt=f"Analyst: Automated AI (CyberSentinel)", ln=True)
    pdf.ln(10)
    
    # 2. The Log Evidence
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="Incident Evidence (Raw Log):", ln=True)
    pdf.set_font("Courier", size=10) # Monospace for code/logs
    pdf.multi_cell(0, 10, txt=log_entry)
    pdf.ln(10)
    
    # 3. AI Analysis
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt="AI Assessment & Remediation:", ln=True)
    pdf.set_font("Arial", size=11)
    
    # Clean up markdown asterisks for cleaner PDF text
    clean_analysis = analysis_text.replace("**", "").replace("* ", "- ")
    pdf.multi_cell(0, 8, txt=clean_analysis)
    
    return pdf.output(dest='S').encode('latin-1') # Return binary data for download
