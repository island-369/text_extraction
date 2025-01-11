from paddleocr import PaddleOCR
import numpy as np

class OCRProcessor:
    def __init__(self):
        """初始化OCR处理器"""
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch', show_log=False)
    
    def process_image(self, image: np.ndarray) -> str:
        """处理图像并返回识别的文本
        
        Args:
            image: numpy数组格式的图像
            
        Returns:
            str: 识别的文本，每个文本块用换行符分隔
        """
        try:
            # 执行OCR识别
            result = self.ocr.ocr(image, cls=True)
            
            if not result or not result[0]:
                return "未能识别到文字"
            
            # 提取文本并按从上到下、从左到右排序
            text_blocks = []
            for line in result[0]:
                if line:
                    text = line[1][0]  # 获取识别的文本
                    confidence = line[1][1]  # 获取置信度
                    if confidence > 0.5:  # 只保留置信度大于0.5的结果
                        text_blocks.append(text)
            
            # 将所有文本块用换行符连接
            return '\n'.join(text_blocks) if text_blocks else "未能识别到文字"
            
        except Exception as e:
            return f"OCR识别出错: {str(e)}" 