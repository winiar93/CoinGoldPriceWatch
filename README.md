# kubernetes-web-app

### Simple flask application to track price of gold coins.
### Prepared to deploy on kubernetes or docker.

![alt text](https://github.com/winiar93/kubernetes-web-app/blob/main/app_screenshot.jpg)

### Stack:
* Flask
* beautifulsoup4
* redis


## HOW2:

### Docker:
* For local use change redis host to `rejson` in scraper file and web file.
* build local docker images:
  `docker compose up --build`
  
### Minikube:
* In case of running in minikube cluster set host to `redis-master.default.svc.cluster.local`
* Before next step check if application works than delete running containers.
* Run commands in cmd:

  `kubectl apply -f deployment_redis.yaml`
  
  `kubectl apply -f deployment-scraper.yaml`
  
  `kubectl apply -f asset-mint-service.yaml`
  
  `kubectl expose deployments scraper --type=NodePort`
  
  `kubectl expose deployment asset-mint --type=NodePort`
  
  `kubectl expose deployment redis-master --port 6379 --type=NodePort`
