from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# Tool to read or edit document contents
@mcp.tool(
    name="read_doc_contents",
    description="Reads the contents of a document given its ID.",
)
def read_document(
    doc_id: str = Field(description="The ID of the document to read.")
):
    if doc_id not in docs:
        return f"Document with ID '{doc_id}' not found."
    return docs[doc_id]

@mcp.tool(
    name="edit_doc_contents",
    description="Edits the contents of a document given its ID and new content.",
)
def edit_document(
    doc_id: str = Field(description="The ID of the document to edit."),
    old_content: str = Field(description="The old content for the document."),
    new_content: str = Field(description="The new content for the document."),
):
    if doc_id not in docs:
        return f"Document with ID '{doc_id}' not found."
    docs[doc_id] = docs[doc_id].replace(old_content, new_content)
    return f"Document with ID '{doc_id}' has been updated."

# Direst resource or template resource access to the docs
@mcp.resourcce(
    "docs://documents",
    mime_type="application/json",
)
def list_documents() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
)
def fetch_document(doc_id: str) -> str:
    if doc_id not in docs:
        # raise ValueError(f"Document with ID '{doc_id}' not found.")
        return f"Document with ID '{doc_id}' not found."
    return docs[doc_id]

@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format.",
)
def format_document(
    doc_id: str = Field(description="The ID of the document to format.")
) -> list[base.Message]:
    prompt = f"""
    You are a document formatting assistant. 
    Your task is to rewrite the contents of the document with ID '{doc_id}' in Markdown format. 
    Ensure that the formatting is clear and consistent, using appropriate Markdown syntax for headings, lists, bold, italics, and other elements as needed.
    Use the edit_document tool to make the changes. After the document has been updated save it inside our server.
    """
    return [
        base.SystemMessage(content=prompt)
    ]

# TODO: Write a prompt to summarize a doc

if __name__ == "__main__":
    mcp.run(transport="stdio")
