import os
import re

source_template = """
<a href="{{url}}" target="_blank">{{title}}</a>
"""
class DesignerAgent:
    def __init__(self, output_dir):
        self.output_dir = output_dir


    def load_html_template(self):
        relative_path = "../templates/article/index.html"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        html_file_path = os.path.join(dir_path, relative_path)
        with open(html_file_path, encoding="utf-8") as f:
            html_template = f.read()
        return html_template

    def designer(self, article):
        html_template = self.load_html_template()
        title = article["title"]
        date = article["date"]
        image = article["image"]
        paragraphs = article["paragraphs"]
        html_template = html_template.replace("{{title}}", title)
        html_template = html_template.replace("{{image}}", image)
        html_template = html_template.replace("{{date}}", date)
        len_paragraphs = len(paragraphs)
        print("required number of paragraphs: 5, current number of paragraphs:", len_paragraphs)
        for i in range(min(len_paragraphs, 5)):
            html_template = html_template.replace(f"{{paragraph{i + 1}}}", paragraphs[i])
        # Add sources
        sources = article["sources"]
        for i in range(min(len(sources), 5)):
            source = sources[i]
            source_html = source_template.replace("{{url}}", source["url"])
            source_html = source_html.replace("{{title}}", source["title"])
            html_template = html_template.replace(f"{{source{i + 1}}}", source_html)
        article["html"] = html_template
        article = self.save_article_html(article)
        return article

    def save_article_html(self, article):
        filename = re.sub(r'[\/:*?"<>| ]', '_', article['query'])
        filename = f"{filename}.html"
        path = os.path.join(self.output_dir, filename)
        with open(path, 'w', encoding="utf-8") as file:
            file.write(article['html'])
        article["path"] = filename
        return article

    def run(self, article: dict):
        article = self.designer(article)
        return article
