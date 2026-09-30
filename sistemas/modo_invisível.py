import cv2
import mediapipe as mp


# ==========================================
# INICIALIZAÇÃO DOS COMPONENTES VISUAIS
# ==========================================
# Prepara os módulos nativos de captura de malha e desenho de pontos do MediaPipe.
mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils

# Inicializa o rastreador configurado para detectar até duas mãos simultâneas na câmera.
rastreador_maos = mp_maos.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Inicializa o canal de captura físico da webcam padrão do notebook.
camera = cv2.VideoCapture(0)


# ==========================================
# CONFIGURAÇÃO DOS TAMBORES VIRTUAIS
# ==========================================
# Dicionário contendo os 4 botões virtuais posicionados na horizontal da tela.
# Formato de cada tambor: (X_centro, Y_centro, raio, nome_visual)
TAMBORES = [
    {"nome": "D", "x": 120, "y": 240, "raio": 45},
    {"nome": "F", "x": 260, "y": 240, "raio": 45},
    {"nome": "J", "x": 400, "y": 240, "raio": 45},
    {"nome": "K", "x": 540, "y": 240, "raio": 45}
]


# ==========================================
# LOOP PRINCIPAL DE PROCESSAMENTO VISUAL
# ==========================================
print("SISTEMA VISÃO: Teste isolado ativo. Pressione ESC na janela do vídeo para fechar.")

while camera.isOpened():
    sucesso, frame = camera.read()
    if not sucesso:
        print("ERRO: Não foi possível ler os frames da sua webcam.")
        break

    # Redimensiona o frame para uma resolução padrão leve e estável de processamento.
    frame = cv2.resize(frame, (640, 480))
    
    # Inverte o vídeo horizontalmente para funcionar como um espelho intuitivo.
    frame = cv2.flip(frame, 1)
    
    # Converte o padrão de cores BGR do OpenCV para RGB exigido pelo MediaPipe.
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = rastreador_maos.process(frame_rgb)

    # Lista que guardará as coordenadas (X, Y) dos dedos indicadores detectados.
    pontas_dedos = []

    # Condicional que processa os pontos anatômicos se houver mãos na imagem.
    if resultado.multi_hand_landmarks:
        for marcas_mao in resultado.multi_hand_landmarks:
            # Desenha as linhas e articulações da mão por cima do vídeo da webcam.
            mp_desenho.draw_landmarks(frame, marcas_mao, mp_maos.HAND_CONNECTIONS)
            
            # Pega o ponto 8 (INDEX_FINGER_TIP) que representa a ponta do dedo indicador.
            indicador = marcas_mao.landmark[mp_maos.HandLandmark.INDEX_FINGER_TIP]
            
            # Converte as coordenadas normalizadas (0.0 a 1.0) para pixels reais da tela (640x480).
            cx = int(indicador.x * 640)
            cy = int(indicador.y * 480)
            
            # Pinta uma bolinha vermelha bem na ponta do seu dedo indicador para calibração.
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
            pontas_dedos.append((cx, cy))

    # ==========================================
    # PROCESSAMENTO DE COLISÕES (APENAS VISUAL)
    # ==========================================
    # Varre os 4 tambores configurados para checar interseção com os dedos.
    for tambor in TAMBORES:
        colidiu = False
        
        # Compara a posição do tambor com cada indicador detectado na tela.
        for (dx, dy) in pontas_dedos:
            # Equação matemática de distância euclidiana para colisões circulares.
            distancia = ((dx - tambor["x"]) ** 2 + (dy - tambor["y"]) ** 2) ** 0.5
            
            # Condicional que valida se a ponta do dedo entrou dentro do raio do tambor.
            if distancia <= tambor["raio"]:
                colidiu = True
                break

        # Pinta o tambor de verde brilhante se houver colisão ativa, ou azul se livre.
        cor_tambor = (0, 255, 0) if colidiu else (255, 0, 0)
        
        # Desenha o círculo do tambor e o rótulo textual centralizado na tela do OpenCV.
        cv2.circle(frame, (tambor["x"], tambor["y"]), tambor["raio"], cor_tambor, 3)
        cv2.putText(
            frame, tambor["nome"], 
            (tambor["x"] - 12, tambor["y"] + 11), 
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3
        )

    # Exibe a janela auxiliar do OpenCV mostrando o feedback do vídeo e dos tambores.
    cv2.imshow("CloneBeat - Laboratorio de Teste de Visao Computacional", frame)

    # Fecha o script imediatamente se a tecla ESC (código 27) for pressionada na janela do vídeo.
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Libera os recursos físicos de captura e encerra as janelas criadas do OpenCV.
camera.release()
cv2.destroyAllWindows()
print("SISTEMA VISÃO: Teste isolado encerrado com sucesso.")
