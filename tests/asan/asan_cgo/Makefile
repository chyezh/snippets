MILVUS_GO_BUILD_TAGS="dynamic,sonic"
CGO_LDFLAGS := $(shell go env CGO_LDFLAGS) -fsanitize=address -fno-omit-frame-pointer
CGO_CFLAGS := $(shell go env CGO_CFLAGS) -fsanitize=address -fno-omit-frame-pointer
MILVUS_GO_BUILD_TAGS := $(MILVUS_GO_BUILD_TAGS)
USE_ASAN := ON

# Build each component and install binary to $GOPATH/bin.
install:
	@echo "Installing binary to './bin'"
	@(env USE_ASAN=$(USE_ASAN) bash $(PWD)/scripts/install_milvus.sh)
	@echo "Installation successful."
