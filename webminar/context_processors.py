from django.conf import settings
 
 
def global_settings(request):
	# return any necessary values
	return {
		'RTMP_URL': settings.RTMP_URL,
		'RTMP_KEY': settings.RTMP_KEY,
		'HLS_URL': settings.HLS_URL,
		'HLS_KEY': settings.HLS_KEY,
		'RTSP_URL': settings.RTSP_URL,
		'JWPLAYER_KEY': settings.JWPLAYER_KEY
	}
