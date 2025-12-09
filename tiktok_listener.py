import asyncio
import aiohttp
import sys
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent

# --- CONFIGURATION ---
DEFAULT_USERNAME = "@saudimarket_ai" # Replace with your target username
LOCAL_API_URL = "http://127.0.0.1:5000/api/chat"
LIVE_DATA_URL = "http://127.0.0.1:5000/api/live_data"

# Get username from CLI or default
target_user = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USERNAME

# Initialize Client
client = TikTokLiveClient(unique_id=target_user)

async def get_active_persona():
    """Fetch the current 'Spotlight' strategy from the app."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(LIVE_DATA_URL) as resp:
                data = await resp.json()
                if data and 'leaderboard' in data and len(data['leaderboard']) > 0:
                    return data['leaderboard'][0]['name']
    except Exception as e:
        print(f"⚠️ Could not fetch active persona: {e}")
    return "General"

async def send_to_ai(username, text):
    """Forward the question to the Flask AI API."""
    active_persona = await get_active_persona()
    
    print(f"🤖 Sending to {active_persona}...")
    
    async with aiohttp.ClientSession() as session:
        payload = {
            "persona": active_persona,
            "message": f"User {username} asks: {text}" 
        }
        try:
            async with session.post(LOCAL_API_URL, json=payload) as resp:
                data = await resp.json()
                print(f"✅ AI Responded: {data.get('response', '')[:50]}...")
        except Exception as e:
            print(f"❌ API Error: {e}")

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"✅ Connected to Room ID: {client.room_id}")

@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    comment = event.comment
    user = event.user.nickname
    
    print(f"💬 {user}: {comment}")
    
    # --- FILTER LOGIC ---
    # Only process longer comments that might be questions
    if len(comment) > 5:
        # Check if it looks like a question or contains keywords
        keywords = ["توقع", "سهم", "بيع", "شراء", "رايك", "ليش", "كم", "??", "؟"]
        if any(k in comment for k in keywords):
            print(f"➡️ Question detected! Forwarding...")
            await send_to_ai(user, comment)

if __name__ == '__main__':
    print(f"🎧 Connecting to TikTok Live: {target_user}")
    print("Press Ctrl+C to stop...")
    client.run()
