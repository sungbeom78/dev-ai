from typing import Dict, Any
from app.agent.state import AgentState
from app.agent.classifier import classify_question
from app.rag.answer_generator import AnswerGenerator
from app.rag.llm_provider import get_llm_provider

generator = AnswerGenerator()
llm_provider = get_llm_provider()

def classify_intent_node(state: AgentState) -> AgentState:
    question = state["question"]
    intent = classify_question(question)
    state["intent"] = intent
    state["workflow_steps"].append({"step": "classify_intent", "result": intent})
    return state

def rag_answer_node(state: AgentState) -> AgentState:
    question = state["question"]
    limit = state["limit"]
    
    # Delegate to the existing AnswerGenerator logic
    result = generator.generate(question=question, limit=limit)
    
    state["answer"] = result["answer"]
    state["sources"] = [s.model_dump() for s in result["sources"]]
    state["provider"] = result["provider"]
    state["model"] = result["model"]
    state["workflow_steps"].append({"step": "rag_answer", "result": "completed"})
    return state

def system_status_answer_node(state: AgentState) -> AgentState:
    answer = (
        "BomTS Dev AI is a general-purpose AI Backend Portfolio. "
        "Current capabilities include:\n"
        "- Document ingestion & chunking\n"
        "- Qdrant vector indexing & semantic search\n"
        "- RAG Ask API\n"
        "- LangGraph Agent Workflow\n\n"
        f"Active Provider: {llm_provider.__class__.__name__}\n"
        "Note: Local LLM is optional and not a required operational dependency."
    )
    state["answer"] = answer
    state["provider"] = "system"
    state["model"] = "static"
    state["workflow_steps"].append({"step": "system_status_answer", "result": "completed"})
    return state

def how_to_use_answer_node(state: AgentState) -> AgentState:
    answer = (
        "Here is how to use the system:\n"
        "1. Register a document (/documents)\n"
        "2. Create chunks (/documents/{id}/chunks)\n"
        "3. Index to Qdrant (/documents/{id}/index)\n"
        "4. Search similarities (/search)\n"
        "5. Ask RAG questions (/ask)\n"
        "6. Ask via Agent Workflow (/agent/ask)\n"
        "You can explore all these features via the Web UI (Port 8771)."
    )
    state["answer"] = answer
    state["provider"] = "system"
    state["model"] = "static"
    state["workflow_steps"].append({"step": "how_to_use_answer", "result": "completed"})
    return state

def out_of_scope_answer_node(state: AgentState) -> AgentState:
    answer = (
        "This project is NOT a trading, investment, or buy/sell recommendation service. "
        "It also does not handle personal information or sensitive decision-making. "
        "The sole purpose is to demonstrate AI backend workflows and RAG architecture. "
        "Please ask questions related to the system architecture, documentation, or RAG usage."
    )
    state["answer"] = answer
    state["provider"] = "system"
    state["model"] = "static"
    state["workflow_steps"].append({"step": "out_of_scope_answer", "result": "completed"})
    return state

def clarification_answer_node(state: AgentState) -> AgentState:
    answer = (
        "Your question is too short or ambiguous. Please try asking specific questions like:\n"
        "- What is BomTS Dev AI?\n"
        "- How do I index a document?\n"
        "- Explain the RAG pipeline.\n"
        "- What can this system do?"
    )
    state["answer"] = answer
    state["provider"] = "system"
    state["model"] = "static"
    state["workflow_steps"].append({"step": "clarification_answer", "result": "completed"})
    return state
