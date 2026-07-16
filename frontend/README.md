# Student Form Application

A full-stack web application for collecting student presentation topic suggestions. Built with React (frontend) and Flask (backend) with file-based data storage.

## 🚀 Features

- Modern, responsive student form with validation
- Real-time form submission to Flask backend
- File-based data storage (JSON)
- Only stores the latest submission (overwrites previous)
- Clean, professional UI with animations

## 📁 Project Structure

```
frontend_ppt/
├── student-form-app/     # React frontend (Vite + React)
│   ├── src/
│   │   ├── App.jsx       # Main form component
│   │   ├── App.css       # Styling
│   │   └── ...
│   └── package.json
│
└── backend/              # Flask backend
    ├── app.py            # Flask API server
    ├── requirements.txt  # Python dependencies
    └── students_data.json # Data storage (auto-generated)
```

## 🛠️ Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- npm or yarn

### Frontend Setup

```bash
cd student-form-app
npm install
npm run dev
```

Frontend will run on: `http://localhost:5173`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend API will run on: `http://localhost:3000`

## 🎯 Usage

1. Start both frontend and backend servers
2. Open `http://localhost:5173` in your browser
3. Fill out the student form with:
   - Presentation Topic
   - Student Name
   - Degree (UG/PG)
   - Year
   - Department
   - Content Suggestions
4. Submit the form
5. Data is saved to `backend/students_data.json`

**Note:** Each new submission replaces the previous one. Only the latest submission is stored.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/submit-student` | Submit student form data |
| GET | `/api/students` | Retrieve stored submissions |

## 🔧 Technologies Used

**Frontend:**
- React 18
- Vite
- CSS3 (with animations)

**Backend:**
- Python Flask
- Flask-CORS
- JSON file storage

## 📝 Data Storage

Data is stored in `students_data.json` with the following structure:

```json
[
  {
    "id": 1234567890,
    "timestamp": "07/16/2026, 04:46:29 PM",
    "topic": "Machine Learning Basics",
    "name": "John Doe",
    "degree": "UG",
    "year": "3",
    "department": "Computer Science",
    "contentSuggestion": "Include practical examples..."
  }
]
```

## 🤝 Contributing

Feel free to fork this project and submit pull requests!

## 📄 License

MIT License - feel free to use this project for learning or production.
