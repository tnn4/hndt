# Python Hacker News API Wrapper (PHNAW)

## Quick start

Get list of id top stories (max: 500)
```py
python3
>>> import phnaw
>>> print(phnaw.get_stories('top'))
```

Get list of id of new stories (max: 500)
```py
>>> print(phnaw.get_stories('new'))
```

Get list of id of best stories (max: 500)
```py
>>> print(phnaw.get_stories('best'))
```

Get list of id of ask HN (max: 200)
```py
>>> print(phnaw.get_stories('ask'))
```

Get list of id of show HN  (max: 200)
```py
>>> print(phnaw.get_stories('show'))
```

Get list of id of job posts (500)
```py
>>> print(phnaw.get_stories('job'))
```

## Development

Base url: https://hacker-news.firebaseio.com/v0/maxitem.json

basic | endpoint
--- | ---
user | `/v0/user/{id}`
item | `/v0/item/{id}`

### Change Notifications
- get front page ranking, new items and new profiles from these endpoints

topic | note | endpoint
---|---|---
newest item  | walk backwards to discover all items |`/v0/maxitem`
top stories  | up to 500 |`/v0/topstories`
new stories  | up to 500 |`/v0/newstories`
best stories | up to 500 |`/v0/beststories`
ask HN       | up to 200 |`/v0/askstories`
show HN      | up to 200 |`/v0/showstories`
job stories  | up to 200 |`/v0/jobstories`
updates      | item and profile changes, number varies| `/v0/updates`


