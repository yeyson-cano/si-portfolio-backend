from pydantic import BaseModel
from typing import Dict, Any, Literal, List, Optional, Union

class ExecuteParams(BaseModel):
    params: Dict[str, Any]
    verbosity: Literal["first", "all", "final"] = "final"

class EpochStats(BaseModel):
    gen: int
    best: float | None
    avg: float | None

class FirstEpochOut(BaseModel):
    best: float | None
    avg: float | None
    population: List[Any]

class FinalOutGenetic(BaseModel):
    best_solution: List[Any]
    total_distance: float

class FinalOutNB(BaseModel):
    metrics: Dict[str, Any]
    confusion: Optional[Dict[str, Any]] = None
    samples: Optional[List[Any]] = None

class FinalOutNN(BaseModel):
    steps: List[Dict[str, Any]]
    final_weights: Dict[str, Any]

class FinalOutVision(BaseModel):
    type: Literal["vision"]
    prediction: str
    confidence: float

class FinalOutNER(BaseModel):
    entities: List[Dict[str, str | float]]

class ExecuteResult(BaseModel):
    history: List[EpochStats] = []
    first_epoch: Optional[FirstEpochOut] = None
    final: Union[
        FinalOutGenetic, 
        FinalOutNB, 
        FinalOutNN,
        FinalOutVision,
        FinalOutNER
    ]
