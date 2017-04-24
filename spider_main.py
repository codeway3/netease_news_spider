import url_manager
import html_parser
import html_outputer
import html_downloader
import comments_crawler
import re


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.crawler = comments_crawler.CommentsCrawler()

    def craw(self, root_url, asked_num):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()  # 从urls集合中获取一个新url
                print('crawing page{}: {}'.format(count, new_url))  # 显示当前爬取页面的url
                html_cont = self.downloader.download(new_url)
                new_urls = self.parser.parse(new_url, html_cont)  # 解析当前页面，获取新的urls集合
                self.urls.add_new_urls(new_urls)  # 将新urls集合添加至旧urls集合中
                cnt = 0
                for url in new_urls:
                    cnt += 1
                    print("url {}/{}: {}".format(cnt, len(new_urls), url))
                    m = re.search(r'\/(\w{16})\.html', url)  # 正则匹配获取新闻ID
                    if m:
                        news_id = m.group(1)
                    else:
                        continue
                    # print(news_id)  # 验证news_id正确性
                    self.crawler.craw(news_id)

                if count == asked_num:
                    break
                count = count + 1
            except Exception as e:
                print('craw failed', e)


if __name__ == '__main__':
    root_url = "http://news.163.com/"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url, 5)
