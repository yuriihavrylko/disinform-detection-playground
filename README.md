## Projector course work
Skeleton for project on projector course

### Docker 

Build
```
docker build --tag yuriihavrylko/prjctr:latest .
```

Push
Build
```
docker push yuriihavrylko/prjctr:latest
```

DH Images:
![Alt text](assets/images.png)

### GH Actions:

Works on push to master/feature*
![Alt text](assets/actions.png)


### Minio setup
Mac/Local
```
brew install minio/stable/minio

minio server --console-address :9001 ~/minio # path to persistent local storage + run on custom port
```

Docker

```
docker run \
   -p 9002:9002 \
   --name minio \
   -v ~/minio:/data \
   -e "MINIO_ROOT_USER=ROOTNAME" \
   -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
   quay.io/minio/minio server /data --console-address ":9002"
```

Kubernetes

```
kubectl create -f deployment/minio.yml
```
