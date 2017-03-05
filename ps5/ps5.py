#
#           .a,s=||+|"|"|+|||<=s_a,>,            .aaaass_a_s,s=i=ii_a_a,,.
#          .m`                     --"?g.    s%"!"~-.                   {a.
#         .v}                         .3p   .m`                         .X;
#         .m`          ._wwyywa,.      )W,=_sW.     _awqmXqwa.           Ii
#         :#.    _.  .wZTWW#  ~?Va.    <WQQQQW;   .d!^9B?   "?>         .<1.
#         =Z.     "???^  -~      ~     )QWQQQQo.                         <1
#         =Z.                         .dZ^^^^"W,                        .v>
#         :m.                         =W~     )q.                       .m`
#         .U;                        .mY       ?o.                      =X .
#          +w.                      .gT         Ya.                    .q:
#           ?s.                    sm!           "q,.              .__av^
#            -"!"!+|=i_s_s_a_s=|>"?"`            . +"!"""!+|+""!"!""~ .
#
#                                  _mWm,      <mmc
#                                  -?V?`      "??`
#
#
#
#
#
#
#             _ww,      aw;      sac        aw,  <ym.     uQW)  mQQQQQQQQm
#             =QWQw,    dWc      QWm,.      dWc  -UWp.   <QW)   dQe
#             =QWVQQc   dQc     QW QQa      dQc   -WQa  _WWe    dQc
#             =Qm  WQw  dQc    mQS  QQa.    dQc     WWc.qQE     dQQQQQQQmm
#             =Qm   ?QQadQc   qQQQQQWWQg,   dQc     {WQwQB      dQe
#             =Qm    "$WQWc  uQW^     VWm,  dQc      9WWB       dQg
#             =$B      ?QWc @$W^       YQE  mWc       TY        3VTYYYYYTY
#


import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self,guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate.replace(tzinfo=pytz.timezone("EST"))

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate




#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self,phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self,text):
        # replace punctuation with ' '
        for char in string.punctuation:
            text = text.replace(char, ' ')

        def is_sublist(a,b):
            if a == []: return True
            if b == []: return False
            return b[:len(a)] == a or is_sublist(a, b[1:])

        return is_sublist(self.phrase.split(),text.lower().split())

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self,phrase):
        super(TitleTrigger, self).__init__(phrase)

    def evaluate(self,story):
        return self.is_phrase_in(story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self,phrase):
        super(DescriptionTrigger,self).__init__(phrase)

    def evaluate(self,story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):

# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
    def __init__(self,triggertime):
        dtime = datetime.strptime(triggertime, "%d %b %Y %H:%M:%S")
        dtime = dtime.replace(tzinfo=pytz.timezone("EST"))
        self.triggertime = dtime

# Problem 6
class BeforeTrigger(TimeTrigger):

    def __init__(self,triggertime):
        super(BeforeTrigger,self).__init__(triggertime)

    def evaluate(self, story):
        return story.get_pubdate() < self.triggertime

class AfterTrigger(TimeTrigger):
    def __init__(self, triggertime):
        super(AfterTrigger, self).__init__(triggertime)

    def evaluate(self, story):
        return story.get_pubdate() > self.triggertime

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self,othertrigger):
        self.othertrigger = othertrigger

    def evaluate(self,story):
        return not self.othertrigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self,othertrigger1,othertrigger2):
        self.othertrigger1 = othertrigger1
        self.othertrigger2 = othertrigger2

    def evaluate(self,story):
        return self.othertrigger1.evaluate(story) and self.othertrigger2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self,othertrigger1,othertrigger2):
        self.othertrigger1 = othertrigger1
        self.othertrigger2 = othertrigger2

    def evaluate(self,story):
        return self.othertrigger1.evaluate(story) or self.othertrigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    result = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                result.append(story)
                break
    return result



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    for item in lines:


    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("machine lea")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

