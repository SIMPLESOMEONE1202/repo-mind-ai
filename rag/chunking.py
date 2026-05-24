from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_code(content, file_path):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(content)

    documents = []

    for index, chunk in enumerate(chunks):

        documents.append({
            "content": chunk,
            "metadata": {
                "source": file_path,
                "chunk_index": index
            }
        })

    return documents