
from flask import render_template, redirect, request, url_for, send_file
from Everest_Downloader import app
from pytube import YouTube
import urllib.request
import re
from Everest_Downloader import db
from Everest_Downloader.models import Song
import os


#renders home view
@app.route('/', methods=['GET', 'POST'])
def home():

    return render_template('base.html')


#download page below
@app.route('/search', methods=["GET", "POST"])
def search():
    global url_link
    if request.method == 'POST':
        try:
            search = str(request.form['url'])
        except:
            KeyError = 'url'

        if len(search) > 1:

            search = search.replace(" ", "+")
            search.lower()

            html = urllib.request.urlopen(
                "https://www.youtube.com/results?search_query=" + search)  # html for search

            video_ids = re.findall(
            r"watch\?v=(\S{11})", html.read().decode())  # decoded html to provide video id

            # get the actual url of the song searched
            url_link = "https://www.youtube.com/watch?v=" + video_ids[0]

            d_load = YouTube(url_link)
            # get title
            title = d_load.title
            #get albumArt
            albumArt = d_load.thumbnail_url
            

            return render_template('download.html', title = title, albumArt = albumArt, url_link = url_link)

        elif len(search) > 1 and search == re.findall(r"watch\?v=(\S{11})"):
            url_link = search
            d_load = YouTube(url_link)
            # get titles
            title = d_load.title
            albumArt = d_load.thumbnail_url
            return render_template('download.html', title=title, albumArt=albumArt, url_link= url_link)

        else:
            return render_template('base.html', eval = 1)


@app.route("/download", methods = ['GET', 'POST'])
def download_Opt():

    if request.method == 'POST':
        try:
            sChoice = str(request.form['Opt'])
        except:
            KeyError = 'Opt'
        d_load = YouTube(url_link)

        if sChoice == "video":
            stream = d_load.streams.get_highest_resolution() 
            filename = stream.download()
            return send_file(filename , as_attachment =True)
        elif sChoice == "audio":
            stream = d_load.streams.last()
            filename = stream.download()

            return send_file(filename, as_attachment =True, attachment_filename = filename.replace(".webm" , ".mp3"))
    
    else:
        return redirect(url_for('home'))







#mixtape page below

@app.route('/mixtape')
def mixtape():
    songs = Song.query.all()

    return render_template('Mixtape.html', songs = songs)



@app.route('/add', methods=['GET', 'POST'])
def add():

     if request.method == 'POST':
        try:
            search = str(request.form['url'])
        except:
            KeyError = 'url'

        if len(search) > 1:

            search = search.replace(" ", "+")
            search.lower()

            html = urllib.request.urlopen(
                "https://www.youtube.com/results?search_query=" + search)  # html for search

            video_ids = re.findall(
            r"watch\?v=(\S{11})", html.read().decode())  # decoded html to provide video id

            # get the actual url of the song searched
            link = "https://www.youtube.com/watch?v=" + video_ids[0]

            d_load = YouTube(link)
            # get title
            title = d_load.title

            mix_List = Song(title,link)
            db.session.add(mix_List)
            db.session.commit()

            return redirect(url_for('mixtape'))
        
        elif len(search) > 1 and search == re.findall(r"watch\?v=(\S{11})"):
            url_link = search
            d_load = YouTube(url_link)
            # get titles
            title = d_load.title

            mix_List = Song(title,link)
            db.session.add(mix_List)
            db.session.commit()

            return redirect(url_for('mixtape'))
            
        else:
            return redirect(url_for('mixtape', eval = 1))
    
     else: 
            return render_template(
        'base.html')

#creating and downloading multiple music list
@app.route('/create', methods =['GET', 'POST'])
def create():
    
    if request.method == "POST":
        try:
            path = str(request.form['dir'])
        except:
            KeyError = 'dir'

        if len(path) > 1:

            path.strip()
            path.replace('\\', '//')

            #path = os.path.join(parent_dir, folder_name)
            '''
            try:
                os.mkdir(path)
            except OSError as e:
                print(e)
            '''
            songs = Song.query.all()
            for song in songs:
                d_load = YouTube(song.link)
                stream = d_load.streams.last()
                filename = stream.download(path, filename = 'title')
                dest = path+"/"+song.title+".mp3"
                webm_file = path+"/"+"title"+".webm"
                try:
                    os.rename(webm_file, dest )
                except WindowsError:
                    os.remove(dest)
                    os.rename(webm_file, dest)

            remove_all()
   
            return redirect(url_for('mixtape'))
        else:
            return render_template("Mixtape.html", eval = 1)
    else:
        return redirect(url_for('mixtape'))



#deletes song
@app.route('/mixtape/<int:id>/delete/')
def delete(id):
    song = Song.query.get(id)
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('mixtape'))

#remove all
@app.route('/mixtape/remove_all/')
def remove_all():
    song = Song.query.all()
    for songs in song:
        db.session.delete(songs)
        db.session.commit()
    return redirect(url_for('mixtape'))








