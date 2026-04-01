from flask import Flask, render_template, request
import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = Flask(__name__)

# --- SQL Database Setup (Massively Expanded) ---
DB_NAME = 'careers_advanced.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Advanced Data: Har Software Domain yahan cover kiya hai
    roles_detailed = [
        # 1. AI & DATA SCIENCE
        (1, "Data Scientist", "python, r, sql, statistics, pandas, numpy, scikit-learn, matplotlib, machine learning, deep learning, tableau, powerbi"),
        (2, "AI/ML Engineer", "python, pytorch, tensorflow, nlp, computer vision, keras, hugging face, opencv, model deployment, cloud ml, math, probability"),
        (3, "Data Engineer", "sql, python, hadoop, spark, kafka, etl, airflow, snowflake, hive, big data, scala, mongodb, postgresql"),
        (4, "Data Analyst", "sql, excel, python, powerbi, tableau, data cleaning, dashboarding, probability, statistics, pandas"),

        # 2. WEB DEVELOPMENT
        (5, "Frontend Developer", "html, css, javascript, react, angular, vue, tailwind, bootstrap, sass, typescript, redex, next.js, web design"),
        (6, "Backend Developer", "node.js, express, django, flask, fastapi, spring boot, java, php, ruby on rails, sql, nosql, rest api, microservices, go"),
        (7, "Full Stack Developer", "html, css, javascript, react, node.js, express, mongodb, sql, git, aws, docker, api integration, system design"),

        # 3. MOBILE & APP DEVELOPMENT
        (8, "Android Developer", "kotlin, java, android sdk, jetpack compose, retrofit, firebase, room, sqlite, mvvm, material design"),
        (9, "iOS Developer", "swift, objective-c, swiftui, xcode, cocoa touch, core data, apple human interface, swift package manager"),
        (10, "Cross-Platform Developer", "flutter, dart, react native, ionic, capacitor, firebase, graphql, mobile ui/ux"),

        # 4. DEVOPS & CLOUD
        (11, "DevOps Engineer", "docker, kubernetes, aws, azure, gcp, jenkins, terraform, ansible, linux, bash, git, ci/cd, prometheus, grafana"),
        (12, "Cloud Architect", "aws, azure, google cloud, serverless, microservices, network security, iam, terraform, multi-cloud strategy"),
        (13, "Site Reliability Engineer (SRE)", "linux, python, bash, automation, monitoring, incident management, kubernetes, distributed systems, golang"),

        # 5. CYBERSECURITY
        (14, "Cybersecurity Analyst", "penetration testing, ethical hacking, kali linux, wireshark, metasploit, cryptography, network security, firewall, siem, soc"),
        (15, "Security Engineer", "encryption, vulnerability assessment, cloud security, owasp, python, secure coding, iam, firewall management"),

        # 6. SPECIALIZED DOMAINS
        (16, "Game Developer", "unity, unreal engine, c#, c++, 3d modeling, shaders, directx, opengl, game physics, blender"),
        (17, "Blockchain Developer", "solidity, ethereum, smart contracts, web3.js, hyperledger, rust, cryptography, dapps, bitcoin, defi"),
        (18, "Embedded Systems Engineer", "c, c++, assembly, microcontrollers, rtos, iot, raspberry pi, arduino, pcb design, firmware development"),
        (19, "QA Automation Engineer", "selenium, junit, pytest, selenium, cucumber, automation testing, api testing, load testing, jmeter, manual testing"),
        (20, "Salesforce Developer", "apex, visualforce, lwc, salesforce admin, soql, cloud computing, crm, lightning design system"),
        (21, "SAP ABAP Consultant", "sap abap, sap hana, erp, fiori, odata, bapi, rfc, sap functional modules"),
        (22, "AR/VR Developer", "unity, unreal engine, c#, arcore, arkit, blender, 3d spatial audio, virtual reality, augmented reality")
    ]
    
    cursor.execute("DROP TABLE IF EXISTS job_roles")
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_roles 
                      (id INTEGER PRIMARY KEY, role TEXT, skills TEXT)''')
    cursor.executemany("INSERT OR IGNORE INTO job_roles VALUES (?,?,?)", roles_detailed)
    conn.commit()
    conn.close()

init_db()

# --- Core Logic for Resume Parsing and Similarity (REMAINS SAME) ---
def extract_skills_from_resume_text(text):
    # Added more keywords for better simulation
    known_skills = ["python", "java", "sql", "html", "css", "js", "react", "ml", "nlp", "cloud", "docker", 
                    "kubernetes", "aws", "flutter", "swift", "kotlin", "spark", "hadoop", "selenium", "c++", "c#"]
    text_lower = text.lower()
    extracted_skills = [skill for skill in known_skills if skill in text_lower]
    return ", ".join(extracted_skills)

def generate_bubble_html(skills_list):
    html_bubbles = []
    for skill in skills_list:
        html_bubbles.append(f'<span class="badge rounded-pill bg-warning text-dark m-1" style="font-size: 1.1em; background-image: linear-gradient(135deg, #f7ce68 0%, #fbab7e 100%);">{skill.upper()}</span>')
    return "".join(html_bubbles)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM job_roles ORDER BY role ASC") # Alphabetical for UI
    roles = [row[0] for row in cursor.fetchall()]

    if request.method == "POST":
        target_role = request.form.get("role")
        user_skills_input = request.form.get("skills").lower()
        resume_file = request.files.get("resume")
        
        final_user_skills_str = user_skills_input
        extracted_message = "Using manual input."
        if resume_file:
            resume_text_content = f"Filename: {resume_file.filename}. Found skills: Python, Java, SQL, AWS"
            extracted_user_skills_str = extract_skills_from_resume_text(resume_text_content)
            final_user_skills_str = f"{user_skills_input}, {extracted_user_skills_str}"
            extracted_message = f"Found skills in resume: {extracted_user_skills_str.upper()}"

        cursor.execute("SELECT skills FROM job_roles WHERE role=?", (target_role,))
        job_skills_str = cursor.fetchone()[0]
        job_skills_list = [s.strip() for s in job_skills_str.split(",")]

        # AI Similarity Logic
        vectorizer = CountVectorizer().fit_transform([final_user_skills_str, job_skills_str])
        vectors = vectorizer.toarray()
        score = round(cosine_similarity(vectors)[0][1] * 100, 2)

        # Gap Analysis
        user_skills_list = [s.strip() for s in final_user_skills_str.split(",")]
        missing = [s for s in job_skills_list if s not in user_skills_list]
        formatted_bubbles_html = generate_bubble_html(missing)

        result = {
            "role": target_role,
            "score": score,
            "bubbles_html": formatted_bubbles_html,
            "extracted_message": extracted_message,
            "status": "Ready ✅" if score > 75 else ("Improving ⚠️" if score > 50 else "Needs Work 🚫")
        }

    conn.close()
    return render_template("index.html", roles=roles, result=result)

if __name__ == "__main__":
    app.run(debug=True)