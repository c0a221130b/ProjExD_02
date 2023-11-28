import sys
import pygame as pg
import random 

WIDTH, HEIGHT = 1600, 900

delta = {  # 練習3
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0)
    }


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外の判定をし、真理値タプルを返す関数
    引数 rct: 効果とんor爆弾SurfaceのRect
    戻り値 : 横方向、縦方向は見出し判定結果(画面内 : True / 画面外 : False)
    """
    yoko, tate = True, True
    
    if rct.left < 0 or WIDTH < rct.right:  # 横方向は見出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向は見出し判定
        tate = False
    return (yoko, tate)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_over_img = pg.image.load("ex02/fig/8.png")

    kk_rotozoom = {  #追加機能1
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 2.0),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 2.0),
        (0, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90, 2.0),
        (+5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 2.0),
        (+5, 0): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 0, 2.0),
        (+5, +5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 2.0),
        (0, +5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -90, 2.0),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 2.0)
    }
        
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_over_img = pg.transform.rotozoom(kk_over_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    
    # 追加機能2
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))  # 練習1 透明のsurfaceをつける
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  #空白の統一 #1
        bb_img.set_colorkey(0,0)
        bb_imgs.append(bb_img)
        
    bb_rct = bb_imgs[0].get_rect()  # 爆弾SurfaceのRectを抽出する
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, WIDTH)
    
    vx, vy = +5, +5


    clock = pg.time.Clock()
    tmr = 0
    flag = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bb_rct):  #練習5 こうかとんと爆弾の衝突判定 追加機能3
            flag = 1


        key_lst = pg.key.get_pressed()
        sum_move = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_move[0] += tpl[0]
                sum_move[1] += tpl[1]

        screen.blit(bg_img, [0, 0])  #背景

        for k, itm in kk_rotozoom.items():  # 追加機能1
            if sum_move == list(k):
                kk_img = itm

        kk_rct.move_ip(sum_move[0], sum_move[1])  # 練習3 こうかとん移動

        if flag:  # 追加機能3
            kk_img = kk_over_img
        screen.blit(kk_img, kk_rct)  # こうかとんをblit

        if check_bound(kk_rct) != (True, True):  # 練習4 こうかとんの位置判定
            kk_rct.move_ip(-sum_move[0], -sum_move[1])

        # 追加機能2
        bb_img = bb_imgs[min(tmr//100, 9)]
        
        yoko, tate = check_bound(bb_rct)  # 練習4 爆弾の位置判定
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        bb_rct.move_ip(vx, vy)  # 練習2 爆弾
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(60)
        
        # 追加機能3
        if flag:
            clock.tick(1)
            print("Game Over")
            return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()