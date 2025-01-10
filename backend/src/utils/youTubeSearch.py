from youtube_search import YoutubeSearch

def search_youtube(search_term):
    results = YoutubeSearch(search_term, max_results=1).to_dict()
    return results



test =[
    {
        'id': 'xR_pWVoVM-M',
        'thumbnails':
            [
                'https://i.ytimg.com/vi/xR_pWVoVM-M/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLCw9rrdvk7x92B01UZQsOlnxG6-9A', 
                'https://i.ytimg.com/vi/xR_pWVoVM-M/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLAcmS5oAn6HXL8RV2QYAPOSLr5eLQ'
            ],
            'title': 'PubMed: Identifying Search Terms',
            'long_desc': None,
            'channel': 'Welch Medical Library',
            'duration': '10:08',
            'views': '43,512 views',
            'publish_time': '4 years ago',
            'url_suffix': '/watch?v=xR_pWVoVM-M&pp=ygUMc2VhcmNoIHRlcm1z'
    }, 
    {
        'id': 'B6-LZHuL_S0',
        'thumbnails':
            [
                'https://i.ytimg.com/vi/B6-LZHuL_S0/hq720.jpg?sqp=-oaymwEjCOgCEMoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLAad-w_3JNbwHUpJwhuPZ2WPx6T_A', 
                'https://i.ytimg.com/vi/B6-LZHuL_S0/hq720.jpg?sqp=-oaymwEXCNAFEJQDSFryq4qpAwkIARUAAIhCGAE=&rs=AOn4CLDTkepxUu_bKQ_5l90nKQPP4LfSJQ'
            ],
            'title': 'Keywords vs Search Terms',
            'long_desc': None,
            'channel': 'Scott Redgate',
            'duration': '4:35',
            'views': '500 views',
            'publish_time': '1 year ago',
            'url_suffix': '/watch?v=B6-LZHuL_S0&pp=ygUMc2VhcmNoIHRlcm1z'
    }]