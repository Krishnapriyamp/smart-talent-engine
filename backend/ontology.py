# ontology.py
import re
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    SENTENCE_TRANSFORMERS_AVAILABLE = True
    SKLEARN_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SKLEARN_AVAILABLE = False

# Model will be loaded lazily
model = None

SKILL_ONTOLOGY = {
    "python": ["python", "python programming", "python development"],
    "java": ["java", "java programming", "java development"],
    "sql": ["sql", "mysql", "postgres", "sqlite", "tsql", "pl/sql", "database"],
    "data science": ["data science", "data scientist", "data analysis", "data analytics"],
    "machine learning": ["machine learning", "ml", "artificial intelligence", "ai"],
    "deep learning": ["deep learning", "neural network", "cnn", "rnn", "lstm", "transformer"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch", "torch"],
    "keras": ["keras"],
    "data analysis": ["data analysis", "data analytics", "analytics", "excel", "spreadsheets"],
    "pandas": ["pandas", "data manipulation"],
    "numpy": ["numpy", "numerical computing"],
    "visualization": ["tableau", "power bi", "matplotlib", "seaborn", "plotly", "dash", "data visualization"],
    "nlp": ["nlp", "natural language processing", "text processing", "spacy", "nltk", "bert"],
    "big data": ["spark", "hadoop", "hive", "pyspark", "kafka", "big data"],
    "cloud": ["aws", "azure", "gcp", "google cloud", "cloud computing"],
    "statistics": ["statistics", "statistical", "probability", "hypothesis testing"],
    "r": ["r language", "r studio", "r programming"],
    "sql server": ["sql server"],
    "scikit-learn": ["scikit-learn", "sklearn", "machine learning algorithms"],
    "software engineering": ["software engineering", "software engineer", "backend", "frontend", "full stack", "devops"],
    "javascript": ["javascript", "js", "node.js", "nodejs", "react", "vue", "angular"],
    "html": ["html", "css", "web development"],
    "git": ["git", "version control", "github"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "api": ["api", "rest", "restful", "graphql"],
    "testing": ["testing", "unit testing", "pytest", "jest", "selenium"]
}

def semantic_skill_extraction(text, threshold=0.4):  # Lowered threshold
    """
    Extract skills using semantic similarity with sentence-transformers.
    """
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        return []

    # Lazy load the model
    global model
    if model is None:
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
        except:
            return []

    # Master skill list
    master_skills = list(SKILL_ONTOLOGY.keys())

    # Split text into sentences/chunks for better matching
    sentences = re.split(r'[.!?]+', text.lower())
    sentences = [s.strip() for s in sentences if s.strip()]

    # Also try the whole text as one chunk
    sentences.append(text.lower().strip())

    found_skills = set()

    try:
        # Encode master skills
        skill_embeddings = model.encode(master_skills)

        # Check each sentence against all skills
        for sentence in sentences:
            if len(sentence) < 5:  # More lenient length check
                continue

            sentence_embedding = model.encode([sentence])
            similarities = cosine_similarity(sentence_embedding, skill_embeddings)[0]

            # Find skills above threshold
            for i, similarity in enumerate(similarities):
                if similarity > threshold:
                    found_skills.add(master_skills[i])

    except Exception as e:
        print(f"Semantic extraction error: {e}")
        return []

    return list(found_skills)

def normalize_skills(text):
    """
    Extract skills using both keyword matching and semantic similarity.
    """
    # Convert text to lowercase
    text = text.lower()

    found_skills = set()

    # 1. Keyword matching (existing logic)
    skills_db = [
        "python", "java", "c++", "c", "c#", "sql",
        "machine learning", "deep learning",
        "data analysis", "pandas", "numpy",
        "tensorflow", "pytorch",
        "fastapi", "django", "react", "node.js", "node js",
        "mysql", "mongodb", "javascript", "html", "css",
        "git", "docker", "kubernetes", "aws", "azure", "gcp"
    ]

    for skill in skills_db:
        if skill == "c":
            if re.search(r"\bc\b", text):
                found_skills.add(skill)
        elif skill in text:
            found_skills.add(skill)

    # 2. Semantic matching (new) - only if available
    if SENTENCE_TRANSFORMERS_AVAILABLE:
        semantic_skills = semantic_skill_extraction(text)
        found_skills.update(semantic_skills)

    # Remove duplicates and return sorted list
    return sorted(list(found_skills))