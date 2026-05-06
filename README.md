# FastAPI-Patient-CRUD
A FastAPI-based REST API for managing patient records, featuring CRUD operations, data validation, and computed health metrics like BMI and health verdict. Includes support for partial updates and sorting, built as a hands-on backend learning project.

# Patient Management API (FastAPI)

A REST API built with FastAPI to manage patient records. This project demonstrates CRUD operations, input validation using Pydantic, computed health metrics (BMI and health status), and query-based sorting.

## 🚀 Features

- Create, read, update, and delete patient records
- Data validation using Pydantic models
- Computed fields:
  - BMI (Body Mass Index)
  - Health verdict (Underweight, Normal, Overweight)
- Partial updates using PATCH-like behavior with PUT
- Query-based sorting (height, weight, BMI)
- Simple JSON-based data storage

---

## ⚙️ Installation & Setup
```bash
git clone https://github.com/your-username/fastapi-patient-api.git
cd fastapi-patient-api

Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

Install dependencies
pip install fastapi uvicorn

Run the server
uvicorn main:app --reload

Open in browser
API: http://127.0.0.1:8000
Interactive docs (Swagger UI): http://127.0.0.1:8000/docs

API Endpoints
🔹 Basic Routes
Method	Endpoint	Description
GET	/	Welcome message
GET	/about	About the API
GET	/view	View all patients
🔹 Patient Operations
Method	Endpoint	Description
GET	/patient/{patient_id}	Get patient by ID
POST	/create	Create a new patient
PUT	/edit/{patient_id}	Update patient (partial update)
DELETE	/delete/{patient_id}	Delete patient
🔹 Query-Based Features
Method	Endpoint	Description
GET	/sort	Sort patients by height, weight, BMI
Example:
/sort?sort_by=weight&order=desc
🧾 Example Request Body
Create Patient
{
  "id": "P001",
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "male",
  "height": 1.75,
  "weight": 70
}
🧠 Computed Fields
BMI = weight / (height²)
Verdict:
< 18.5 → Underweight
18.5 – 24.9 → Normal
≥ 25 → Overweight
