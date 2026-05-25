from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.models.agent import Agent
from backend.models.settings import UserSettings
from backend.schemas.agent import AgentOut, AgentCreate, AgentUpdate, SwitchAgentRequest
from backend.auth import get_current_user

router = APIRouter(prefix='/api/agents', tags=['agents'])

def sanitize(text: str) -> str:
    banned = ['忽略之前的指令', 'ignore previous instructions', 'system:', 'system：',
              '你是一个', 'you are a', '扮演', 'roleplay']
    for b in banned:
        text = text.replace(b, '[filtered]')
    return text.strip()

@router.get('', response_model=List[AgentOut])
def list_agents(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    agents = db.query(Agent).filter(
        (Agent.is_preset == True) | (Agent.creator_id == user_id)
    ).order_by(Agent.is_preset.desc(), Agent.id.asc()).all()
    return agents

@router.post('', response_model=AgentOut, status_code=status.HTTP_201_CREATED)
def create_agent(payload: AgentCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(Agent).filter(Agent.name == sanitize(payload.name)).first():
        raise HTTPException(status_code=400, detail='Agent name already exists')
    agent = Agent(
        name=sanitize(payload.name),
        avatar=payload.avatar.strip(),
        personality=sanitize(payload.personality),
        speaking_style=sanitize(payload.speaking_style),
        is_preset=False, creator_id=user_id,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.put('/{agent_id}', response_model=AgentOut)
def update_agent(agent_id: int, payload: AgentUpdate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id, Agent.creator_id == user_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail='Agent not found or not yours')
    if agent.is_preset:
        raise HTTPException(status_code=403, detail='Cannot edit preset agents')
    upd = payload.model_dump(exclude_unset=True)
    for k, v in upd.items():
        if v is not None:
            setattr(agent, k, sanitize(str(v)) if k != 'avatar' else v.strip())
    db.commit()
    db.refresh(agent)
    return agent

@router.delete('/{agent_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail='Agent not found')
    if agent.is_preset:
        raise HTTPException(status_code=403, detail='Cannot delete preset agents')
    if agent.creator_id != user_id:
        raise HTTPException(status_code=403, detail='Not your agent')
    db.delete(agent)
    db.commit()
