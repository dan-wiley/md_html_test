FROM pandoc/minimal:3.1.1-ubuntu"
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install panflute
RUN pip install beautifulsoup4
RUN ln -s /usr/bin/python3 /usr/bin/python
