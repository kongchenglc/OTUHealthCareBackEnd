from fastapi import FastAPI, Request
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许跨域请求 (CORS) 以便前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以根据需要指定前端的域名
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加载Hugging Face对话模型 (如GPT2)
generator = pipeline('text-generation', model='meta-llama/Llama-3.2-1B-Instruct')

@app.post("/chat/")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get('message') 
    
    # 调用 Hugging Face 模型生成 AI 回复
    response = generator(user_message)[0]['generated_text']
    return {"response": response}

@app.get("/chat/")
async def chat(message: str):
    try:
        # 使用 Hugging Face 模型生成 AI 回复
        response = generator(message, max_new_tokens=256)[0]['generated_text']
        return {"response": response}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)