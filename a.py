
import pygame#3つインポートする
import sys
import random

# Pygameの初期設定
pygame.init()

# 画面サイズ
screen_width = 800
screen_height = 600

# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# ゲーム画面の設定
screen = pygame.display.set_mode((screen_width, screen_height))#10,11行で設定したものを使う
pygame.display.set_caption("弾幕を避けろ！")

# 時間管理
clock = pygame.time.Clock()

# 背景画像の読み込みとサイズ調整
background = pygame.image.load(r'C:/Users/tfmyr/OneDrive/デスクトップ/python-expert/lesson20/images.jpg')#同じフォルダに入った背景画像を読み込み


background = pygame.transform.scale(background, (screen_width, screen_height))#サイズ調整

# プレイヤーのクラス
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))#自機のサイズ
        self.image.fill(RED)#カラー
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.centery = screen_height // 2  # 画面の中央に配置
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        # プレイヤーの移動
        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:#左キーを押したら左へ
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:#右キーで右へ
            self.speed_x = 5
        if keystate[pygame.K_UP]:#上キーで上へ
            self.speed_y = -5
        if keystate[pygame.K_DOWN]:#下キーで下へ
            self.speed_y = 5
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # 画面の外に出ないようにする
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
        if self.rect.top < 0:
            self.rect.top = 0

# 弾幕のクラス
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))#敵のサイズ
        self.image.fill(WHITE)#色
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(screen_width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height + 10:
            self.rect.x = random.randrange(screen_width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 8)

# スプライトグループの設定
all_sprites = pygame.sprite.Group()#スプライトを統括
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# 初期の弾幕を生成
for _ in range(90):
    bullet = Bullet()
    all_sprites.add(bullet)
    bullets.add(bullet)

# 音楽の読み込みと再生
pygame.mixer.music.load('C:/Users/tfmyr/OneDrive/デスクトップ/python-expert/lesson20/Used_car_fair.mp3')#使う音楽を読み込み

pygame.mixer.music.play(loops=-1)  # loops=-1で無限ループ

# ゲームループ
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # スプライトの更新
    all_sprites.update()

    # プレイヤーと弾幕の衝突判定
    hits = pygame.sprite.spritecollide(player, bullets, False)#スプライトをつかう
    if hits:
        running = False

    # 描画
    screen.blit(background, (0, 0))  # 背景を描画
    all_sprites.draw(screen)  # スプライトを描画

    # 画面更新
    pygame.display.flip()

    # FPS
    clock.tick(45)

pygame.quit()
sys.exit()
