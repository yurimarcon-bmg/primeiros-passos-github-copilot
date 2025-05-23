"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
   "Clube de Xadrez": {
      "description": "Aprenda estratégias e participe de torneios de xadrez",
      "schedule": "Sextas, 15h30 - 17h",
      "max_participants": 12,
      "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
   },
   "Aula de Programação": {
      "description": "Aprenda fundamentos de programação e desenvolva projetos de software",
      "schedule": "Terças e quintas, 15h30 - 16h30",
      "max_participants": 20,
      "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
   },
   "Educação Física": {
      "description": "Educação física e atividades esportivas",
      "schedule": "Segundas, quartas e sextas, 14h - 15h",
      "max_participants": 30,
      "participants": ["john@mergington.edu", "olivia@mergington.edu"]
   },
   # Esportivas
   "Futebol": {
      "description": "Treinamento e partidas de futebol para todos os níveis",
      "schedule": "Terças e quintas, 16h - 17h30",
      "max_participants": 22,
      "participants": ["lucas@mergington.edu", "ana@mergington.edu"]
   },
   "Vôlei": {
      "description": "Aulas e jogos de vôlei para iniciantes e avançados",
      "schedule": "Quartas, 15h - 16h30",
      "max_participants": 14,
      "participants": ["marcos@mergington.edu", "lara@mergington.edu"]
   },
   # Artísticas
   "Teatro": {
      "description": "Expressão artística e encenação de peças teatrais",
      "schedule": "Segundas e quartas, 16h - 17h30",
      "max_participants": 18,
      "participants": ["carla@mergington.edu", "roberto@mergington.edu"]
   },
   "Oficina de Pintura": {
      "description": "Aulas práticas de pintura em diferentes técnicas",
      "schedule": "Sextas, 14h - 15h30",
      "max_participants": 15,
      "participants": ["juliana@mergington.edu", "felipe@mergington.edu"]
   },
   # Intelectuais
   "Clube de Leitura": {
      "description": "Discussão de livros e desenvolvimento do hábito de leitura",
      "schedule": "Terças, 17h - 18h",
      "max_participants": 16,
      "participants": ["paula@mergington.edu", "ricardo@mergington.edu"]
   },
   "Olimpíada de Matemática": {
      "description": "Preparação para olimpíadas e desafios matemáticos",
      "schedule": "Quintas, 15h - 16h",
      "max_participants": 25,
      "participants": ["aline@mergington.edu", "gustavo@mergington.edu"]
   }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    # Get the specificy activity
    activity = activities[activity_name]

    # Validar se o estudante já está inscrito
    if email in activity["participants"]:
      raise HTTPException(status_code=400, detail="Estudante já inscrito")

    # Add student
    activity["participants"].append(email)
    return {"message": f"{email} inscrito(a) em {activity_name} com sucesso"}


@app.delete("/activities/{activity_name}/unenroll")
def unenroll_from_activity(activity_name: str, email: str):
    """Remove um estudante de uma atividade"""
    # Validar se a atividade existe
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    # Obter a atividade específica
    activity = activities[activity_name]

    # Validar se o estudante está inscrito
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Estudante não está inscrito nesta atividade")

    # Remover o estudante
    activity["participants"].remove(email)
    return {"message": f"{email} desinscrito(a) de {activity_name} com sucesso"}
