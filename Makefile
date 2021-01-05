install:
	pip install -r requirements.txt

test:
	python -m unittest discover -s tests -p 'test_*.py'

docker:
	docker run -it --name mosquitto -p 1883:1883 eclipse-mosquitto

run:
	python -m mqttrdc.mqtt_controller

doc:
	pdoc --html --force --output-dir docs mqttrdc

show-doc:
	pdoc --http : mqttrdc

.PHONY: install test docker run doc show-doc