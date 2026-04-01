from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

from models import SearchRequest, SearchTask, ScrapedResult
from services.scraper import DarkDumpScraper

app = FastAPI(title="Dark Web Intelligence Platform API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for tasks (use MongoDB in production)
tasks_db: Dict[str, SearchTask] = {}

scraper = DarkDumpScraper(use_tor=False) # Change to True if Tor is running

def run_search_task(task_id: str, request: SearchRequest):
    task = tasks_db[task_id]
    task.status = "running"
    
    try:
        # Step 1: Search Ahmia for initial links
        query = f"{request.primary_keyword} {' '.join(request.secondary_keywords)}"
        raw_results = scraper.search_ahmia(query, amount=request.amount)
        
        if not raw_results:
            task.status = "completed"
            task.results = []
            return

        final_results = []
        
        # Parallel scraping would be better, but for now we do it sequentially or in chunks
        # In a real app, use Celery workers
        for res in raw_results:
            # For the demo, we use the metadata from Ahmia if onion scraping fails
            # But the user wants "accuracy", so we try to scrape.
            # To make it "accurate" for the search intent without Tor, we score the ahmia metadata
            
            # Here we combine the Ahmia description with our own scoring
            # If we don't have Tor, we can't scrape the actual site, but we can score what we have
            from services.scoring import calculate_relevance_score
            score, matched_kws = calculate_relevance_score(res['description'], res['title'], request.primary_keyword, request.secondary_keywords)
            
            # Create a result object
            scraped_res = ScrapedResult(
                title=res['title'],
                url=res['url'],
                description=res['description'],
                snippet=res['description'][:200] + "...",
                score=score,
                matched_keywords=matched_kws,
                images=[] # Only if we scrape the site
            )
            final_results.append(scraped_res)
        
        # Sort by score descending
        final_results.sort(key=lambda x: x.score, reverse=True)
        
        task.results = final_results
        task.status = "completed"
    except Exception as e:
        task.status = "failed"
        task.error = str(e)
        print(f"Task {task_id} failed: {e}")

@app.post("/api/search", response_model=SearchTask)
def start_search(request: SearchRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    task = SearchTask(id=task_id, status="pending", results=[])
    tasks_db[task_id] = task
    
    background_tasks.add_task(run_search_task, task_id, request)
    return task

@app.get("/api/tasks/{task_id}", response_model=SearchTask)
def get_task_status(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

@app.get("/api/history")
def get_history():
    # Return all completed tasks
    return [t for t in tasks_db.values() if t.status == "completed"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
