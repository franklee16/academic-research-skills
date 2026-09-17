"""
PPT Agent 单元测试
"""
import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aut_sci_ppt import PPTAgent
from aut_sci_ppt.config import Config
from aut_sci_ppt.parser.text_parser import TextParser
from aut_sci_ppt.paginator.smart_paginator import SmartPaginator
from aut_sci_ppt.models import (
    CoverData, ContentListData, ListItem, HeaderInfo,
    SectionData, Page, PAGE_TYPE_CONTENT_LIST, PAGE_TYPE_COVER
)


class TestTextParser(unittest.TestCase):
    """测试文本解析器"""
    
    def setUp(self):
        self.parser = TextParser()
    
    def test_parse_basic_meta(self):
        """测试基本元数据解析"""
        text = """
        主题：测试汇报
        申请人：张三
        导师：李四教授
        时间：2025-01-01
        """
        result = self.parser.parse(text)
        
        self.assertEqual(result.meta.title, "测试汇报")
        self.assertEqual(result.meta.author, "张三")
        self.assertEqual(result.meta.advisor, "李四教授")
        self.assertEqual(result.meta.date, "2025-01-01")
    
    def test_parse_sections(self):
        """测试章节解析"""
        text = """
        主题：测试汇报
        申请人：张三
        
        1. 教育背景
        - 学校：清华大学
        - 专业：计算机科学
        """
        result = self.parser.parse(text)
        
        self.assertGreater(len(result.sections), 0)
    
    def test_validate_missing_title(self):
        """测试缺少标题时的验证"""
        text = """
        申请人：张三
        """
        result = self.parser.parse(text)
        warnings = self.parser.validate(result)
        
        self.assertTrue(any("标题" in w for w in warnings))
    
    def test_validate_missing_author(self):
        """测试缺少申请人时的验证"""
        text = """
        主题：测试汇报
        """
        result = self.parser.parse(text)
        warnings = self.parser.validate(result)
        
        self.assertTrue(any("申请人" in w for w in warnings))


class TestSmartPaginator(unittest.TestCase):
    """测试智能分页器"""
    
    def setUp(self):
        self.config = Config()
        self.paginator = SmartPaginator(self.config)
    
    def test_paginate_basic(self):
        """测试基本分页"""
        from aut_sci_ppt.models import ParsedData, CoverData
        
        parsed = ParsedData()
        parsed.meta = CoverData(title="测试", author="张三")
        
        pages = self.paginator.paginate(parsed)
        
        # 应该至少有封面页和结束页
        self.assertGreaterEqual(len(pages), 2)
        self.assertEqual(pages[0].page_type, 'cover')
        self.assertEqual(pages[-1].page_type, 'ending')
    
    def test_section_numbering(self):
        """测试章节编号"""
        from aut_sci_ppt.models import ParsedData, CoverData, ContentListData, ListItem, Page
        
        parsed = ParsedData()
        parsed.meta = CoverData(title="测试", author="张三")
        
        # 添加多个章节
        for i in range(3):
            content = ContentListData(title=f"章节{i+1}", items=[ListItem(text=f"内容{i+1}")])
            parsed.sections.append(Page(page_type=PAGE_TYPE_CONTENT_LIST, data=content))
        
        pages = self.paginator.paginate(parsed)
        
        # 查找所有 section 页
        section_pages = [p for p in pages if p.page_type == 'section']
        
        # 应该有3个章节页
        self.assertEqual(len(section_pages), 3)
        
        # 章节编号应该正确
        for i, section in enumerate(section_pages, 1):
            self.assertEqual(section.data.part_num, str(i))


class TestPPTagent    """测试 PPT Agent 主(unittest.TestCase):
类"""
    
    def setUp(self):
        self.agent = PPTAgent()
    
    def test_generate_basic(self):
        """测试基本生成"""
        text = """
        主题：测试汇报
        申请人：张三
        导师：李四
        
        1. 教育背景
        - 学校：清华大学
        """
        
        output_path = "test_output.pptx"
        result = self.agent.generate(text, output_path)
        
        self.assertEqual(result, output_path)
        
        # 清理测试文件
        if os.path.exists(output_path):
            os.remove(output_path)
    
    def test_preview(self):
        """测试预览功能"""
        text = """
        主题：测试汇报
        申请人：张三
        
        1. 教育背景
        - 学校：清华大学
        
        2. 获奖经历
        - 奖项1
        """
        
        preview = self.agent.preview(text)
        
        self.assertIsInstance(preview, list)
        self.assertGreater(len(preview), 0)


class TestConfig(unittest.TestCase):
    """测试配置类"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = Config()
        
        self.assertIsNotNone(config.page_size)
        self.assertIsNotNone(config.fonts)
        self.assertIsNotNone(config.colors)
    
    def test_log_level(self):
        """测试日志级别配置"""
        config = Config(log_level="DEBUG")
        
        self.assertEqual(config.log_level, "DEBUG")


class TestChandraFallback(unittest.TestCase):
    """测试 Chandra 不可用时的降级路径

    对应改进：ChandraEnhancedAgent 降级路径从未被测试覆盖的问题。
    以下测试在 CHANDRA_AVAILABLE=False 的条件下运行，验证降级链正确工作。
    """

    def test_chandra_unavailable_agent_initializes(self):
        """Chandra 不可用时，ChandraEnhancedAgent 应能正常初始化（不崩溃）"""
        import unittest.mock as mock
        # 模拟 CHANDRA_AVAILABLE = False
        with mock.patch.dict("sys.modules", {"chandra": None}):
            try:
                import importlib
                import sys
                # 动态 patch chandra_adapter 的 CHANDRA_AVAILABLE
                chandra_adapter_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "..", "chandra_adapter.py"
                )
                if os.path.exists(chandra_adapter_path):
                    # patch 变量后重新构造 agent
                    with mock.patch("chandra_adapter.CHANDRA_AVAILABLE", False):
                        sys.path.insert(0, os.path.dirname(os.path.dirname(
                            os.path.dirname(os.path.abspath(__file__)))))
                        from chandra_enhanced_agent import ChandraEnhancedAgent
                        agent = ChandraEnhancedAgent(enable_enhancements=True)
                        # chandra_adapter 应为 None（降级）
                        self.assertIsNone(agent.chandra_adapter)
                        status = agent.get_chandra_status()
                        self.assertFalse(status.get("chandra_available", True))
            except ImportError:
                self.skipTest("ChandraEnhancedAgent 未安装，跳过测试")

    def test_chandra_unavailable_generate_falls_back(self):
        """Chandra 不可用时，generate_from_pdf 应降级到标准 PDF 提取，不抛异常"""
        import unittest.mock as mock
        try:
            import sys
            sys.path.insert(0, os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))))
            with mock.patch("chandra_adapter.CHANDRA_AVAILABLE", False):
                from chandra_enhanced_agent import ChandraEnhancedAgent

                agent = ChandraEnhancedAgent(enable_enhancements=True)

                # 使用一个不存在的 PDF 路径触发早期失败，验证降级路径不崩溃
                result = agent.generate_from_pdf(
                    "/nonexistent/path.pdf",
                    "test_fallback_output.pptx",
                    enable_review_gate=False,
                    enable_formula_rendering=False,
                    use_chandra=True,  # 即使请求 Chandra，也应自动降级
                )
                # 文件不存在时应返回 None 或空字符串，不应抛出未捕获异常
                self.assertFalse(result)  # None / False / "" 均视为降级成功
        except ImportError:
            self.skipTest("ChandraEnhancedAgent 未安装，跳过测试")
        finally:
            if os.path.exists("test_fallback_output.pptx"):
                os.remove("test_fallback_output.pptx")

    def test_review_gate_file_handshake(self):
        """ReviewGate 文件握手协议：approve 后响应文件应被正确解析"""
        import tempfile
        from review_gate import ReviewGate

        with tempfile.TemporaryDirectory() as tmpdir:
            gate = ReviewGate(checkpoint_dir=tmpdir)

            cp = gate.create_checkpoint(
                stage="outline",
                content={"chapters": ["第一章", "第二章"]},
                description="测试检查点"
            )
            cp_id = cp.checkpoint_id

            # 模拟 boss 批准：直接写响应文件（测试文件握手机制）
            import json
            resp_file = os.path.join(tmpdir, f"REVIEW_RESPONSE_{cp_id}.json")
            with open(resp_file, "w", encoding="utf-8") as f:
                json.dump({"status": "approved", "feedback": "看起来不错"}, f)

            # wait_for_approval 应在检测到响应文件后立即返回 True
            result = gate.wait_for_approval(cp_id, timeout_seconds=5)
            self.assertTrue(result)
            # 响应文件应被消费（删除）
            self.assertFalse(os.path.exists(resp_file))


if __name__ == '__main__':
    unittest.main()

