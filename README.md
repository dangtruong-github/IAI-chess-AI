# IAI-chess-AI

## Hướng dẫn mở chương trình:

B1: Cài đặt phần mềm Visual Studio Code + python

B2: Clone repo chứa code của chương trình bằng cú pháp:
```
git clone https://github.com/anhnd1/IAI-chess-AI
```

B4: Mở chương trình Visual Studio Code, vào thư mục chứa repo đã clone ở trên, và cài đặt thư viện pygame + chess qua cú pháp sau trong terminal:
```
pip install pygame
pip install chess
```

B5: Chạy file ```main.py``` để bắt đầu chơi:

## Hướng dẫn chơi:

Sau khi mở thành công chương trình, màn hình sẽ hiện ra cửa sổ sau:

![image](https://github.com/anhnd1/IAI-chess-AI/assets/91740502/324668d2-1452-4ad2-8472-378a128d30c4)

Có 3 chế độ chơi: người với người, người với bot, bot với bot.

Ở chế độ người với bot, chọn vua đen để đi bên đen, vua trắng để đi bên trắng.
Quân trắng luôn ở phía dưới, chưa hỗ trợ xoay bàn cờ.

Với chế độ chơi có người tham gia, người chơi được phép quay trở lại nước đi trước.