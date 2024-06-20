# YAML Error Alerts
Our environment runs our containers in Kubernetes. We add YAML files to the sre-course-infra GitHub repo
and FluxCD (our continuous deployment tool) automatically deploys the YAML files. 
FluxCD uses Kustomization objects (./apps/resources/student-kustomizations) to track what YAML files it should continuously deploy.  

Notice in your Kustomization file flux is instructed to deploy each YAML file inside your team folder (./apps/eks-sre-course/<your-team-folder>).  


What if there is an error in a YAML file in your team folder? FluxCD will not deploy the changes. How will you know about an error? To find YAML errors you can use kubectl to search the logs of a kustomization.  

```
 kubectl get kustomizations -A | grep <cohort-team-env>
```

However, this requires you to authenticate in the CLI. We can take advantage of Grafana logs using the **Loki** data source and run the query below to access the logs from the command above. Replace cohort and team with your actual cohort and team.  
```
{job="flux-system/kustomize-controller"} |= `cohort` |= `team` |= `error`
```

## Automated Alerts
Both solutions above will show YAML errors, but you will have to check the logs. 
Having an automated alert send a message when there is YAML error will save you time from searching logs.
Follow the steps below to create a Microsoft Team that will receive an alert each time a YAML error is created.

1. Create the Microsoft Team and add your team members to it.
2. Create a webhook and save the URL to the webhook. [Make a Webhook](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet)
3. In Grafana create a new Folder. Use your cohort and team number to name it, such as c500team01. [Make a Folder](https://grafana.computerlab.online/dashboards/folder/new)
4. Then create a dashboard in that folder using the same naming convention, such as c500team01-alerts. Remember to use your actual cohort and team.
5. Create a panel, edit it, select Loki, name it YAML Errors, and use the query below. It is similar to the one above, except it will be a line chart displaying the number of YAML errors per minute.
```
sum(
count_over_time({job="flux-system/kustomize-controller"} |= `cohort` |= `team` |= `error`[1m])
or vector(0)
)
```

6. Save the dashboard. In the YAML Errors panel, click on the alerts tab. Make sure the alert fires when the threshold is above 0. Add a group to the alert, such as your cohort-team-yaml errors. All other settings should remain the same. Save the alert.
7. Navigate to the [contact points page](https://grafana.computerlab.online/alerting/notifications) under alerts in Grafana. Add a new contact point. Use your cohort and team number to name the contact point. Select Microsoft Teams and add your webhook URL. Test and save the contact point.
8. Navigate to [notification policies](https://grafana.computerlab.online/alerting/routes) then click new policy, and click add matcher. The label should be **grafana_folder** and the value is the name of your grafana folder from above. Select your contact point and save the policy.

If you follow those steps correctly, a Microsoft team alert will be sent if there is a YAML error. **Try introducing a YAML error** and adding another panel to your dashboard to see the specific error messages.

You can add a panel with this command to your dashboard to read the logs, just select the logs visualization type and update your cohort and team like before.  

```
{job="flux-system/kustomize-controller"} |= `cohort` |= `team` |= `error`
```

   
