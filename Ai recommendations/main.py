import os
from fastapi import FastAPI, HTTPException, Response
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv
import io
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.units import inch

# Load environment variables from a .env file
load_dotenv()

# Configure the Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize FastAPI app
app = FastAPI()

# Define the input schema
class CandidateInput(BaseModel):
    batch: str
    mcq_scores: dict[str, int]
    project_score: int
    course_completion_status: int
    internships: list[str]
    certifications: list[str]

# Initialize the AI model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

@app.post("/recommendations/")
async def get_recommendations(candidate: CandidateInput):
    input_data = (
        f"Batch: {candidate.batch}, "
        f"MCQ Scores: {candidate.mcq_scores}, "
        f"Project Score: {candidate.project_score}, "
        f"Course Completion Status: {candidate.course_completion_status}, "
        f"Internships: {candidate.internships}, "
        f"Certifications: {candidate.certifications}."
    )
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config
        )
        
        response = model.generate_content([input_data])
        recommendations = response.text if response else "No recommendations available."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Generate Graphs
    fig, ax = plt.subplots()
    ax.bar(candidate.mcq_scores.keys(), candidate.mcq_scores.values(), color='skyblue')
    ax.set_xlabel('MCQ')
    ax.set_ylabel('Score')
    ax.set_title('MCQ Scores')
    plt.xticks(rotation=45, ha='right')
    graph_path = "mcq_scores.png"
    plt.savefig(graph_path, bbox_inches='tight')
    plt.close()

    # Create a PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subtitle_style = styles['Heading2']
    content_style = ParagraphStyle(
        'Content',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=12,
        spaceBefore=12,
        spaceAfter=12
    )
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceBefore=12,
        spaceAfter=6
    )
    subheading_style = ParagraphStyle(
        'Subheading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceBefore=6,
        spaceAfter=6
    )
    bold_style = ParagraphStyle(
        'Bold',
        parent=styles['BodyText'],
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceBefore=6,
        spaceAfter=6
    )

    content = []

    # Page 1: Report with Performance Graph
    content.append(Paragraph("Student Performance Report", title_style))
    content.append(Spacer(1, 12))
    
    # Add graph image
    content.append(Image(graph_path, width=6*inch, height=4*inch))
    content.append(Spacer(1, 12))
    
    # Add student details
    content.append(Paragraph(f"<b>Batch:</b> {candidate.batch}", content_style))
    content.append(Paragraph("<b>MCQ Scores:</b>", content_style))
    for key, value in candidate.mcq_scores.items():
        content.append(Paragraph(f"- <b>{key}:</b> {value}", content_style))
    content.append(Paragraph(f"<b>Project Score:</b> {candidate.project_score}", content_style))
    content.append(Paragraph(f"<b>Course Completion Status:</b> {candidate.course_completion_status}%", content_style))
    content.append(Paragraph(f"<b>Internships:</b> {', '.join(candidate.internships)}", content_style))
    content.append(Paragraph(f"<b>Certifications:</b> {', '.join(candidate.certifications)}", content_style))
    
    # Page 2: Recommendations
    content.append(PageBreak())
    content.append(Paragraph("Recommendations", title_style))
    content.append(Spacer(1, 12))
    
    # Add recommendations with bold headings
    recommendations = recommendations.replace("**", "")  # Remove any extra ** from recommendations text
    recommendations_list = recommendations.split('\n')
    for rec in recommendations_list:
        # Apply bold formatting to headings
        if rec.startswith("- "):
            rec = rec.replace("- ", "<b>-</b> ")
        content.append(Paragraph(rec, content_style))

    # Build PDF
    doc.build(content)

    # Get the value of the BytesIO buffer and create a response
    buffer.seek(0)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    # Return the PDF as a response
    return Response(content=pdf_bytes, media_type="application/pdf", headers={
        "Content-Disposition": "attachment; filename=recommendations.pdf"
    })

@app.get("/")
def read_root():
    return {"message": "AI Recommendation System is up and running!"}
