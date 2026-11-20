import os
import re
import json

DESKTOP_DIR = r"C:\Users\kurro\Desktop\猫ショート動画_完成品まとめ"
TXT_PATH = os.path.join(DESKTOP_DIR, "動画一覧と説明.txt")
PORTAL_DIR = r"C:\Users\kurro\.gemini\antigravity\brain\48810adb-2838-4770-a5c3-bcc3461ad3c4\scratch\cat_shorts_portal"

# 全38作品の確定Catbox URL
catbox_urls = {
    1: "https://files.catbox.moe/jtlflc.mp4",
    2: "https://files.catbox.moe/2ca114.mp4",
    3: "https://files.catbox.moe/1iv0dx.mp4",
    4: "https://files.catbox.moe/1v1xau.mp4",
    5: "https://files.catbox.moe/txqwr1.mp4",
    6: "https://files.catbox.moe/fksvt7.mp4",
    7: "https://files.catbox.moe/c5mpjj.mp4",
    8: "https://files.catbox.moe/ck8i1j.mp4",
    9: "https://files.catbox.moe/w0er65.mp4",
    10: "https://files.catbox.moe/vnfvlq.mp4",
    11: "https://files.catbox.moe/rwfwkx.mp4",
    12: "https://files.catbox.moe/6d11oh.mp4",
    13: "https://files.catbox.moe/ut9uii.mp4",
    14: "https://files.catbox.moe/ikkis7.mp4",
    15: "https://files.catbox.moe/ia4syv.mp4",
    16: "https://files.catbox.moe/czdzru.mp4",
    17: "https://files.catbox.moe/t6pxly.mp4",
    18: "https://files.catbox.moe/1fz52b.mp4",
    19: "https://files.catbox.moe/ed4rma.mp4",
    20: "https://files.catbox.moe/et7nsx.mp4",
    21: "https://files.catbox.moe/sj7k4e.mp4",
    22: "https://files.catbox.moe/glt002.mp4",
    23: "https://files.catbox.moe/az84us.mp4",
    24: "https://files.catbox.moe/5kz3em.mp4",
    25: "https://files.catbox.moe/x8jybb.mp4",
    26: "https://files.catbox.moe/ghjq19.mp4",
    27: "https://files.catbox.moe/c79uq8.mp4",
    28: "https://files.catbox.moe/s62wx7.mp4",
    29: "https://files.catbox.moe/cfsaof.mp4",
    30: "https://files.catbox.moe/23dmmj.mp4",
    31: "https://files.catbox.moe/5gupvc.mp4",
    32: "https://files.catbox.moe/9ng9a5.mp4",
    33: "https://files.catbox.moe/clie1m.mp4",
    34: "https://files.catbox.moe/iyswen.mp4",
    35: "https://files.catbox.moe/lwe0e8.mp4",
    36: "https://files.catbox.moe/4aodpa.mp4",
    37: "https://files.catbox.moe/fno817.mp4",
    999: "https://files.catbox.moe/5rychw.mp4"
}

with open(TXT_PATH, "r", encoding="utf-8") as f:
    raw_text = f.read()

blocks = re.split(r"\n(?=\d+\.\s*【第|\★\s*【豪華完全版】)", raw_text)

items = []
for b in blocks:
    b = b.strip()
    if not b:
        continue
    
    part_m = re.search(r"【第(\d+)弾", b)
    is_special = "豪華完全版" in b
    
    if part_m:
        pnum = int(part_m.group(1))
    elif is_special:
        pnum = 999
    else:
        continue
    
    file_m = re.search(r"【.+?】(.+?\.mp4)", b)
    fname = file_m.group(1).strip() if file_m else ""
    
    sec_m = re.search(r"\((\d+秒|\d+分\d+秒)\)", fname)
    dur = sec_m.group(1) if sec_m else ""
    
    title = fname.replace(".mp4", "")
    if dur:
        title = title.replace(f"({dur})", "").strip()
    
    theme_m = re.search(r"テーマ:\s*(.+)", b, re.DOTALL)
    desc = ""
    if theme_m:
        desc = theme_m.group(1).strip()
    elif is_special:
        sm = re.search(r"-\s*(.+)", b)
        if sm:
            desc = sm.group(1).strip()
            
    # タイトルから第XX弾プレフィックスを綺麗に整える
    display_title = re.sub(r"^第\d+弾_", "", title)
    
    hashtags = "#猫 #猫のいる暮らし #保護猫 #猫あるある #癒やし猫 #Shorts #YouTubeShorts #TikTok猫"
    
    # SNSステータスマッピングの取得
    MASTER_PATH = r"C:\Users\kurro\video-publisher\data\sns_post_status_master.json"
    with open(MASTER_PATH, "r", encoding="utf-8") as mf:
        master_data = json.load(mf)
    
    # 弾数またはタイトルからマスターデータを検索
    ig_info = {"status": "未確認"}
    x_info = {"status": "未確認"}
    for v_entry in master_data.values():
        if v_entry["group"] == "猫ショート動画":
            v_fname = v_entry["filename"]
            if pnum == 999 and "豪華完全版" in v_fname:
                ig_info = v_entry["instagram"]
                x_info = v_entry["x"]
                break
            elif pnum != 999 and f"第{pnum}弾" in v_fname:
                ig_info = v_entry["instagram"]
                x_info = v_entry["x"]
                break

    items.append({
        "id": pnum,
        "partLabel": "豪華完全版" if pnum == 999 else f"第{pnum}弾",
        "title": title,
        "displayTitle": display_title,
        "duration": dur,
        "description": desc,
        "videoUrl": catbox_urls.get(pnum, ""),
        "thumbnail": f"thumbnails/thumb_{pnum}.jpg",
        "instagram": ig_info,
        "x": x_info,
        "hashtags": hashtags,
        "postText": f"{title}\n\n{desc}\n\n{hashtags}"
    })

# 1..37, 999 順にソート
items.sort(key=lambda x: x["id"])

print(f"Built {len(items)} items.")
for it in items:
    print(f"[{it['partLabel']}] {it['displayTitle']} ({it['duration']}) -> {it['videoUrl']}")

# JSON出力
out_file = os.path.join(PORTAL_DIR, "videos_data.js")
with open(out_file, "w", encoding="utf-8") as f:
    f.write("const CAT_VIDEOS = " + json.dumps(items, ensure_ascii=False, indent=2) + ";\n")

print(f"\nSaved {out_file}")
