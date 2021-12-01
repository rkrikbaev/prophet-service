build:
	docker build -t rkrikbaev/servie-prophet:v1.0.1 .
run:
	docker run -it --rm -v /Users/rustamkrikbayev/PycharmProjects/webserveAs1C/service/prophet:/app -p 8005:8005 rkrikbaev/pyinstaller:prophet