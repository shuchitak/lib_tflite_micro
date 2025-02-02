# patch the library if flag not present
.tflite_micro_patched.flag:
	cd lib_tflite_micro/submodules/tflite-micro && patch -p0 -i ../../../patches/tflite-micro.patch
	touch .tflite_micro_patched.flag

build: .tflite_micro_patched.flag
	(cd xinterpreters/xinterpreters/host && make install)

clean:
	(cd xinterpreters/xinterpreters/host && make clean)

init:
	python3 fetch_dependencies.py
	python3 -m venv .venv && \
	. .venv/bin/activate && \
	pip3 install --upgrade pip && \
	pip3 install -r requirements.txt

test:
	(. .venv/bin/activate && pip3 install ./xinterpreters)
	(. .venv/bin/activate && cd host_cmd_line_interpreter && make test)
	(. .venv/bin/activate && cd xinterpreters/xinterpreters/host && make test)
	@echo ""
	@echo "All tests PASS"
	@echo ""
