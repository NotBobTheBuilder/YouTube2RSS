#!/usr/bin/env python
import sys

from gdata.youtube import service as YT

from urlparse import *

from feed.date import rfc3339
from feed.date import rfc822

def PrintEntryDetails(entry):
  YT_ID = parse_qs(urlparse(entry.media.player.url).query)['v'][0]
  rss = ''
  rss+= '<item>'
  rss+= "<guid isPermaLink='false'>youtube:%s</guid>" % YT_ID
  rss+= '<title>%s</title>' % entry.media.title.text
  rss+= '<pubDate>%s</pubDate>' % rfc822.timestamp_from_tf(
      rfc3339.tf_from_timestamp(entry.published.text)
      )
  rss+= '<description><iframe width="560" height="315" src="https://www.youtube.com/embed/%(url)s?rel=0" frameborder="0" allowfullscreen="true" ></iframe><div>%(desc)s</div></description>' % {"url" : YT_ID, "desc" : entry.media.description.text}
  rss+= '</item>'
  return rss

def PrintVideoFeed(yfeed):
    rss=''
    for entry in yfeed.entry:
        rss+=PrintEntryDetails(entry)

    return rss

def GetChannel(channelName):
    yt_service = YT.YouTubeService()

    # You can also retrieve a YouTubeVideoFeed by passing in the URI
    uri = 'http://gdata.youtube.com/feeds/api/users/%s/uploads?max-videos=25' % channelName
    yfeed = yt_service.GetYouTubeVideoFeed(uri)
    videoCount = int(yfeed.total_results.text)
    rss = PrintVideoFeed(yfeed)
    videoCount-=25
    if videoCount>0: feedPair = [uri+'&start-index=',25]
    while videoCount>0:
        yfeed = yt_service.GetYouTubeVideoFeed(feedPair[0]+str(feedPair[1]))
        #print feedPair[0]+str(feedPair[1])
        rss+=PrintVideoFeed(yfeed)
        videoCount-=25
        feedPair[1]+=25
    return rss



def main(argv=sys.argv):
    print GetChannel(argv[1])

if __name__ == "__main__":
    main()
