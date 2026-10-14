import random
import discord
from discord import app_commands

# Thiết lập Intents cần thiết cho Bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Từ điển lưu số xu ảo của người chơi: { user_id: so_xu }
# Mặc định người chơi mới sẽ có 0 xu
user_balances = {}


def get_balance(user_id: int) -> int:
  if user_id not in user_balances:
    user_balances[user_id] = 0  # Không còn tặng 1000 xu nữa, mặc định là 0
  return user_balances[user_id]


@client.event
async def on_ready():
  await tree.sync()
  print(f"Bot đã đăng nhập thành công dưới tên: {client.user}")


# Lệnh kiểm tra số dư xu hiện tại
@tree.command(name="sodu", description="Kiểm tra số dư xu ảo của bạn")
async def sodu(interaction: discord.Interaction):
  balance = get_balance(interaction.user.id)
  await interaction.response.send_message(
      f"💰 **{interaction.user.name}** đang có: **{balance:,} xu**",
      ephemeral=True,
  )


# Lệnh chơi Tài Xỉu
@tree.command(name="taixiu", description="Đặt cược Tài hoặc Xỉu")
@app_commands.choices(
    lua_chon=[
        app_commands.Choice(name="Tài (1)", value="tai"),
        app_commands.Choice(name="Xỉu (2)", value="xiu"),
    ]
)
@app_commands.describe(
    lua_chon="Chọn Tài hoặc Xỉu", so_xu="Số lượng xu bạn muốn cược"
)
async def taixiu(
    interaction: discord.Interaction, lua_chon: str, so_xu: int
):
  user_id = interaction.user.id
  balance = get_balance(user_id)

  # Kiểm tra số xu hợp lệ
  if so_xu <= 0:
    await interaction.response.send_message(
        "❌ Số xu cược phải lớn hơn 0!", ephemeral=True
    )
    return

  if so_xu > balance:
    await interaction.response.send_message(
        f"❌ Bạn không đủ xu! Số dư hiện tại của bạn chỉ có **{balance:,} xu**.",
        ephemeral=True,
    )
    return

  # Tiến hành lắc 3 viên xúc xắc (mỗi viên từ 1 đến 6)
  dice1 = random.randint(1, 6)
  dice2 = random.randint(1, 6)
  dice3 = random.randint(1, 6)
  total = dice1 + dice2 + dice3

  # Xác định kết quả Tài hay Xỉu
  if 4 <= total <= 10:
    ket_qua = "xiu"
    ket_qua_text = "XỈU"
  elif 11 <= total <= 17:
    ket_qua = "tai"
    ket_qua_text = "TÀI"
  else:
    ket_qua = "xiu" if total <= 10 else "tai"
    ket_qua_text = "XỈU" if total <= 10 else "TÀI"

  # Tạo chuỗi hiển thị xúc xắc bằng emoji
  dice_emojis = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
  dice_str = f"{dice_emojis[dice1]} {dice_emojis[dice2]} {dice_emojis[dice3]}"

  # Kiểm tra thắng hay thua
  embed = discord.Embed(
      title="🎲 KẾT QUẢ TÀI XỈU 🎲", color=discord.Color.gold()
  )
  embed.add_field(
      name="Lượt cược",
      value=f"Người chơi: {interaction.user.mention}\nLựa chọn: **{lua_chon.upper()}**\nCược: **{so_xu:,} xu**",
      inline=False,
  )

  if lua_chon == ket_qua:
    user_balances[user_id] += so_xu
    embed.add_field(
        name="Kết quả lắc",
        value=f"{dice_str} (Tổng: **{total}** - **{ket_qua_text}**)",
        inline=False,
    )
    embed.add_field(
        name="Thắng cược 🎉",
        value=f"Chúc mừng! Bạn đã thắng **+{so_xu:,} xu**.\nSố dư mới: **{user_balances[user_id]:,} xu**",
        inline=False,
    )
    embed.color = discord.Color.green()
  else:
    user_balances[user_id] -= so_xu
    embed.add_field(
        name="Kết quả lắc",
        value=f"{dice_str} (Tổng: **{total}** - **{ket_qua_text}**)",
        inline=False,
    )
    embed.add_field(
        name="Thua cược 😢",
        value=f"Rất tiếc! Bạn đã mất **-{so_xu:,} xu**.\nSố dư mới: **{user_balances[user_id]:,} xu**",
        inline=False,
    )
    embed.color = discord.Color.red()

  await interaction.response.send_message(embed=embed)


# Thay 'TOKEN_CUA_BAN' bằng Token Bot Discord thực tế của bạn
client.run("CHUA_CO_TOKEN")
from keep_alive import keep_alive

# Gọi hàm này ngay trước khi bot run
keep_alive()

# Code chạy bot của bạn ở dưới (Ví dụ: client.run('TOKEN'))
