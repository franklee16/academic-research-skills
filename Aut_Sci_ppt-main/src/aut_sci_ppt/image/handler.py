"""
PPT Agent 图片处理器
"""
import os
from pathlib import Path
from typing import Tuple, Dict, Optional
from PIL import Image


class ImageHandler:
    """图片处理器"""
    
    VALID_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    
    def __init__(self, config: Dict = None):
        if config is None:
            config = {}
        self.default_size = config.get('default_size', {'width': 4, 'height': 3})
        self.default_position = config.get('default_position', 'right')
    
    def validate(self, image_path: str) -> bool:
        """验证图片格式"""
        if not os.path.exists(image_path):
            return False
        
        ext = Path(image_path).suffix.lower()
        return ext in self.VALID_FORMATS
    
    def get_image_size(self, image_path: str) -> Tuple[int, int]:
        """获取图片原始尺寸"""
        try:
            with Image.open(image_path) as img:
                return img.size
        except Exception:
            return (0, 0)
    
    def calculate_size(self, image_path: str, max_width: float = None, max_height: float = None) -> Tuple[float, float]:
        """
        计算图片尺寸，保持纵横比
        """
        if max_width is None:
            max_width = self.default_size['width']
        if max_height is None:
            max_height = self.default_size['height']
        
        dpi = 96
        
        orig_width, orig_height = self.get_image_size(image_path)
        if orig_width == 0 or orig_height == 0:
            return (max_width, max_height)
        
        width_inches = orig_width / dpi
        height_inches = orig_height / dpi
        
        aspect_ratio = width_inches / height_inches
        
        if width_inches > max_width:
            width_inches = max_width
            height_inches = width_inches / aspect_ratio
        
        if height_inches > max_height:
            height_inches = max_height
            width_inches = height_inches * aspect_ratio
        
        return (width_inches, height_inches)
    
    def calculate_position(self, layout: str, page_width: float, page_height: float, 
                          img_width: float, img_height: float, 
                          content_left: float = 0.5, content_top: float = 1.5) -> Tuple[float, float]:
        """计算图片位置"""
        content_width = page_width - content_left - 0.5
        content_height = page_height - content_top - 1.0
        
        if layout == 'left':
            left = content_left
            top = content_top
        elif layout == 'right':
            left = page_width - img_width - 0.5
            top = content_top
        elif layout == 'top':
            left = (page_width - img_width) / 2
            top = content_top
        elif layout == 'bottom':
            left = (page_width - img_width) / 2
            top = page_height - img_height - 0.5
        elif layout == 'center':
            left = (page_width - img_width) / 2
            top = (page_height - img_height) / 2
        else:
            left = page_width - img_width - 0.5
            top = content_top
        
        return (left, top)
    
    def add_image_to_slide(self, slide, image_path: str, position: str = None,
                          size: Dict[str, float] = None) -> bool:
        """添加图片到幻灯片"""
        from pptx.util import Inches
        
        if not self.validate(image_path):
            return False
        
        if position is None:
            position = self.default_position
        
        if size is None:
            size = self.default_size
        
        width, height = self.calculate_size(
            image_path, 
            max_width=size.get('width', self.default_size['width']),
            max_height=size.get('height', self.default_size['height'])
        )
        
        page_width = 10
        page_height = 7.5
        
        left, top = self.calculate_position(
            position, page_width, page_height, width, height
        )
        
        try:
            slide.shapes.add_picture(
                image_path,
                Inches(left), Inches(top),
                Inches(width), Inches(height)
            )
            return True
        except Exception as e:
            print(f"Error adding image: {e}")
            return False


# 全局实例
default_image_handler = ImageHandler()
