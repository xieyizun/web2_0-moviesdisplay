import os.path

import tornado.options
import tornado.ioloop
import tornado.httpserver
import tornado.web

from tornado.options import define, options
define ("port", default=8888, help = "run on the given port", type=int)

class item:
	def __init__(self, name, file_type, content):
		self.name = name
		self.file_type = file_type
		self.content = content
		
class MovieVeiewHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('introduction.html')

class MoviesHandler(tornado.web.RequestHandler):
	def get(self, movie):
		file_path = os.path.join(os.path.dirname(__file__), "static/movie/" + movie)
		filenames = os.listdir(file_path)

		files = []
		for filename in filenames:
			if os.path.splitext(filename)[1][1:] == 'txt':
				file_txt = open(os.path.join(file_path, filename), 'r')
				file_type = os.path.splitext(filename)[1][1:]
				content = []
				for line in file_txt:
					content.append(line.strip('\n'))
				file_instance = item(filename, file_type, content)
				files.append(file_instance)

		files.sort(key = lambda x:(x.file_type, x.name))
		self.render('template.html', files = files, title = movie)

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers = [(r'/', MovieVeiewHandler), (r'/(["tmnt2", "tmnt", "mortalkombat", "princessbride"]+)', MoviesHandler),(r'/XIEYIZUN_MOVIES_PAGE/(["tmnt2", "tmnt", "mortalkombat", "princessbride"]+)', MoviesHandler),],
		debug = True,
		template_path = os.path.join(os.path.dirname(__file__), "template"),
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		autoescape = None,
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()




