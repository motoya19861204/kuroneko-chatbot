from PIL import Image

# 画像を開く
img = Image.open('Neko-up.jpg')
w, h = img.size

# 正方形のサイズを決定（長い方に合わせるか、短い方に合わせるか）
# アイコンなので、全体が収まるようにパディング（余白を追加）する
size = max(w, h)
new_img = Image.new('RGB', (size, size), (255, 255, 255)) # 白背景
# 中央に貼り付け
new_img.paste(img, ((size - w) // 2, (size - h) // 2))

# 保存
new_img.resize((512, 512)).save('apple-touch-icon.png')
print("Square icon generated successfully.")
