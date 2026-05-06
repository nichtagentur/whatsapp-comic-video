import os, base64, json, urllib.request
key = os.environ["OPENROUTER_API_KEY"]
img = base64.b64encode(open("frame.png","rb").read()).decode()
prompt = "Transform this image into a vibrant comic book illustration: bold black ink outlines, halftone dot shading, saturated pop-art colors, dynamic Ben-Day dots, comic panel style. Keep subject and composition identical. Vertical 9:16."
body = json.dumps({"model":"google/gemini-2.5-flash-image","modalities":["image","text"],
    "messages":[{"role":"user","content":[
        {"type":"text","text":prompt},
        {"type":"image_url","image_url":{"url":f"data:image/png;base64,{img}"}}]}]}).encode()
req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
    data=body, headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"})
data = json.loads(urllib.request.urlopen(req,timeout=120).read())
msg = data["choices"][0]["message"]
imgs = msg.get("images",[])
print("images:",len(imgs))
if imgs:
    url = imgs[0]["image_url"]["url"]
    b64 = url.split(",",1)[1] if "," in url else url
    open("comic.png","wb").write(base64.b64decode(b64))
    print("saved comic.png",os.path.getsize("comic.png"))
else:
    print(msg.get("content","")[:300])
