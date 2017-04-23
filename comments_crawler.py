import json
import requests


class CommentsCrawler(object):
    def __init__(self):
        self.offset = 0
        self.newListSize = 1
        self.results = []
        self.model = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/newList?offset={}&limit=30&showLevelThreshold=72&headLimit=1&tailLimit=2&callback=getData&ibc=newspc'

    def getId(self, newsId):
        self.newsId = newsId

    def getComments(self):
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
            print('{} {}'.format(self.newListSize, self.offset))


if __name__ == '__main__':
    crawler = CommentsCrawler()
    newsId = 'CIKJGSUN0001875N'
    crawler.getId(newsId)
    crawler.getComments()
    print(crawler.results)
