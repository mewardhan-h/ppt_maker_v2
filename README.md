# 🏥 GVMCH AI PPT Maker v2

**Automated Medical Presentation Generator** using AI-powered content generation

A full-stack application that generates professional medical PowerPoint presentations using NVIDIA LLM for content generation and formatting. Built for Government Villupuram Medical College and Hospital (GVMCH).

---

## 🌟 Features

- **AI-Powered Content Generation**: Uses NVIDIA's GLM-5.2 LLM to generate comprehensive medical content
- **Dual-Stage Pipeline**: 
  - Stage 1: Rich content generation tailored to student level
  - Stage 2: Strict formatting for PowerPoint conversion
- **Customizable Input**: Specify topic, degree (UG/PG), year, department, and content focus
- **Token Usage Tracking**: Real-time monitoring of LLM token consumption
- **Professional Branding**: Auto-includes GVMCH logos and institutional branding
- **Download Ready**: Generate and download PPT files directly from browser

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  (User Input Form)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Backend  │  (Orchestration)
└────────┬────────┘
         │
         ├─► Stage 1: NVIDIA LLM (Content Generation)
         │            ↓
         │        stage1_raw_content.txt
         │
         ├─► Stage 2: NVIDIA LLM (Formatting)
         │            ↓
         │        basic_text_converted.txt
         │
         └─► Stage 3: python-pptx (PPT Generation)
                      ↓
                  presentation.pptx
```

---

## 📁 Project Structure

```
ppt_maker/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── stage1.py                 # Content generation (NVIDIA LLM)
│   ├── stage2.py                 # Formatting (NVIDIA LLM)
│   ├── text_to_ppt.py            # PPT generation (python-pptx)
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # API keys (NOT in git)
│   └── assets/
│       ├── logo_left.jpg         # GVMCH left logo
│       └── logo_right.jpg        # GVMCH right logo
│
├── frontend/
│   └── student-form-app/         # React application
│       ├── src/
│       │   ├── App.jsx           # Main form component
│       │   └── App.css           # Styling
│       ├── package.json
│       └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.12+**
- **Node.js 18+**
- **NVIDIA API Key** (from [NVIDIA AI](https://build.nvidia.com/))

### 1️⃣ Backend Setup

```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies (choose one):
# Option 1: All dependencies with exact versions (recommended for production)
pip install -r requirements.txt

# Option 2: Minimal dependencies (pip auto-installs sub-dependencies)
pip install -r requirements-minimal.txt

# Create .env file
echo NVIDIA_API_KEY=your_api_key_here > .env

# Start Flask server
python app.py
```

Backend will run on: **http://localhost:3000**

### 2️⃣ Frontend Setup

```bash
cd frontend/student-form-app

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:5173**

---

## 🎯 Usage

1. **Open** `http://localhost:5173` in your browser
2. **Fill the form**:
   - Topic (e.g., "Soft Tissue Sarcoma")
   - Name
   - Degree (UG/PG)
   - Year of Study
   - Department
   - Content Suggestion (optional)
   - Number of Slides (5-30)
3. **Click** "Generate PPT"
4. **Wait** 30-60 seconds (LLM processing)
5. **Download** your presentation!

---

## 📊 Token Usage

The application tracks token consumption for cost monitoring:

```
💰 ESTIMATED TOKEN USAGE:
   Input tokens:  ~3,542
   Output tokens: ~8,120
   Total tokens:  ~11,662
```

**Estimation formula**: 1 token ≈ 4 characters

---

## 🎨 PPT Slide Structure

Every generated presentation follows this structure:

- **Slide 1**: Introduction & Overview (with branding)
- **Slides 2-N**: Content slides (3-6 bullets each)
- **Final Slide**: **Conclusion** (key takeaways)

### Branding Elements (All Slides):
- Logo Left: Top-left corner
- Logo Right: Top-right corner
- Title: Centered between logos

---

## 🔧 Configuration

### Backend APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/submit-student` | POST | Generate PPT from form data |
| `/api/students` | GET | View submission history |
| `/api/download-ppt` | GET | Download generated PPT |

### Environment Variables

```env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxx
```

---

## 📦 Dependencies

### Backend (Python)
- `Flask` - Web framework
- `flask-cors` - CORS handling
- `python-pptx` - PPT generation
- `openai` - NVIDIA LLM client
- `python-dotenv` - Environment variables

### Frontend (React)
- `react` - UI framework
- `vite` - Build tool

---

## 🐛 Troubleshooting

### "Cannot connect to backend"
- Ensure Flask server is running on port 3000
- Check `http://localhost:3000/api/students` in browser

### "NVIDIA_API_KEY not set"
- Create `.env` file in `backend/` folder
- Add your NVIDIA API key

### "Timeout error"
- LLM calls have 10-minute timeout
- Check internet connection
- Verify API key is valid

### "404 Model not found"
- Ensure `stage2.py` uses NVIDIA LLM (not Gemini)
- Model should be `z-ai/glm-5.2`

---

## 📝 Development Notes

### Stage 1: Content Generation
- **Model**: NVIDIA `z-ai/glm-5.2`
- **Temperature**: 1.0 (creative)
- **Max Tokens**: 16,384
- **Timeout**: 600s (10 minutes)

### Stage 2: Formatting
- **Model**: NVIDIA `z-ai/glm-5.2`
- **Temperature**: 0.3 (consistent)
- **Max Tokens**: 16,384
- **Timeout**: 600s (10 minutes)

### Stage 3: PPT Generation
- **Library**: python-pptx
- **Slide Size**: 13.33" × 7.5" (widescreen)
- **Font**: Calibri (24pt content, 44pt titles)

---

## 🔐 Security Notes

⚠️ **IMPORTANT**: 
- `.env` file contains API keys and is **NOT** committed to git
- Never share your NVIDIA API key publicly
- Review `.gitignore` before pushing

---

## 🛠️ Future Enhancements

- [ ] Add multiple LLM provider support
- [ ] Template selection (themes, layouts)
- [ ] Image/diagram generation
- [ ] Export to PDF
- [ ] User authentication
- [ ] Presentation history
- [ ] Custom branding upload

---

## 👨‍💻 Author

**Mewardhan**  
Government Villupuram Medical College and Hospital (GVMCH)

---

## 📄 License

This project is created for educational purposes at GVMCH.

---

## 🙏 Acknowledgments

- NVIDIA AI for LLM API
- Government Villupuram Medical College and Hospital
- Python-PPTX community

---

**Made with ❤️ for medical education**
