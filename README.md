# 🚀 AI-Driven Career Path & Skill Gap Analyzer

### "Bridging the gap between Academic Learning and Industry Standards using NLP."

---

## 📌 Project Overview
In the rapidly evolving tech landscape, students often face **Information Asymmetry** regarding the specific skills required for industry roles. This project is a **Decision Support System** that quantifies a candidate's readiness for various software domains. 

By utilizing **Vector Space Modeling** and **Cosine Similarity**, the application analyzes a user's current skill set (via manual input or resume parsing) and compares it against a structured **SQLite** database of industry benchmarks.

---

## 🛠️ Technical Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python (Flask Micro-framework) |
| **Machine Learning** | Scikit-Learn (NLP Pipeline) |
| **Database** | SQLite (Relational Storage) |
| **Frontend** | HTML5, CSS3, Bootstrap 5 (Glassmorphism UI) |
| **Deployment** | Gunicorn (WSGI Server) |

---

## 🧠 The Intelligence Engine (How it Works)

### 1. Vectorization
The system uses `CountVectorizer` to transform unstructured text into numerical vectors. This creates a high-dimensional vocabulary of technical skills.

### 2. Mathematical Match (Cosine Similarity)
Instead of basic keyword matching, I implemented **Cosine Similarity** to measure the angular distance between the User Vector ($A$) and the Job Requirement Vector ($B$).

$$\text{Similarity Score} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$

### 3. Gap Analysis
The system performs a **Set Difference** operation to identify missing "Technical Nodes" and generates a logical learning roadmap.

---

## 📊 Complexity Analysis
- **Time Complexity:** $O(V)$, where $V$ is the vocabulary size. The matching is near-instant (< 50ms).
- **Space Complexity:** $O(k)$ using **Sparse Matrix** representation, ensuring high memory efficiency by only storing non-zero technical attributes.

---

## 🚀 Key Features
- **Glassmorphism UI:** A futuristic, translucent interface for better UX.
- **Dynamic Database:** Over 20+ specialized software roles from DevOps to Blockchain.
- **Resume Parsing:** Logic to extract keywords from uploaded PDF files.
- **Real-time Scoring:** Instant feedback on career readiness.

---

## 📝 Author
**Ayush Kumar** *MCA (Artificial Intelligence & Machine Learning)* *LNCT University, Bhopal*

---