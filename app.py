import streamlit as st

from services.github_service import clone_repository

from services.llm_service import (
    generate_response
)

from utils.file_parser import (
    get_repository_files,
    read_file_content
)

from rag.chunking import chunk_code

from rag.vector_store import (
    store_chunks,
    search_similar_chunks
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Developer Intelligence Platform",
    layout="wide"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🚀 Developer Intelligence Platform")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "repository_indexed" not in st.session_state:
    st.session_state.repository_indexed = False

if "current_repo" not in st.session_state:
    st.session_state.current_repo = None

# ---------------------------------------------------
# MAIN TITLE
# ---------------------------------------------------

st.title("🚀 Developer Intelligence Platform")

# ---------------------------------------------------
# REPOSITORY INPUT
# ---------------------------------------------------

repo_url = st.text_input(
    "Enter GitHub Repository URL"
)

# ---------------------------------------------------
# ANALYZE REPOSITORY
# ---------------------------------------------------

if st.button("Analyze Repository"):

    if repo_url:

        with st.spinner("Cloning repository..."):

            result = clone_repository(
                repo_url
            )

        if result["success"]:

            repo_path = result[
                "local_path"
            ]

            st.success(
                "Repository cloned successfully!"
            )

            with st.spinner(
                "Parsing repository files..."
            ):

                repository_files = (
                    get_repository_files(
                        repo_path
                    )
                )

            st.write(
                f"### Files Parsed: {len(repository_files)}"
            )

            all_chunks = []

            with st.spinner(
                "Creating chunks..."
            ):

                for file_path in repository_files:

                    content = read_file_content(
                        file_path
                    )

                    if content:

                        chunks = chunk_code(
                            content,
                            file_path
                        )

                        all_chunks.extend(
                            chunks
                        )

            st.write(
                f"### Total Chunks Created: {len(all_chunks)}"
            )

            with st.spinner(
                "Generating embeddings and storing in ChromaDB..."
            ):

                store_chunks(
                    result["repo_name"],
                    all_chunks
                    )

            st.success(
                "Repository indexed successfully!"
            )

            st.session_state.repository_indexed = True
            st.session_state.current_repo = (
                result["repo_name"]
            )

        else:

            st.error(result["error"])

# ---------------------------------------------------
# CHAT SECTION
# ---------------------------------------------------

st.divider()

st.header("💬 Chat With Repository")

# Warn if repo not indexed
if not st.session_state.repository_indexed:

    st.info(
        "Please analyze a repository first."
    )

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Chat input
user_query = st.chat_input(
    "Ask anything about the repository"
)

# ---------------------------------------------------
# HANDLE USER QUERY
# ---------------------------------------------------

if user_query:

    if not st.session_state.repository_indexed:

        st.warning(
            "Please analyze a repository first."
        )

    else:

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

        # Display user message
        with st.chat_message("user"):

            st.markdown(user_query)

        # Retrieve chunks
        with st.spinner(
            "Searching repository..."
        ):

            results = search_similar_chunks(
                st.session_state.current_repo,
                user_query
            )

            retrieved_docs = (
                results["documents"][0]
            )

        # Generate AI response
        with st.chat_message("assistant"):

            response_placeholder = st.empty()

            stream = generate_response(
                user_query,
                retrieved_docs
            )

            full_response = ""

            for chunk in stream:

                content = (
                    chunk.choices[0]
                    .delta.content
                )

                if content:

                    full_response += content

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            response_placeholder.markdown(
                full_response
            )

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

        # Retrieved context section
        with st.expander(
            "Retrieved Context"
        ):

            for doc in retrieved_docs:

                st.code(doc[:1500])