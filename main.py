from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from starlette.responses import JSONResponse
from data_ingestion.ingestion import DataIngestion
from agents.workflow import GraphBuilder
from data_models.models import QuestionRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # set specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)) -> Dict[str, str]:
    """
    Endpoint to upload and ingest files into the vector database.

    Parameters
    ----------
    files : List[UploadFile]
        List of files to be uploaded and processed.

    Returns
    -------
    dict
        Success message or error details.
    """
    try:
        ingestion = DataIngestion()
        ingestion.run_pipeline(files)
        return {"message": "Files successfully processed and stored."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/query")
async def query_chatbot(request: QuestionRequest) -> Dict[str, Any]:
    """
    Endpoint to query the chatbot with a user's question.

    Parameters
    ----------
    request : QuestionRequest
        The request payload containing the user's question.

    Returns
    -------
    dict
        The chatbot's answer or error details.
    """
    try:
        graph_service = GraphBuilder()
        graph_service.build()
        graph = graph_service.get_graph()

        # Prepare messages for the workflow graph
        messages = {"messages": [request.question]}

        result = graph.invoke(messages)

        # Extract the final output from the result
        if isinstance(result, dict) and "messages" in result:
            final_output = result["messages"][-1].content  # Last AI response
        else:
            final_output = str(result)

        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})