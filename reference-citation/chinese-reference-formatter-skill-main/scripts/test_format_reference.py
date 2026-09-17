import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("format_reference.py")


def run_formatter(payload, start=1):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--start", str(start)],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout


def test_formats_english_journal_with_bibtex():
    output = run_formatter(
        {
            "type": "article",
            "title": "Semi-supervised classification with graph convolutional networks",
            "authors": ["Kipf, Thomas N", "Welling, Max"],
            "journal": "International Conference on Learning Representations",
            "year": 2017,
            "doi": "10.48550/arXiv.1609.02907",
            "sources": ["https://openreview.net/forum?id=SJU4ayYgl"],
        }
    )

    assert "标准参考文献：[1] Kipf T N, Welling M. Semi-supervised Classification with Graph Convolutional Networks[J]. International Conference on Learning Representations, 2017. DOI:10.48550/arXiv.1609.02907." in output
    assert "@article{kipf-2017-semi-supervised-classification" in output
    assert "author = {Kipf, Thomas N and Welling, Max}" in output
    assert "核验来源：https://openreview.net/forum?id=SJU4ayYgl" in output


def test_limits_more_than_three_english_authors():
    output = run_formatter(
        {
            "type": "inproceedings",
            "title": "Focal loss for dense object detection",
            "authors": [
                "Lin, Tsung-Yi",
                "Goyal, Priya",
                "Girshick, Ross",
                "He, Kaiming",
                "Dollár, Piotr",
            ],
            "booktitle": "Proceedings of the IEEE International Conference on Computer Vision",
            "year": 2017,
            "pages": "2980-2988",
        }
    )

    assert "Lin T Y, Goyal P, Girshick R, et al. Focal Loss for Dense Object Detection[C]. Proceedings of the IEEE International Conference on Computer Vision, 2017:2980-2988." in output


def test_formats_chinese_journal():
    output = run_formatter(
        {
            "type": "article",
            "title": "理想的图书馆员和信息专家的素质与形象",
            "authors": ["李炳穆"],
            "journal": "图书情报工作",
            "year": 2000,
            "issue": "2",
            "pages": "5-8",
        }
    )

    assert "标准参考文献：[1] 李炳穆. 理想的图书馆员和信息专家的素质与形象[J]. 图书情报工作, 2000(2):5-8." in output
    assert "5-8.." not in output
    assert "title = {理想的图书馆员和信息专家的素质与形象}" in output


def test_formats_online_resource_with_access_date():
    output = run_formatter(
        {
            "type": "online",
            "title": "出版业信息化驶入快车道",
            "authors": ["萧玉"],
            "published_date": "2001-12-19",
            "access_date": "2002-04-15",
            "url": "http://www.creader.com/news/200112-19/200112-190019.html",
        }
    )

    assert "萧玉. 出版业信息化驶入快车道[EB/OL]. (2001-12-19)[2002-04-15]. http://www.creader.com/news/200112-19/200112-190019.html." in output


def test_reports_unmatched_title():
    output = run_formatter({"title": "definitely not a real paper title", "status": "not_found"})

    assert "未找到与“definitely not a real paper title”明确对应的公开文献。" in output
