``` bash
$ pwd
./pl-crawler/
```

``` bash
$ docker volume create \
    --driver local \
    --name crawl_logs \
    --opt type=none \
    --opt o=bind \
    --opt device="$(pwd)"/logs
```

``` bash
$ docker rmi pycrawler
```

``` bash
$ docker build . -t pycrawler
```

``` bash
$ docker run \
    --log-driver=none -a stdin -a stdout -a stderr \
    --mount type=bind,source="$(pwd)"/logs,target=/home/logs \
    --security-opt seccomp=seccomp_profile.json \
    --ipc host \
    --name test \
    -e TEST_ID='1' \
    -e DATASET="test" \
    -e BROWSER="chrome" \
    -e URL="google.com" \
    -it pycrawler
```
