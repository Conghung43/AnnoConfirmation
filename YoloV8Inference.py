# from IPython import display
# display.clear_output()

# import ultralytics
# ultralytics.checks()

from ultralytics import YOLO

from IPython.display import display, Image

model = YOLO(r'Model\best.pt')
results = model.predict(source=r"E:\yolov9\data\0218\outputSegV8\valid\images\CV3-2000M-19RT-Snapshot-20240205-152926-387-3152229228420_0_2.jpg", conf=0.25)
print(results[0].masks.xy)