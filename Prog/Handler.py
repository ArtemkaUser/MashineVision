import cv2


class Handler:
    def __init__(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (9, 9), 1)
        edged = cv2.Canny(gray_blur, 15, 30)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
        circuit = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]
        # circuit is array in arrays in list,
        # I cannot use max_id = circuit.index(max(circuit)

        max_len_array = 0
        max_id = 0
        for i in range(len(circuit)):
            if max_len_array < len(circuit[i]):
                max_len_array = len(circuit[i])
                max_id = i
        self.circuit = circuit[max_id]