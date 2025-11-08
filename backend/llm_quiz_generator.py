from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


def generate_quiz_from_content(content: str, num_questions: int = 10) -> Dict[str, Any]:
    """
    Generate quiz questions and summary from article content using Gemini.
    
    Args:
        content: The scraped article content
        num_questions: Number of questions to generate (5-10)
        
    Returns:
        Dictionary with 'summary' and 'questions' keys
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    # Initialize Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7,
        max_output_tokens=4096
    )
    
    # Create prompt template
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """You are an expert quiz generator. Your task is to create educational multiple-choice questions based on the provided article content.

Instructions:
1. Generate exactly {num_questions} multiple-choice questions
2. Each question should have 4 options (A, B, C, D)
3. Only one option should be correct
4. Make questions clear, relevant, and test understanding of key concepts
5. Include a brief explanation for each question
6. Write a concise summary of the article (2-3 sentences)
7. Return the response as valid JSON only, no markdown formatting

Output format (JSON):
{{
    "summary": "Brief summary of the article",
    "questions": [
        {{
            "question": "Question text?",
            "options": [
                {{"text": "Option A", "is_correct": true}},
                {{"text": "Option B", "is_correct": false}},
                {{"text": "Option C", "is_correct": false}},
                {{"text": "Option D", "is_correct": false}}
            ],
            "explanation": "Brief explanation of the correct answer"
        }}
    ]
}}"""),
        ("human", "Article content:\n\n{content}\n\nGenerate a quiz based on this content.")
    ])
    
    # Format prompt
    formatted_prompt = prompt_template.format_messages(
        num_questions=num_questions,
        content=content[:8000]  # Limit content to avoid token limits
    )
    
    # Generate response
    try:
        response = llm.invoke(formatted_prompt)
        response_text = response.content
        
        # Try to extract JSON from response (handle markdown code blocks if present)
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        quiz_data = json.loads(response_text)
        
        # Validate structure
        if "summary" not in quiz_data or "questions" not in quiz_data:
            raise ValueError("Invalid quiz structure returned from LLM")
        
        # Validate questions
        if not isinstance(quiz_data["questions"], list):
            raise ValueError("Questions must be a list")
        
        if len(quiz_data["questions"]) < 5 or len(quiz_data["questions"]) > 10:
            raise ValueError(f"Expected 5-10 questions, got {len(quiz_data['questions'])}")
        
        # Validate each question
        for i, q in enumerate(quiz_data["questions"]):
            if "question" not in q or "options" not in q:
                raise ValueError(f"Question {i+1} missing required fields")
            if not isinstance(q["options"], list) or len(q["options"]) != 4:
                raise ValueError(f"Question {i+1} must have exactly 4 options")
            
            correct_count = sum(1 for opt in q["options"] if opt.get("is_correct", False))
            if correct_count != 1:
                raise ValueError(f"Question {i+1} must have exactly one correct answer")
        
        return quiz_data
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error generating quiz: {str(e)}")

