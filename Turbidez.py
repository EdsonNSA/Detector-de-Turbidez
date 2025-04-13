import cv2
import numpy as np
import datetime
import os

cap = cv2.VideoCapture(1)

os.makedirs("capturas", exist_ok=True)

font = cv2.FONT_HERSHEY_SIMPLEX

roi_x1, roi_y1 = 220, 140
roi_x2, roi_y2 = roi_x1 + 100, roi_y1 + 100

def calcular_turbidez(roi_gray):
    return np.std(roi_gray)

def salvar_imagem(frame, turbidez):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"capturas/amostra_{timestamp}_turbidez_{turbidez:.2f}.png"
    cv2.imwrite(filename, frame)
    print(f"[SALVO] {filename}")

def classificar_turbidez(turbidez):
    if turbidez < 10:
        return "Baixa", (0, 255, 0)
    elif turbidez < 30:
        return "Moderada", (0, 255, 255)
    else:
        return "Alta", (0, 0, 255)

print("[INFO] Pressione 'x' para salvar imagem, 'q' para sair.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("[ERRO] Falha ao acessar o vídeo.")
        break

    frame = cv2.flip(frame, 1)
    altura, largura, _ = frame.shape

    if roi_x2 <= largura and roi_y2 <= altura:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        roi = gray[roi_y1:roi_y2, roi_x1:roi_x2]

        turbidez = calcular_turbidez(roi)
        nivel, cor = classificar_turbidez(turbidez)

        cv2.putText(frame, f"Turbidez: {turbidez:.2f}", (10, 30), font, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Nivel: {nivel}", (10, 70), font, 1, cor, 2)
        cv2.putText(frame, "Aperte 'x' para salvar | 'q' para sair", (10, altura - 10), font, 0.6, (200, 200, 200), 1)

        cv2.rectangle(frame, (roi_x1, roi_y1), (roi_x2, roi_y2), cor, 2)

    cv2.imshow("Detector de Turbidez (Celular)", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('x'):
        salvar_imagem(frame, turbidez)

cap.release()
cv2.destroyAllWindows()
