import streamlit as st
import requests

# ----------- CONFIG ----------- #
API_URL = "http://localhost:8000/chat"

st.set_page_config(
    page_title="UHC Policy Chatbot",
    layout="wide"
)

# ----------- UI HEADER ----------- #
st.title(" UHC Policy Chatbot")
st.markdown("Ask questions about insurance coverage, criteria, and policies.")

# ----------- SESSION STATE ----------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------- DISPLAY CHAT HISTORY ----------- #
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------- INPUT BOX ----------- #
query = st.chat_input("Ask your question...")

if query:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    # ----------- API CALL ----------- #
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = requests.post(
                    API_URL,
                    params={"query": query}
                )

                data = response.json()

                answer = data.get("answer", "")
                sources = data.get("sources", [])

                # ----------- DISPLAY ANSWER ----------- #
                st.markdown("### Answer")
                st.write(answer)

                # ----------- DISPLAY SOURCES ----------- #
                if sources:
                    st.markdown("### Sources")

                    unique_sources = set(
                        (s["policy"], s["section"]) for s in sources
                    )

                    for policy, section in unique_sources:
                        st.markdown(f"- **{policy}** ({section})")

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                error_msg = f" Error: {str(e)}"
                st.error(error_msg)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })