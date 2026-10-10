# -*- coding: utf-8 -*-

import os
import sys
import unittest


TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SPIDER_DIR = os.path.dirname(TEST_DIR)
if SPIDER_DIR not in sys.path:
    sys.path.insert(0, SPIDER_DIR)

import cleaning
import classify
import sources
import storage


class StorageTests(unittest.TestCase):
    def test_normalize_news_url_normalizes_scheme_host_and_trailing_slash(self):
        self.assertEqual(
            storage.normalize_news_url("WWW.Example.com/news/"),
            "http://www.example.com/news",
        )


class CleaningTests(unittest.TestCase):
    def test_collect_content_image_urls_filters_placeholder_and_resolves_relative(self):
        html = """
        <div>
          <img src="/images/a.jpg" />
          <img data-src="https://cdn.example.com/loading.gif" />
          <img data-original="//cdn.example.com/b.png" />
        </div>
        """
        result = cleaning.collect_content_image_urls(html, "https://example.com/article")
        self.assertEqual(
            result,
            ["https://example.com/images/a.jpg", "https://cdn.example.com/b.png"],
        )

    def test_inject_images_before_body_adds_images_once(self):
        result = cleaning.inject_images_before_body("正文", ["https://a.com/1.jpg"], max_n=1)
        self.assertIn("<img", result)
        self.assertTrue(result.endswith("正文"))


class SourcesTests(unittest.TestCase):
    def test_build_article_fetch_headers_adds_referer(self):
        headers = sources.build_article_fetch_headers("https://news.example.com/path/a.html")
        self.assertEqual(headers["Referer"], "https://news.example.com/")

    def test_extract_video_url_from_html_prefers_media_urls(self):
        html = '<meta property="og:video:url" content="//video.example.com/a.mp4" />'
        result = sources.extract_video_url_from_html(html, "https://news.example.com/a.html")
        self.assertEqual(result, "https://video.example.com/a.mp4")


class ClassifyTests(unittest.TestCase):
    def test_classify_news_category_detects_international_news(self):
        category = classify.classify_news_category(
            "联合国安理会就中东局势举行紧急会议",
            "多国代表在联合国讨论中东局势与外交协调，外交部回应国际安全关切。",
            "https://example.com/world/1",
            "人民网",
        )
        self.assertEqual(category, "国际")

    def test_classify_news_category_detects_science_technology(self):
        category = classify.classify_news_category(
            "国产人工智能芯片实现新突破",
            "科研团队发布新一代人工智能芯片和半导体技术成果。",
            "https://example.com/tech/1",
            "新华社",
        )
        self.assertEqual(category, "科技")


if __name__ == "__main__":
    unittest.main()
