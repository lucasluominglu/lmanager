def application(environ,start_reponse):
	start_reponse('200 ok',[('Content-Type','txet/heml')])
	return [b'<h1> hello word</h1>']