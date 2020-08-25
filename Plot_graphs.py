

#Ploting timeseries of facetime
import matplotlib.pyplot as plt 
import numpy as np
import imageio
import os
import glob


def plot_bars(timeseries_df,length_each_frame):
    timeseries_df2=timeseries_df.copy()
    timeseries_df2.pop("name")
    timeseries_df2.pop("time")
    timeseries_df2.pop("record_source")
    timeseries_df2.pop("date")
    
    # if max(timeseries_df2.max()) > 120:
    #     timeseries_df2=timeseries_df2[timeseries_df2.columns]/60
    #     label='speaker (minutes)'
    # else:
    label='speaker (seconds)'
        
    try:
        timeseries_df2.pop('break_time')
    except KeyError :
        pass
    try:
        timeseries_df2.pop('none')
    except KeyError :
        pass
        
    files = glob.glob('./gif/all/*')
    for f in files:
        os.remove(f)
    
    order=timeseries_df2.max().sort_values(ascending=False).keys().tolist() #####
    
    
    y_pos=np.arange(len(order))
    x_speak=[]
    ims=0
    imss=[]
    
    


    color=['darkblue', 'mediumblue', 'slateblue', 'cadetblue', 'dodgerblue',
           "lightseagreen","mediumaquamarine", "mediumturquoise", "skyblue",
           "powderblue","darkseagreen", "palegreen", "darkgrey","silver","gainsboro",
           "khaki", "moccasin","bisque","thistle"]

    for i in timeseries_df.iterrows():
        for ii in np.arange(len(order)):
            x_speak.append(i[1][(order[ii])])
        plt.figure(figsize=(15,3))
        plt.barh(y_pos, x_speak, align='center',color=color)
        plt.yticks(y_pos,order)
        plt.xlim(xmax=int(1.10*max(timeseries_df2.max().values)))
        plt.xlabel(label)
        
        x_speak=[]
        ims+=1
        imss.append(ims)
        
    #Saving the frames
        plt.savefig('./gif/all/'+str(ims)+'.png',dpi=150)
        plt.show()
        
    
    #Creating Gif
    folder = './gif/all' 
    files = [f"{folder}\\{file}.png" for file in (imss)]
    
    
    images = [imageio.imread(file) for file in files]
    imageio.mimwrite('./gif/movie.gif', images, fps=1/length_each_frame)
    
    print("Gif saved")
    
    
    
    # def plot_plot(timeseries_df,length_each_frame):
    # timeseries_df2=timeseries_df.copy()
    # timeseries_df2.pop("name")
    # timeseries_df2.pop("time")
    # timeseries_df2.pop("record_source")
    # timeseries_df2.pop("date")
    # try:
    #     timeseries_df2.pop('break_time')
    # except KeyError :
    #     pass
    # try:
    #     timeseries_df2.pop('none')
    # except KeyError :
    #     pass
        
    # files = glob.glob('./gif/all/*')
    # for f in files:
    #     os.remove(f)
    
    # order=timeseries_df2.max()[1:].sort_values(ascending=False).keys().tolist()
    
    
    # y_pos=np.arange(len(order))
    # x_speak=[]
    # ims=0
    # imss=[]
    
    


    # color=['darkblue', 'mediumblue', 'slateblue', 'cadetblue', 'dodgerblue',
    #        "lightseagreen","mediumaquamarine", "mediumturquoise", "skyblue",
    #        "powderblue","darkseagreen", "palegreen", "darkgrey","silver","gainsboro",
    #        "khaki", "moccasin","bisque","thistle"]

    # for i in timeseries_df.iterrows():
    #     for ii in np.arange(len(order)):
    #         x_speak.append(i[1][(order[ii])])
    #     plt.figure(figsize=(15,3))
    #     plt.barh(y_pos, x_speak, align='center',color=color)
    #     plt.yticks(y_pos,order)
    #     plt.xlim(xmax=int(1.05*max(timeseries_df2.max()[1:].values)))
        
    #     x_speak=[]
    #     ims+=1
    #     imss.append(ims)
        
    # #Saving the frames
    #     plt.savefig('./gif/all/'+str(ims)+'.png',dpi=150)
    #     plt.show()
        
    
    # #Creating Gif
    # folder = './gif/all' 
    # files = [f"{folder}\\{file}.png" for file in (imss)]
    
    
    # images = [imageio.imread(file) for file in files]
    # imageio.mimwrite('./gif/movie.gif', images, fps=1/length_each_frame)
    
