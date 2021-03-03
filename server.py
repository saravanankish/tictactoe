import pygame
import socket
import threading

pygame.init()

screen = pygame.display.set_mode((500, 600))
running = True
pygame.display.set_caption("Tic Tac Toe")


HOST = "127.0.0.1"
PORT = 65432
connection_established = False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = None, None


imgx = pygame.image.load("./images/imgx.png")
imgo = pygame.image.load("./images/img0.png")

l = [((25, 275), (475, 275)), ((25, 425), (475, 425)),
     ((175, 125), (175, 575)), ((325, 125), (325, 575))]
h1 = ((40, 200), (460, 200))
h2 = ((40, 350), (460, 350))
h3 = ((40, 500), (460, 500))
v1 = ((100, 140), (100, 560))
v2 = ((250, 140), (250, 560))
v3 = ((400, 140), (400, 560))
d1 = ((45, 140), (450, 555))
d2 = ((450, 145), (45, 555))
img_pos = [(25, 125), (175, 125), (325, 125), (25, 275), (175, 275),
           (325, 275), (25, 425), (175, 425), (325, 425)]

font = pygame.font.SysFont(None, 45)
font1 = pygame.font.SysFont(None, 25)

# Game Logic
board = [' ' for i in range(9)]
chance = 9
rec = 1
replay = 0
winner = None


def createThread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()


def receiveData():
    global rec, point, chance, replay, board
    while True:
        data = conn.recv(1024).decode()
        print(data)
        if data and data[:5] != "reset" and data[:5] != "repet":
            point, chance = int(data.split("*")[0]), int(data.split("*")[1])
            board[point] = "X" if (chance + 1) % 2 else "O"
            rec = 1
        elif data[:5] == "reset":
            replay = 1
        elif data[:5] == "repet":
            board = [' ' for i in range(9)]
            chance = 9
            rec = 1


def waitingForConnection():
    global connection_established, conn, addr
    conn, addr = sock.accept()
    print(f'{addr} is connected')
    connection_established = True
    receiveData()


def winCheck(board):
    global winner
    if board[0] == board[1] == board[2] != " ":
        winner = board[0]
        pygame.draw.line(screen, (0, 255, 0), h1[0], h1[1], 4)
        return True
    if board[3] == board[4] == board[5] != " ":
        winner = board[3]
        pygame.draw.line(screen, (0, 255, 0), h2[0], h2[1], 4)
        return True
    if board[6] == board[7] == board[8] != " ":
        winner = board[6]
        pygame.draw.line(screen, (0, 255, 0), h3[0], h3[1], 4)
        return True
    if board[0] == board[3] == board[6] != " ":
        winner = board[0]
        pygame.draw.line(screen, (0, 255, 0), v1[0], v1[1], 4)
        return True
    if board[1] == board[4] == board[7] != " ":
        winner = board[1]
        pygame.draw.line(screen, (0, 255, 0), v2[0], v2[1], 4)
        return True
    if board[2] == board[5] == board[8] != " ":
        winner = board[2]
        pygame.draw.line(screen, (0, 255, 0), v3[0], v3[1], 4)
        return True
    if board[0] == board[4] == board[8] != " ":
        winner = board[0]
        pygame.draw.line(screen, (0, 255, 0), d1[0], d1[1], 4)
        return True
    if board[2] == board[4] == board[6] != " ":
        winner = board[2]
        pygame.draw.line(screen, (0, 255, 0), d2[0], d2[1], 4)
        return True
    return False


def clickEvent(pos, chance):
    point = -1
    if not winCheck(board) and chance:
        if pos[0] > 25 and pos[0] < 425 and pos[1] > 175 and pos[1] < 575:
            if pos[1] < 275:
                if pos[0] < 175:
                    if board[0] == " ":
                        if chance % 2:
                            board[0] = "X"
                        else:
                            board[0] = "O"
                        chance -= 1
                        point = 0
                elif pos[0] < 325:
                    if board[1] == " ":
                        if chance % 2:
                            board[1] = "X"
                        else:
                            board[1] = "O"
                        chance -= 1
                        point = 1
                else:
                    if board[2] == " ":
                        if chance % 2:
                            board[2] = "X"
                        else:
                            board[2] = "O"
                        chance -= 1
                        point = 2
            elif pos[1] < 425:
                if pos[0] < 175:
                    if board[3] == " ":
                        if chance % 2:
                            board[3] = "X"
                        else:
                            board[3] = "O"
                        chance -= 1
                        point = 3
                elif pos[0] < 325:
                    if board[4] == " ":
                        if chance % 2:
                            board[4] = "X"
                        else:
                            board[4] = "O"
                        chance -= 1
                        point = 4
                else:
                    if board[5] == " ":
                        if chance % 2:
                            board[5] = "X"
                        else:
                            board[5] = "O"
                        chance -= 1
                        point = 5
            else:
                if pos[0] < 175:
                    if board[6] == " ":
                        if chance % 2:
                            board[6] = "X"
                        else:
                            board[6] = "O"
                        chance -= 1
                        point = 6
                elif pos[0] < 325:
                    if board[7] == " ":
                        if chance % 2:
                            board[7] = "X"
                        else:
                            board[7] = "O"
                        chance -= 1
                        point = 7
                else:
                    if board[8] == " ":
                        if chance % 2:
                            board[8] = "X"
                        else:
                            board[8] = "O"
                        chance -= 1
                        point = 8
    return board, chance, point


def addText(msg, color, f1):
    text = font.render(msg, True, color)
    text_rect = text.get_rect()
    if f1:
        text1 = font1.render(f1.split('/')[0], True, f1.split('/')[1])
        text1_rect = text1.get_rect()
        text_rect.center = 500 / 2, 125 / 2 - 15
        text1_rect.center = 500 / 2, 125 / 2 + 15
        screen.blit(text1, text1_rect)
    else:
        text_rect.center = 500 / 2, 125 / 2
    screen.blit(text, text_rect)


if __name__ == '__main__':
    createThread(waitingForConnection)
    while running:

        screen.fill((255, 255, 255))
        if not connection_established:
            addText("Waiting for Player2 to connect", "Red", None)
        for i in l:
            pygame.draw.line(screen, (0, 0, 0), i[0], i[1], 3)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_q]:
            running = False
        if key_pressed[pygame.K_SPACE]:
            if not replay:
                if board.count(" ") == 0 or winCheck(board):
                    send_data = "reset" + str(point) + "*" + str(chance)
                    conn.send(send_data.encode())
            else:
                send_data = "repet" + str(point) + "*" + str(chance)
                conn.send(send_data.encode())
                board = [' ' for i in range(9)]
                chance = 9
                replay = 0
                rec = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and connection_established and rec:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    board, chance, point = clickEvent(pos, chance)
                    send_data = str(point) + "*" + str(chance)
                    conn.send(send_data.encode())
                    rec = 0

        for i in range(9):
            if board[i] == "X":
                screen.blit(imgx, img_pos[i])
            elif board[i] == "O":
                screen.blit(imgo, img_pos[i])
        if winCheck(board):
            if not replay:
                if winner == "X":
                    addText("You Won", "Green", "Press Space to Replay/Green")
                else:
                    addText("Player2 Won", "Red",
                            "Press Space to Replay/Green")
            else:
                if winner == "X":
                    addText("You Won", "Green",
                            "Player2 asks replay press space to accept/Green")
                else:
                    addText("Player2 Won", "Red",
                            "Player2 asks replay press space to accept/Green")
        elif not(winCheck(board)) and board.count(" ") == 0:
            if not replay:
                addText("Draw Match", "Orange", "Press Space to Replay/Green")
            else:
                addText("Draw Match", "Orange",
                        "Player2 asks replay press space to accept/Green")
        else:
            if not rec:
                addText("Player2 is Playing", "Red", None)
            if rec and connection_established:
                addText("Your Turn", "Green", None)

        pygame.display.update()
