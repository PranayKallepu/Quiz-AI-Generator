# AI Wiki Quiz Generator

A full-stack web application that generates quizzes from Wikipedia articles using AI (Google Gemini). Built with FastAPI (Python) backend and React + Tailwind CSS frontend.

## 🎯 Features

- **Wikipedia Article Scraping**: Extract content from any Wikipedia article URL
- **AI-Powered Quiz Generation**: Uses Google Gemini via LangChain to generate 5-10 multiple-choice questions
- **Article Summaries**: Automatically generates concise summaries of articles
- **Quiz History**: View and access all previously generated quizzes
- **Interactive Quiz Interface**: Take quizzes with immediate feedback and explanations
- **Modern UI**: Clean, responsive design built with React and Tailwind CSS

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **LangChain**: Framework for working with LLMs
- **Google Gemini**: AI model for quiz generation
- **BeautifulSoup4**: Web scraping library
- **PostgreSQL/MySQL**: Database for storing quiz data

### Frontend
- **React**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js 16+ and npm
- PostgreSQL or MySQL database
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd quiz-ai
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
# For PostgreSQL:
DATABASE_URL=postgresql://username:password@localhost:5432/quiz_db

# For MySQL:
# DATABASE_URL=mysql+pymysql://username:password@localhost:3306/quiz_db
```

#### Create Database

**PostgreSQL:**
```bash
createdb quiz_db
```

**MySQL:**
```sql
CREATE DATABASE quiz_db;
```

#### Run the Backend Server

```bash
# From the backend directory
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Run the Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📁 Project Structure

```
quiz-ai/
├── backend/
│   ├── main.py                 # FastAPI application and endpoints
│   ├── database.py             # Database connection and session management
│   ├── models.py               # SQLAlchemy models and Pydantic schemas
│   ├── scraper.py              # Wikipedia article scraping logic
│   ├── llm_quiz_generator.py   # LangChain + Gemini quiz generation
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables (create from .env.example)
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable React components
│   │   │   ├── Modal.jsx       # Modal component for quiz details
│   │   │   └── QuizDisplay.jsx # Component for displaying quizzes
│   │   ├── tabs/               # Tab components
│   │   │   ├── GenerateQuizTab.jsx  # Quiz generation interface
│   │   │   └── HistoryTab.jsx       # Quiz history view
│   │   ├── services/
│   │   │   └── api.js          # API service layer
│   │   ├── App.jsx             # Main app component
│   │   ├── main.jsx            # React entry point
│   │   └── index.css           # Global styles with Tailwind
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

## 🔌 API Endpoints

### POST `/generate_quiz`
Generate a quiz from a Wikipedia article URL.

**Request Body:**
```json
{
  "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
}
```

**Response:**
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
  "title": "Artificial Intelligence",
  "date_generated": "2024-01-15T10:30:00",
  "full_quiz_data": {
    "summary": "...",
    "questions": [...]
  }
}
```

### GET `/history`
Get a list of all generated quizzes.

**Response:**
```json
[
  {
    "id": 1,
    "url": "...",
    "title": "...",
    "date_generated": "..."
  }
]
```

### GET `/quiz/{quiz_id}`
Get full quiz data by ID.

**Response:**
```json
{
  "id": 1,
  "url": "...",
  "title": "...",
  "date_generated": "...",
  "full_quiz_data": {...}
}
```

## 🎮 Usage

1. **Start the Backend**: Make sure your database is running and the backend server is started
2. **Start the Frontend**: Run `npm run dev` in the frontend directory
3. **Generate a Quiz**:
   - Navigate to the "Generate Quiz" tab
   - Enter a Wikipedia article URL (e.g., `https://en.wikipedia.org/wiki/Python_(programming_language)`)
   - Click "Generate Quiz"
   - Wait for the AI to process the article and generate questions
4. **View History**: Click the "History" tab to see all previously generated quizzes
5. **Take a Quiz**: Click on questions to select answers, then click "Show Results" to see your score

## 🐛 Troubleshooting

### Backend Issues

- **Database Connection Error**: Make sure your database is running and the `DATABASE_URL` in `.env` is correct
- **Gemini API Error**: Verify your `GEMINI_API_KEY` is set correctly in `.env`
- **Import Errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`

### Frontend Issues

- **API Connection Error**: Ensure the backend is running on `http://localhost:8000`
- **CORS Errors**: The backend CORS middleware should allow requests from `http://localhost:5173`
- **Build Errors**: Try deleting `node_modules` and reinstalling: `rm -rf node_modules && npm install`

## 📝 Notes

- The application requires an internet connection to scrape Wikipedia articles
- Quiz generation may take 10-30 seconds depending on article length and API response time
- Generated quizzes are stored in the database and persist across sessions
- The scraper extracts main content paragraphs and removes citations/references

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

