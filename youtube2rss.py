#!/usr/bin/env python
import sys

from gdata.youtube import service as YT

from urlparse import parse_qs, urlparse

from feed.date import rfc3339
from feed.date import rfc822

def PrintEntryDetails(entry):
  rss = """
<item>
  <guid isPermaLink="false">youtube:{yt_id}</guid>
  <title>{title_text}</title> 
  <pubDate>{timestamp}</pubDate>
  <description>
    <iframe width="560"
            height="315"
            src="https://www.youtube.com/embed/{yt_id}?rel=0"
            frameborder="0"
            allowfullscreen="true">
    </iframe>
  <div>{desc}</div>
  </description>
</item>
"""
  yt_id     = parse_qs(urlparse(entry.media.player.url).query)['v'][0]
  timestamp = rfc822.timestamp_from_tf(
      rfc3339.tf_from_timestamp(entry.published.text)
  )
  return rss.format(
      yt_id       = yt_id,
      title_text  = entry.media.title.text,
      timestamp   = timestamp,
      desc        = entry.media.description.text
  )

def PrintVideoFeed(yfeed):
    return "".join(PrintEntryDetails(entry) for entry in yfeed.entry)

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
