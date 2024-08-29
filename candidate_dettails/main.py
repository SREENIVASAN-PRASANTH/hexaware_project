from fastapi import FastAPI, Form , UploadFile, File, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Union
from typing import List, Optional, Dict
import os

def ensure_directory_exists(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)

app = FastAPI()

batches = {
    "Java" : [],
    ".NET" : [],
    "Data Engineering" : []
}

BATCH_MIN_SIZE = 25
BATCH_MAX_SIZE = 30

class McqScore(BaseModel):
    score : int
    total : int
    
class ProjectEvaluation(BaseModel):
    score : int
    feedback : str
    
class TrainingProgress(BaseModel):
    course_completion : float = 0.0
    mcq_scores : List[McqScore] = []
    project_evaluations : List[ProjectEvaluation] = []
    
class CandidateInfo(BaseModel):
    name : str
    email : EmailStr
    degree : str
    specialization : str
    phone_number : str
    certifications : Optional[List[str]] = None
    internship_details : Optional[str] = None
    courses_completed : Optional[List[str]] = None
    linkedin_profile : Optional[str] = None
    github_profile : Optional[str] = None
    programming_languages_known : List[str]
    training_progress : TrainingProgress = TrainingProgress()
    batch_name : Optional[str] = None
    
def allocate_batch(candidate : CandidateInfo) -> str:
    if any(cert in candidate.certifications for cert in ["AWS","Java"]):
        batch_name = "Java"
    elif any(cert in candidate.certifications for cert in ["Azure", ".NET"]):
        batch_name  =".NET"
    elif "Python" in candidate.certifications:
        batch_name = "Data Engineering"
    else:
        raise HTTPException(status_code = 400,detail = "No matching batch found for the given certifications.")
    
    
    if len(batches[batch_name]) >=BATCH_MAX_SIZE:
        raise HTTPException(status_code = 400, detail = f"{batch_name} batch is full. Cannot allocate at this time")
    
    candidate.batch_name = batch_name
    batches[batch_name].append(candidate)
    
    return batch_name

@app.post("/submit_candidate_info/")
async def submit_candidate_info(
            name : str = Form(...),
            email : EmailStr = Form(...),
            degree : str = Form(...),
            specialization : str = Form(...),
            phone_number : str = Form(...),
            certifications : Optional[str] = Form(None),
            internship_details : Optional[str] = Form(None),
            courses_completed : Optional[str] = Form(None),
            github_profile : Optional[str] = Form(None),
            programming_languages_known : Optional[str] = Form(None),
            cert_files: Union[UploadFile, List[UploadFile], None] = File(None),
            internship_files: Union[UploadFile, List[UploadFile], None] = File(None),
            course_files: Union[UploadFile, List[UploadFile], None] = File(None)  
            ):
    
    #converting comma separated values to list
    certifications_list = certifications.split(",") if certifications else []
    courses_completed_list = courses_completed.split(",") if courses_completed else []
    programming_languages_known_list = programming_languages_known.split(",") if programming_languages_known else []
    
    if cert_files and not isinstance(cert_files, list):
        cert_files = [cert_files]
    if internship_files and not isinstance(internship_files, list):
        internship_files = [internship_files]
    if course_files and not isinstance(course_files, list):
        course_files = [course_files]
    
    candidate= CandidateInfo(
        name = name,
        email=email,
        degree=degree,
        specialization=specialization,
        phone_number=phone_number,
        certifications=certifications_list or [],
        internship_details=internship_details,
        courses_completed=courses_completed_list or [],
        github_profile=github_profile,
        programming_languages_known=programming_languages_known_list
    )
    
    batch_name = allocate_batch(candidate)
    
    ensure_directory_exists("/certifications")
    ensure_directory_exists("/internships")
    ensure_directory_exists("/courses")
    
    if cert_files:
        for file in cert_files:
            file_location = f"D:/python projects/hexaware project/certifications/{file.filename}"
            with open(file_location, "wb") as f:
                f.write(await file.read())
    
    if internship_files:
        for file in internship_files:
            file_location = f"D:/python projects/hexaware project/{file.filename}"
            with open(file_location, "wb") as f:
                f.write(await file.read())

    if course_files:
        for file in course_files:
            file_location = f"D:/python projects/hexaware project/courses/{file.filename}"
            with open(file_location, "wb") as f:
                f.write(await file.read())
            
    return {"message" : f"Candidate {name} has been allocated to the {batch_name} batch."}


@app.post("/update_progress/{email}")
def update_progress(email:str,course_completion:float = Form(...)):
    for batch in batches.values():
        for candidate in batch:
            if candidate.email == email:
                candidate.training_progress.course_completion = course_completion
                return {"message" : f"Progress updated for {candidate.name}"}
    raise HTTPException(status_code = 404, detail = "Candidate Not Found")

@app.post("/record_mcq_scores/{email}")
def record_mcq_score(email:str, score : int = Form(...),total : int = Form(...)):
    for batch in batches.values():
        for candidate in batch:
            if candidate.email == email:
                candidate.training_progress.mcq_scores.append(McqScore(score= score,total = total))
                return {"message" : f"MCQ score recorded for {candidate.name}"}
    raise HTTPException(status_code = 404, detail = "Candidate Not Found")

@app.post("/record_project_evaluation/{email}")
def record_project_evaluation(email : str,score : int = Form(...), feedback : str = Form(...)):
    for batch in batches.values():
        for candidate in batch:
            if candidate.email == email:
                candidate.training_progress.project_evaluations.append(ProjectEvaluation(score = score,feedback = feedback))
                return {"message" : f"Project evaluation recorded for {candidate.name}"}
    raise HTTPException(status_code = 404, detail = "Candidate Not Found")

def generate_recommendations(candidate : CandidateInfo) -> dict[str,str]:
    recommendations = {}
    
    if candidate.training_progress.course_completion < 70.0:
        recommendations["focus area"] = "Course Completion"
        recommendations["suggestions"] = "Increase course completion rate by dedicating more time."
        
    average_mcq_score = sum([score.score for score in candidate.training_progress.mcq_scores]) / max(1,len(candidate.training_progress.mcq_scores))
    
    if average_mcq_score < 50:
        recommendations["focus area"] = "MCQ Performance"
        recommendations["suggestions"] = "Review MCQ topics and practice more questions."
        
    return recommendations

@app.get("/get_recommendations/{email}")
def get_recommendations(email:str):
    for batch in batches.values():
        for candidate in batch:
            if candidate.email == email:
                recommendations = generate_recommendations(candidate)
                return {
                    "candidate" : candidate.name,
                    "recommendations" : recommendations
                }
    raise HTTPException(status_code=404,detail = "Candidate Not Found")

@app.get("/batches/")
def get_batches() -> Dict[str, List[CandidateInfo]]:
    return {batch_name: [candidate.dict() for candidate in candidates] for batch_name, candidates in batches.items()}
    
@app.get("/")
def home_page():
    return {"message" : "Welcome to AI Skill Navigator Application."}
    
    
    
    
    
    
    
    