import re
import heapq
import streamlit as st

st.set_page_config(page_title="ResumeRank AI", page_icon="📄", layout="wide")

# ---------- DSA ALGORITHMS ----------
def kmp_search(text, pattern):
    text, pattern = text.lower(), pattern.lower()
    if not pattern:
        return True
    lps = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1; j += 1
            if j == len(pattern):
                return True
        elif j:
            j = lps[j - 1]
        else:
            i += 1
    return False

def rabin_karp_search(text, pattern):
    text, pattern = text.lower(), pattern.lower()
    if not pattern:
        return True
    m, n = len(pattern), len(text)
    if m > n:
        return False
    base, mod = 256, 101
    ph = th = 0
    high = pow(base, m - 1, mod)
    for i in range(m):
        ph = (base * ph + ord(pattern[i])) % mod
        th = (base * th + ord(text[i])) % mod
    for i in range(n - m + 1):
        if ph == th and text[i:i+m] == pattern:
            return True
        if i < n - m:
            th = (base * (th - ord(text[i]) * high) + ord(text[i+m])) % mod
            th %= mod
    return False

def lcs_length(a, b):
    a, b = a.lower()[:1500], b.lower()[:1500]
    dp = [0] * (len(b) + 1)
    for ca in a:
        prev = 0
        for j, cb in enumerate(b, 1):
            old = dp[j]
            dp[j] = prev + 1 if ca == cb else max(dp[j], dp[j-1])
            prev = old
    return dp[-1]

def merge_sort(items):
    if len(items) <= 1:
        return items
    mid = len(items)//2
    left, right = merge_sort(items[:mid]), merge_sort(items[mid:])
    out = []; i = j = 0
    while i < len(left) and j < len(right):
        if left[i]["score"] >= right[j]["score"]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

def extract_keywords(text):
    stop = {"the","and","for","with","from","this","that","are","you","your",
            "have","has","will","our","into","using","role","job","work",
            "years","year","required","requirements","candidate","skills"}
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.-]{1,30}", text.lower())
    return sorted({w.strip(".") for w in words if w not in stop and len(w) >= 3})

def score_resume(resume, jd, skills):
    kmp_hits = [s for s in skills if kmp_search(resume, s)]
    rk_hits = [s for s in skills if rabin_karp_search(resume, s)]
    matched = sorted(set(kmp_hits) | set(rk_hits))
    skill_score = len(matched) / len(skills) * 60 if skills else 0

    rwords = set(re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,30}", resume.lower()))
    jwords = set(re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,30}", jd.lower()))
    keyword_score = min(20, len(rwords & jwords) / max(1, len(extract_keywords(jd))) * 20)

    lcs = lcs_length(resume, jd)
    dp_score = min(20, lcs / max(1, min(len(resume), len(jd))) * 20)
    total = min(100, skill_score + keyword_score + dp_score)
    return round(total, 2), matched, kmp_hits, rk_hits

def read_file(uploaded):
    name = uploaded.name.lower()
    data = uploaded.getvalue()
    if name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(uploaded)
            return "\n".join((p.extract_text() or "") for p in reader.pages)
        except Exception as e:
            return "PDF extraction error: " + str(e)
    if name.endswith(".docx"):
        try:
            from docx import Document
            import io
            doc = Document(io.BytesIO(data))
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            return "DOCX extraction error: " + str(e)
    return ""

SAMPLE_JD = """Python developer with skills in Python, SQL, Machine Learning,
Pandas, Scikit-learn, FastAPI, Git and data analysis. Experience building
machine learning projects and APIs is preferred."""

SAMPLE_RESUMES = {
    "Ananya Sharma": """Python developer with experience in Python, SQL, Pandas,
Machine Learning, Scikit-learn, Git and data analysis. Built ML projects and REST APIs.""",
    "Rahul Kumar": """Software developer experienced in Java, Python, SQL, Git
and web development. Worked on data analysis projects and machine learning basics.""",
    "Priya Reddy": """Data science student with Python, Pandas, Machine Learning,
Scikit-learn, SQL, data analysis and Git. Built classification and prediction projects."""
}

# ---------- UI ----------
with st.sidebar:
    st.markdown("## 📄 ResumeRank AI")
    st.caption("DSA-Based Intelligent Resume Screening")
    page = st.radio("Navigation", ["Dashboard", "Screen Resumes", "DSA Insights", "About Project"])
    st.divider()
    st.info("KMP • Rabin-Karp • Dynamic Programming • Merge Sort • Hash Table • Priority Queue")

if page == "Dashboard":
    st.title("ResumeRank AI")
    st.write("### Intelligent Resume Screening & Candidate Ranking System")
    st.divider()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Candidates", "3")
    c2.metric("DSA Algorithms", "5+")
    c3.metric("Screening", "Automated")
    c4.metric("Output", "Ranked List")

    st.subheader("System Workflow")
    cols = st.columns(5)
    for col, n, title, desc in zip(cols, range(1,6),
        ["Upload","Extract","Search","Score","Rank"],
        ["JD + resumes","Resume text","KMP + Rabin-Karp","DP similarity","Merge Sort + PQ"]):
        with col:
            st.markdown(f"### {n}. {title}")
            st.write(desc)

    st.subheader("Problem → Solution")
    st.write("Manual resume screening can take time when many candidates apply. "
             "This application automates text extraction, skill searching, matching-score "
             "calculation and candidate ranking.")

elif page == "Screen Resumes":
    st.title("🔎 Screen & Rank Candidates")
    left, right = st.columns(2)

    with left:
        jd_file = st.file_uploader("Upload Job Description", type=["pdf","docx","txt"])
        jd_text = read_file(jd_file) if jd_file else SAMPLE_JD
        st.text_area("Job Description", jd_text, height=220)

    with right:
        resume_files = st.file_uploader("Upload Resumes (multiple)",
                                         type=["pdf","docx","txt"],
                                         accept_multiple_files=True)
        if not resume_files:
            st.caption("Demo mode: 3 sample resumes will be ranked.")

    skills_input = st.text_input(
        "Required Skills (comma separated)",
        "Python, SQL, Machine Learning, Pandas, Scikit-learn, FastAPI, Git, Data Analysis"
    )
    skills = [x.strip().lower() for x in skills_input.split(",") if x.strip()]

    if st.button("🚀 Screen Resumes", use_container_width=True):
        candidates = ([{"name": f.name, "text": read_file(f)} for f in resume_files]
                      if resume_files else
                      [{"name": n, "text": t} for n,t in SAMPLE_RESUMES.items()])

        results = []
        for c in candidates:
            score, matched, kmp, rk = score_resume(c["text"], jd_text, skills)
            results.append({"name":c["name"],"score":score,"matched":matched,
                            "kmp":kmp,"rk":rk})
        st.session_state["ranked"] = merge_sort(results)

    ranked = st.session_state.get("ranked", [])
    if ranked:
        st.divider()
        st.subheader("🏆 Ranked Candidates")
        for i,c in enumerate(ranked,1):
            with st.container(border=True):
                a,b,d = st.columns([1,5,2])
                a.markdown(f"## #{i}")
                b.markdown(f"### {c['name']}")
                b.write("Matched skills: " + (", ".join(c["matched"]) or "None"))
                d.metric("Match Score", f"{c['score']}%")
                st.progress(int(c["score"]))
                with st.expander("View DSA analysis"):
                    st.write("**KMP matches:** " + (", ".join(c["kmp"]) or "None"))
                    st.write("**Rabin-Karp matches:** " + (", ".join(c["rk"]) or "None"))
                    st.write("**Dynamic Programming:** LCS-based text similarity contributes to score.")
                    st.write("**Merge Sort:** orders candidates by matching score.")
        heap = [(-c["score"], c["name"]) for c in ranked]
        heapq.heapify(heap)
        st.success(f"Priority Queue: highest-ranked candidate = {heap[0][1]}")

elif page == "DSA Insights":
    st.title("🧠 DSA Algorithm Insights")
    rows = [
        ("KMP","Pattern searching","Efficiently searches required skills in resume text."),
        ("Rabin-Karp","Hash-based search","Uses hashing/rolling hash for keyword searching."),
        ("Dynamic Programming","Similarity","LCS estimates common text between resume and job description."),
        ("Merge Sort","Ranking","Sorts candidates from highest to lowest matching score."),
        ("Hash Table","Lookup","Fast storage and lookup of skills/keywords."),
        ("Priority Queue","Top candidates","Retrieves the highest-scoring candidates quickly.")
    ]
    for n,p,e in rows:
        with st.container(border=True):
            st.markdown(f"### {n} — {p}")
            st.write(e)

elif page == "About Project":
    st.title("📌 About the Project")
    st.write("The system automates resume screening by extracting information, "
             "comparing resumes with a job description, calculating a matching score "
             "and ranking candidates.")
    st.subheader("Objectives")
    for x in ["Automatically screen resumes",
              "Extract skills, education, experience and certifications",
              "Compare resumes with job description",
              "Calculate matching score",
              "Rank candidates",
              "Reduce manual screening effort"]:
        st.write("• " + x)
    st.subheader("Technology Stack")
    st.write("Python • Streamlit • Pandas • Scikit-learn • SQLite/MySQL")
    st.info("Review-2 demo: Upload JD → upload 2–3 resumes → Screen Resumes → explain scores → open DSA analysis.")
