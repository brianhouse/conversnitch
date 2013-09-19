import threading, queue, time, twitter
from housepy import config, log


class TweetSender(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue.Queue()
        self.sender = twitter.Twitter(auth=twitter.OAuth(   config['twitter']['access_token'], 
                                                            config['twitter']['access_token_secret'], 
                                                            config['twitter']['consumer_key'], 
                                                            config['twitter']['consumer_secret']
                                                        ))        
        self.start()        


    def run(self):
        while True:
            message = self.queue.get()
            log.info("SENDING TWEET: %s" % message)
            self.sender.statuses.update(status=message)
            log.info("--> sent")


if __name__ == "__main__":
    tweet_sender = TweetSender()
    tweet_sender.queue.put("A message")
    while True:
        time.sleep(1)