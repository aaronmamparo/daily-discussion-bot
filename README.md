# Environment Variables
* REDDIT_CLIENT_ID
* REDDIT_CLIENT_SECRET
* REDDIT_USERNAME
* REDDIT_PASSWORD
* SUBREDDIT
* N_TOPICS_TO_POST

# Topics Sources
* https://conversationstartersworld.com/would-you-rather-questions/
* https://conversationstartersworld.com/questions-to-get-to-know-someone/
* https://conversationstartersworld.com/good-questions-to-ask/

To scrape, run this in the browser's javascript console:
```javascript
var topics = [];
jQuery('.entry-content p').each(function(i, p) {
  topics.push(p.innerText);
});
console.log(JSON.stringify(topics));
```
