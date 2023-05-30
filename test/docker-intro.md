# Intro to Docker 
In this activity, you will create two docker images and deploy two containers, one from each image. One image will be a dev environment and the other testing. Both containers will be a web server serving different content on the same host operating system. 

This activity demonstrates the power of containerization and the ability to run multiple services on a single host operating system.   

Containerization allows us to run images on the host operating system. A major benefit of containerization is that containers use the same hardware (kernel) as the host operating system. Containers. 

Images allow bundling up packages or installation instructions into a file, eliminating the need to perform installation steps on the host OS or create dependency conflicts. It is important to note that images and containerization do not necessarily rely on Docker. Docker is just a suite of tools for creating and deploying images into containers. Kubernetes, for example, can use the same images but uses a different runtime for running the containers.

## Learning Objectives
You will be able to create a dockerfile, build images, deploy multiple containers on the same host OS and understand different keywords in dockerfiles. Completing the bonus portion will teach you about volumes between containers and the host OS.

## Setup
- Make sure that you have ports 80 and 8080 open on your host OS firewall before starting this activity. If on AWS navigate to your instance, then Security, and click on your Security Group. Edit inbound rules, then verify or add a rule for ports 8080 and 80. For the source select "Anywhere IPv4". Save your settings.

1. Install docker on your amazonlinux2 host OS, then start the docker daemon.
    - `sudo yum -y update`
    - `sudo yum -y install docker`
    - `sudo service docker start`

    > If you want to run docker without sudo (recommended) add your user to the docker group by running `sudo usermod -aG docker $USER`. You will then need to log out and log back in. 


2. You will create two docker images and containers from the same underlying image. The image is httpd, a well know web server. Visit this web page and review the documentation for the image https://hub.docker.com/_/httpd/ 

3. Create two directories for each dockerfile.
    - `mkdir dev-site test-site`


# Test Site
Start with the test website.

1. CD into test-site
    - `cd test-site`
2. Create a file named `dockerfile` with this content 
    ```dockerfile
    FROM httpd:2.4
    ```
    > The **FROM** keyword allows us to specify a base image for our docker image to be built from.. 

3. Build your dockerfile into an image
    - `sudo docker build -t test-httpd .`
    > This command searches for a file named dockerfile in the current directory, builds it and tags (-t) the image as *test-httpd*

4. List your images to verify your image was created.
    - `sudo docker images`

5. Deploy your image to a container. Use --name to name the container and the image name at the end of the command.
    - `sudo docker run -dit --name test-httpd-container -p 80:80 test-httpd`
    > The -d tells it to run in background, -it allows the continer to connect to your terminal session.
    > -p is the bort binding, above we are binding port 80 of the host OS to port 80 on the container.

6. List your running docker images
    - `sudo docker ps -a`
        - Notice that port 80 of the host is routed to port 80 of the container. The -a is to display all details.
7. Visit the website in the browser to make sure it works. You should see the default web page! 
    - `http://<YOUR_PUBLIC_IP>`


# Dev Site

This website will serve our own HTML files.

## Instructions

1. CD into the dev site folder
    - `cd ~/dev-site`
2. Make a folder for html files named `public-html` and cd into it.
    - `mkdir public-html`
    - `cd public-html`
3. Paste the content below into `index.html`
    ```html
    <html>  
    <body>  
        <h1>  
        This is the Dev Site  
        </h1>  
        <h2>Cohort number <COHORT> </h2>  
    </body>  
    </html>  
    ```
    > We will use `sed` to replace the `<COHORT>` with your actual cohort number
4. Go back to the root of the dev-site
    - `cd ~/dev-site`
5. Create a file named `dockerfile` and paste this content. Replace 500 with your cohort number.
    ```DOCKERFILE
    FROM httpd:2.4
    COPY ./public-html/ /usr/local/apache2/htdocs/
    ENV cohort=500
    RUN sed -i "s/<COHORT>/$cohort/g" /usr/local/apache2/htdocs/*
    EXPOSE 80
    CMD ["httpd-foreground"]
    ```
    > The **COPY** keyword will copy the files from the host machine in public-html to the container htdocs folder at image build time. Httpd will automatically serve files in htdocs folder when it is started. 

    > The **ENV** keyword sets an enviornment variable that we can access later with $cohort. The **RUN** keyword executes a command when building the image, such as sed. Here we are replacing `<COHORT>` with the value of $cohort for each file in htdocs. **EXPOSE** opens the port 80 of the container, it is not needed here because the base image already exposes that port.

    > The **CMD** keyword should only be used once, it is different from RUN because it is not executed while the image is being build. Instead, CMD is the command to run when the image is executed as a container. This is known as the main process, and when this process is done executing the container will stop. To keep your container alive, this command should not exit. In this case `httpd-foreground` is the same command the base image executes. Therefore, the entire line can be removed since the base image already executes the `httpd-foreground` command.
    
    > 

6. Build your dockerfile into an image
    - `sudo docker build -t dev-httpd .`

7. List your images to verify your image was created.
    - `sudo docker images`

8. Deploy your image to a container.
    - `sudo docker run -dit --name dev-httpd-container -p 8080:80 dev-httpd`

6. List your running docker images
    - `sudo docker ps -a`
        - Notice that port 8080 of the host OS is being routed to port 80 of the dev-httpd container. The httpd service is already configured to listen on port 80. Now all requests to port 8080 are forwarded to port 80 of the container.
7. Visit the website in the browser, this time change the port to 8080 and you should see your dev site. You can go back and forth between sites simply by adjusting the ports in the browser.
    - `http://<YOUR_PUBLIC_IP>:8080`

# Volumes (Bonus)
A volume is a shared folder between the host OS or other containers. We can create a volume from public-html on the host OS to htdocs on the container. A volume could enable editing the files in the public-html folder and reflecting the changes in the htdocs folder of the container.

Without using volumes you would have to rebuild the image and container each time you changed the file because the dockerfile (and `COPY` command) is only executed at image creation (`docker build`). You could edit the files in the container, but that requires `docker exec` and volumes are still more convenient.

## Instructions
The activity walks you through editing the web page on the host before adding a volume. Then you will edit the file after adding a volume and compare the difference. This activity uses the dev environment only.

1. Edit the host HTML file. You can add any changes you like, as long as they will be noticeable in the web browser.
    - `vim ~/dev-site/public-html/index.html`

2. Visit `http://<YOUR_PUBLIC_IP>:8080` and take note if the changes made in step 1 are visible.

3. Delete the container and re-create it with a volume mount using the `docker run` command and adding `-v /full/path/on/host:/path/on/container`. The docker run command will fail if the container name is already taken.

```bash
sudo docker rm -f dev-httpd-container
sudo docker run -dit -v /home/ec2-user/dev-site/public-html:/usr/local/apache2/htdocs \
--name dev-httpd-container -p 8080:80 dev-httpd
```

4. Edit the host HTML file again with a noticeable change.
    - `vim ~/dev-site/public-html/index.html`

5. Visit `http://<YOUR_PUBLIC_IP>:8080` and take note if the changes made in step 1 and step 4 are visible.


# Cleanup

1. Stop the docker containers.
    - `sudo docker stop dev-httpd-container test-httpd-container`
    > To start a stopped container use `sudo docker start <CONTAINER_NAME>`
2. Delete the containers.
    - `sudo docker rm dev-httpd-container test-httpd-container`
    > You could have stopped and deleted in one step with -f
3. Delete the images.
    - `sudo docker rmi dev-httpd test-httpd httpd:2.4`
4. Now run these commands to verify you have deleted the images and the containers.
    - `sudo docker ps -a`
    - `sudo docker images`



# Conclusion
In this activity you created a basic test docker container and verified it was accessible over the internet. You then created another container from a more sophisticated dockerfile on the same host OS. If you completed the bonus you added a volume linking a host directory to a container and updated the website via the host OS. Finally, you performed the operations needed to remove the containers and images. These skills are essential for navigating modern microservice stacks.
