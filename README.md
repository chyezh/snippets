# snippets
snippets of code

## Build your milvus local development environment

### Setup Environment

```bash
# Set the path to your milvus repository
export MILVUS_DEV_PATH="$REPOSITORY_PATH/chyezh/milvus"
# Set the path to your milvus volumes to store the milvus cluster.
export MILVUS_VOLUME_DIRECTORY="$HOME/tmp/milvus-volumes"
# Set the path to your inf data volumes
export MILVUS_INF_VOLUME_DIRECTORY="$HOME/volumes"
# Set the path to your monitor data volumes
export MONITOR_VOLUME_DIRECTORY="$MILVUS_INF_VOLUME_DIRECTORY/monitor"
# Set the path to your filebrowser volumes
export FILEBROWSER_VOLUME_DIRECTORY="$MILVUS_INF_VOLUME_DIRECTORY/filebrowser"
```
### Start Monitoring

```bash
cd monitor && cp -r * $MONITOR_VOLUME_DIRECTORY
cd $MONITOR_VOLUME_DIRECTORY && docker compose up -d
```

### Add untility functions

you can find some utility functions in `zsh/.zshrc`
such as

- `jmilvusll` to jump to the last milvus log directory.
- `jmilvuslv` to jump to the last milvus volume directory.

### Start Milvus

```bash
docker network create milvus_inf
milvus_control -s -c start_milvus_full
jmilvusll
```
