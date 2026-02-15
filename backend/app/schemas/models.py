from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class DatabaseType(str, Enum):
    POSTGRES = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    SQL_SERVER = "sqlserver"

class QueryRequest(BaseModel):
    """
    Request model for query analysis
    """
    query: str = Field(..., description="SQL query to analyze")
    db_type: DatabaseType = Field(default=DatabaseType.POSTGRES)
    schema_info: Optional[str] = Field(None, description="Schema DDL for better context")
    focus: str = Field(default="performance", description="Analysis focus: performance|security|readability")

class OptimizationSuggestion(BaseModel):
    """
    Individual optimization suggestion
    """
    type: str   # index_missing, query_rewrite, join_optimization
    severity: str   # critical, high, medium, low
    suggestion: str
    reason: str
    estimated_improvement: str  # e.g., "40% faster"

class ExecutionPlan(BaseModel):
    """
    Query execution plan details
    """
    plan_type: str
    operations: List[Dict[str, Any]]
    total_cost: float
    estimated_rows: int

class QueryAnalysisResult(BaseModel):
    """
    Complete analysis result
    """
    query: str
    parsed_query: Dict[str, Any]
    optimization_suggestions: List[OptimizationSuggestion]
    execution_plan: Optional[ExecutionPlan]
    optimized_query: Optional[str]
    performance_metrics: Dict[str, Any]
    security_issues: List[str]
    readability_score: float
    analysis_time_ms: float
