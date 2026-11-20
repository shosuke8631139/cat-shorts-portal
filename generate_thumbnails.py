import os
import re
import subprocess

VIDEO_DIR = r"C:\Users\kurro\Desktop\猫ショート動画_完成品まとめ"
OUT_DIR = r"C:\Users\kurro\.gemini\antigravity\brain\48810adb-2838-4770-a5c3-bcc3461ad3c4\scratch\cat_shorts_portal\thumbnails"

os.makedirs(OUT_DIR, exist_ok=True)

files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]

for f in files:
    if f.startswith('初期テスト版'):
        continue
    
    vid_id = None
    if f.startswith('豪華完全版'):
        vid_id = 999
    else:
        m = re.match(r'第(\d+)弾', f)
        if m:
            vid_id = int(m.group(1))
            
    if vid_id is None:
        continue
        
    in_path = os.path.join(VIDEO_DIR, f)
    out_path = os.path.join(OUT_DIR, f"thumb_{vid_id}.jpg")
    
    # 冒頭1.2秒（画像とタイトルが綺麗に出ているフレーム）を抽出
    # 405x720 の軽量JPEG
    cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:01.200",
        "-i", in_path,
        "-vframes", "1",
        "-vf", "scale=405:720",
        "-q:v", "3",
        "-threads", "2",
        out_path
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"OK: thumb_{vid_id}.jpg from {f}")
    else:
        # 1.2秒で取れない場合は0.5秒でリトライ
        cmd[3] = "00:00:00.500"
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0:
            print(f"OK (retry): thumb_{vid_id}.jpg from {f}")
        else:
            print(f"FAIL: {f}")

print("All thumbnails extracted successfully!")
