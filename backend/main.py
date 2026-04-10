from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List

try:
    from parser import extract_profile
    from ranking import rank_candidates
    from auth import create_user_table, register_user, login_user
except ImportError:
    from parser import extract_profile
    from ranking import rank_candidates
    from auth import create_user_table, register_user, login_user

app = FastAPI()

# ✅ Create user table at startup
create_user_table()

# ✅ CORS (Frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 In-memory DB for candidates
candidates_db = []

# =========================
# 🔐 AUTH APIs
# =========================

@app.post("/register")
def register(user: dict):
    if user.get("password") != user.get("confirm_password"):
        return {"success": False, "error": "Passwords do not match"}

    sanitized_user = {
        "name": user.get("name", "").strip(),
        "email": user.get("email", "").strip().lower(),
        "password": user.get("password", ""),
        "company": user.get("company", "").strip(),
        "role": user.get("role", "").strip(),
    }

    success = register_user(sanitized_user)
    return {"success": success}


@app.post("/login")
def login(user: dict):
    email = user.get("email", "").strip().lower()
    password = user.get("password", "")
    success = login_user(email, password)
    return {"success": success}


# =========================
# 📄 RESUME UPLOAD
# =========================

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    print(f"📄 Received {len(files)} files for upload")

    candidates_db.clear()

    for f in files:
        print(f"📄 Processing file: {f.filename}, size: {f.size} bytes")

        # 🔥 Ensure file pointer is reset
        f.file.seek(0)

        profile = extract_profile(f)

        # 🔥 DEBUG RESUME TEXT
        print("\n" + "="*50)
        print("DEBUG RESUME OUTPUT")
        print("="*50)

        if "raw_text" in profile:
            print("RESUME TEXT SAMPLE:\n", profile["raw_text"][:500])
            print("Length:", len(profile["raw_text"]))
        else:
            print("⚠️ No raw_text found in profile")

        print("="*50)

        profile["name"] = f.filename
        candidates_db.append(profile)

    print(f"✅ Successfully uploaded {len(files)} resumes")
    return {"message": f"{len(files)} resumes uploaded", "count": len(files)}


# =========================
# 📊 RANKING
# =========================

@app.post("/rank")
def rank(jd: dict):

    # ✅ FIX: return empty list instead of error object
    if not candidates_db:
        return []

    # 🔥 DEBUG JD TEXT
    print("\n" + "="*50)
    print("DEBUG JD OUTPUT")
    print("="*50)

    print("JD TEXT:\n", jd)
    print("="*50)

    results = rank_candidates(jd, candidates_db)
    return results