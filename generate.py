import os, json, time, urllib.request

key = os.environ["OPENROUTER_API_KEY"]
img_url = "https://tmpfiles.org/dl/36777048/comic.png"
H = {"Authorization":f"Bearer {key}","Content-Type":"application/json"}

body = json.dumps({
    "model":"bytedance/seedance-2.0-fast",
    "prompt":"vibrant comic book animation, bold ink lines, halftone shading, saturated pop-art colors, dynamic motion, character animates naturally with subtle camera push-in",
    "frame_images":[{"type":"image_url","image_url":{"url":img_url},"frame_type":"first_frame"}],
    "size":"720x1280",
    "duration":5
}).encode()

req = urllib.request.Request("https://openrouter.ai/api/v1/videos", data=body, headers=H)
r = json.loads(urllib.request.urlopen(req,timeout=60).read())
print("submit:",r)
poll = r["polling_url"]
vid = r["id"]
for i in range(120):
    time.sleep(10)
    pr = urllib.request.Request(poll, headers={"Authorization":f"Bearer {key}"})
    s = json.loads(urllib.request.urlopen(pr,timeout=30).read())
    print(f"[{i*10}s] {s.get('status')} {s.get('progress','')}")
    if s.get("status") in ("completed","succeeded","success"):
        print(json.dumps(s,indent=2)[:800])
        break
    if s.get("status") in ("failed","error"):
        print("FAIL",s); raise SystemExit(1)
# download
dl = urllib.request.Request(f"https://openrouter.ai/api/v1/videos/{vid}/content?index=0",
    headers={"Authorization":f"Bearer {key}"})
data = urllib.request.urlopen(dl,timeout=120).read()
open("comic.mp4","wb").write(data)
print("saved comic.mp4",len(data))
