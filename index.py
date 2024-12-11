from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "q2plBD0CvtizDgODNzFSG+CwEqgqB91YeSayuU2DQ56rfG5rNzr9nIofa38BOTMdhFx4vc58SLNh+9UXPoUBIRta/aT10i3BXyk98WVdoNr7KwHwl4+lLNlVePk6dG1JccwQP1Sj8m8uHJD7PapXkAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "c416f3a07e8c6da7cce101b216b80b2a"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# เก็บสถานะผู้ใช้ชั่วคราว
user_state = {}

# ข้อมูลฮาร์ดโค้ดตัวอย่าง
data = {
    "music": {
        "thai": {
            "top hits": [
                "Rain wedding - Jeff Satur",
                "DAY ONE - PUN",
                "Spring(ดอกไม้ที่รอฝน) - TheToy, NONTTANONT",
                "จดจำ Only Monday",
                "Your Ever – Cocktail feat.Q Flure"
            ],
            "tpop": [
                "Situationship – 4EVE",
                "LIAR-BUS",
                "WATCH YOUR STEP-BUS",
                "TEEDEE TADA – DIAMOND NARAKORN",
                "TRUST ME- LYKN",
                "Get to know me – MXFRUIT"
            ],
            "rock band": [
                "Free Fall- Slot Machine",
                "ฟังดูง่ายง่าย- Silly fools",
                "ทบทวน - 25hours",
                "ช่างมัน - COCKTAIL",
                "นิทาน - Musketeers"
            ],
            "folk song": [
                "แก้มน้องนางนั้นเเดงกว่าใคร – เขียนไขและวานิช",
                "อะไรเอ่ยสวยกว่า…ทะเล – WHATFALSE",
                "วันทั้งวันฉันเพ้อถึงแต่เธอ – ฮันเตอร์",
                "ดวงดาวแห่งรัก – Dr.fuu",
                "นางงามตู้กระจก – คาราบาว"
            ]
        },
        "china": {
            "c-pop": [
                "Change – E.so 瘦子",
                "Focus – 刘宇",
                "Bad Girl Behave – Karencici",
                "Trick or treat – AIM",
                "小城夏天-LBI利比"
            ],
            "ost": [
                "Forever Star（《偷偷藏不住》- 張洢豪",
                "Moonlight (月夜) - Shuang Sheng, Yao Yang (双笙, 妖扬)",
                "Upwards to the Moon(左手指月)- Sa Dingding萨顶顶",
                "Penannular Love 《玦恋》- Zhou Shen (周深)",
                "Falling You- 曾可妮 · 都智文"
            ],
            "tiktok hits": [
                "全世界都快乐除了我自己-愉快涵&ZenoG",
                "洛希没有极限 – XMASwu",
                "起舞- 艾热",
                "热爱105°的你",
                "少年"
            ]
        }
    },
    "movie": {
        "thai": {
            "animation": [
                "9ศาสตรา",
                "The Giant King ยักษ์",
                "ก้านกล้วย",
                "Echo Planet เอคโค่ จิ๋วก้องโลก",
                "Khun Thong Daeng: The Inspirations คุณทองแดง"
            ],
            "series": [
                "บุพเพสันนิวาส",
                "The Gifted",
                "แนนโน๊ะ",
                "น้ำตากามเทพ",
                "High School Frenemy มิตรภาพคราบศัตรู"
            ],
            "movie": [
                "วิมานหนาม",
                "หลานม่า",
                "ฉลาดเกมส์โกง",
                "พี่มากพระโขนง",
                "ไอฟาย…แต๊งกิ้วเลิฟยู้",
                "คิดถึงวิทยา"
            ]
        },
        "china": {
            "animation": [
                "ตำนานจอมยุทธ์ภูตถังซาน Soul Land",
                "หน่วยเทพอสูร Slay the god",
                "สัประยุทธ์ทะลุฟ้า Fight Break Sphere",
                "ฝืนลิขิตฟ้า ขอข้าเป็นเซียน Renegade Immortal",
                "จูเซียน กระบี่เทพสังหาร Jade Dynasty"
            ],
            "series": [
                "Hidden love",
                "The Untamed陈情令",
                "Till The End Of The Moon",
                "Put Your Head On My Shoulder",
                "A Love So Beautiful",
                "Who Rules The World"
            ],
            "movie": [
                "One and Only",
                "Monster Hunt",
                "The Battle at Lake Changjin",
                "Wolf Warrior 2",
                "Ne zha",
                "The Wandering Earth"
            ]
        }
    },
    "travel": {
        "thai": {
            "summer": {
                "Bangkok": {
                    "places": [
                        "วัดพระแก้ว",
                        "วัดอรุณราชวรารามราชวรมหาวิหาร",
                        "วัดสระเกศราชวรมหาวิหาร (ภูเขาทอง)",
                        "พิพิธภัณฑสถานแห่งชาติพระนคร",
                        "ตลาดน้ำคลองลัดมะยม"
                    ],
                    "menu": [
                        "ข้าวตอกตั้ง",
                        "น้ำพริกลงเรือ",
                        "แกงรัญจวน",
                        "ข้าวแช่ชาววัง"
                    ]
                },
                "Chonburi": {
                    "places": [
                        "หาดบางแสน",
                        "เขาสามมุก",
                        "เกาะล้าน (Pattaya)",
                        "หาดจอมเทียน (Pattaya)",
                        "หาดบางเสร่ (สัตหีบ)",
                        "เกาะแสมสาร (สัตหีบ)"
                    ],
                    "menu": [
                        "ข้าวหลามหนองมน",
                        "แจงลอน",
                        "ไก่หุบบอน",
                        "ข้าวแห้งเป็ด",
                        "หมึกไข่ผัดน้ำดำ",
                        "หอยจ้อปู"
                    ]
                },
                "Krabi": {
                    "places": [
                        "อ่าวนาง (Nang Bay)",
                        "หาดนพรัตน์ธารา (Nopparat Thara Beach)",
                        "หมู่เกาะพีพี (Phi Phi Islands)"
                    ],
                    "menu": [
                        "ปลาจุกเครื่อง",
                        "หอยชักตีน",
                        "แกงส้มปลากะพงยอดมะพร้าว",
                        "ขนมจีนน้ำยาปูใส่ไก่ทอด",
                        "น้ำพริกผักเหนาะ"
                    ]
                }
            },
            "rainy": {
                "Nakhon Nayok": {
                    "places": [
                        "อุทยานวังตะไคร้",
                        "เขาช่องลม",
                        "ล่องแก่งแม่น้ำนครนายก",
                        "น้ำตกสาริกา"
                    ],
                    "menu": [
                        "น้ำพริกป่ามะดัน",
                        "ขนมข้าวกระยาคู",
                        "ต้มยำปลาคัง",
                        "ปลาดูสมุนไพร"
                    ]
                }
            },
            "winter": {
                "Chiang Mai": {
                    "places": [
                        "Doi Inthanon",
                        "ดอยหลวงเชียงดาว",
                        "วัดอุโมงค์ (วัดสวนพุทธธรรม)",
                        "วัดพระธาตุดอยคำ",
                        "วัดต้นเกว๋น"
                    ],
                    "menu": [
                        "ผักกาดจอ",
                        "น้ำพริกหนุ่ม",
                        "ไส้อั่ว",
                        "ลาบคั่ว",
                        "ขนมจีนน้ำเงี้ยว",
                        "จิ้นส้ม"
                    ]
                }
            }
        },
        "china": {
            "summer": {
                "三亚 (Sanya)": {
                    "places": [
                        "หาดซันย่า",
                        "อ่าวหย่าหลง",
                        "เกาะหนานซาน",
                        "เขตอนุรักษ์ลิงเกาะลู่หุ่ยโถว"
                    ],
                    "menu": [
                        "椰小鸡 (ไก่ต้มน้ำมะพร้าว)",
                        "椰子饭 (ข้าวอบมะพร้าว)",
                        "阿三靓汤 (ซุปพิเศษของอาสาน)",
                        "虾饼 (ขนมปังกุ้ง)"
                    ]
                }
            },
            "rainy": {
                "云南-昆明、大理 (Kunming/Dali)": {
                    "places": [
                        "ทะเลสาบเตียนฉือ",
                        "เขาหิมะมังกรหยก",
                        "เมืองโบราณต้าหลี่"
                    ],
                    "menu": [
                        "鲜花饼 (ขนมดอกไม้)",
                        "手抓饭 (ข้าวมือ)",
                        "过桥米线 (เส้นข้ามสะพาน)",
                        "包浆豆腐 (เต้าหู้ตุ๋น)"
                    ]
                }
            },
            "winter": {
                "黑龙江-哈尔滨 (Harbin)": {
                    "places": [
                        "เทศกาลน้ำแข็งฮาร์บิน",
                        "เกาะสุริยะ",
                        "สวนสัตว์หิมะ"
                    ],
                    "menu": [
                        "锅包肉 (หมูชุบแป้งทอด)",
                        "杀猪菜 (ซุปหมู)",
                        "哈尔滨熏鸡 (ไก่รมควันฮาร์บิน)",
                        "铁锅烀饼 (ขนมปังฮาร์บิน)"
                    ]
                }
            }
        }
    }
}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_msg = event.message.text.strip().lower()

    if user_id not in user_state:
        user_state[user_id] = {"step": 0, "category": None, "country": None, "season": None}

    state = user_state[user_id]

    if user_msg == "เริ่มใหม่" or user_msg == "แนะนำ":
        state.update({"step": 0, "category": None, "country": None, "season": None})
        reply_text = "เริ่มใหม่! คุณต้องการแนะนำอะไร: เพลง, หนัง หรือสถานที่ท่องเที่ยว?"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        return

    if state["step"] == 0:
        if "เพลง" in user_msg:
            state["category"] = "music"
            reply_text = "เลือกประเทศ: ไทย หรือ จีน?"
            state["step"] = 1
        elif "หนัง" in user_msg:
            state["category"] = "movie"
            reply_text = "เลือกประเทศ: ไทย หรือ จีน?"
            state["step"] = 1
        elif "สถานที่ท่องเที่ยว" in user_msg:
            state["category"] = "travel"
            reply_text = "คุณต้องการท่องเที่ยวประเทศใด: ไทย หรือ จีน?"
            state["step"] = 1
        else:
            reply_text = "โปรดระบุ: เพลง, หนัง หรือสถานที่ท่องเที่ยว"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        return

    if state["step"] == 1:
        category = state["category"]
        if category == "music":
            if "ไทย" in user_msg:
                state["country"] = "thai"
                reply_text = "เลือกหมวดเพลง: top hits, tpop, rock band หรือ folk song?"
                state["step"] = 2
            elif "จีน" in user_msg:
                state["country"] = "china"
                reply_text = "เลือกหมวดเพลง: cpop, ost หรือ tiktok hits?"
                state["step"] = 2
            else:
                reply_text = "โปรดระบุประเทศ: ไทย หรือ จีน"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return

        elif category == "movie":
            if "ไทย" in user_msg:
                state["country"] = "thai"
                reply_text = "เลือกประเภทหนัง: animation, series หรือ movie?"
                state["step"] = 2
            elif "จีน" in user_msg:
                state["country"] = "china"
                reply_text = "เลือกประเภทหนัง: animation, series หรือ movie?"
                state["step"] = 2
            else:
                reply_text = "โปรดระบุประเทศ: ไทย หรือ จีน"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return

        elif category == "travel":
            if "ไทย" in user_msg:
                state["country"] = "thai"
                reply_text = "คุณต้องการเลือกฤดูใด: ร้อน, ฝน หรือ หนาว?"
                state["step"] = 2
            elif "จีน" in user_msg:
                state["country"] = "china"
                reply_text = "คุณต้องการเลือกฤดูใด: ร้อน, ฝน หรือ หนาว?"
                state["step"] = 2
            else:
                reply_text = "โปรดระบุประเทศ: ไทย หรือ จีน"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return

    if state["step"] == 2:
        category = state["category"]
        country = state.get("country")

        if category == "music":
            # ตรวจสอบหมวดเพลง
            if user_msg in data["music"][country]:
                items = "\n".join(f"- {item}" for item in data["music"][country][user_msg])
                # เพิ่มคำอธิบายให้เลือกหมวดอื่นๆ ต่อได้
                all_categories = ", ".join(data["music"][country].keys())
                reply_text = (
                    f"แนะนำเพลงในหมวด {user_msg}:\n{items}\n\n"
                    f"คุณสามารถพิมพ์หมวดอื่นในหมวดหมู่เพลง {country} ได้เลย เช่น {all_categories}\n"
                    f"หรือหากต้องการเริ่มใหม่ พิมพ์ 'เริ่มใหม่' หรือ 'แนะนำ'"
                )
            else:
                reply_text = "ไม่มีข้อมูลในหมวดหมู่นี้\nคุณสามารถพิมพ์หมวดอื่น หรือพิมพ์ 'เริ่มใหม่' เพื่อเริ่มต้นใหม่"

            # ไม่ reset step ให้ผู้ใช้พิมพ์หมวดอื่นต่อได้
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return

        elif category == "movie":
            # ตรวจสอบประเภทหนัง
            if user_msg in data["movie"][country]:
                items = "\n".join(f"- {item}" for item in data["movie"][country][user_msg])
                all_categories = ", ".join(data["movie"][country].keys())
                reply_text = (
                    f"แนะนำหนังในหมวด {user_msg}:\n{items}\n\n"
                    f"คุณสามารถพิมพ์หมวดอื่นในหมวดหมู่หนัง {country} ได้เลย เช่น {all_categories}\n"
                    f"หรือหากต้องการเริ่มใหม่ พิมพ์ 'เริ่มใหม่' หรือ 'แนะนำ'"
                )
            else:
                reply_text = "ไม่มีข้อมูลในหมวดหมู่นี้\nคุณสามารถพิมพ์หมวดอื่น หรือพิมพ์ 'เริ่มใหม่' เพื่อเริ่มต้นใหม่"

            # ไม่ reset step ให้ผู้ใช้พิมพ์หมวดอื่นต่อได้
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return

        elif category == "travel":
            # ตรวจสอบฤดู
            season_map = {"ร้อน": "summer", "ฝน": "rainy", "หนาว": "winter"}
            if user_msg in season_map:
                state["season"] = season_map[user_msg]
                reply_text = f"เริ่มแนะนำสถานที่สำหรับฤดู{user_msg}ใน {state['country'].capitalize()}..."
                for province, details in data["travel"][state["country"]][state["season"]].items():
                    places = "\n".join(f"- {place}" for place in details["places"])
                    menu = "\n".join(f"- {dish}" for dish in details["menu"])
                    message = f"📍 จังหวัด/เมือง: {province}\n\n🏞️ สถานที่ท่องเที่ยว:\n{places}\n\n🍴 เมนูแนะนำ:\n{menu}"
                    line_bot_api.push_message(user_id, TextSendMessage(text=message))
                
                # แสดงฤดูที่มีให้เลือกทั้งหมด
                all_seasons = ", ".join(season_map.keys())
                reply_text += (
                    f"\nสิ้นสุดการแนะนำในฤดู{user_msg}!\n"
                    f"คุณสามารถพิมพ์ฤดูอื่นในประเทศ {state['country']} ได้ต่อ เช่น {all_seasons}\n"
                    f"หรือหากต้องการเริ่มใหม่ พิมพ์ 'เริ่มใหม่' หรือ 'แนะนำ'"
                )
            else:
                reply_text = "โปรดระบุฤดู: ร้อน, ฝน หรือ หนาว\nหากต้องการเริ่มใหม่ พิมพ์ 'เริ่มใหม่' หรือ 'แนะนำ'"

            # ไม่ reset step เพื่อให้ผู้ใช้สามารถพิมพ์ฤดูอื่นต่อได้
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
            return


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)