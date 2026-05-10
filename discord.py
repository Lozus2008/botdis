import discord
import re
import os

# Cấu hình
TOKEN = os.environ[MTUwMjk4NDk4MzY2NzY3MTE0MA.GOVzbQ.n1otgG504GLqyIdyFa9pXJu-ke2kEpEasxinl4

]
SOURCE_CHANNEL_ID = 1411414144598409317  # ID kênh nguồn (nơi thông báo acc)
DEST_CHANNEL_ID = 1487353828394139648    # ID kênh của bạn (nơi nhận kết quả lọc)

intents = discord.Intents.default()
intents.message_content = True  # Quan trọng: Phải bật để đọc nội dung chat

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot đã sẵn sàng với tên: {client.user}')

@client.event
async def on_message(message):
    # Tránh bot tự đọc tin nhắn của chính nó
    if message.author == client.user:
        return

    # Chỉ lọc tin nhắn từ kênh mục tiêu
    if message.channel.id == SOURCE_CHANNEL_ID:
        content = message.content
        
        # 1. Tìm tên Player sau chữ "Player: " (Dùng Regex để lấy nội dung trong ngoặc kép)
        # Regex này tìm mẫu Player: "tên_bất_kỳ"
        player_match = re.search(r'Player:\s*"([^"]+)"', content)
        
        # 2. Tìm tất cả các từ có chứa chữ "serum" (không phân biệt hoa thường)
        serum_matches = re.findall(r'\b\w*serum\w*\b', content, re.IGNORECASE)

        # Kiểm tra nếu khớp điều kiện thì mới xử lý
        if player_match or serum_matches:
            dest_channel = client.get_channel(DEST_CHANNEL_ID)
            
            response = "🔍 **Kết quả lọc tin nhắn mới:**\n"
            if player_match:
                response += f"👤 **Player:** `{player_match.group(1)}`\n"
            
            if serum_matches:
                response += f"🧪 **Serum liên quan:** {', '.join(serum_matches)}\n"
            
            response += f"🔗 [Đi đến tin nhắn gốc]({message.jump_url})"
            
            await dest_channel.send(response)

client.run(TOKEN)