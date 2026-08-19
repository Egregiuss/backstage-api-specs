from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="Football Results API",
    description="API for football fixtures, scores, teams and standings",
    version="1.0.0",
)


class FixtureStatus(str, Enum):
    scheduled = "scheduled"
    live = "live"
    finished = "finished"
    postponed = "postponed"


class Team(BaseModel):
    id: str
    name: str
    shortName: str
    logo: Optional[str] = None
    league: str
    country: str


class Fixture(BaseModel):
    id: str
    homeTeam: Team
    awayTeam: Team
    homeScore: Optional[int] = None
    awayScore: Optional[int] = None
    status: FixtureStatus
    kickoff: datetime
    league: str
    season: int


class Standing(BaseModel):
    position: int
    team: Team
    played: int
    won: int
    drawn: int
    lost: int
    goalsFor: int
    goalsAgainst: int
    points: int


fixtures_db: dict = {}
teams_db: dict = {}
standings_db: list = []


@app.get("/fixtures", response_model=list[Fixture])
def list_fixtures(
    date: Optional[str] = None,
    league: Optional[str] = None,
    season: Optional[int] = None,
):
    results = list(fixtures_db.values())
    if league:
        results = [f for f in results if f.league == league]
    if season:
        results = [f for f in results if f.season == season]
    return results


@app.get("/fixtures/{id}", response_model=Fixture)
def get_fixture(id: str):
    if id not in fixtures_db:
        raise HTTPException(status_code=404, detail="Fixture not found")
    return fixtures_db[id]


@app.get("/teams", response_model=list[Team])
def list_teams(league: Optional[str] = None):
    results = list(teams_db.values())
    if league:
        results = [t for t in results if t.league == league]
    return results


@app.get("/teams/{id}", response_model=Team)
def get_team(id: str):
    if id not in teams_db:
        raise HTTPException(status_code=404, detail="Team not found")
    return teams_db[id]


@app.get("/standings", response_model=list[Standing])
def get_standings(league: str, season: int):
    return [
        s for s in standings_db
        if s.team.league == league
    ]
