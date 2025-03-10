from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/")
async def root():
    return {"Message": "Hello, Welcome to Bookly"}


#  Headers as a response or getting headers in request


@app.get("/headers")
def getting_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    host: str = Header(None),
    user_agent: str = Header(None)
):
    header = {}
    header["accept"] = accept
    header["content_type"] = content_type
    header["Host"] = host
    header["user_agent"] = user_agent
    return header
