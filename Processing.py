import cv2
import mediapipe as mp
from SendDataSerially import send_data


def main():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # Reduce image size to 640x480
    width, height = 640, 480

    webcam = cv2.VideoCapture(0)            #webcam
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.6) as hands:
        while webcam.isOpened():
            success, img = webcam.read()

            if not success:
                break

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (width, height))

            results = hands.process(img)

            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for idx, landmark in enumerate(hand_landmarks.landmark):
    #                    print(f"Landmark {idx}: ({landmark.x}, {landmark.y}, {landmark.z})")
                        pass

                    # Calculate finger openness
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
                    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

                    # Determine finger status (closed/open)
                    thumb_status = "0" if thumb_tip > hand_landmarks.landmark[
                        mp_hands.HandLandmark.THUMB_IP].y else "1"
                    index_status = "0" if index_tip > hand_landmarks.landmark[
                        mp_hands.HandLandmark.INDEX_FINGER_PIP].y else "1"
                    middle_status = "0" if middle_tip > hand_landmarks.landmark[
                        mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y else "1"
                    ring_status = "0" if ring_tip > hand_landmarks.landmark[
                        mp_hands.HandLandmark.RING_FINGER_PIP].y else "1"
                    pinky_status = "0" if pinky_tip > hand_landmarks.landmark[
                        mp_hands.HandLandmark.PINKY_PIP].y else "1"

                    # print(f"Thumb status: {thumb_status}")
                    # print(f"Index finger status: {index_status}")
                    # print(f"Middle finger status: {middle_status}")
                    # print(f"Ring finger status: {ring_status}")
                    # print(f"Pinky finger status: {pinky_status}")

                    data = [thumb_status,index_status,middle_status,ring_status,pinky_status]
                    data = "".join(str(datas) for datas in data)
                    print(data)
                    send_data(data)


                    mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=3, circle_radius=3))

            cv2.imshow('HandDetector', img)

            if cv2.waitKey(5) & 0xFF == ord("q"):
                break

    webcam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()