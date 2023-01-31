"""
Beschreibung:
    Task: Finger Counter für eine Hand

    Erstelle eine Augmented Reality Applikation zu Zählen der Finger.
    Für diesen Task benötigst Du zwei zusätzliche Libraries:
        - opencv-python
        - mediapipe

    Programm-Ablauf
     - erstelle eine Verbindung zu einem Video-Device (Kamera/Video) cv2.Capture(<Video-Source>)
     - setzte die die Ausgabe View auf eine Größe von 800 x 600
     - initialisiere MediaPipe Hands und Drawing Modul
        - mp.solutions.hands
        - mp.solutions.drawing_utils
     - erstelle eine Liste mit den Landmarks für die vier Finger der Hand
       jeweils ein Tupel aus Fingerspitze (TIP) und dem zweiten Fingerglied (PIP)
        - Zeigefinger      ( 8,  6)
        - Mittelfinger     (12, 10)
        - Ringfinger       (16, 14)
        - Kleinerfinger    (20, 18)
     - erstelle für den Daumen ein Tuple aus der Fingerspitze und dem zweiten Fingerglied
        - Daumen           ( 4,  2)
     - erstelle eine Endlosschleife mit 'while'
        - lese eine Bild von der Videoquelle
        - bei Lesefehler überspring die nachfolgende Anweisungen
        - spiegele das Bild
        - konvertiere das Bild vom BGR in das RGB Farbschema
        - starte eine Handerkennung
        - wenn eine Hand gefunden wurde hole die die Landmarks
        - zeichne die Fingerlinien
        - iteriere über die Landmarks und errechne die Position der
          Finger Landmarks auf der View
        - speichere die Landmark Positionen in ein Liste mit Tupeln
        - iteriere über die Landmark Positionen Liste und zeichne einen farbigen
          Kreis an jeder Position
        - iteriere über die Finger Coordinaten-Liste und prüfe ob die Y-Position der
          Fingerspitze kleiner als die Y-Position des ersten Fingerglieds dieses Fingers.
          Wenn größer inkrementiere den Finger-Counter um eins
        - prüfe ob die X-Position der Fingerspitze des Daumens, größer ist als die
          X-Position des ersten Fingerglieds des Daumens
          Wenn größer inkrementiere den Finger-Counter um eins
        - erstelle ein farbiges Rechteck und zeige in diesem die Anzahl der gezählten
          Finger an

    Libraries:
        - opencv-python !Version 4.5.5.64
        - mediapipe
"""

import cv2
import mediapipe as mp


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    finger_coordinates = [(8, 6), (12, 10), (16, 14), (20, 18)]
    thumb_coordinates = (4, 2)

    while True:
        success, image = cap.read()

        if not success:
            continue

        image = cv2.flip(image, 1)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        multi_hand_landmarks = results.multi_hand_landmarks

        up_count = 0
        if multi_hand_landmarks:
            for multi_hand_landmark in multi_hand_landmarks:
                hand_points = []
                mp_drawing.draw_landmarks(image, multi_hand_landmark, mp_hands.HAND_CONNECTIONS)

                for i, hand_landmark in enumerate(multi_hand_landmark.landmark):
                    h, w, _ = image.shape
                    cx, cy = int(hand_landmark.x * w), int(hand_landmark.y * h)
                    hand_points.append((cx, cy))

                for hand_point in hand_points:
                    cv2.circle(image, hand_point, 10, (200, 0, 200), cv2.FILLED)

                for finger_coordinate in finger_coordinates:
                    if hand_points[finger_coordinate[0]][1] < hand_points[finger_coordinate[1]][1]:
                        up_count += 1

                if hand_points[17][0] < hand_points[5][0]:
                    if hand_points[thumb_coordinates[0]][0] > hand_points[thumb_coordinates[1]][0]:
                        up_count += 1
                elif hand_points[thumb_coordinates[0]][0] < hand_points[thumb_coordinates[1]][0]:
                    up_count += 1

                up_count_text = str(up_count)

                (w, h), b = cv2.getTextSize(up_count_text, cv2.FONT_HERSHEY_PLAIN, 10, 25)

                label_w = 225
                label_h = 200
                label_x1 = 50
                label_y1 = 25
                label_x2 = label_x1 + label_w
                label_y2 = label_y1 + label_h
                lable_coordinate1 = (label_x1, label_y1)
                lable_coordinate2 = (label_x2, label_y2)

                txt_coordinate = (label_x1 + (label_w - w) // 2, label_y2 - 50)
                cv2.rectangle(image, lable_coordinate1, lable_coordinate2, (255, 255, 0), cv2.FILLED)
                cv2.putText(image, up_count_text, txt_coordinate, cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 255), 25)

        cv2.imshow('image', image)
        if cv2.waitKey(1) == 27:
            break


if __name__ == '__main__':
    main()
