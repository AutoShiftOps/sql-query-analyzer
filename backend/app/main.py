from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from schemas.models import QueryRequest, QueryAnalysisResult
from agents.sql_analyzer import SQLAnalyzerAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="SQL Query Analyzer",
    description="AI-powered SQL query analysis and optimization tool",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzer
analyzer = SQLAnalyzerAgent()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SQL Query Analyzer"}

@app.post("/analyze", response_model=QueryAnalysisResult)
async def analyze_query(request: QueryRequest):
    """
    Analyze SQL query for optimization opportunities
    
    - Detects performance issues
    - Suggests indexes
    - Provides rewritten optimized query
    - Checks security implications
    """
    try:
        start_time = time.time()
        
        # Validate query
        if not request.query or len(request.query.strip()) < 5:
            raise HTTPException(status_code=400, detail="Query too short")
        
        logger.info(f"Analyzing query: {request.query[:50]}...")
        
        # Run analysis
        result = await analyzer.analyze(
            query=request.query,
            db_type=request.db_type.value,
            schema_info=request.schema_info
        )
        
        analysis_time = (time.time() - start_time) * 1000
        
        return QueryAnalysisResult(
            query=request.query,
            parsed_query=result.get("parsing_result", {}),
            optimization_suggestions=result.get("optimization_suggestions", []),
            execution_plan=result.get("execution_plan"),
            optimized_query=result.get("optimized_query"),
            performance_metrics={
                "complexity_score": result.get("parsing_result", {}).get("complexity_score", 0),
                "subqueries": result.get("parsing_result", {}).get("subqueries", 0)
            },
            security_issues=result.get("security_issues", []),
            readability_score=result.get("readability_score", 0),
            analysis_time_ms=analysis_time
        )
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/docs")
async def get_documentation():
    """API documentation"""
    return {
        "title": "SQL Query Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Analyze SQL query",
            "GET /health": "Health check",
            "GET /docs": "This documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)