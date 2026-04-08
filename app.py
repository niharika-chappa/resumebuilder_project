from flask import Flask, render_template, request, make_response
from xhtml2pdf import pisa
from io import BytesIO
import os  # <- added for Render deployment

app = Flask(__name__)

# Convert HTML to PDF
def convert_html_to_pdf(source_html):
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(source_html, dest=pdf, encoding="UTF-8")

    if pisa_status.err:
        return None

    pdf.seek(0)
    return pdf


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "title": request.form["title"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "location": request.form["location"],
            "linkedin": request.form["linkedin"],
            "github": request.form["github"],
            "photo": request.form.get("photo", ""),
            "summary": request.form["summary"],
            "skills": [skill.strip() for skill in request.form["skills"].split(",")],
            "languages": [lang.strip() for lang in request.form.get("languages", "").split(",") if lang.strip()],
            "certifications": request.form.get("certifications", ""),
            "internships": request.form.get("internships", ""),
            "education": request.form["education"],
            "projects": request.form["projects"],
            "experience": request.form["experience"]
        }

        # Download PDF button clicked
        if "download_pdf" in request.form:
            html = render_template("resume_pdf.html", data=data)
            pdf = convert_html_to_pdf(html)

            if pdf:
                response = make_response(pdf.read())
                response.headers["Content-Type"] = "application/pdf"
                response.headers["Content-Disposition"] = f'attachment; filename={data["name"]}_Resume.pdf'
                return response
            else:
                return "Error generating PDF"

        # Normal Preview Resume
        return render_template("resume.html", data=data)

    return render_template("index.html")


# ---- Updated for Render deployment ----
if __name__ == "__main__":
    # Use host 0.0.0.0 and port from Render environment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)