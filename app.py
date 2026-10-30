import streamlit as st
from llm import generate_itinerary

st.set_page_config(page_title="AI Travel Assistant", page_icon="✈️", layout="wide")
st.title("✈️ AI Travel Assistant")
st.caption("Chat to gather preferences, then generate a structured itinerary.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Where do you want to go, and for how many days?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input — normal conversation only
if prompt := st.chat_input("Tell me about your trip..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Simple reply (no structured generation here)
    with st.chat_message("assistant"):
        reply = "Got it. Tell me more or click **Generate Final Itinerary** when you're ready."
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Generate button — runs structured output once
if st.button("Generate Final Itinerary", type="primary"):
    if len(st.session_state.messages) < 2:
        st.warning("Chat a bit first so I know your preferences.")
    else:
        with st.spinner("Compiling your itinerary..."):
            try:
                itinerary = generate_itinerary(st.session_state.messages)

                st.success("Itinerary ready")
                st.subheader(f"{itinerary.destination} — {itinerary.duration_days} days")
                st.write(itinerary.summary)

                if itinerary.total_estimated_budget_usd:
                    st.metric("Estimated Budget", f"${itinerary.total_estimated_budget_usd:,.0f}")

                for day in itinerary.days:
                    with st.expander(f"Day {day.day}: {day.title}", expanded=True):
                        for act in day.activities:
                            cost = f" (${act.estimated_cost_usd})" if act.estimated_cost_usd else ""
                            st.markdown(f"**{act.time}** — {act.title}{cost}")
                            st.caption(act.description)

                if itinerary.tips:
                    st.info("**Tips:** " + " • ".join(itinerary.tips))

            except Exception as e:
                st.error(f"Something went wrong: {e}")
