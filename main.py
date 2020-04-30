import json
import math
import glob, os
from enum import Enum
from pprint import pprint
import time
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
###################################
class Stats:
  def  __init__ (self):
    self.msg_count = 0
    self.recv_reacts = {}
    self.giv_reacts = {}
    self.photos = 0
    self.tod = []

  msg_count = 0
  recv_reacts = {}
  giv_reacts = {}
  photos = 0
  tod = []
###################################
thebois = {}
###################################
os.chdir('/content/drive/My Drive/moist_analytics')
for file in glob.glob("*.json"):
    with open(file) as json_file:
      data = json.load(json_file)
      for p in data['messages']:
        stats= thebois.get(p["sender_name"], Stats())
        stats.msg_count += 1
        timestamp = time.gmtime(math.floor(int(p["timestamp_ms"])/1000))

        hr = timestamp[3]
        min = (timestamp[4] / 60)

        stats.tod.append(math.floor(hr))

        if 'photos' in p:
          if len(p["photos"]) > 0:
            stats.photos += len(p["photos"])
        if 'reactions' in p:
          if len(p["reactions"]) > 0:
            for reaction in p["reactions"]:
              react = stats.recv_reacts.get(reaction["reaction"],0)
              react += 1
              stats.recv_reacts[reaction["reaction"]] = react

              reactee_stats = thebois.get(reaction['actor'], Stats())
              giv_react = reactee_stats.giv_reacts.get(reaction["reaction"],0)
              giv_react += 1
              reactee_stats.giv_reacts[reaction["reaction"]] = giv_react

        thebois[p["sender_name"]] = stats

###################################

for boi in (thebois):
  print(boi + ":")
  print("  Messages : " + str(thebois[boi].msg_count))
  print("  Photos   :   " + str(thebois[boi].photos))
  print("  Reactions Recieved: ")
  for react in sorted(thebois[boi].recv_reacts.keys()):
    print("     " + str(react.encode('latin1').decode('utf8')) +  ": " + str(thebois[boi].recv_reacts[react]))
  total_r += sum(thebois[boi].recv_reacts.values())

  print("  Reactions Given: ")
  for react in sorted(thebois[boi].giv_reacts.keys()):
      print("     " + str(react.encode('latin1').decode('utf8')) +  ": " + str(thebois[boi].giv_reacts[react]))
  total_g += sum(thebois[boi].giv_reacts.values())
  np.random.seed(19380801)
  points = {}
  for i in range (0,math.ceil(max(thebois[boi].tod))):
    points[str(i)] = 0
  for time in thebois[boi].tod:
      freq = points.get(str(time),0)
      freq += 1
      points[str(time)] = freq
  # pprint(points)
  x =  points.keys()
  y_pos = points.values()
  # print(sum(y_pos))
  plt.bar(x,y_pos, align='center', alpha=0.5)
  # plt.xticks(y_pos, objects)
  plt.ylabel('Message Count')
  plt.xlabel('Hour')
  plt.title(boi)

  plt.show()

###################################


