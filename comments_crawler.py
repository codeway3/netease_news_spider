import sys
import json
import requests


class CommentsCrawler(object):
    def _set_id(self, newsId):
        self.offset = 0
        self.newListSize = 1
        self.results = []
        self.model = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/newList?offset={}&limit=30&showLevelThreshold=72&headLimit=1&tailLimit=2&callback=getData&ibc=newspc'
        self.newsId = newsId

    def _get_comments(self):
        while self.offset < self.newListSize:
            url = self.model.format(self.newsId, self.offset)
            r = requests.get(url)
            data = r.text
            data = data[8:]
            data = data[:-3]
            j = json.loads(data)
            self.newListSize = j['newListSize']
            commentIds = j['commentIds']
            comments = j['comments']
            for commentId in commentIds:
                commentId = commentId.split(',')
                comment = comments[commentId[-1]]
                self.results.append(comment['content'])
            self.offset += 30
            if self.offset > self.newListSize:
                self.offset = self.newListSize
            sys.stdout.write('\r共{}条评论，正在爬取第{}条'.format(self.newListSize, self.offset))
        sys.stdout.write('\n')
        # sys.stdout.flush()

    def _print_results(self):
        print('编号{}新闻爬取完毕！'.format(self.newsId))
        print('sample: ', self.results[:10])

    def craw(self, newsId):
        self._set_id(newsId)
        self._get_comments()
        self._print_results()


if __name__ == '__main__':
    crawler = CommentsCrawler()
    newsId = 'CIKJGSUN0001875N'
    crawler.craw(newsId)
