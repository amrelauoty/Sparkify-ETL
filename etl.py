import os
import glob
import psycopg2
import pandas as pd 
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description:
    - reads the song files from its path
    - inserts the songs data and artists data to songs and artists dimensions
    """
    # open song file
    df = pd.read_json(filepath,lines=True)

    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].to_numpy()
    song_data = song_data.tolist()[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].to_numpy()
    artist_data = artist_data.tolist()[0] 
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description:
    - reads the log files data from its path filtred by NextSong page
    - inserts the time records from the log files into time dimension
    - inserts the user records from the log files into users dimensions
    - inserts the transactions which is the songs listening to songplays fact 
    """
    # open log file
    df = df = pd.read_json(filepath,lines=True) 

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = [(pd.to_datetime(data, unit='ms'),data.hour,data.day,data.week,data.month,data.year,data.day_of_week) for data in t]
    column_labels = ('timestamp', 'hour', 'day', 'week of year', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(data=time_data,columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (index,row['ts'],row['userId'],row['level'],songid,artistid,row['sessionId'],row['location'],row['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description:
    Get all the files with .json extension which are the songs files and log files
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=a9o2m6e7w7")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()