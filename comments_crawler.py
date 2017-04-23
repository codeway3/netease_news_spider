import json
import requests

if __name__ == '__main__':
    results = []
    newsId = 'CIKJGSUN0001875N'
    offset = 0
    newListSize = 1
    while offset < newListSize:
        url = 'http://comment.news.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/{}/comments/newList?offset={}&limit=30&showLevelThreshold=72&headLimit=1&tailLimit=2&callback=getData&ibc=newspc'.format(newsId, offset)
        r = requests.get(url)
        data = r.text
        data = data[8:]
        data = data[:-3]
        j = json.loads(data)
        newListSize = j['newListSize']
        commentIds = j['commentIds']
        comments = j['comments']
        for commentId in commentIds:
            commentId = commentId.split(',')
            comment = comments[commentId[-1]]
            results.append(comment['content'])
        offset += 30
        print('{} {}'.format(newListSize, offset))
    print(results)
