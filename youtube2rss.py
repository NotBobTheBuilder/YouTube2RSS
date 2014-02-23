#!/usr/bin/env python
import sys

from gdata.youtube import service as YT

from urlparse import parse_qs, urlparse

from feed.date import rfc3339
from feed.date import rfc822

class Channel:
    def __init__(self, channel):
        self.channel  = channel

        self.service  = YT.YouTubeService()
        uri           = "http://gdata.youtube.com/feeds/api/users/{u}/uploads"
        self.uri      = uri.format(u=channel)
        self.yfeed    = self.service.GetYouTubeVideoFeed(self.uri)
        self.vidcount = int(self.yfeed.total_results.text) 

    def __iter__(self):
        self.index = 0
        return self

    def next(self):
        if self.index >= self.vidcount:
            raise StopIteration
        self.index += 1

        if len(self.yfeed.entry) == 0:
            self.fetch_next()

        return self.yfeed.entry.pop(0)

    def __str__(self):
        return "\n".join(PrintEntryDetails(entry) for entry in self)

    def fetch_next(self):
        uri = self.uri + "?start-index=" + str(self.index)
        self.yfeed = self.service.GetYouTubeVideoFeed(uri)

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

if __name__ == "__main__":
    print str(Channel(sys.argv[1]))
