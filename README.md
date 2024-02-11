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


### Streamlit 

Run:
```
streamlit run src/serving/streamlit.py
```

![Alt text](assets/streamlit.png)


Deploy k8s:
```
kubectl create -f deployment/app-ui.yml
kubectl port-forward --address 0.0.0.0 svc/app-ui.yml 8080:8080
```


### Fast API 

Postman

![Alt text](assets/fastapi.png)



Deploy k8s:
```
kubectl create -f deployment/app-fasttext.yml
kubectl port-forward --address 0.0.0.0 svc/app-fasttext 8090:8090
```

### DVC

Install DVC

```
brew install dvc
```

Init in repo

```
dvc init --subdir
git status
git commit -m "init DVC"
```

Move file with data and add to DVC, commit DBV data config

```
dvc add ./data/data.csv
git add data/.gitignore data/data.csv.dvc
git commit -m "create data"
```

Add remote data storage and push DVC remote config
(ensure that bucket already created)

```
dvc remote add -d minio s3://ml-data
dvc remote modify minio endpointurl [$AWS_ENDPOINT](http://10.0.0.6:9000)

git add .dvc/config
git commit -m "configure remote"
git push 
```

Upload data
```
export AWS_ACCESS_KEY_ID='...'
export AWS_SECRET_ACCESS_KEY='...'
dvc push


### Label studio

```
docker pull heartexlabs/label-studio:latest
docker run -it -p 8080:8080 -v `pwd`/mydata:/label-studio/data heartexlabs/label-studio:latest
```

![Alt text](assets/labeling.png)


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


