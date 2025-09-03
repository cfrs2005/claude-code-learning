# Lesson 6: Bilibili 视频字幕提取与内容处理

## 🎯 学习目标

- 掌握从 Bilibili 视频提取字幕的技术方法
- 学习视频内容的自动化处理和分析
- 理解字幕数据的结构化和应用
- 实现基于视频内容的学习资料生成

## 📖 理论基础

### 为什么需要视频字幕提取？

视频教程是学习的重要资源，但有以下痛点：

1. **内容检索困难** - 视频内容无法像文本一样搜索
2. **学习效率低** - 需要完整观看才能找到关键信息
3. **笔记整理麻烦** - 手动记录视频内容耗时耗力
4. **多语言障碍** - 无法快速翻译或理解外语内容

### 技术原理

#### 1. Bilibili 字幕获取机制
```
视频页面 → API 调用 → 字幕文件下载 → 格式解析 → 内容提取
```

#### 2. 字幕格式标准
- **JSON 格式** - B站标准字幕格式，包含时间轴和文本
- **SRT 格式** - 通用字幕格式，便于兼容各种工具
- **ASS 格式** - 高级字幕格式，支持样式和特效

#### 3. 内容处理流程
```
原始字幕 → 文本清洗 → 内容分段 → 关键词提取 → 结构化整理 → 学习资料生成
```

## 🚀 实战演练

### 步骤 1: Bilibili 字幕提取工具

创建 `bilibili-subtitle-extractor.py`:

```python
#!/usr/bin/env python3
"""
Bilibili 视频字幕提取工具
支持从 B 站视频提取字幕并转换为各种格式
"""

import requests
import json
import re
import os
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import argparse
import srt
import ass


class BilibiliSubtitleExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_video_info(self, url: str) -> Dict:
        """获取视频基本信息"""
        # 提取 BV 号
        bvid = self.extract_bvid(url)
        if not bvid:
            raise ValueError("无法从 URL 中提取 BV 号")
        
        # 获取视频信息
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
        response = self.session.get(api_url)
        response.raise_for_status()
        
        data = response.json()
        if data['code'] != 0:
            raise ValueError(f"获取视频信息失败: {data['message']}")
        
        return data['data']
    
    def extract_bvid(self, url: str) -> Optional[str]:
        """从 URL 中提取 BV 号"""
        patterns = [
            r'BV[a-zA-Z0-9]+',
            r'bvid=([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(0) if 'BV' in match.group(0) else match.group(1)
        return None
    
    def get_subtitle_list(self, bvid: str) -> List[Dict]:
        """获取字幕列表"""
        api_url = f"https://api.bilibili.com/x/web-interface/v2/aid/info?bvid={bvid}"
        response = self.session.get(api_url)
        response.raise_for_status()
        
        data = response.json()
        if data['code'] != 0:
            return []
        
        # 获取字幕信息
        video_data = data.get('data', {})
        subtitle_info = video_data.get('subtitle', {})
        
        if not subtitle_info.get('allow_submit', False):
            return []
        
        subtitles = subtitle_info.get('list', [])
        return subtitles
    
    def download_subtitle(self, subtitle_url: str) -> Dict:
        """下载字幕文件"""
        response = self.session.get(subtitle_url)
        response.raise_for_status()
        return response.json()
    
    def convert_to_srt(self, subtitle_data: Dict) -> str:
        """转换为 SRT 格式"""
        srt_subs = []
        
        for i, body in enumerate(subtitle_data.get('body', []), 1):
            start_time = body['from']
            end_time = body['to']
            content = body['content']
            
            # 转换时间格式
            start_srt = self.seconds_to_srt_time(start_time)
            end_srt = self.seconds_to_srt_time(end_time)
            
            srt_sub = srt.Subtitle(
                index=i,
                start=srt.srt_timedelta_to_timedelta(start_srt),
                end=srt.srt_timedelta_to_timedelta(end_srt),
                content=content
            )
            srt_subs.append(srt_sub)
        
        return srt.compose(srt_subs)
    
    def convert_to_ass(self, subtitle_data: Dict) -> str:
        """转换为 ASS 格式"""
        script = ass.Script()
        
        # 添加样式
        style = ass.Style(
            name='Default',
            fontname='Arial',
            fontsize=20,
            primarycolor=&HFFFFFF,
            secondarycolor=&H000000,
            outlinecolor=&H000000,
            backcolor=&H80000000,
            bold=0,
            italic=0,
            underline=0,
            strikeout=0,
            scalex=100,
            scaley=100,
            spacing=0,
            angle=0,
            borderstyle=1,
            outline=1,
            shadow=0,
            alignment=2,
            marginl=0,
            marginr=0,
            marginv=0,
            encoding=1
        )
        script.styles.append(style)
        
        # 添加字幕
        for body in subtitle_data.get('body', []):
            start_time = body['from']
            end_time = body['to']
            content = body['content']
            
            event = ass.Dialogue(
                style='Default',
                start=start_time,
                end=end_time,
                text=content
            )
            script.events.append(event)
        
        return str(script)
    
    def seconds_to_srt_time(self, seconds: float) -> srt.srt_timedelta:
        """秒数转换为 SRT 时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        
        return srt.srt_timedelta(
            hours=hours,
            minutes=minutes,
            seconds=secs,
            milliseconds=milliseconds
        )
    
    def extract_text_content(self, subtitle_data: Dict) -> str:
        """提取纯文本内容"""
        text_parts = []
        for body in subtitle_data.get('body', []):
            text_parts.append(body['content'])
        return '\n'.join(text_parts)
    
    def process_video(self, url: str, output_dir: str = 'output') -> Dict:
        """处理视频字幕提取的完整流程"""
        # 创建输出目录
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 获取视频信息
        video_info = self.get_video_info(url)
        bvid = video_info['bvid']
        title = video_info['title']
        
        print(f"正在处理视频: {title}")
        print(f"BV 号: {bvid}")
        
        # 获取字幕列表
        subtitles = self.get_subtitle_list(bvid)
        
        if not subtitles:
            print("该视频没有可用的字幕")
            return {}
        
        results = {}
        
        for subtitle in subtitles:
            subtitle_id = subtitle['id']
            subtitle_lang = subtitle['lan']
            subtitle_url = subtitle['subtitle_url']
            
            print(f"正在下载字幕: {subtitle_lang}")
            
            # 下载字幕
            subtitle_data = self.download_subtitle(subtitle_url)
            
            # 生成文件名
            safe_title = re.sub(r'[^\w\s-]', '', title).strip()
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            
            base_filename = f"{safe_title}_{subtitle_lang}"
            
            # 保存各种格式
            formats = {
                'json': lambda data: json.dumps(data, ensure_ascii=False, indent=2),
                'srt': self.convert_to_srt,
                'ass': self.convert_to_ass,
                'txt': self.extract_text_content
            }
            
            format_files = {}
            for format_name, format_func in formats.items():
                filename = f"{base_filename}.{format_name}"
                filepath = Path(output_dir) / filename
                
                try:
                    if format_name == 'json':
                        content = format_func(subtitle_data)
                    else:
                        content = format_func(subtitle_data)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    format_files[format_name] = str(filepath)
                    print(f"  已保存: {filename}")
                    
                except Exception as e:
                    print(f"  保存 {format_name} 格式失败: {e}")
            
            results[subtitle_lang] = {
                'subtitle_id': subtitle_id,
                'language': subtitle_lang,
                'files': format_files
            }
        
        return {
            'video_info': video_info,
            'subtitles': results
        }


def main():
    parser = argparse.ArgumentParser(description='Bilibili 视频字幕提取工具')
    parser.add_argument('url', help='Bilibili 视频 URL')
    parser.add_argument('-o', '--output', default='output', help='输出目录')
    parser.add_argument('--formats', nargs='+', default=['json', 'srt', 'txt'],
                       help='输出的字幕格式')
    
    args = parser.parse_args()
    
    extractor = BilibiliSubtitleExtractor()
    
    try:
        result = extractor.process_video(args.url, args.output)
        
        if result:
            print("\n提取完成!")
            print(f"视频标题: {result['video_info']['title']}")
            print(f"提取的字幕语言: {list(result['subtitles'].keys())}")
        else:
            print("字幕提取失败")
            
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
```

### 步骤 2: 字幕内容分析工具

创建 `subtitle-analyzer.py`:

```python
#!/usr/bin/env python3
"""
字幕内容分析工具
用于分析和处理提取的字幕内容
"""

import json
import re
from typing import Dict, List, Set
from collections import Counter, defaultdict
import jieba
import jieba.analyse
from pathlib import Path


class SubtitleAnalyzer:
    def __init__(self):
        # 加载中文分词词典
        jieba.initialize()
    
    def load_subtitle(self, file_path: str) -> Dict:
        """加载字幕文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_keywords(self, subtitle_data: Dict, top_k: int = 20) -> List[tuple]:
        """提取关键词"""
        text_content = self.extract_text_content(subtitle_data)
        
        # 使用 TF-IDF 提取关键词
        keywords = jieba.analyse.extract_tags(
            text_content,
            topK=top_k,
            withWeight=True
        )
        
        return keywords
    
    def extract_text_content(self, subtitle_data: Dict) -> str:
        """提取纯文本内容"""
        text_parts = []
        for body in subtitle_data.get('body', []):
            text_parts.append(body['content'])
        return ' '.join(text_parts)
    
    def analyze_content_structure(self, subtitle_data: Dict) -> Dict:
        """分析内容结构"""
        body_list = subtitle_data.get('body', [])
        
        # 时间分析
        durations = []
        for body in body_list:
            duration = body['to'] - body['from']
            durations.append(duration)
        
        # 文本长度分析
        text_lengths = [len(body['content']) for body in body_list]
        
        # 语速分析 (字/分钟)
        speech_rates = []
        for i, body in enumerate(body_list):
            duration_minutes = (body['to'] - body['from']) / 60
            if duration_minutes > 0:
                speech_rate = len(body['content']) / duration_minutes
                speech_rates.append(speech_rate)
        
        return {
            'total_segments': len(body_list),
            'total_duration': max(durations) if durations else 0,
            'average_duration': sum(durations) / len(durations) if durations else 0,
            'average_text_length': sum(text_lengths) / len(text_lengths) if text_lengths else 0,
            'average_speech_rate': sum(speech_rates) / len(speech_rates) if speech_rates else 0,
            'content_density': sum(text_lengths) / sum(durations) if durations else 0
        }
    
    def generate_study_notes(self, subtitle_data: Dict) -> str:
        """生成学习笔记"""
        keywords = self.extract_keywords(subtitle_data)
        structure = self.analyze_content_structure(subtitle_data)
        text_content = self.extract_text_content(subtitle_data)
        
        notes = f"""# 学习笔记

## 视频信息
- 总时长: {structure['total_duration']:.2f} 秒
- 字幕段数: {structure['total_segments']}
- 平均语速: {structure['average_speech_rate']:.2f} 字/分钟

## 关键词
"""
        
        for keyword, weight in keywords[:10]:
            notes += f"- {keyword} (权重: {weight:.3f})\n"
        
        notes += "\n## 内容摘要\n"
        
        # 简单的内容摘要（取前500个字符）
        summary = text_content[:500] + "..." if len(text_content) > 500 else text_content
        notes += summary
        
        return notes
    
    def generate_timeline(self, subtitle_data: Dict) -> List[Dict]:
        """生成时间线"""
        timeline = []
        
        for body in subtitle_data.get('body', []):
            timeline.append({
                'timestamp': body['from'],
                'time_formatted': self.format_timestamp(body['from']),
                'content': body['content'],
                'duration': body['to'] - body['from']
            })
        
        return timeline
    
    def format_timestamp(self, seconds: float) -> str:
        """格式化时间戳"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def search_content(self, subtitle_data: Dict, query: str) -> List[Dict]:
        """搜索内容"""
        results = []
        query_lower = query.lower()
        
        for body in subtitle_data.get('body', []):
            content = body['content']
            if query_lower in content.lower():
                results.append({
                    'timestamp': body['from'],
                    'time_formatted': self.format_timestamp(body['from']),
                    'content': content,
                    'context': self.get_context(subtitle_data, body, 2)
                })
        
        return results
    
    def get_context(self, subtitle_data: Dict, target_body: Dict, context_size: int) -> List[str]:
        """获取上下文"""
        body_list = subtitle_data.get('body', [])
        target_index = -1
        
        for i, body in enumerate(body_list):
            if body == target_body:
                target_index = i
                break
        
        if target_index == -1:
            return []
        
        start_index = max(0, target_index - context_size)
        end_index = min(len(body_list), target_index + context_size + 1)
        
        context = []
        for i in range(start_index, end_index):
            if i != target_index:
                context.append(body_list[i]['content'])
        
        return context


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='字幕内容分析工具')
    parser.add_argument('subtitle_file', help='字幕文件路径 (JSON格式)')
    parser.add_argument('-o', '--output', default='analysis', help='输出目录')
    parser.add_argument('--search', help='搜索内容')
    parser.add_argument('--keywords', type=int, default=20, help='关键词数量')
    
    args = parser.parse_args()
    
    analyzer = SubtitleAnalyzer()
    
    try:
        # 加载字幕文件
        subtitle_data = analyzer.load_subtitle(args.subtitle_file)
        
        # 创建输出目录
        Path(args.output).mkdir(parents=True, exist_ok=True)
        
        # 基本分析
        structure = analyzer.analyze_content_structure(subtitle_data)
        print("=== 内容结构分析 ===")
        print(f"总段数: {structure['total_segments']}")
        print(f"总时长: {structure['total_duration']:.2f} 秒")
        print(f"平均语速: {structure['average_speech_rate']:.2f} 字/分钟")
        
        # 关键词提取
        keywords = analyzer.extract_keywords(subtitle_data, args.keywords)
        print(f"\n=== 前{args.keywords}个关键词 ===")
        for keyword, weight in keywords:
            print(f"{keyword}: {weight:.3f}")
        
        # 生成学习笔记
        notes = analyzer.generate_study_notes(subtitle_data)
        notes_file = Path(args.output) / 'study_notes.md'
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(notes)
        print(f"\n学习笔记已保存: {notes_file}")
        
        # 生成时间线
        timeline = analyzer.generate_timeline(subtitle_data)
        timeline_file = Path(args.output) / 'timeline.json'
        with open(timeline_file, 'w', encoding='utf-8') as f:
            json.dump(timeline, f, ensure_ascii=False, indent=2)
        print(f"时间线已保存: {timeline_file}")
        
        # 搜索功能
        if args.search:
            results = analyzer.search_content(subtitle_data, args.search)
            print(f"\n=== 搜索结果: '{args.search}' ===")
            for result in results:
                print(f"[{result['time_formatted']}] {result['content']}")
        
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
```

### 步骤 3: 学习资料生成器

创建 `learning-material-generator.py`:

```python
#!/usr/bin/env python3
"""
学习资料生成器
基于字幕内容生成各种学习资料
"""

import json
import markdown
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import re


class LearningMaterialGenerator:
    def __init__(self):
        pass
    
    def load_subtitle_data(self, file_path: str) -> Dict:
        """加载字幕数据"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_quiz_questions(self, subtitle_data: Dict, question_count: int = 10) -> List[Dict]:
        """生成测验题目"""
        body_list = subtitle_data.get('body', [])
        questions = []
        
        # 简单的关键词提取和题目生成
        for i in range(0, min(question_count * 3, len(body_list)), 3):
            body = body_list[i]
            content = body['content']
            
            if len(content) > 10:  # 只处理有一定长度的内容
                # 生成填空题
                question = self.create_fill_in_blank_question(content, body['from'])
                if question:
                    questions.append(question)
                
                if len(questions) >= question_count:
                    break
        
        return questions
    
    def create_fill_in_blank_question(self, content: str, timestamp: float) -> Dict:
        """创建填空题"""
        # 简单的填空题生成逻辑
        words = re.findall(r'\b[\w\u4e00-\u9fff]+\b', content)
        
        if len(words) >= 3:
            # 选择中间位置的词作为答案
            answer_word = words[len(words) // 2]
            question_text = content.replace(answer_word, '________')
            
            return {
                'type': 'fill_in_blank',
                'question': question_text,
                'answer': answer_word,
                'timestamp': timestamp,
                'options': [answer_word] + self.generate_distractors(words, answer_word)
            }
        
        return None
    
    def generate_distractors(self, words: List[str], correct_answer: str) -> List[str]:
        """生成干扰项"""
        distractors = []
        for word in words:
            if word != correct_answer and len(word) > 1:
                distractors.append(word)
                if len(distractors) >= 3:
                    break
        
        return distractors
    
    def generate_study_guide(self, subtitle_data: Dict) -> str:
        """生成学习指南"""
        body_list = subtitle_data.get('body', [])
        
        guide = "# 学习指南\n\n"
        guide += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # 按内容分段
        sections = self.divide_into_sections(body_list)
        
        for i, section in enumerate(sections, 1):
            guide += f"## 第{i}部分\n\n"
            
            # 提取关键点
            key_points = self.extract_key_points(section)
            for point in key_points:
                guide += f"- {point}\n"
            
            guide += "\n"
            
            # 添加详细内容
            for body in section:
                guide += f"{body['content']}\n"
            
            guide += "\n---\n\n"
        
        return guide
    
    def divide_into_sections(self, body_list: List[Dict], section_size: int = 10) -> List[List[Dict]]:
        """将字幕分段"""
        sections = []
        for i in range(0, len(body_list), section_size):
            section = body_list[i:i + section_size]
            sections.append(section)
        return sections
    
    def extract_key_points(self, section: List[Dict]) -> List[str]:
        """提取关键点"""
        key_points = []
        
        for body in section:
            content = body['content']
            
            # 简单的关键点识别
            if any(keyword in content for keyword in ['重要', '关键', '核心', '要点', '注意']):
                key_points.append(content)
            elif len(content) > 20 and '。' in content:
                # 较长的句子可能是重要内容
                key_points.append(content)
        
        return key_points[:5]  # 最多返回5个关键点
    
    def generate_flashcards(self, subtitle_data: Dict) -> List[Dict]:
        """生成闪卡"""
        body_list = subtitle_data.get('body', [])
        flashcards = []
        
        for body in body_list:
            content = body['content']
            
            if len(content) > 10 and len(content) < 100:
                # 将内容分为问题和答案
                parts = content.split('，')
                if len(parts) >= 2:
                    question = parts[0].strip() + '？'
                    answer = '，'.join(parts[1:]).strip()
                    
                    flashcards.append({
                        'front': question,
                        'back': answer,
                        'timestamp': body['from']
                    })
        
        return flashcards
    
    def generate_vocabulary_list(self, subtitle_data: Dict) -> List[Dict]:
        """生成词汇表"""
        body_list = subtitle_data.get('body', [])
        vocabulary = []
        
        # 简单的词汇提取
        seen_words = set()
        
        for body in body_list:
            content = body['content']
            words = re.findall(r'\b[\w\u4e00-\u9fff]+\b', content)
            
            for word in words:
                if len(word) > 1 and word not in seen_words:
                    vocabulary.append({
                        'word': word,
                        'context': content,
                        'timestamp': body['from']
                    })
                    seen_words.add(word)
        
        return vocabulary
    
    def export_to_anki(self, flashcards: List[Dict], output_file: str):
        """导出到 Anki 格式"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for card in flashcards:
                # Anki 格式: front;back;tags
                f.write(f"{card['front']};{card['back']};video_learning\n")
    
    def export_all_materials(self, subtitle_data: Dict, output_dir: str):
        """导出所有学习资料"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 1. 学习指南
        study_guide = self.generate_study_guide(subtitle_data)
        with open(Path(output_dir) / 'study_guide.md', 'w', encoding='utf-8') as f:
            f.write(study_guide)
        
        # 2. 测验题目
        quiz_questions = self.generate_quiz_questions(subtitle_data)
        with open(Path(output_dir) / 'quiz_questions.json', 'w', encoding='utf-8') as f:
            json.dump(quiz_questions, f, ensure_ascii=False, indent=2)
        
        # 3. 闪卡
        flashcards = self.generate_flashcards(subtitle_data)
        with open(Path(output_dir) / 'flashcards.json', 'w', encoding='utf-8') as f:
            json.dump(flashcards, f, ensure_ascii=False, indent=2)
        
        # 4. Anki 格式闪卡
        self.export_to_anki(flashcards, Path(output_dir) / 'flashcards_anki.txt')
        
        # 5. 词汇表
        vocabulary = self.generate_vocabulary_list(subtitle_data)
        with open(Path(output_dir) / 'vocabulary.json', 'w', encoding='utf-8') as f:
            json.dump(vocabulary, f, ensure_ascii=False, indent=2)
        
        print(f"学习资料已生成到: {output_dir}")
        print(f"- study_guide.md: 学习指南")
        print(f"- quiz_questions.json: 测验题目")
        print(f"- flashcards.json: 闪卡数据")
        print(f"- flashcards_anki.txt: Anki 闪卡")
        print(f"- vocabulary.json: 词汇表")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='学习资料生成器')
    parser.add_argument('subtitle_file', help='字幕文件路径 (JSON格式)')
    parser.add_argument('-o', '--output', default='learning_materials', help='输出目录')
    parser.add_argument('--quiz-count', type=int, default=10, help='测验题目数量')
    
    args = parser.parse_args()
    
    generator = LearningMaterialGenerator()
    
    try:
        # 加载字幕数据
        subtitle_data = generator.load_subtitle_data(args.subtitle_file)
        
        # 生成所有学习资料
        generator.export_all_materials(subtitle_data, args.output)
        
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()
```

### 步骤 4: Claude Code 集成命令

创建 `.claude/commands/bilibili-subtitle-extractor.md`:

```markdown
---
description: 从 Bilibili 视频提取字幕并生成学习资料
argument-hint: [Bilibili视频URL]
allowed-tools: Write, Read, LS, Glob, Grep, Bash(python:*), Bash(curl:*)
---

# Bilibili 字幕提取和学习资料生成

你是一个专业的视频内容处理专家。请帮助用户从 Bilibili 视频提取字幕，并生成各种学习资料。

## 工作流程

### 1. 视频信息获取
- 解析 Bilibili URL，提取 BV 号
- 获取视频基本信息（标题、UP主、时长等）
- 检查视频是否有可用字幕

### 2. 字幕提取
- 下载所有可用的字幕文件
- 转换为多种格式（JSON、SRT、TXT）
- 保存到 organized 的目录结构

### 3. 内容分析
- 提取关键词和重要概念
- 分析内容结构和语速
- 生成时间线和内容索引

### 4. 学习资料生成
- 生成结构化的学习笔记
- 创建测验题目和闪卡
- 生成词汇表和学习指南
- 导出到 Anki 兼容格式

## 技术实现

使用提供的 Python 工具链：
- `bilibili-subtitle-extractor.py`: 字幕提取
- `subtitle-analyzer.py`: 内容分析
- `learning-material-generator.py`: 学习资料生成

## 输出格式

### 目录结构
```
output/
├── video_title/
│   ├── subtitles/
│   │   ├── video_title_zh.json
│   │   ├── video_title_zh.srt
│   │   └── video_title_zh.txt
│   ├── analysis/
│   │   ├── study_notes.md
│   │   ├── timeline.json
│   │   └── keywords.txt
│   └── learning_materials/
│       ├── study_guide.md
│       ├── quiz_questions.json
│       ├── flashcards.json
│       ├── flashcards_anki.txt
│       └── vocabulary.json
```

### 学习资料内容
- **学习指南**: 结构化的内容总结和关键点
- **测验题目**: 基于内容的理解测试
- **闪卡**: 便于记忆的知识点卡片
- **词汇表**: 视频中的重要词汇
- **时间线**: 带时间戳的内容索引

## 使用示例

```bash
# 基本使用
/bilibili-subtitle-extractor https://www.bilibili.com/video/BV1HEt4zAEqe

# 指定输出目录
/bilibili-subtitle-extractor https://www.bilibili.com/video/BV1HEt4zAEqe -o my_video

# 生成学习资料
/bilibili-subtitle-extractor https://www.bilibili.com/video/BV1HEt4zAEqe --generate-materials
```

请分析以下 Bilibili 视频：
$ARGUMENTS
```

## 📊 应用场景

### 1. 语言学习
```python
# 语言学习应用
subtitle_analyzer = SubtitleAnalyzer()
subtitle_data = subtitle_analyzer.load_subtitle('video.json')

# 提取词汇表
vocabulary = subtitle_analyzer.generate_vocabulary_list(subtitle_data)

# 生成语言学习闪卡
flashcards = subtitle_analyzer.generate_language_flashcards(subtitle_data)
```

### 2. 课程笔记整理
```python
# 自动化课程笔记
material_generator = LearningMaterialGenerator()
study_guide = material_generator.generate_study_guide(subtitle_data)

# 生成复习资料
quiz_questions = material_generator.generate_quiz_questions(subtitle_data)
```

### 3. 内容搜索和检索
```python
# 内容搜索功能
search_results = subtitle_analyzer.search_content(subtitle_data, "机器学习")

# 生成内容索引
timeline = subtitle_analyzer.generate_timeline(subtitle_data)
```

## 💡 高级功能

### 1. 多语言支持
- 自动检测字幕语言
- 多语言字幕并行处理
- 跨语言内容对比

### 2. 智能内容分析
- 关键概念提取
- 知识点关联分析
- 难度评估和分类

### 3. 个性化学习
- 基于用户水平的材料生成
- 自适应测验难度
- 学习进度跟踪

## 🎯 实战案例

### 案例 1: 技术教程学习

**视频**: Claude Code 高级技巧教程

**处理流程**:
1. 提取字幕内容
2. 分析技术关键词
3. 生成代码示例摘要
4. 创建实践测验题目

**输出**:
- 技术概念词汇表
- 代码要点总结
- 实践练习题目
- Anki 学习卡片

### 案例 2: 学术讲座处理

**视频**: 机器学习专题讲座

**处理流程**:
1. 提取专业术语
2. 生成概念关系图
3. 创建理论框架笔记
4. 生成复习测验

**输出**:
- 专业术语表
- 理论框架总结
- 概念关系图
- 学术理解测验

## 📝 练习作业

1. **基础练习**: 使用工具提取一个 Bilibili 视频的字幕，并生成基本的学习资料。

2. **进阶练习**: 自定义学习资料生成模板，针对特定类型的内容（如技术教程、语言学习等）。

3. **综合练习**: 创建一个完整的视频学习工作流，从字幕提取到学习资料生成的自动化流程。

4. **创新应用**: 设计一个基于字幕内容的智能学习助手，能够回答关于视频内容的问题。

## 🎓 总结

### 关键学习要点

1. **字幕提取技术** - 掌握从视频平台提取字幕的方法
2. **内容分析能力** - 理解如何从文本中提取有价值的信息
3. **学习资料生成** - 自动化创建各种学习辅助材料
4. **个性化学习** - 基于内容特点定制学习材料

### 实际应用价值

- **学习效率提升** - 自动化笔记和资料生成
- **内容组织优化** - 结构化的视频内容处理
- **知识管理** - 系统化的学习和复习材料
- **跨平台应用** - 适用于各种视频学习平台

---

**课程完成**: 恭喜！你已经掌握了 Bilibili 视频字幕提取和内容处理的技术。这些技能可以帮助你更高效地处理视频学习内容，自动化生成学习资料，提升学习效果。