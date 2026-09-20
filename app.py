import re
import heapq
import streamlit as st

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="ResumeRank AI",
    page_icon="📄",
    layout="wide"
)

# ============================================================
# BROWN + BEIGE DESIGN
# ============================================================

st.markdown("""
<style>

/* ================= MAIN PAGE ================= */

.stApp {
    background-color: #F5EBDD;
    color: #4A2C20;
}

h1 {
    color: #5A3425 !important;
}

h2 {
    color: #68402D !important;
}

h3 {
    color: #79513A !important;
}

p, label {
    color: #5A3425;
}


/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background-color: #4A2C20;
}

section[data-testid="stSidebar"] * {
    color: #FFF4E6 !important;
}

section[data-testid="stSidebar"] .stAlert {
    background-color: #68402D !important;
    border: 1px solid #A87955 !important;
}


/* ================= BUTTON ================= */

.stButton > button {
    background-color: #7A4B32 !important;
    color: #FFF9F0 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background-color: #5A3425 !important;
}

.stButton > button p {
    color: #FFF9F0 !important;
}


/* ================= INPUTS ================= */

.stTextInput > div > div > input {
    background-color: #FFF9F0 !important;
    color: #4A2C20 !important;
    border: 1px solid #C9A889 !important;
    border-radius: 8px !important;
}

.stTextArea textarea {
    background-color: #FFF9F0 !important;
    color: #4A2C20 !important;
    border: 1px solid #C9A889 !important;
    border-radius: 8px !important;
}


/* ================= FILE UPLOADER ================= */

[data-testid="stFileUploaderDropzone"] {
    background-color: #FFF7EA !important;
    border: 1px dashed #B89575 !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: #68402D !important;
}


/* ================= METRICS ================= */

[data-testid="stMetric"] {
    background-color: #FFF9F0;
    border: 1px solid #D8BFA5;
    border-radius: 10px;
    padding: 10px;
}


/* ================= PROGRESS ================= */

.stProgress > div > div > div > div {
    background-color: #8B5E3C;
}


/* ============================================================
   DSA INSIGHTS PAGE
   ============================================================ */

.dsa-intro {
    background-color: #EFE0CB;
    border-left: 4px solid #7A4B32;
    padding: 9px 13px;
    border-radius: 7px;
    margin-bottom: 14px;
    color: #5A3425;
    font-size: 13px;
}


/* ================= SMALL DSA CARD ================= */

.dsa-card {
    background-color: #FFF9F0;
    border: 1px solid #D7B997;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 5px;
    box-shadow: 0px 2px 5px rgba(74, 44, 32, 0.10);
}


/* ================= ALGORITHM NAME ================= */

.dsa-title {
    background-color: #6B3E26;
    color: #FFF9F0 !important;
    padding: 7px 10px;
    font-size: 14px;
    font-weight: 800;
}


/* ================= PURPOSE ================= */

.dsa-purpose {
    background-color: #EBD8B7;
    color: #5A3425 !important;
    padding: 5px 9px;
    font-size: 10px;
    font-weight: 800;
}


/* ================= DESCRIPTION ================= */

.dsa-description {
    color: #5A3425 !important;
    padding: 6px 9px 2px 9px;
    font-size: 10px;
    line-height: 1.3;
}


/* ================= EXAMPLE ================= */

.dsa-example {
    background-color: #F3E5D1;
    color: #68402D !important;
    margin: 3px 9px 7px 9px;
    padding: 5px 7px;
    border-radius: 5px;
    font-size: 9px;
    line-height: 1.3;
}


/* ================= CODE LABEL ================= */

.code-label {
    background-color: #4A2C20;
    color: #FFF9F0 !important;
    margin: 0 9px;
    padding: 5px 7px;
    border-radius: 5px 5px 0 0;
    font-size: 9px;
    font-weight: 700;
}


/* ================= CODE BLOCK ================= */

div[data-testid="stCodeBlock"] {
    margin: 0 9px 9px 9px !important;
}

div[data-testid="stCodeBlock"] pre {
    background-color: #302119 !important;
    border: 1px solid #6B3E26 !important;
    border-radius: 0 0 5px 5px !important;
    padding: 7px !important;
}

div[data-testid="stCodeBlock"] code {
    color: #F7E8D2 !important;
    font-size: 9px !important;
    line-height: 1.25 !important;
}


/* ================= PROCESS BOXES ================= */

.process-box {
    background-color: #FFF9F0;
    border: 1px solid #D7B997;
    border-radius: 8px;
    padding: 9px;
    min-height: 105px;
}

.process-title {
    color: #6B3E26 !important;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 4px;
}

.process-text {
    color: #5A3425 !important;
    font-size: 10px;
    line-height: 1.3;
}


/* ================= CANDIDATE CARDS ================= */

.candidate-card {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
    border: 1px solid #D8BFA5;
}

.rank1 {
    background-color: #EBD8B7;
}

.rank2 {
    background-color: #F2E4CC;
}

.rank3 {
    background-color: #F8EDDA;
}

.rankother {
    background-color: #FFF9F0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# KMP
# ============================================================

def kmp_search(text, pattern):

    text = text.lower()
    pattern = pattern.lower()

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

    i = 0
    j = 0

    while i < len(text):

        if text[i] == pattern[j]:

            i += 1
            j += 1

            if j == len(pattern):
                return True

        elif j:

            j = lps[j - 1]

        else:
            i += 1

    return False


# ============================================================
# RABIN-KARP
# ============================================================

def rabin_karp_search(text, pattern):

    text = text.lower()
    pattern = pattern.lower()

    if not pattern:
        return True

    m = len(pattern)
    n = len(text)

    if m > n:
        return False

    base = 256
    mod = 101

    pattern_hash = 0
    text_hash = 0

    high = pow(base, m - 1, mod)

    for i in range(m):

        pattern_hash = (
            base * pattern_hash +
            ord(pattern[i])
        ) % mod

        text_hash = (
            base * text_hash +
            ord(text[i])
        ) % mod

    for i in range(n - m + 1):

        if (
            pattern_hash == text_hash
            and text[i:i + m] == pattern
        ):
            return True

        if i < n - m:

            text_hash = (
                base *
                (
                    text_hash -
                    ord(text[i]) * high
                )
                + ord(text[i + m])
            ) % mod

            text_hash %= mod

    return False


# ============================================================
# DYNAMIC PROGRAMMING - LCS
# ============================================================

def lcs_length(a, b):

    a = a.lower()[:1500]
    b = b.lower()[:1500]

    dp = [0] * (len(b) + 1)

    for ca in a:

        previous = 0

        for j, cb in enumerate(b, 1):

            old = dp[j]

            if ca == cb:
                dp[j] = previous + 1
            else:
                dp[j] = max(
                    dp[j],
                    dp[j - 1]
                )

            previous = old

    return dp[-1]


# ============================================================
# MERGE SORT
# ============================================================

def merge_sort(items):

    if len(items) <= 1:
        return items

    mid = len(items) // 2

    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])

    output = []

    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i]["score"] >= right[j]["score"]:
            output.append(left[i])
            i += 1

        else:
            output.append(right[j])
            j += 1

    return output + left[i:] + right[j:]


# ============================================================
# KEYWORD EXTRACTION
# ============================================================

def extract_keywords(text):

    stop = {
        "the", "and", "for", "with",
        "from", "this", "that", "are",
        "you", "your", "have", "has",
        "will", "our", "into", "using",
        "role", "job", "work", "years",
        "year", "required", "requirements",
        "candidate", "skills"
    }

    words = re.findall(
        r"[a-zA-Z][a-zA-Z+#.-]{1,30}",
        text.lower()
    )

    return sorted({
        word.strip(".")
        for word in words
        if word not in stop
        and len(word) >= 3
    })


# ============================================================
# RESUME SCORE
# ============================================================

def score_resume(resume, jd, skills):

    kmp_hits = [
        skill
        for skill in skills
        if kmp_search(resume, skill)
    ]

    rk_hits = [
        skill
        for skill in skills
        if rabin_karp_search(resume, skill)
    ]

    matched = sorted(
        set(kmp_hits) | set(rk_hits)
    )

    skill_score = (
        len(matched) / len(skills) * 60
        if skills
        else 0
    )

    rwords = set(
        re.findall(
            r"[a-zA-Z][a-zA-Z+#.-]{2,30}",
            resume.lower()
        )
    )

    jwords = set(
        re.findall(
            r"[a-zA-Z][a-zA-Z+#.-]{2,30}",
            jd.lower()
        )
    )

    keyword_score = min(
        20,
        len(rwords & jwords)
        / max(1, len(extract_keywords(jd)))
        * 20
    )

    lcs = lcs_length(resume, jd)

    dp_score = min(
        20,
        lcs /
        max(
            1,
            min(len(resume), len(jd))
        )
        * 20
    )

    total = min(
        100,
        skill_score +
        keyword_score +
        dp_score
    )

    return (
        round(total, 2),
        matched,
        kmp_hits,
        rk_hits
    )


# ============================================================
# FILE READER
# ============================================================

def read_file(uploaded):

    name = uploaded.name.lower()
    data = uploaded.getvalue()

    if name.endswith(".txt"):

        return data.decode(
            "utf-8",
            errors="ignore"
        )

    if name.endswith(".pdf"):

        try:

            import PyPDF2

            reader = PyPDF2.PdfReader(uploaded)

            return "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        except Exception as e:

            return "PDF extraction error: " + str(e)

    if name.endswith(".docx"):

        try:

            from docx import Document
            import io

            doc = Document(
                io.BytesIO(data)
            )

            return "\n".join(
                paragraph.text
                for paragraph in doc.paragraphs
            )

        except Exception as e:

            return "DOCX extraction error: " + str(e)

    return ""


# ============================================================
# SAMPLE DATA
# ============================================================

SAMPLE_JD = """
Python developer with skills in Python, SQL, Machine Learning,
Pandas, Scikit-learn, FastAPI, Git and data analysis.
Experience building machine learning projects and APIs is preferred.
"""

SAMPLE_RESUMES = {

    "Ananya Sharma": """
    Python developer with experience in Python, SQL, Pandas,
    Machine Learning, Scikit-learn, Git and data analysis.
    Built ML projects and REST APIs.
    """,

    "Rahul Kumar": """
    Software developer experienced in Java, Python, SQL, Git
    and web development. Worked on data analysis projects
    and machine learning basics.
    """,

    "Priya Reddy": """
    Data science student with Python, Pandas, Machine Learning,
    Scikit-learn, SQL, data analysis and Git.
    Built classification and prediction projects.
    """
}


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📄 ResumeRank AI")

    st.caption(
        "DSA-Based Intelligent Resume Screening"
    )

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Screen Resumes",
            "DSA Insights",
            "About Project"
        ]
    )

    st.divider()

    st.info(
        "KMP • Rabin-Karp • Dynamic Programming • "
        "Merge Sort • Hash Table • Priority Queue"
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.title("ResumeRank AI")

    st.write(
        "### Intelligent Resume Screening & Candidate Ranking System"
    )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Candidates", "3")
    c2.metric("DSA Algorithms", "6")
    c3.metric("Screening", "Automated")
    c4.metric("Output", "Ranked List")

    st.subheader("System Workflow")

    cols = st.columns(5)

    workflow = [
        ("1", "Upload", "JD + resumes"),
        ("2", "Extract", "Resume text"),
        ("3", "Search", "KMP + Rabin-Karp"),
        ("4", "Score", "DP similarity"),
        ("5", "Rank", "Merge Sort + PQ")
    ]

    for col, item in zip(cols, workflow):

        with col:

            st.markdown(
                f"### {item[0]}. {item[1]}"
            )

            st.write(item[2])

    st.subheader("Problem → Solution")

    st.write(
        "Manual resume screening can take time when many "
        "candidates apply. This application automates text "
        "extraction, skill searching, matching-score "
        "calculation and candidate ranking."
    )


# ============================================================
# SCREEN RESUMES
# ============================================================

elif page == "Screen Resumes":

    st.title("🔎 Screen & Rank Candidates")

    left, right = st.columns(2)

    with left:

        jd_file = st.file_uploader(
            "Upload Job Description",
            type=["pdf", "docx", "txt"]
        )

        jd_text = (
            read_file(jd_file)
            if jd_file
            else SAMPLE_JD
        )

        st.text_area(
            "Job Description",
            jd_text,
            height=220
        )

    with right:

        resume_files = st.file_uploader(
            "Upload Resumes (multiple)",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )

        if not resume_files:

            st.caption(
                "Demo mode: 3 sample resumes will be ranked."
            )

    skills_input = st.text_input(
        "Required Skills (comma separated)",
        "Python, SQL, Machine Learning, Pandas, Scikit-learn, FastAPI, Git, Data Analysis"
    )

    skills = [
        skill.strip().lower()
        for skill in skills_input.split(",")
        if skill.strip()
    ]

    if st.button(
        "🚀 Screen Resumes",
        use_container_width=True
    ):

        candidates = (
            [
                {
                    "name": file.name,
                    "text": read_file(file)
                }
                for file in resume_files
            ]
            if resume_files
            else
            [
                {
                    "name": name,
                    "text": text
                }
                for name, text
                in SAMPLE_RESUMES.items()
            ]
        )

        results = []

        for candidate in candidates:

            score, matched, kmp, rk = score_resume(
                candidate["text"],
                jd_text,
                skills
            )

            results.append({
                "name": candidate["name"],
                "score": score,
                "matched": matched,
                "kmp": kmp,
                "rk": rk
            })

        st.session_state["ranked"] = merge_sort(
            results
        )

    ranked = st.session_state.get(
        "ranked",
        []
    )

    if ranked:

        st.divider()

        st.subheader("🏆 Ranked Candidates")

        for i, candidate in enumerate(
            ranked,
            1
        ):

            if i == 1:
                card_class = "rank1"

            elif i == 2:
                card_class = "rank2"

            elif i == 3:
                card_class = "rank3"

            else:
                card_class = "rankother"

            st.markdown(
                f"""
                <div class="candidate-card {card_class}">
                    <h3>#{i} &nbsp; {candidate['name']}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            a, b, d = st.columns([1, 5, 2])

            with a:
                st.markdown(f"## #{i}")

            with b:

                st.markdown(
                    f"### {candidate['name']}"
                )

                st.write(
                    "Matched skills: "
                    +
                    (
                        ", ".join(
                            candidate["matched"]
                        )
                        if candidate["matched"]
                        else "None"
                    )
                )

            with d:

                st.metric(
                    "Match Score",
                    f"{candidate['score']}%"
                )

            st.progress(
                int(candidate["score"])
            )

            with st.expander(
                "View DSA analysis"
            ):

                st.write(
                    "**KMP — Skill Searching:** "
                    +
                    (
                        ", ".join(candidate["kmp"])
                        if candidate["kmp"]
                        else "None"
                    )
                )

                st.write(
                    "**Rabin-Karp — Hash-Based Searching:** "
                    +
                    (
                        ", ".join(candidate["rk"])
                        if candidate["rk"]
                        else "None"
                    )
                )

                st.write(
                    "**Dynamic Programming — Similarity:** "
                    "LCS-based text similarity contributes to the score."
                )

                st.write(
                    "**Merge Sort — Ranking:** "
                    "Orders candidates from highest to lowest score."
                )

        heap = [
            (-candidate["score"], candidate["name"])
            for candidate in ranked
        ]

        heapq.heapify(heap)

        st.success(
            "Priority Queue — Top Candidate: "
            + heap[0][1]
        )


# ============================================================
# DSA INSIGHTS
# ============================================================

elif page == "DSA Insights":

    st.title("🧠 DSA Algorithm Insights")

    st.markdown(
        """
        <div class="dsa-intro">

        <b>How DSA is used in ResumeRank AI:</b>
        KMP + Rabin-Karp search skills →
        Hash Table provides lookup →
        Dynamic Programming calculates similarity →
        Merge Sort ranks candidates →
        Priority Queue selects top candidates.

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # FIRST ROW
    # ========================================================

    col1, col2, col3 = st.columns(3)


    # ================= KMP =================

    with col1:

        st.markdown(
            """
            <div class="dsa-card">

                <div class="dsa-title">
                    🔎 KMP (Knuth-Morris-Pratt)
                </div>

                <div class="dsa-purpose">
                    PURPOSE: SKILL SEARCHING
                </div>

                <div class="dsa-description">
                    <b>What it does:</b>
                    Searches required skills inside resume text.
                </div>

                <div class="dsa-example">
                    <b>Example:</b>
                    Finds Python, SQL and Machine Learning.
                </div>

                <div class="code-label">
                    CODE — KMP
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            """def kmp_search(text, pattern):
    lps = [0] * len(pattern)
    # Build LPS and search
    return True""",
            language="python"
        )


    # ================= RABIN KARP =================

    with col2:

        st.markdown(
            """
            <div class="dsa-card">

                <div class="dsa-title">
                    🔐 Rabin-Karp
                </div>

                <div class="dsa-purpose">
                    PURPOSE: HASH-BASED SEARCHING
                </div>

                <div class="dsa-description">
                    <b>What it does:</b>
                    Searches keywords using hashing.
                </div>

                <div class="dsa-example">
                    <b>Example:</b>
                    Finds required skills in resume text.
                </div>

                <div class="code-label">
                    CODE — RABIN-KARP
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            """def rabin_karp_search(text, pattern):
    base, mod = 256, 101
    # Calculate rolling hash
    return True""",
            language="python"
        )


    # ================= DYNAMIC PROGRAMMING =================

    with col3:

        st.markdown(
            """
            <div class="dsa-card">

                <div class="dsa-title">
                    🧩 Dynamic Programming (LCS)
                </div>

                <div class="dsa-purpose">
                    PURPOSE: RESUME-JD SIMILARITY
                </div>

                <div class="dsa-description">
                    <b>What it does:</b>
                    Compares resume and Job Description text.
                </div>

                <div class="dsa-example">
                    <b>Example:</b>
                    Common text contributes to matching score.
                </div>

                <div class="code-label">
                    CODE — DYNAMIC PROGRAMMING
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            """def lcs_length(a, b):
    dp = [0] * (len(b) + 1)
    # Build LCS DP table
    return dp[-1]""",
            language="python"
        )


    # ========================================================
    # SECOND ROW
    # ========================================================

    col4, col5, col6 = st.columns(3)


    # ================= MERGE SORT =================

    with col4:

        st.markdown(
            """
            <div class="dsa-card">

                <div class="dsa-title">
                    🔀 Merge Sort
                </div>

                <div class="dsa-purpose">
                    PURPOSE: CANDIDATE RANKING
                </div>

                <div class="dsa-description">
                    <b>What it does:</b>
                    Sorts candidates by matching score.
                </div>

                <div class="dsa-example">
                    <b>Example:</b>
                    92% → 85% → 76% → 64%
                </div>

                <div class="code-label">
                    CODE — MERGE SORT
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            """def merge_sort(items):
    if len(items) <= 1:
        return items
    # Divide and merge
    return sorted_items""",
            language="python"
        )


    # ================= HASH TABLE =================

    with col5:

        st.markdown(
            """
            <div class="dsa-card">

                <div class="dsa-title">
                    🗂️ Hash Table
                </div>

                <div class="dsa-purpose">
                    PURPOSE: FAST SKILL LOOKUP
                </div>

                <div class="dsa-description">
                    <b>What it does:</b>
                    Stores skills for quick lookup.
                </div>

                <div class="dsa-example">
                    <b>Example:</b>
                    Quickly checks whether a skill exists.
                </div>

                <div class="code-label">
                    CODE — HASH TABLE
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            """skill_table = {}

for skill in skills:
    skill_table[skill] = True

# Fast lookup
if "python" in skill_table:
    print("Found")""",
            language="python"
        )


    # ================= PRIORITY QUEUE =================

    with col6:

        st.markdown(
            """
            <div class="dsa-card">

                <div class="dsa-title">
                    🏆 Priority Queue
                </div>

                <div class="dsa-purpose">
                    PURPOSE: TOP CANDIDATE SELECTION
                </div>

                <div class="dsa-description">
                    <b>What it does:</b>
                    Retrieves the highest-scoring candidates.
                </div>

                <div class="dsa-example">
                    <b>Example:</b>
                    Gets the highest matching candidate quickly.
                </div>

                <div class="code-label">
                    CODE — PRIORITY QUEUE
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.code(
            """import heapq

heap = []
heapq.heappush(
    heap, (-score, candidate)
)

# Get top candidate""",
            language="python"
        )


    # ========================================================
    # COMPLETE PROCESS
    # ========================================================

    st.divider()

    st.subheader(
        "🔄 Complete DSA Process in ResumeRank AI"
    )

    p1, p2, p3, p4, p5 = st.columns(5)


    with p1:

        st.markdown(
            """
            <div class="process-box">

                <div class="process-title">
                    1. 🔎 Search
                </div>

                <div class="process-text">
                    <b>KMP + Rabin-Karp</b><br><br>
                    Find required skills and keywords.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p2:

        st.markdown(
            """
            <div class="process-box">

                <div class="process-title">
                    2. 🗂️ Lookup
                </div>

                <div class="process-text">
                    <b>Hash Table</b><br><br>
                    Quickly check required skills.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p3:

        st.markdown(
            """
            <div class="process-box">

                <div class="process-title">
                    3. 🧩 Compare
                </div>

                <div class="process-text">
                    <b>Dynamic Programming</b><br><br>
                    Calculate resume-JD similarity.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p4:

        st.markdown(
            """
            <div class="process-box">

                <div class="process-title">
                    4. 🔀 Rank
                </div>

                <div class="process-text">
                    <b>Merge Sort</b><br><br>
                    Order candidates by score.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p5:

        st.markdown(
            """
            <div class="process-box">

                <div class="process-title">
                    5. 🏆 Select
                </div>

                <div class="process-text">
                    <b>Priority Queue</b><br><br>
                    Retrieve top candidates.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ABOUT PROJECT
# ============================================================

elif page == "About Project":

    st.title("📌 About the Project")

    st.write(
        "The system automates resume screening by extracting "
        "information, comparing resumes with a job description, "
        "calculating a matching score and ranking candidates."
    )

    st.subheader("Objectives")

    objectives = [
        "Automatically screen resumes",
        "Extract skills, education, experience and certifications",
        "Compare resumes with job description",
        "Calculate matching score",
        "Rank candidates",
        "Reduce manual screening effort"
    ]

    for objective in objectives:

        st.write("• " + objective)

    st.subheader("Technology Stack")

    st.write(
        "Python • Streamlit • Pandas • "
        "Scikit-learn • SQLite/MySQL"
    )

    st.info(
        "Review-2 demo: Upload JD → upload 2–3 resumes → "
        "Screen Resumes → explain scores → open DSA Insights."
    )