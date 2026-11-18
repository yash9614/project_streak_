from app.router import router
from app.smalltalk import talk
from app.faq import get_relevant_qa, generate_answer
from app.sql import generate_sql, run_query, answer_from_data

def ask(query: str) -> str:
    route = router(query).name
    if route == "small-talk":
        return talk(query)
    elif route == "faq":
        context = get_relevant_qa(query)
        return generate_answer(query, context)
    elif route == "sql":
        sql = generate_sql(query)
        clean_sql = sql.replace("```sql", "").replace("```", "").strip()
        df = run_query(clean_sql)
        return answer_from_data(query, df)
    else:
        return f"Route '{route}' not implemented yet"