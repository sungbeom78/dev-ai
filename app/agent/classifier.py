def classify_question(question: str) -> str:
    """
    Rule-based intent classifier.
    Returns one of: rag_query, system_status, how_to_use, out_of_scope, needs_clarification
    """
    q_lower = question.lower()
    
    # 1. out_of_scope
    out_of_scope_keywords = ["buy", "sell", "stock", "trading", "investment advice", "recommend"]
    if any(k in q_lower for k in out_of_scope_keywords):
        return "out_of_scope"
        
    # 2. needs_clarification
    if len(q_lower.strip()) < 5 or q_lower.strip() in ["help", "hi", "hello", "?"]:
        return "needs_clarification"
        
    # 3. system_status
    status_keywords = ["status", "health", "provider", "model", "can this system do", "what is this system"]
    if any(k in q_lower for k in status_keywords):
        return "system_status"
        
    # 4. how_to_use
    usage_keywords = ["how", "usage", "register", "index", "search", "chunk"]
    if any(k in q_lower for k in usage_keywords):
        return "how_to_use"
        
    # 5. default: rag_query
    return "rag_query"
