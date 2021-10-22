build:
	docker build -t rkrikbaev/service-prophet:v1.1.4 .
run:
	docker run --rm -v /Users/rustamkrikbayev/prophet/service:/app -p 8005:8005 rkrikbaev/service-prophet:v1.1.4