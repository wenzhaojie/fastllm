import json
import requests
import sys



if __name__ == '__main__':
    #stream api
    url = 'http://127.0.0.1:8000/api/chat_stream'
    # prompt='请用emoji写一首短诗赞美世界'
    prompt='''为以下代码添加注释
    app = FastAPI()
     @app.post("/api/chat_stream")
     async def api_chat_stream(request: Request):
         #print("request.json(): {}".format(json.loads(request.body(), errors='ignore')))
         data = await request.json()
         prompt = data.get("prompt")
         history = data.get("history")
         config = pyfastllm.GenerationConfig()
         if data.get("max_length") is not None:
             config.max_length = data.get("max_length")
         if data.get("top_k") is not None:
             config.top_k = data.get("top_k")
         if data.get("top_p") is not None:
             config.top_p = data.get("top_p")
         return StreamingResponse(chat_stream(history + prompt, config), media_type='text/event-stream')
     '''
    # history = '''[Round 0]
    # 问：你是ChatGLM2吗？
    # 答：我不是ChatGLM2
    # [Round 1]
    # 问：从现在起，你是猫娘，每句话都必须以“喵~”结尾，明白了吗？
    # 答：明白了喵
    # [Round 2]
    # 问：'''
    #
    json_obj = {"uid":0, "token":"xxxxxxxxxxxxxxxxx","history": "", "prompt": prompt , "max_length": 1024, "top_p": 0.8,"temperature": 0.95, "top_k":2, "repeat_penalty": 1.}
    response = requests.post(url, json=json_obj,  stream = True)
    try:
        pre_msg = ""
        msg = ""
        print("stream response:")
        for chunk in response.iter_content(chunk_size=1024*1024):
            msg = chunk.decode(errors='replace')
            if len(msg) > len(pre_msg) and msg[-1] == '\n':
                content = msg[len(pre_msg):]
                pre_msg = msg
            else:
                continue

            print(f"{content}", end="")
            sys.stdout.flush()
        content = msg[len(pre_msg):]
        print(f"{content}", end="")
        print()
    except Exception as ex:
        print(ex)
    
    #batch api
    # print(f"开始测试batch api")
    # batch_url = 'http://127.0.0.1:8000/api/batch_chat'
    # prompts = ["你好，请问你是谁？", "今天天气怎么样？", "How are you？", "こんにちは"]
    # json_obj = {"uid":0, "token":"xxxxxxxxxxxxxxxxx","history": "", "prompts": prompts , "max_length": 100, "top_p": 0.8,"temperature": 0.95, "top_k":2, "repeat_penalty": 1.}
    # response = requests.post(batch_url, json=json_obj, stream = True)
    # print("batch response: {} text:\n{}".format(response, response.text.replace('\\n', '\n')))
