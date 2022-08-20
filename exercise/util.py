
import numpy as np

def angle(a, b):
    return np.degrees(np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))))

def bone(points, start, end):
    return np.array(points[end]) - np.array(points[start])
