import time

from mss.linux import MSS as mss
import cv2 as cv
import numpy as np
import pyautogui
import torch


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.coordinates = np.array([x, y])

    def __sub__(self, other) -> float:
        """Calculates euclidean distance between two Points."""
        return np.linalg.norm(self.coordinates - other.coordinates)

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"


class Target:
    def __init__(self, target: torch.Tensor) -> None:
        self.x: float = target[0].item()
        self.y: float = target[1].item()
        self.w: float = target[2].item()
        self.h: float = target[3].item()
        self.confidence: float = target[4].item()
        self.label: int = int(target[5].item())
        self.tensor: torch.Tensor = target
        self.coordinates = np.array([self.x, self.y])

    def __repr__(self) -> str:
        return f"Target({self.label}: x={self.x}, y={self.y})"


def get_targets(results: list, labels: list[int]) -> list[Target]:
    """Returns a list with results filtered by the classes specified in the labels argument."""
    return [Target(target) for target in results.xywh[0] if target[5] in labels]


def sort_targets(targets: list[Target], aim_center: Point) -> list[Target]:
    """Sort targets by distance from the aim center."""
    return sorted(targets, key=lambda target: aim_center - target)


def on_target(aim_center, target, precision=0.5) -> bool:
    return aim_center - target < precision


def shoot() -> None:
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()


def main():
    AIM_CENTER = Point(x=960, y=540)

    fps = 0
    display_time = 1
    start_time = time.time()

    model = torch.hub.load("ultralytics/yolov5", "custom",
                           path="stalcraft-model.pt")

    if torch.cuda.is_available():
        model.cuda()

    with mss() as sct:
        while "Screen Capturing":
            screenshot = np.array(sct.grab(sct.monitors[1]))

            results = model(screenshot)
            results.render()

            cv.imshow('CV TEST', results.imgs[0])

            targets = get_targets(results, labels=[2, 3])

            if targets:
                target = sort_targets(targets, AIM_CENTER)[0]

                pyautogui.moveTo(target.x, target.y)
                if on_target(AIM_CENTER, target, precision=10):
                    shoot()

            fps += 1
            TIME = time.time() - start_time
            if TIME >= display_time:
                print(f"FPS: {fps / TIME}")
                fps = 0
                start_time = time.time()

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break


if __name__ == "__main__":
    main()