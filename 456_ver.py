from tkinter.constants import E
import numpy as np
import math
import tkinter as tk
import random
import time



class State(tk.Frame):

    def __init__(self,master=None,model=None):
        #ジカンケイソク
        self.start_time = time.time()

        #番手のPlayerを把握(Red or Yellow)
        self.Player_Color = "#FF0000"
        #クリック位置
        self.x = 0
        self.y = 0

        #ゲーム情報
        self.Player_A = "CPU"
        self.Player_B = "CPU"
        self.Turn = 0

        #選択した駒
        self.Choice_x = -1
        self.Choice_y = -1

        #盤面用変数
        self.width = 7
        self.height = 21
        self.info = 2

        #駒の数
        self.piece_num =10

        #駒の移動可能な場所を管理
        self.Can_Move_Points = []
        self.Checked_Points = []
        self.ReCheck_Points = []

        #盤面上の点（仮想の点を含む9×24で構成）
        self.Boad_dot=[]

        for i in range(self.width):
            tmp_list = []
            for j in range(self.height):
                tmp_list.append(Boad_Info())
            self.Boad_dot.append(tmp_list)

        #キャンバスの生成
        tk.Frame.__init__(self,master)
        self.c = tk.Canvas(self,width=524,height=524,highlightthickness=0)
        self.c.bind('<Button-1>',self.Player_turn)
        self.c.pack()
        
        #仮想の点を-1で初期化
        #初期化時に使う盤面外のマスをカウント
        self.out_Boad_dot = 0

        for i in range(self.width):
            for j in range(self.height):
                #上▼の盤面外を-1で初期化
                if j < self.out_Boad_dot:
                    self.Boad_dot[i][j].State_Dot=-1
                #間を-1に
                elif j%2 != i%2:
                    self.Boad_dot[i][j].State_Dot=-1
                #下▲の盤面外を-1で初期化
                elif j >= self.height-self.out_Boad_dot:
                    self.Boad_dot[i][j].State_Dot=-1

            if int(self.width/2) > i:
                self.out_Boad_dot += 1
            elif int(self.width/2) <= i:
                self.out_Boad_dot -= 1
        
        #Region指定
        #黄色(左上)
        step = 0
        for i in reversed(range(0,(int(self.width/2))+1)):
            step += 1
            count = 0
            for j in range(self.height):
                if count >= step:
                    pass
                elif self.Boad_dot[i][j].State_Dot != -1:
                   if i%2 == j%2:
                       count+=1
                       #regionの色を指定
                       if count != step:
                           self.Boad_dot[i][j].Region_Color = "#FFFF00"

        #赤色(左下)                
        step = 0
        for i in reversed(range(0,int((self.width/2))+1)):
            step += 1
            count = 0
            for j in reversed(range(self.height)):
                if count >= step:
                    pass
                elif self.Boad_dot[i][j].State_Dot != -1:
                   if i%2 == j%2:
                       count+=1
                        #regionの色を指定
                       if count != step:
                           self.Boad_dot[i][j].Region_Color = "#FF0000"
        
        #駒(盤面)の色を変更する
        #赤色(右上)
        step = 0
        for i in range(int(self.width/2),self.width):
            step += 1
            count = 0
            for j in range(self.height):
                if count >= step:
                    pass
                elif self.Boad_dot[i][j].State_Dot != -1:
                   if i%2 == j%2:
                       self.Boad_dot[i][j].Piece_Color = "#FF0000"
                       self.Boad_dot[i][j].State_Dot = 1
                       count+=1
                       #regionの色を指定
                       if count != step:
                           self.Boad_dot[i][j].Region_Color = "#FF0000"
        
                       

        #黄色(右下)
        step = 0
        for i in range(int(self.width/2),self.width):
            step += 1
            count = 0
            for j in reversed(range(self.height)):
                if count >= step:
                    pass
                elif self.Boad_dot[i][j].State_Dot != -1:
                   if i%2 == j%2:
                       self.Boad_dot[i][j].Piece_Color = "#FFFF00"
                       self.Boad_dot[i][j].State_Dot = 1
                       count+=1
                        #regionの色を指定
                       if count != step:
                           self.Boad_dot[i][j].Region_Color = "#FFFF00"
        
        #王の指定(2つだけなので決め打ち宣言)
        self.Boad_dot[self.width-1][0].are_you_king = True
        self.Boad_dot[self.width-1][self.height-1].are_you_king = True


        self.on_draw()


        #if self.Player_A == "CPU":
        #    self.Random_turn()

    #人間が操作する時の処理
    def Player_turn(self,event):
        #盤面の描画を呼び出し
        self.on_draw()

        if self.Turn == 0:
            if self.Player_A == "CPU":
                self.Turn+=1
                self.Random_turn()
                

        #駒選択
        #クリックされた座標を取得
        self.Click_x = event.x
        self.Click_y = event.y
        #座標から盤面の座標に変換
        self.Choice_x = round((self.Click_x -self.ini_x) / self.small_width)
        self.Choice_y = round((self.Click_y -self.ini_y) / (self.Small_Square_Edge/2))

        #選択された場所が盤面内かを確認
        if (self.Choice_x < 0 or self.Choice_x > self.width-1 or self.Choice_y < 0 or self.Choice_y > self.height-1):
            print("画面見てる?駒選択するんやで^^")
            return 
        elif (self.Boad_dot[self.Choice_x][self.Choice_y].State_Dot == -1):
            print("駒ない場所押してますね^^")
            return
        if (self.Boad_dot[self.Choice_x][self.Choice_y].Piece_Color == self.Player_Color ):        
            #選択した駒を強調表示
            self.draw_Select()

            #選択した駒を保存
            self.Berfor_Choice_x = self.Choice_x
            self.Berfor_Choice_y = self.Choice_y

            #移動可能リスト
            self.Can_Move_Points = []

            #確認済みリスト
            self.Checked_Points = [(self.Click_x,self.Click_y)]

            #再行動確認リスト
            self.ReCheck_Points = []

            #選択した駒の周辺6マスを取得
            self.arround_list = self.Get_Connection_Parh(self.Choice_x,self.Choice_y)
            self.Checked_Points.append((self.Choice_x,self.Choice_y))
            
            for x,y in self.arround_list:
                #駒がない場合
                if self.Boad_dot[x][y].State_Dot == 0:
                    self.Can_Move_Points.append((x,y))
                #駒存在時
                else:                   
                    if self.Boad_dot[self.Choice_x][self.Choice_y].are_you_king == True:
                        #王様の処理                        
                        #飛び越した先に駒があるのかを判定
                        Jump_Over_x = x + (x-self.Choice_x)
                        Jump_Over_y = y + (y-self.Choice_y)
                        while True:
                            if self.Check_Point_True(Jump_Over_x,Jump_Over_y):
                                if self.Boad_dot[Jump_Over_x][Jump_Over_y].State_Dot == 0:
                                    if not (((Jump_Over_x,Jump_Over_y)) in self.Checked_Points):
                                        self.Can_Move_Points.append((Jump_Over_x,Jump_Over_y))
                                        self.ReCheck_Points.append((Jump_Over_x,Jump_Over_y))
                                        self.Checked_Points.append((Jump_Over_x,Jump_Over_y))
                                        break
                                    else:
                                        break
                                else:
                                    Jump_Over_x = Jump_Over_x + (x-self.Choice_x)
                                    Jump_Over_y = Jump_Over_y + (y-self.Choice_y)
                            else:
                                break
                    
                    #飛び越す駒が王かどうかの判定
                    elif self.Boad_dot[x][y].are_you_king == False: 
                        #飛び越した先に駒があるのかを判定
                        Jump_Over_x = x + (x-self.Choice_x)
                        Jump_Over_y = y + (y-self.Choice_y)
                        if self.Check_Point_True(Jump_Over_x,Jump_Over_y):
                            if self.Boad_dot[Jump_Over_x][Jump_Over_y].State_Dot == 0:
                                if not (((Jump_Over_x,Jump_Over_y)) in self.Checked_Points):
                                    self.Can_Move_Points.append((Jump_Over_x,Jump_Over_y))
                                    self.ReCheck_Points.append((Jump_Over_x,Jump_Over_y))
                                    self.Checked_Points.append((Jump_Over_x,Jump_Over_y))


                
            #ここから動いた後にさらに飛び越す場所を探すが動く処理が未完成だから後回し
            while True:
                if (len(self.ReCheck_Points) == 0):
                    break
                #動いた後にさらに超えれるかを確認
                else:
                    self.arround_list = []
                    tmp_x,tmp_y = self.ReCheck_Points.pop(0)
                    self.arround_list = self.Get_Connection_Parh(tmp_x,tmp_y)

                    for x,y in self.arround_list:
                        #駒の存在を確認
                        if self.Boad_dot[x][y].State_Dot == 1:
                            if self.Boad_dot[self.Choice_x][self.Choice_y].are_you_king == True:
                                #王様の処理                        
                                #飛び越した先に駒があるのかを判定
                                Jump_Over_x = x + (x-tmp_x)
                                Jump_Over_y = y + (y-tmp_y)
                                while True:
                                    if self.Check_Point_True(Jump_Over_x,Jump_Over_y):
                                        if self.Boad_dot[Jump_Over_x][Jump_Over_y].State_Dot == 0:
                                            if not (((Jump_Over_x,Jump_Over_y)) in self.Checked_Points):
                                                self.Can_Move_Points.append((Jump_Over_x,Jump_Over_y))
                                                self.ReCheck_Points.append((Jump_Over_x,Jump_Over_y))
                                                self.Checked_Points.append((Jump_Over_x,Jump_Over_y))
                                                break
                                            else:
                                                break
                                        else:
                                            Jump_Over_x = Jump_Over_x + (x-tmp_x)
                                            Jump_Over_y = Jump_Over_y + (y-tmp_y)
                                    else:
                                        break
 
                            #王かどうかの判定
                            elif self.Boad_dot[x][y].are_you_king == False:
                                #飛び越した先に駒があるのかを判定
                                Jump_Over_x = x + (x-tmp_x)
                                Jump_Over_y = y + (y-tmp_y)
                                if self.Check_Point_True(Jump_Over_x,Jump_Over_y):
                                    if self.Boad_dot[Jump_Over_x][Jump_Over_y].State_Dot == 0:
                                        if not (((Jump_Over_x,Jump_Over_y)) in self.Checked_Points):
                                            self.Can_Move_Points.append((Jump_Over_x,Jump_Over_y))
                                            self.ReCheck_Points.append((Jump_Over_x,Jump_Over_y))
                                            self.Checked_Points.append((Jump_Over_x,Jump_Over_y))                           

            
            self.draw_Can_Move()

        #駒の移動
        if ((self.Choice_x,self.Choice_y) in self.Can_Move_Points ):
            #動く前のマスの情報を書き換える
            self.Boad_dot[self.Berfor_Choice_x][self.Berfor_Choice_y].State_Dot = 0
            self.Boad_dot[self.Berfor_Choice_x][self.Berfor_Choice_y].Piece_Color = "#000000"
            
            #動いた後のマス情報を書き換える
            self.Boad_dot[self.Choice_x][self.Choice_y].State_Dot = 1
            self.Boad_dot[self.Choice_x][self.Choice_y].Piece_Color = self.Player_Color

            #王の情報更新
            self.Boad_dot[self.Choice_x][self.Choice_y].are_you_king = self.Boad_dot[self.Berfor_Choice_x][self.Berfor_Choice_y].are_you_king
            self.Boad_dot[self.Berfor_Choice_x][self.Berfor_Choice_y].are_you_king = False
            
            self.on_draw()

            self.Change_Player()

        else:
            return

    
    #ランダム行動
    def Random_turn(self):
        #盤面の描画を呼び出し
        self.on_draw()
        #駒選択
        Piece_Point_list = []
        #後進する確率
        self.epsilon = 0.01

        for i in range(self.width):
            for j in range(self.height):
                if self.Boad_dot[i][j].Piece_Color == self.Player_Color:
                    Piece_Point_list.append((i,j))

        while True:
            x,y = random.choice(Piece_Point_list)

            #座標から盤面の座標に変換
            self.Choice_x = x
            self.Choice_y = y

            #王の駒が定められた位置にある場合は移動させない
            if self.Boad_dot[self.Choice_x][self.Choice_y].are_you_king == True:
                #黄色
                if self.Choice_x == 0 and self.Choice_y == 0:
                    continue
                #赤色
                elif self.Choice_x == 0 and self.Choice_y == self.height-1:
                    continue

            if (self.Boad_dot[self.Choice_x][self.Choice_y].Piece_Color == self.Player_Color ):        
                #選択した駒を強調表示
                self.draw_Select()

                #選択した駒を保存
                self.Berfor_Choice_x = self.Choice_x
                self.Berfor_Choice_y = self.Choice_y

                #移動可能リスト
                self.Can_Move_Points = []

                #確認済みリスト
                self.Checked_Points = [(x,y)]

                #再行動確認リスト
                self.ReCheck_Points = []

                #選択した駒の周辺6マスを取得
                self.arround_list = self.Get_Connection_Parh(self.Choice_x,self.Choice_y)
                self.Checked_Points.append((self.Choice_x,self.Choice_y))
                
                for x,y in self.arround_list:
                    #駒がない場合
                    if self.Boad_dot[x][y].State_Dot == 0:
                        self.Can_Move_Points.append((x,y))
                    #駒存在時
                    else:
                        #王かどうかの判定
                        if self.Boad_dot[x][y].are_you_king == False: 
                            #飛び越した先に駒があるのかを判定
                            Jump_Over_x = x + (x-self.Choice_x)
                            Jump_Over_y = y + (y-self.Choice_y)
                            if self.Check_Point_True(Jump_Over_x,Jump_Over_y):
                                if self.Boad_dot[Jump_Over_x][Jump_Over_y].State_Dot == 0:
                                    if not (((Jump_Over_x,Jump_Over_y)) in self.Checked_Points):
                                        self.Can_Move_Points.append((Jump_Over_x,Jump_Over_y))
                                        self.ReCheck_Points.append((Jump_Over_x,Jump_Over_y))
                                        self.Checked_Points.append((Jump_Over_x,Jump_Over_y))
                    
                #ここから動いた後にさらに飛び越す場所を探すが動く処理が未完成だから後回し
                while True:                
                    if (len(self.ReCheck_Points) == 0):
                        break
                    #動いた後にさらに超えれるかを確認
                    else:
                        self.arround_list = []
                        tmp_x,tmp_y = self.ReCheck_Points.pop(0)
                        self.arround_list = self.Get_Connection_Parh(tmp_x,tmp_y)

                        for x,y in self.arround_list:
                            #駒の存在を確認
                            if self.Boad_dot[x][y].State_Dot == 1:
                                #王かどうかの判定
                                if self.Boad_dot[x][y].are_you_king == False:
                                    #飛び越した先に駒があるのかを判定
                                    Jump_Over_x = x + (x-tmp_x)
                                    Jump_Over_y = y + (y-tmp_y)
                                    if self.Check_Point_True(Jump_Over_x,Jump_Over_y):
                                        if self.Boad_dot[Jump_Over_x][Jump_Over_y].State_Dot == 0:
                                            if not (((Jump_Over_x,Jump_Over_y)) in self.Checked_Points):
                                                self.Can_Move_Points.append((Jump_Over_x,Jump_Over_y))
                                                self.ReCheck_Points.append((Jump_Over_x,Jump_Over_y))
                                                self.Checked_Points.append((Jump_Over_x,Jump_Over_y))                           

                
                self.draw_Can_Move()

            #駒の移動
            if (len(self.Can_Move_Points) != 0 ):
                for x,y in self.Can_Move_Points:
                    #距離可能のマスと現在の位置を計算
                    self.distance_list = []
                    distance_x = self.Choice_x -x
                    distance_y = self.Choice_y -y

                    #戻る手の場合距離を0に変更
                    if self.Player_Color == "#FF0000":
                        if distance_x < 0 or distance_y > 0:
                            self.distance_list.append(0)
                        else:
                            self.distance_list.append((abs(distance_x)+abs(distance_y)))
                    else:
                        if distance_x < 0 or distance_y < 0:
                            self.distance_list.append(0)
                        else:
                            self.distance_list.append((abs(distance_x)+abs(distance_y)))

                 
                #0しかない時はbreak
                if (self.distance_list.count(0))  == len(self.distance_list):
                        if random.random() >= self.epsilon :
                            continue
                        else:
                            self.Max_Move=[i for i, v in enumerate(self.distance_list) if v == max(self.distance_list)]
                else:
                    #距離最大の移動を取得
                    self.Max_Move=[i for i, v in enumerate(self.distance_list) if v == max(self.distance_list)]
                


                self.Choice_x,self.Choice_y = self.Can_Move_Points[random.choice(self.Max_Move)]

                #動く前のマスの情報を書き換える
                self.Boad_dot[self.Berfor_Choice_x][self.Berfor_Choice_y].State_Dot = 0
                self.Boad_dot[self.Berfor_Choice_x][self.Berfor_Choice_y].Piece_Color = "#000000"
                
                #動いた後のマス情報を書き換える
                self.Boad_dot[self.Choice_x][self.Choice_y].State_Dot = 1
                self.Boad_dot[self.Choice_x][self.Choice_y].Piece_Color = self.Player_Color

                #王の情報更新
                self.Boad_dot[self.Choice_x][self.Choice_y].are_you_king = self.Boad_dot[self.Berfor_Choice_x][self.Berfor_Choice_y].are_you_king
                self.Boad_dot[self.Berfor_Choice_x][self.Berfor_Choice_y].are_you_king = False
                
                self.on_draw()

                self.Change_Player()
                       
                break

    def Change_Player(self):
            global boad
            #駒の移動可能な場所を初期化
            self.Can_Move_Points = []
            self.Checked_Points = []
            self.ReCheck_Points = []
            self.Turn += 1
            if self.Win_Check():
                        #文字列の表示
                if self.Player_Color == "#FF0000":
                    str = '赤の勝利'
                else:
                    str = '黄の勝利'
                self.c.create_text(10,10,text=str, font = 'courier 16',anchor=tk.NW)
                print(str)
                print(self.Turn)
                print("計測時間",time.time()-self.start_time)
                print("======ゲーム終了=========") 
                boad.destroy()
                return 

            if self.Player_Color =="#FF0000":
                self.Player_Color = "#FFFF00"
                if self.Player_B == "CPU":
                    boad.after(10,self.Random_turn)
                    #self.Random_turn()

            elif self.Player_Color =="#FFFF00":
                self.Player_Color="#FF0000"
                if self.Player_A == "CPU":
                    boad.after(10,self.Random_turn)
                    #self.Random_turn()


    #繋がっている周辺の座標を返す
    def Get_Connection_Parh(self,x,y):
        arround_list = []
        #左2つ
        for i in range(2):
            Next_x = x -1
            Next_y = y + 1+(-2*i)
            if self.Check_Point_True(Next_x,Next_y):
                arround_list.append((Next_x,Next_y))


        #上下
        for i in range(2):
            Next_x = x
            Next_y = y + (2-4*i)
            if self.Check_Point_True(Next_x,Next_y):
                arround_list.append((Next_x,Next_y))

        #右2つ
        for i in range(2):
            Next_x = x +1
            Next_y = y + 1+(-2*i)
            if self.Check_Point_True(Next_x,Next_y):
                arround_list.append((Next_x,Next_y))
        
        return arround_list



    #座標が移動可能領域か(駒の有無判定はしない)
    #Region,座標の整合性を確認
    #移動可能領域ならTrueがReturn
    def Check_Point_True(self,x,y):
        if (x < 0 or x > self.width-1 or y < 0 or y > self.height-1):
            return False

        elif (self.Boad_dot[x][y].State_Dot == -1):
            return False

        elif ((self.Boad_dot[x][y].Region_Color != "#FFFFFF") and (self.Boad_dot[x][y].Region_Color != self.Player_Color)):
            return False
        
        return True

    #選択した駒を強調表示
    def draw_Select(self):
        draw_x = self.ini_x + self.Choice_x*self.small_width
        draw_y = self.ini_y*(1+self.Choice_x) + (self.Choice_y-self.Choice_x)*20
        self.c.create_oval(draw_x-2,draw_y-2,draw_x+2,draw_y+2,width=0.0,fill="#000000")
        

    #移動可能の座標を強調
    def draw_Can_Move(self):
        for x,y in self.Can_Move_Points:
            draw_x = self.ini_x + x*self.small_width
            draw_y = self.ini_y*(1+x) + (y-x)*20
            self.c.create_oval(draw_x-2,draw_y-2,draw_x+2,draw_y+2,width=1.0,fill="#FFFFFF")
        
            
    def Win_Check(self):
        #黄色(左上)
        if self.Player_Color == "#FFFF00":
            #決め打ち王チェック
            if self.Boad_dot[0][0].are_you_king != True:
                return False

            Count_True_Piece = 0
            step = 0
            for i in reversed(range(0,4)):
                step += 1
                count = 0
                for j in range(self.height):
                    if count > step:
                        continue
                    elif self.Boad_dot[i][j].State_Dot != -1:
                        if i%2 == j%2:
                            #count+=1
                            #regionの色を指定
                            if count != step:
                                if self.Boad_dot[i][j].Piece_Color == "#FFFF00":
                                    Count_True_Piece += 1
                            count+=1

        #赤色(左下)   
        elif self.Player_Color == "#FF0000":  
            #決め打ち王チェック
            if self.Boad_dot[0][self.height-1].are_you_king != True:
                return False
            Count_True_Piece = 0           
            step = 0
            for i in reversed(range(0,4)):
                step += 1
                count = 0
                for j in reversed(range(self.height)):
                    if count >= step:
                        pass
                    elif self.Boad_dot[i][j].State_Dot != -1:
                        if i%2 == j%2:
                            #count+=1
                                #regionの色を指定
                            if count != step:
                                if self.Boad_dot[i][j].Piece_Color == "#FF0000":
                                    Count_True_Piece +=1
                            count+=1
        #print(Count_True_Piece)
        if Count_True_Piece == self.piece_num:
            return True

        return False

    def on_draw(self):
        self.ini_x = 90
        self.ini_y = 20
        self.Edge_len = 160
        self.Small_Square_Edge=self.Edge_len/4
        self.half_boad_width = int(math.sqrt(self.Edge_len**2 - (self.Edge_len/2)**2))
        self.small_width = int(math.sqrt(self.Small_Square_Edge**2 - (self.Small_Square_Edge/2)**2))
        self.c.delete('all')
        
        self.c.create_line(self.ini_x,self.ini_y,self.ini_x,self.ini_y+self.Edge_len*3,width=2.0,fill='#000000')
        self.c.create_line(self.ini_x+self.half_boad_width*2,self.ini_y,self.ini_x+self.half_boad_width*2,self.ini_y+self.Edge_len*3,width=2.0,fill='#000000')
        self.c.create_line(self.ini_x,self.ini_y,self.ini_x+self.half_boad_width*2,self.ini_y+self.Edge_len,width=2.0,fill='#000000')
        self.c.create_line(self.ini_x,self.ini_y+self.Edge_len,self.ini_x+self.half_boad_width*2,self.ini_y,width=2.0,fill='#000000')
        self.c.create_line(self.ini_x,self.ini_y+self.Edge_len*3,self.ini_x+self.half_boad_width*2,self.ini_y+self.Edge_len*2,width=2.0,fill='#000000')
        self.c.create_line(self.ini_x,self.ini_y+self.Edge_len*2,self.ini_x+self.half_boad_width*2,self.ini_y+self.Edge_len*3,width=2.0,fill='#000000')

        for i in range(4):
            self.c.create_line(self.ini_x,self.ini_y+self.Small_Square_Edge*i,self.ini_x+self.small_width*i,self.ini_y+self.Small_Square_Edge/2*i,width=0.2,fill='#000000')

        for i in range(7):
            self.c.create_line(self.ini_x,self.ini_y+self.Small_Square_Edge*(5+i),self.ini_x+self.half_boad_width*2,self.ini_y+self.Small_Square_Edge*(1+i),width=0.2,fill='#000000')

        for i in range(4):
            self.c.create_line(self.ini_x+self.half_boad_width+self.small_width*(1+i),self.ini_y+self.Small_Square_Edge*(10)+self.Small_Square_Edge/2*(i+1),self.ini_x+self.half_boad_width*2,self.ini_y+self.Small_Square_Edge*(9+i),width=0.2,fill='#000000')

        for i in range(4):
            self.c.create_line(self.ini_x+self.small_width*(1+i),self.ini_y+self.Small_Square_Edge/2*(1+i),self.ini_x+self.small_width*(1+i),(self.ini_y+self.Edge_len*3)-(self.Small_Square_Edge/2*(1+i)),width=0.2,fill='#000000')

        for i in range(3):
            self.c.create_line((self.ini_x+self.half_boad_width*2)-self.small_width*(1+i),self.ini_y+self.Small_Square_Edge/2*(1+i),(self.ini_x+self.half_boad_width*2)-self.small_width*(1+i),(self.ini_y+self.Edge_len*3)-(self.Small_Square_Edge/2*(1+i)),width=0.2,fill='#000000')

        for i in range(3):
             self.c.create_line(self.ini_x,self.ini_y+self.Small_Square_Edge*(9+i),(self.ini_x+self.small_width*(3)-self.small_width*i),(self.ini_y+self.Small_Square_Edge*(10)+self.Small_Square_Edge/2*(i+1)),width=0.2,fill='#000000')
        
        for i in range(7):
            self.c.create_line(self.ini_x,self.ini_y+self.Small_Square_Edge*(1+i),self.ini_x+self.half_boad_width*2,self.ini_y+self.Small_Square_Edge*(5+i),width=0.2,fill='#000000')

        for i in range(3):
             self.c.create_line((self.ini_x+self.half_boad_width*2)-self.small_width*(i+1),self.ini_y+self.Small_Square_Edge/2*(1+i),(self.ini_x+self.half_boad_width*2),(self.ini_y+self.Small_Square_Edge*(i+1)),width=0.2,fill='#000000')

        #駒配置
        for i in range(self.width):
            for j in range(self.height):
                if self.Boad_dot[i][j].State_Dot != -1:
                    draw_x = self.ini_x + i*self.small_width
                    draw_y = self.ini_y*(1+i) + (j-i)*20
                    self.c.create_oval(draw_x-5,draw_y-5,draw_x+5,draw_y+5,width=0.0,fill=self.Boad_dot[i][j].Piece_Color)
                    if self.Boad_dot[i][j].are_you_king == True:
                        self.c.create_text(draw_x-3,draw_y-3,text="王", font = ("#FFFFFF",5,"bold"),anchor=tk.NW)

        #文字列の表示
        if self.Player_Color == "#FF0000":
            str = '赤'
        else:
            str = '黄'
        self.c.create_text(10,10,text=str, font = 'courier 16',anchor=tk.NW)

class Boad_Info:
    def __init__(self):
        #マスの色（Red,Yellow,White）
        self.Region_Color = '#FFFFFF'
        #どこのマスと繋がっているか
        self.Dot_Path = []
        #駒の存在(1or0)、仮想の点(-1)
        self.State_Dot = 0
        #駒存在時の色保存(黒or赤or黄色)
        self.Piece_Color = "#000000"
        #Kingの判定用
        self.are_you_king = False


while True:
    boad = State() 
    boad.pack()
    boad.mainloop()

