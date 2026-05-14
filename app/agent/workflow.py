from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import (
    classify_intent_node,
    rag_answer_node,
    system_status_answer_node,
    how_to_use_answer_node,
    out_of_scope_answer_node,
    clarification_answer_node
)

def build_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("classify_intent", classify_intent_node)
    workflow.add_node("rag_answer", rag_answer_node)
    workflow.add_node("system_status_answer", system_status_answer_node)
    workflow.add_node("how_to_use_answer", how_to_use_answer_node)
    workflow.add_node("out_of_scope_answer", out_of_scope_answer_node)
    workflow.add_node("clarification_answer", clarification_answer_node)
    
    # Set entry point
    workflow.set_entry_point("classify_intent")
    
    # Conditional edge logic
    def route_by_intent(state: AgentState) -> str:
        return state["intent"]
        
    # Add conditional edges
    workflow.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "rag_query": "rag_answer",
            "system_status": "system_status_answer",
            "how_to_use": "how_to_use_answer",
            "out_of_scope": "out_of_scope_answer",
            "needs_clarification": "clarification_answer"
        }
    )
    
    # All answer nodes go to END
    workflow.add_edge("rag_answer", END)
    workflow.add_edge("system_status_answer", END)
    workflow.add_edge("how_to_use_answer", END)
    workflow.add_edge("out_of_scope_answer", END)
    workflow.add_edge("clarification_answer", END)
    
    return workflow.compile()

agent_app = build_workflow()
