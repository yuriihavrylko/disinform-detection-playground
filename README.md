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
