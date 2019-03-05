build.all:
	make -C http build
	make -C pricing build
	make -C ranking build

services.up:
	make -C http app.up
	make -C pricing app.up
	make -C ranking app.up

app.up: build.all
	docker-compose up

install:
	brew install docker-compose