from langgraph.graph import StateGraph
from langgraph_openai import ChatOpenAI
from langgraph.prompts import PromptTemplate
from typing import Dict, List, Any, Annotated
import operator

# Define agent state
class QueryAnalysisState:
    """State for query analysis workflow"""
    query: str
    db_type: str
    schema_info: str
    parsing_result: Dict[str, Any]
    optimization_suggestions: List[Dict]
    execution_plan: Dict
    optimized_query: str
    security_issues: List[str]
    readability_score: float

class SQLAnalyzerAgent:
    """Multi-agent system for SQL query analysis using LangGraph"""

    def __init__(self, openai_api_key: str = None):
        self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build LangGraph workflow"""
        workflow = StateGraph(QueryAnalysisState)

        # Define nodes
        workflow.add_node("parse_query", self._parse_query_node)
        workflow.add_node("analyze_performence", self._analyze_performance_node)
        workflow.add_node("check_security", self._check_security_node)
        workflow.add_node("generate_optimization", self._generate_optimization_node)
        workflow.add_node("assess_readability", self._assess_readability_node)
        workflow.add_node("create_optimized", self._create_optimized_query_node)

        # Define edges
        workflow.add_edge("parse_query", "analyze_performance")
        workflow.add_edge("parse_query", "check_security")
        workflow.add_edge("analyze_performance", "generate_optimization")
        workflow.add_edge("check_security", "generate_optimization")
        workflow.add_edge("generate_optimization", "assess_readability")
        workflow.add_edge("assess_readability", "create_optimized")
        
        workflow.set_entry_point("parse_query")
        
        return workflow.compile()

    async def _parse_query_node(self, state: QueryAnalysisState) -> Dict:
        """Node: Parse query structure"""
        from tools.query_parser import QueryParser
        parser = QueryParser()
        parsing_result = parser.parse(state.query)
        return {"parsing_result": parsing_result}
    
    async def _analyze_performance_node(self, state: QueryAnalysisState) -> Dict:
        """Node: Analyze performance aspects"""
        prompt = PromptTemplate(
            input_variables=["query", "db_type", "parsing_result"],
            template="""Analyze this SQL query for performance issues:
            
Query: {query}
Database: {db_type}
Parsed Structure: {parsing_result}

Identify:
1. Missing indexes
2. Inefficient joins
3. Subquery optimization opportunities
4. Table scan risks

Provide specific, actionable recommendations."""
        )
        
        analysis = await self.llm.ainvoke(prompt.format(
            query=state.query,
            db_type=state.db_type,
            parsing_result=state.parsing_result
        ))
        
        return {"execution_plan": self._extract_plan_details(analysis)}
    
    async def _check_security_node(self, state: QueryAnalysisState) -> Dict:
        """Node: Check for security issues"""
        security_checks = []
        
        # Check for SQL injection patterns
        if "union" in state.query.lower() and state.schema_info is None:
            security_checks.append("Potential SQL injection risk - use parameterized queries")
        
        if "drop" in state.query.lower() or "truncate" in state.query.lower():
            security_checks.append("Destructive operation detected")
        
        return {"security_issues": security_checks}
    
    async def _generate_optimization_node(self, state: QueryAnalysisState) -> Dict:
        """Node: Generate optimization suggestions"""
        suggestions = []
        
        # Example suggestions
        if "select *" in state.query.lower():
            suggestions.append({
                "type": "column_selection",
                "severity": "medium",
                "suggestion": "Specify explicit columns instead of SELECT *",
                "reason": "Reduces data transfer and improves query planning",
                "estimated_improvement": "5-10% faster"
            })
        
        return {"optimization_suggestions": suggestions}
    
    async def _assess_readability_node(self, state: QueryAnalysisState) -> Dict:
        """Node: Assess query readability"""
        readability_score = 100
        
        # Deduct points for complexity
        if state.parsing_result["complexity_score"] > 50:
            readability_score -= 20
        
        return {"readability_score": readability_score}
    
    async def _create_optimized_query_node(self, state: QueryAnalysisState) -> Dict:
        """Node: Create optimized version"""
        prompt = PromptTemplate(
            input_variables=["query", "suggestions"],
            template="""Create an optimized version of this query based on suggestions:
            
Original: {query}
Suggestions: {suggestions}

Provide only the optimized SQL query."""
        )
        
        optimized = await self.llm.ainvoke(prompt.format(
            query=state.query,
            suggestions=state.optimization_suggestions
        ))
        
        return {"optimized_query": optimized.content}
    
    async def analyze(self, query: str, db_type: str, schema_info: str = None) -> Dict:
        """Execute complete analysis"""
        initial_state = QueryAnalysisState(
            query=query,
            db_type=db_type,
            schema_info=schema_info or "",
            parsing_result={},
            optimization_suggestions=[],
            execution_plan={},
            optimized_query="",
            security_issues=[],
            readability_score=0
        )
        
        result = await self.graph.ainvoke(initial_state)
        return result