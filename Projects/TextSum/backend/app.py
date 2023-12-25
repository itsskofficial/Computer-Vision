from fastapi import FastAPI, Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from fastapi.responses import Response
from TextSum.pipeline.prediction import PredictionPipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main():
    return {"message" : "This is a simple text summarization app"}

@app.post("/summarize")
async def summarize(text: str, response: Response):

    try:
        prediction_object = PredictionPipeline()
        text = prediction_object.predict(text)
        response.status_code = HTTP_200_OK
        return {"result" : text}
    
    except Exception as e:
        response.status_code = HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": e}

if __name__=="__main__":
    app.run(debug = True)