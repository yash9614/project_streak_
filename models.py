from pydantic import BaseModel, Field
from typing import List, Optional


class Activity(BaseModel):
    time: str = Field(description="Morning / Afternoon / Evening")
    title: str
    description: str
    estimated_cost_usd: Optional[float] = None


class DayPlan(BaseModel):
    day: int
    title: str
    activities: List[Activity]


class TravelItinerary(BaseModel):
    destination: str
    duration_days: int
    total_estimated_budget_usd: Optional[float] = None
    summary: str
    days: List[DayPlan]
    tips: List[str] = Field(default_factory=list)
