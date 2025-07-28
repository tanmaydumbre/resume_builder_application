from flask import Flask, render_template, request, send_file, redirect, url_for
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from textwrap import wrap
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    summary = request.form['summary']
    education = request.form['education']
    skills = request.form['skills']
    experience = request.form['experience']
    languages = request.form['languages']
    certificates = request.form['certificates']
    awards = request.form['awards']
    interests = request.form['interests']

    file_path = f"static/{name}_resume.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)

    width, height = A4
    x = 50
    y = height - 50

    def draw_section(title, content):
        nonlocal y
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x, y, title)
        y -= 20
        c.setFont("Helvetica", 12)
        for line in wrap(content, 95):
            c.drawString(x, y, line)
            y -= 15
        y -= 10

    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, name)
    y -= 25
    c.setFont("Helvetica", 12)
    c.drawString(x, y, f"Email: {email} | Phone: {phone}")
    y -= 30

    draw_section("Profile Summary", summary)
    draw_section("Experience", experience)
    draw_section("Education", education)
    draw_section("Skills", skills)
    draw_section("Languages", languages)
    draw_section("Certificates", certificates)
    draw_section("Honors & Awards", awards)
    draw_section("Interests", interests)

    c.save()

    return send_file(file_path, as_attachment=True)

@app.route('/test')
def test():
    return "Flask is working!"


if __name__ == '__main__':
    app.run(debug=True)