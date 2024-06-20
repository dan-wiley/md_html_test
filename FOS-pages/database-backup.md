# Overview

One simple approach to making a database backup to create another Persistent Volume Claim and using a cronjob to backup 
the database.  

In Kubernetes, a Persistent Volume Claim (PVC) is a request for storage by a Pod. It allows Pods to request specific resources on a Persistent Volume (PV), which abstracts the underlying storage implementation details. This setup is crucial for applications that require persistent storage, such as databases.  

## Persistent Volume (PV)
A Persistent Volume (PV) in Kubernetes is a piece of networked storage provisioned by an administrator or dynamically provisioned using Storage Classes. PVs abstract the underlying storage details (like AWS EBS volumes) and provide a uniform interface for Pods to consume storage.  

## Storage Class (SC) - AWS GP3  
A Storage Class defines the types of PVs that can be dynamically provisioned and their properties. In our case, we use AWS Elastic Block Storage (EBS) GP3 volumes, a type of storage optimized for transactional and throughput-intensive workloads. GP3 volumes are commonly used in AWS EC2 instances and provide flexibility in adjusting performance and cost based on application requirements.

Notice in the prod env that the deployment-deb-prod.yaml file contains an import for a persistent volume claim, which is then mounted to the container. Below is a sample of the code template.
```
        volumeMounts: # The volume mounted to the container
        - name: orderbookdb-<TEAM> # Must match name of volume below
          mountPath: /var/lib/mysql # Location of MYSQL Database
      restartPolicy: Always
      volumes:
      - name: orderbookdb-<TEAM> # Create and name a volume from a PVC
        persistentVolumeClaim: # import the PVC
          claimName: ebs-gp3-claim-<TEAM> # Must be the same name as the PersistentVolumeClaim
```

The code above simply imports an existing Persistent Volume Claim (PVC), and mounts it. The code below creates the PVC in pv-claim-prod.yaml.  
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ebs-gp3-claim-<TEAM>
  namespace: <COHORT>-<TEAM>-prod # Team's namespace
spec:
  storageClassName: gp3 # Must be the same as the PersistentVolume. Look for kind: StorageClass yaml file
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

## How to implement a backup

Simply create another Persistent Volume Claim (PVC) file (different file name, and metadata.name). Then, create this cronjob to back up the database with the mysqldump command. Do not forget to update the namespace.
```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: mysql-backup-cronjob
  namespace: <COHORT>-<TEAM>-<ENV>
spec:
  schedule: "*/20 * * * 1-5"  # Every 20 mins
  jobTemplate:
    spec:
      template:
        spec:
          volumes:
          - name: backup-dir
            persistentVolumeClaim:
              claimName: ebs-gp3-claim-second-team06 # Use the second persistent volume claim
          containers:
          - name: mysql-backup
            image: public.ecr.aws/docker/library/mysql:8.0.31  # Use the mysql:8.0.31 image
            env:
            - name: MYSQL_ROOT_PASSWORD
              value: "wiley123"  # Replace with your MySQL root password
            command: ["/bin/bash", "-c"]
            args:
            - |
              #!/bin/bash

              # MySQL connection details
              MYSQL_USER=root
              MYSQL_HOST=orderbookdb
              MYSQL_PORT=3306

              # Backup directory
              BACKUP_DIR=/var/lib/mysql/backup
              BACKUP_FILE="$BACKUP_DIR/backup-$(date +%Y-%m-%d-%H-%M-%S).sql"

              # Dump MySQL databases to a file
              mysqldump -u $MYSQL_USER -p$MYSQL_ROOT_PASSWORD -h $MYSQL_HOST -P $MYSQL_PORT --all-databases > $BACKUP_FILE

              # Cleanup old backups
              MAX_BACKUPS=5
              cd "$BACKUP_DIR" || exit 1
              num_backups=$(ls -1 | wc -l)
              if ((num_backups > MAX_BACKUPS)); then
                  # Sort backup files by modification time and delete the oldest ones
                  ls -1t | tail -n +$((MAX_BACKUPS + 1)) | xargs rm -f
              fi
            volumeMounts:
            - name: backup-dir
              mountPath: /var/lib/mysql/backup  # Mount the backup directory from the second volume
          restartPolicy: OnFailure
```

Having the database backed up on two EBS volumes is a good idea, now if something happens to one, we have a backup. 
Better yet, if the Kubernetes administrator creates another storage class, we can update the storage class
in the new PVC to back it up with a different storage class (such as a different cloud provider like Azure).

Run the command below to verify the backup is made correctly.
```
kubectl describe cronjob mysql-backup-cronjob -n <COHORT>-<TEAM>-<ENV>
kubectl get pvc -n <COHORT>-<TEAM>-<ENV>
```

## Restore from backup
If you ever need to restore from a backup, you can simply connect a pod to the PVC and restore from it. Another way to achieve this goal is to take snapshots of the PVC. However, additional tools must be installed in our cluster for snapshots.

If you want to take this implementation to a hot-warm setup, create another deployment and mount the new PVC to it. If the first one fails, you can use the new one. The new deployment can also be used for read operations.
