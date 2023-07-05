import cv2
import math
import mediapipe as mp


#iniciar o objeto


cap = cv2.VideoCapture(1)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# descomentar e explicar: (pega a largura e altura da janela do pc)
#(screen_width, screen_height) = pyautogui.size()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8,
                       min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

# pinça
pinch = False

# Defina uma função para contar os dedos
def countFingers(image, hand_landmarks, handNo=0):

    # tornando global
    global pinch

    if hand_landmarks:
        # Obtenha todos os pontos de referência da PRIMEIRA mão VISÍVEL
        landmarks = hand_landmarks[handNo].landmark

    # Conte os dedos
        fingers = []

        for lm_index in tipIds:
            # Obtenha os valores y da ponta e da parte inferior do dedo
            finger_tip_y = landmarks[lm_index].y
            finger_bottom_y = landmarks[lm_index - 2].y

    # Verifique se ALGUM DEDO está ABERTO ou FECHADO
            if lm_index != 4:
                if finger_tip_y < finger_bottom_y:
                    fingers.append(1)

                if finger_tip_y > finger_bottom_y:
                    fingers.append(0)

        totalFingers = fingers.count(1)

        
        finger_tip_x = int((landmarks[8].x)*width)
        finger_tip_y = int((landmarks[8].y)*height)

        thumb_tip_x = int((landmarks[4].x)*width)
        thumb_tip_y = int((landmarks[4].y)*height)

        # Desenhe uma LINHA entre a PONTA DO DEDO e a PONTA DO POLEGAR
        

        
        center_x = int((finger_tip_x + thumb_tip_x)/2)
        center_y = int((finger_tip_y + thumb_tip_y)/2)


        # Desenhe um CÍRCULO no CENTRO da LINHA entre a PONTA DO DEDO e a PONTA DO POLEGAR
        

        # Calcule a DISTÂNCIA entre a PONTA DO DEDO e a PONTA DO POLEGAR
       



        # print("Distância: ", distance)

        # print("Tamanho da Tela do Computador:", screen_width,
        # screen_height, "Tamanho da Janela de Resultado: ", width, height)
        # print("Posição do Mouse: ", mouse.position,
        # "Posição Central da Linha das Pontas: ", center_x, center_y)

        # Defina a posição do mouse na tela em relação ao tamanho da janela de resultado
        relative_mouse_x = (center_x/width)*screen_width
        relative_mouse_y = (center_y/height)*screen_height

        mouse.position = (relative_mouse_x, relative_mouse_y)

        # explicar: (dica:Verifica as condições de formação da PINÇA)
        if distance > 40:
            if pinch == True:
                pinch = False
                mouse.release(Button.left)

        if distance <= 40:
            if (pinch == False):
                pinch = True
                mouse.press(Button.left)


# Defina uma função para
def drawHandLanmarks(image, hand_landmarks):

    # Desenhar as conexões entre os pontos de referência
    if hand_landmarks:

        for landmarks in hand_landmarks:

            mp_drawing.draw_landmarks(
                image, landmarks, mp_hands.HAND_CONNECTIONS)


while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)

    # Detecte os pontos de referência das mãos
    results = hands.process(image)

    # Obtenha a posição do ponto de referência do resultado processado
    hand_landmarks = results.multi_hand_landmarks

    # Desenhe os pontos de referência
    drawHandLanmarks(image, hand_landmarks)

    # Obtenha a posição dos dedos da mão
    countFingers(image, hand_landmarks)

    cv2.imshow("Controlador de Midia", image)

    # Saia da tela ao pressionar a barra de espaço
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
