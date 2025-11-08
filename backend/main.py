from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from contextlib import asynccontextmanager
import sys
from pathlib import Path

# Add backend directory to path
sys.path.append(str(Path(__file__).parent))

from database import get_db, init_db
from models import Quiz, QuizResponse, QuizListResponse, QuizCreate, QuizGenerateRequest
from scraper import scrape_wikipedia_article
from llm_quiz_generator import generate_quiz_from_content


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    init_db()
    yield
    # Shutdown (if needed in the future)


app = FastAPI(
    title="AI Wiki Quiz Generator API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://quiz-ai-generator.vercel.app"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "AI Wiki Quiz Generator API"}


@app.post("/generate_quiz", response_model=QuizResponse)
async def generate_quiz(
    request: QuizGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a quiz from a Wikipedia article URL.
    
    Args:
        request: Request body with URL
        db: Database session
        
    Returns:
        Generated quiz data
    """
    try:
        url = request.url
        # Validate URL is Wikipedia
        if "wikipedia.org" not in url.lower():
            raise HTTPException(status_code=400, detail="URL must be a Wikipedia article")
        
        # Scrape article
        try:
            title, content = scrape_wikipedia_article(url)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error scraping article: {str(e)}")
        
        # Generate quiz
        try:
            quiz_data = generate_quiz_from_content(content, num_questions=7)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")
        
        # Save to database
        quiz_record = Quiz(
            url=url,
            title=title,
            scraped_content=content[:5000],  # Store first 5000 chars
            full_quiz_data=quiz_data
        )
        
        db.add(quiz_record)
        db.commit()
        db.refresh(quiz_record)
        
        return QuizResponse.model_validate(quiz_record)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/history", response_model=List[QuizListResponse])
async def get_history(db: Session = Depends(get_db)):
    """
    Get list of all generated quizzes.
    
    Returns:
        List of quiz summaries
    """
    quizzes = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
    return [QuizListResponse.model_validate(q) for q in quizzes]


@app.get("/quiz/{quiz_id}", response_model=QuizResponse)
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get full quiz data by ID.
    
    Args:
        quiz_id: Quiz ID
        db: Database session
        
    Returns:
        Full quiz data
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return QuizResponse.model_validate(quiz)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

