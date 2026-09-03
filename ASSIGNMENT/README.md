# AI-Based Intelligent Campus Helpdesk and Facility Fault-Diagnosis Assistant

Academic Artificial Intelligence Assignment Project implementing Knowledge-Based Reasoning, Machine Learning (Decision Tree & MLP Neural Network), Tabular Q-Learning Reinforcement Learning, PySpark Local Analytics, Stateful Chatbot Agent, and a React Dashboard.

---

## 🚀 1. EXECUTIVE SUMMARY & ARCHITECTURE

The **AI-Based Intelligent Campus Helpdesk** automates facility problem management (Air Conditioners, Projectors, Wi-Fi, Lab Equipment, Lighting, Classroom Infrastructure) across campus departments.

### End-to-End Pipeline:
`REPORT → UNDERSTAND → DIAGNOSE → CLASSIFY → PREDICT RISK → ROUTE → TRACK → RESOLVE/ESCALATE → LEARN`

1. **Knowledge Reasoning Engine (`backend/reasoning/`)**:
   - Production Rules R1–R12 with Priority matching.
   - **Forward Chaining**: Fact matching & proof trace derivation.
   - **Backward Chaining**: Targeted clarifying question generation for missing symptoms.
   - **CNF & Propositional Resolution**: Clause transformation `(~A1 v ~A2 v ... v C)` & resolution refutation steps.
   - **Consistency & Safety**: Contradiction detection and circular dependency loop protection.
   - **Diagnosis Caching**: MD5 symptom hash cache for instant re-queries.

2. **Machine Learning (`backend/learning/`)**:
   - **Decision Tree (`DecisionTreeClassifier(criterion='gini', max_depth=6)`)**: Predicts fault category and SLA priority. Exposes confusion matrix & feature importances.
   - **Escalation Neural Network (`MLPClassifier` + `SimpleImputer` + `StandardScaler`)**: Predicts ticket escalation risk with missing value imputation.

3. **Tabular Q-Learning Routing Agent (`backend/routing/`)**:
   - State: `(fault_category, priority, workload_bucket)`.
   - Action: Assign ticket to maintenance staff.
   - Reward: `- (resolution_time + 1.5 * workload_imbalance_std)` + skill match bonus.
   - Trained over 500 episodes with epsilon decay. Evaluated against Random & Round-Robin baselines.

4. **PySpark Local Analytics (`backend/analytics/spark_jobs.py`)**:
   - Local mode PySpark RDD/DataFrame aggregations computing category distribution, department totals, escalation rates, and mean resolution time.

---

## 🛠️ 2. REQUIRED TECH STACK

- **Backend**: Python 3.10+, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic, PyJWT.
- **AI/ML**: scikit-learn, NumPy, Pandas.
- **Reinforcement Learning**: Custom Tabular Q-Learning implementation.
- **Analytics**: PySpark (local mode).
- **Frontend**: React 18, Vite, Modern Responsive Dashboard CSS.
- **Testing**: pytest (12/12 test cases passing).

---

## 📁 3. PROJECT FOLDER STRUCTURE

```
campus-helpdesk-ai/
├── backend/
│   ├── app.py                     # FastAPI Application routes
│   ├── config.py                  # Environment config
│   ├── database.py                # SQLAlchemy DB setup
│   ├── models.py                  # User, Ticket, Rule, RoutingHistory, Notification, OverrideLog
│   ├── schemas.py                 # Pydantic schemas
│   ├── auth.py                    # JWT & Password hashing
│   ├── reasoning/                 # KB, Forward/Backward chaining, CNF & Resolution
│   ├── learning/                  # Dataset generator, Preprocessing, Decision Tree, MLP
│   ├── routing/                   # Q-Learning Agent & Environment
│   ├── agent/                     # Chatbot Intent Classifier, Entity Extractor, Dialogue Manager
│   ├── analytics/                 # PySpark local analytics jobs
│   ├── notifications/             # Notification service
│   ├── services/                  # Diagnosis, Classification, Escalation, Routing, Ticket services
│   ├── models_artifacts/          # decision_tree.pkl, escalation_model.pkl, q_table.pkl
│   ├── data/                      # historical_tickets.csv
│   ├── scripts/                   # Data generation, Seeding, Training, Spark scripts
│   └── tests/                     # Test suite (TC01 - TC12)
├── frontend/
│   ├── src/                       # React components, pages, services, layouts
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── requirements.txt
└── README.md
```

---

## ⚙️ 4. INSTALLATION & SETUP INSTRUCTIONS (WINDOWS)

### Step 1: Clone / Navigate to Workspace
```powershell
cd C:\Users\palla\.gemini\antigravity-ide\scratch\campus-helpdesk-ai
```

### Step 2: Virtual Environment & Dependencies
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Run Data Generation, Database Seed & Training Scripts
```powershell
python -m backend.scripts.generate_data
python -m backend.scripts.seed_database
python -m backend.scripts.train_models
python -m backend.scripts.train_rl
python -m backend.scripts.run_spark
```

### Step 4: Run Automated Test Suite (All 12 Test Cases)
```powershell
python -m pytest backend/tests -v
```

---

## 🏃 5. RUNNING THE APPLICATION

### Start Backend API Server (Port 8000)
```powershell
python -m uvicorn backend.app:app --reload --port 8000
```
Swagger UI available at: `http://localhost:8000/docs`

### Start Frontend React Application (Port 5173)
In a new terminal window:
```powershell
cd frontend
npm install
npm run dev
```
Open Browser at: `http://localhost:5173`

---

## 🔑 6. DEMO LOGIN CREDENTIALS

| Role | Email | Password | Access / Capabilities |
| :--- | :--- | :--- | :--- |
| **Student** | `student@campus.edu` | `student123` | Report faults, Chat with AI Assistant, Track own tickets, View proof traces |
| **Staff (Arun)** | `staff1@campus.edu` | `staff123` | View assigned tickets queue, Start work, Add resolution notes, Escalate |
| **Staff (Priya)** | `staff2@campus.edu` | `staff123` | View ECE network tickets, Update resolution |
| **Admin** | `admin@campus.edu` | `admin123` | System stats, Knowledge Base CRUD, AI Decision Override, PySpark Analytics, Audit logs |

---

## 🧪 7. ASSIGNMENT TEST CASES VALIDATION (TC01 - TC12)

All 12 required test cases pass with 100% success in `pytest`:

| Test Case | Description | Verification Method | Status |
| :--- | :--- | :--- | :--- |
| **TC01** | Valid AC report -> Power supply failure | Forward Chaining matched R1 rule | **PASSED** |
| **TC02** | Insufficient symptoms -> Clarification question | Backward Chaining missing facts extraction | **PASSED** |
| **TC03** | Contradictory rules -> Inconsistency flag | `detect_contradictions()` | **PASSED** |
| **TC04** | Historical ticket -> Decision Tree prediction | `TicketDecisionTreeModel.predict()` | **PASSED** |
| **TC05** | Missing values -> Escalation model predicts | `SimpleImputer` pipeline handling NaNs | **PASSED** |
| **TC06** | High escalation risk -> Priority handling | High-risk marked CRITICAL | **PASSED** |
| **TC07** | Q-learning -> Improvement over random | Q-policy reward vs Random policy reward | **PASSED** |
| **TC08** | Normal user attempts Admin page -> HTTP 403 | JWT Role-based dependency check | **PASSED** |
| **TC09** | Duplicate / incomplete report -> Rejected | `HTTPException(409 / 422)` | **PASSED** |
| **TC10** | Out-of-scope chatbot query -> Safe fallback | Intent classifier fallback reply | **PASSED** |
| **TC11** | Identical diagnosis twice -> Cached result | MD5 symptom hash cache | **PASSED** |
| **TC12** | Circular rules -> Safe termination | Visited rule set & iteration limit | **PASSED** |

---

## 📊 8. PYSPARK ANALYTICS SUMMARY

- **Engine**: PySpark Local DataFrame & RDD Engine
- **Total Tickets Analyzed**: 120
- **Most Frequent Fault**: `CLASSROOM_FAN` / `WIFI_NO_CONNECTIVITY`
- **Department Distribution**: ECE (36), Biotechnology (27), EEE (22), Mechanical (20), CSE (15)
- **Average Resolution Time**: 35.67 hours
