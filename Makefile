# https://pyinstaller.org/en/stable/
# https://medium.com/hackernoon/the-one-stop-guide-to-easy-cross-platform-python-freezing-part-1-c53e66556a0a

macos: build run-macos

build:
	python3 -m venv venv
	. venv/bin/activate && \
	pip3 install -U pyinstaller && \
	pip3 install -r requirements.txt && \
	pyinstaller ./SoundbarBlocker.py --workpath ./build/tmp --distpath ./build --noconfirm --clean --windowed --paths ./venv/lib/python3.11/site-packages
	rm -rf ./build/tmp

run-macos:
	./build/SoundbarBlocker.app/Contents/MacOS/SoundbarBlocker

clean:
	rm -rf build
	rm SoundbarBlocker.spec
	rm -rf venv
