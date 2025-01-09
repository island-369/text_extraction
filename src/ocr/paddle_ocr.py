from paddleocr import PaddleOCR

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    
    def process_image(self, image):
        """处理图像并返回识别结果"""
        result = self.ocr.ocr(image)
        if result[0]:
            return '\n'.join([line[1][0] for line in result[0]])
        return '未能识别到文字' 