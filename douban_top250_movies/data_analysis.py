# -*- coding: utf-8 -*-
# encoding:utf-8
import random
import matplotlib.pyplot as plt
import numpy as np
import pymongo
import settings
from matplotlib.font_manager import FontProperties

plt.rcdefaults()

font = FontProperties(fname=r'resources/造字工房可可体.ttf', size=12)


def pic_show(con_name, movie_field, x_label, y_label, title):
    # Retrieve data from mongoDB
    client = pymongo.MongoClient(settings.MONGODB_URL, settings.MONGODB_PORT)
    db = client[settings.MONGODB_DB]
    collection = db[con_name]

    # Define two lists to save the data
    count = []
    movie_property = []

    # Append data into two lists respectively
    for item in collection.find():
        count.append(item['count'])
        movie_property.append(item[movie_field])

    # Bar chart's bottom range
    y_pos = np.arange(len(movie_property))

    # Random color method
    r = lambda: random.randint(0, 255)
    color = '#%02X%02X%02X' % (r(), r(), r())

    # Create a horizontal bar chart
    plt.barh(y_pos, count, color=color, align='center', alpha=0.4)

    # Set the locations and labels of the yticks
    plt.yticks(y_pos, movie_property, fontproperties=font)

    # Add text to the axes (x, y, string)
    for count, y_pos in zip(count, y_pos):
        plt.text(count, y_pos, count, horizontalalignment='center', verticalalignment='center')

    # Give y,x axes and title's label
    plt.ylabel(y_label, fontproperties=font)
    plt.xlabel(x_label, fontproperties=font)
    plt.title(title, fontproperties=font)

    # Y-limits of axes
    plt.ylim(+(len(movie_property)), -1.0)

    # Save the bar chart into a file
    plt.savefig('output/' + con_name + '.png')

    # Clear the entire current figure
    plt.clf()


pic_show('category', 'movie_category', u'分类出现次数', u'风格分类', u'豆瓣top250电影风格统计')
pic_show('country', 'movie_country', u'国家出现次数', u'国家分类', u'豆瓣top250电影国家统计')
