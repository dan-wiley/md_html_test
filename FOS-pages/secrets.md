# Secrets

Passwords in source code are bad practice. We can hide our passwords through secrets. Kubernetes comes with an object called secret, but this would require us to manually run a `kubectl apply` command with the secret. To make it worthwhile with our infra, we can use External Secrets.

> Below is an example of how to make the secret object. Just update the namespace and place the manifest below in your project directory.

NOTE: The ExternalSecret Kubernetes manifest below shows you how to reference the existing parameterstore values, and create secrets from them. **You do not need to create any secrets in AWS, they already exist**. The existing values are `/eks-sre-course/mysql`, `/eks-sre-course/mysql_connection` and `/eks-sre-course/mysql_exporter`. 

```
apiVersion: external-secrets.io/v1alpha1
kind: ExternalSecret
metadata:
  name: mysql-secret
  namespace: <COHORT>-<TEAM>-<ENV>
spec:
  secretStoreRef:
    name: parameterstore
    kind: ClusterSecretStore
  target:
    name: mysql-secret
  data:
    - secretKey: MYSQL_PASSWORD
      remoteRef:
        key: /eks-sre-course/mysql
    - secretKey: MYSQL_CONNECTION
      remoteRef:
        key: /eks-sre-course/mysql_connection
    - secretKey: MYSQL_EXPORTER
      remoteRef:
        key: /eks-sre-course/mysql_exporter
```

In the deployment-db file, update the env variable value to use the valueFrom, as shown below

```
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: MYSQL_PASSWORD
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: MYSQL_PASSWORD
```


You may have noticed that some passwords exist in the Orderbook source code. You can remove them by using **os. getenv** with an environment variable and supplying the value of the env variable in the Kubernetes deployment when the container is created. If you use os.getenv("MYSQL_PASSWORD") in the source code of the fastapi (from the pss-orderbook repo) than the deployment-api.yaml file will need the env variable set from the secret, as shown above.



There is an additional file with a password, exporter-setup.sql. You can delete this file if you **add this lifecycle hook to the deployment-db.yaml file**. Just make sure the env variable MYSQL_PASSWORD is set. The postStart event will trigger and exec the command immediately when the container starts. Be sure to read the documentation on lifecycle hooks before modifying the deployment https://kubernetes.io/docs/tasks/configure-pod-container/attach-handler-lifecycle-event/ . Also, read the documentation on the docker-entrypoint-initdb.d from the MySQL docker hub.

```
        lifecycle:
          postStart:
            exec:
              command:
              - "/bin/sh"
              - "-c"
              - |
                echo "Hello, World!" > /tmp/poststart.log
                echo "CREATE USER 'exporter'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';" > /tmp/exporter.sql
                echo "GRANT PROCESS, REPLICATION CLIENT ON *.* TO 'exporter'@'%';" >> /tmp/exporter.sql
                echo "GRANT SELECT ON *.* TO 'exporter'@'%';" >> /tmp/exporter.sql
                cp /tmp/exporter.sql /docker-entrypoint-initdb.d/exporter.sql
```
