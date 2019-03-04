build.all:
	make -C http build
	make -C pricing build
	make -C ranking build

app.up:
	docker-compose up

install:
	brew install docker-compose