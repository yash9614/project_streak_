from semantic_router import Route, IndexedRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(name="sentence-transformers/all-MiniLM-L6-v2")

small_talk = Route(
    name="small-talk",
    utterances=["How are you?", "What is your name?", "Are you a robot?", "What do you do?"]
)

faq = Route(
    name="faq",
    utterances=[
        "What is the return policy?",
        "Do you accept cash?",
        "How can I track my order?",
        "What payment methods are accepted?"
    ]
)

sql = Route(
    name="sql",
    utterances=[
        "Show me Nike shoes under 3000",
        "What is the price of Puma running shoes?",
        "Are there any formal shoes in size 9?",
        "List shoes with more than 50% discount"
    ]
)

router = IndexedRouter(encoder=encoder, routes=[small_talk, faq, sql])