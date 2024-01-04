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

### Label studio

```
docker pull heartexlabs/label-studio:latest
docker run -it -p 8080:8080 -v `pwd`/mydata:/label-studio/data heartexlabs/label-studio:latest
```

![Alt text](assets/labeling.png)

