import yt_dlp

ydl_opts = {}

def dwl_vid(video_url , name):
    # try:
    #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    #         ydl.download([video_url])
    #     return 'success'
    # except Exception as e:
    #     return f'error: {str(e)}'
    try:
        download_options = {
            'outtmpl': f'./files/videos/{name}.3gpp',  
            'format': 'best',
            'cookiefile': "cookies\www.youtube.com_cookies.txt"  
        }
        with yt_dlp.YoutubeDL(download_options) as ydl:
            ydl.download([video_url])
            
        return True
    except:
        return False