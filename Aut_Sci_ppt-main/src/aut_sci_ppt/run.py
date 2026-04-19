"""
ShuoC Ppt - 主运行入口
融合 AI 解析 + 交互节点 + PPT 生成
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aut_sci_ppt import PPTAgent
from aut_sci_ppt.parser.ai_parser import ai_parse
from aut_sci_ppt.interactive import InteractiveController

def run_paper_workflow():
    """
    PDF 文献 → 提纲.md（含图片）→ 用户修改 → 生成PPT
    """
    from aut_sci_ppt.paper_workflow import generate_outline, parse_outline_to_ppt_input

    print("\n📄 PDF 文献汇报工作流")
    print("=" * 50)
    pdf_path = input("请输入 PDF 文件路径：").strip().strip('"')
    if not os.path.exists(pdf_path):
        print(f"❌ 文件不存在：{pdf_path}")
        return

    # Step 1: 提取内容+图片，生成提纲 md
    print("\n⏳ 正在分析PDF并提取图片，大约需要30秒...")
    md_path = generate_outline(pdf_path)
    print(f"\n✅ 提纲已生成：{md_path}")
    print(f"\n👉 请用编辑器打开并修改该文件，修改完成后回来继续。")
    print(f"   路径：{md_path}")
    input("\n修改完成后，按 Enter 继续生成PPT...")

    # Step 2: 读取修改后的提纲
    with open(md_path, "r", encoding="utf-8") as f:
        outline_text = f.read()

    # Step 3: 解析提纲 → 图片已在 outline_dir/figures/ 中，直接引用路径
    outline_dir = os.path.dirname(md_path)
    figures_dir = os.path.join(outline_dir, "figures")
    print("\n⏳ 正在解析提纲并生成PPT数据...")
    ppt_text, label_to_path = parse_outline_to_ppt_input(
        outline_text, pdf_path, output_dir=figures_dir
    )

    # 询问输出路径
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    default_out = os.path.join(outline_dir, f"{pdf_name}_汇报.pptx")
    out = input(f"\nPPT输出路径（默认：{default_out}）：").strip()
    output_path = out if out else default_out

    # Step 4: 生成PPT
    print(f"\n⏳ 生成PPT中，预计需要20秒...")
    agent = PPTAgent()
    try:
        result = agent.generate(ppt_text, output_path)
        print(f"\n✅ PPT生成成功：{result}")
    except Exception as e:
        print(f"\n❌ 生成失败：{e}")
        raise


def run():
    ctrl = InteractiveController()
    agent = PPTAgent()

    print("\n🎯 ShuoClaw PPT 生成器")
    print("=" * 50)
    print("  1. 直接输入内容生成PPT")
    print("  2. 从PDF文献生成汇报PPT（推荐）")
    print("  3. 增强版模式（新能力：深度解析+审核+公式渲染）")
    mode = input("选择模式（默认1）：").strip() or "1"

    if mode == "2":
        run_paper_workflow()
        return
    
    if mode == "3":
        # 增强版模式
        print("\n⏳ 加载增强版 Agent...")
        try:
            from enhanced_agent import EnhancedPPTAgent
            enhanced_agent = EnhancedPPTAgent(enable_enhancements=True)
            
            print("\n📄 增强版 PDF 文献汇报工作流")
            print("=" * 50)
            pdf_path = input("请输入 PDF 文件路径：").strip().strip('"')
            if not os.path.exists(pdf_path):
                print(f"❌ 文件不存在：{pdf_path}")
                return
            
            # 询问功能配置
            enable_review = input("启用节点审核机制？(y/n，默认y)：").strip().lower() != 'n'
            enable_formula = input("启用 LaTeX 公式渲染？(y/n，默认y)：").strip().lower() != 'n'
            
            # 输出路径
            pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
            default_out = os.path.join(os.path.dirname(pdf_path), f"{pdf_name}_汇报.pptx")
            out = input(f"\nPPT输出路径（默认：{default_out}）：").strip()
            output_path = out if out else default_out
            
            # 生成 PPT
            print(f"\n⏳ 生成 PPT 中...")
            result = enhanced_agent.generate_from_pdf(
                pdf_path,
                output_path,
                enable_review_gate=enable_review,
                enable_formula_rendering=enable_formula
            )
            
            if result:
                print(f"\n✅ PPT 生成成功：{result}")
            else:
                print(f"\n⚠️ PPT 生成被中止")
        
        except ImportError:
            print("❌ 增强版 Agent 不可用，请检查 enhanced_agent.py")
            return
        except Exception as e:
            print(f"❌ 生成失败：{e}")
            import traceback
            traceback.print_exc()
        
        return

    # 节点1：询问基本信息
    basic = ctrl.ask_basic_info()

    # 询问内容输入方式
    print("\n📝 内容输入方式：")
    print("  1. 直接输入文本（输入完成后输入 END 结束）")
    print("  2. 输入文件路径（.txt / .md）")
    mode = input("选择（默认1）：").strip() or "1"

    user_content = ""
    if mode == "2":
        fpath = input("文件路径：").strip()
        with open(fpath, "r", encoding="utf-8") as f:
            user_content = f.read()
    else:
        print("请输入内容（输入 END 结束）：")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        user_content = "\n".join(lines)

    # 拼接基本信息到内容
    full_input = f"""主题：{basic['title']}
汇报人：{basic['author']}
导师：{basic.get('advisor','')}
日期：{basic.get('date','')}
场景：{basic.get('scene','通用')}

{user_content}"""

    # AI 解析
    print("\n⏳ AI 解析内容中...")
    try:
        structured = ai_parse(full_input)
        outline = structured.get("sections", [])
        print("✅ AI 解析完成")
    except Exception as e:
        print(f"⚠️  AI 解析失败（{e}），将使用规则解析")
        structured = None
        outline = []

    # 节点2：确认大纲
    if outline:
        confirmed = ctrl.confirm_outline(outline)
        if not confirmed:
            feedback = ctrl.confirmed.get("outline_feedback", "")
            if feedback:
                print(f"\n⏳ 根据反馈重新生成大纲：{feedback}")
                full_input += f"\n\n修改要求：{feedback}"
                structured = ai_parse(full_input)
                outline = structured.get("sections", [])
                ctrl.confirm_outline(outline)

    # 节点3：预览页数并确认生成
    preview = agent.preview(full_input) if not structured else []
    page_count = len(outline) * 2 + 3  # 估算：封面+目录+章节+内容+结尾
    if not ctrl.confirm_generate(page_count):
        print("已取消生成。")
        return

    # 输出路径
    output_path = ctrl.ask_output_path()

    # 生成 PPT
    print("\n⏳ 生成 PPT 中...")
    try:
        if structured:
            # 将结构化数据转为文本再传入（兼容现有 parser）
            text = _structured_to_text(structured)
            result = agent.generate(text, output_path)
        else:
            result = agent.generate(full_input, output_path)
        print(f"\n✅ PPT 生成成功：{result}")
    except Exception as e:
        print(f"\n❌ 生成失败：{e}")
        return

    # 节点4：询问修改
    modification = ctrl.ask_modification()
    if modification:
        print(f"\n⏳ 正在处理修改：{modification}")
        full_input += f"\n\n修改要求：{modification}"
        try:
            structured = ai_parse(full_input)
            text = _structured_to_text(structured)
            result = agent.generate(text, output_path)
            print(f"✅ 修改完成：{result}")
        except Exception as e:
            print(f"❌ 修改失败：{e}")

def _structured_to_text(data: dict) -> str:
    """将结构化数据转回文本格式（兼容现有 parser）"""
    lines = []
    meta = data.get("meta", {})
    if meta.get("title"):    lines.append(f"主题：{meta['title']}")
    if meta.get("author"):   lines.append(f"申请人：{meta['author']}")
    if meta.get("advisor"):  lines.append(f"导师：{meta['advisor']}")
    if meta.get("date"):     lines.append(f"时间：{meta['date']}")
    lines.append("")
    for i, sec in enumerate(data.get("sections", []), 1):
        lines.append(f"{i}. {sec.get('title','章节'+str(i))}")
        for item in sec.get("items", sec.get("points", [])):
            lines.append(f"- {item}")
        for evt in sec.get("events", []):
            lines.append(f"- {evt.get('date','')} {evt.get('title','')}：{evt.get('description','')}")
        lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    run()
