# Linux Networking and Sys Admin
In this activity, we will be covering some basic commands for performing system administration in Linux.
It is important to be able to identify what processes are using the most resources, what ports they are running on, how much memory your machine has left, network commands, and more. 

## Memory
Not having enough can cause applications to fail or perform poorly. Simply run the command below to see a summary of your machine's memory.
```
cat /proc/meminfo
```

From the output, pay special attention to the values below.  
- **MemTotal** gives you the total RAM installed.  
- **MemFree** shows the currently unused RAM.  
- **MemAvailable** estimates the RAM available for new applications, considering caches and buffers that can be freed.

Alternatively, you can use this command below
```
 free --mega -h # --mega for megabytes, -h for human readable.
 # man free # for options
```

If you want to watch it live, you can use the **watch "free --bytes"** command or simply use **vmstat 1**.
A better approach may be to use **ps** and sort by memory. this was we can see what processes are using the most memory.
```
ps aux --sort -rss # rss is Resident Set Size (memory descending)
ps aux --sort -%mem # % of rss used by the process. The minus sign before %mem indicates descending order, whereas a plus sign would do ascending.
ps -eo user,pid,%mem,stat,cmd --sort=-%mem # only include output (-o) columns that we want (user,pid,%mem,stat,cmd)
ps aux --sort -%cpu # can also sort by cpu
ps aux --forest # useful to see a tree of parent processes
watch 'ps aux --sort -%mem | head' # run the command every 2 seconds
top # use top
```

## Inodes
A Linux filesystem uses blocks to store file data. Each block is a fixed-size unit of storage, commonly 4 KB (4096 bytes).  

An inode is a data structure that stores metadata about a file, such as its size, ownership, permissions, and timestamps, along with pointers to the blocks where the file's actual data is stored. Each file or directory is represented by an inode, which has a unique inode number.

### Example
To illustrate, consider a file that is 8 KB in size. You can use the command below to create one:

```
dd if=/dev/urandom of=8kb_file bs=1K count=8
```

The file would need two 4 KB blocks to store its data.  
The inode for this file would contain metadata about the file and pointers to the two blocks where the data is stored.  
Use the stat command below to examine the file.
```
stat 8kb_file
```

- You may notice it says 16 blocks. This is because the stat command considers each block to be 512 bytes.
 Notice that each 4096 io block contains 8 512-byte blocks, and the file size is 8192 bytes (2 blocks).

**You can also run out of inodes, to check how many you have use this command:**
```
df -i
```

## Network

### Network Diagnostic Tools

#### Ping
The ping command uses the Internet Control Message Protocol (ICMP) to test the connectivity between your machine and another host. It sends ICMP echo requests and waits for replies. This command is especially useful for testing if two machines can communicate with each other.

ping <hostname_or_IP>
For example, to ping Google's DNS server:

```
ping 8.8.8.8
```

This will continue to send packets until you stop it (usually with Ctrl+C). You can specify the number of packets to send using the -c option:

```
ping -c 4 8.8.8.8
```

#### nslookup
The nslookup command is used to query DNS to obtain domain name or IP address mapping.

nslookup <hostname_or_IP>
For example, to find the IP address of example.com:

```
nslookup example.com
```
You can also perform a reverse lookup to find the domain name associated with an IP address:

```
nslookup 8.8.8.8
```

#### traceroute
The traceroute command shows the path that packets take to reach a network host. It can help diagnose routing issues.

traceroute <hostname_or_IP>
For example, to trace the route to example.com:

```
traceroute example.com
```

#### dig
The dig (Domain Information Groper) command is used to query DNS name servers. It provides detailed information about DNS records.  

dig <hostname>
For example, to get DNS information for example.com:

```
dig example.com
# You can also query specific DNS record types, such as A, MX, TXT, etc.:
dig example.com A
dig example.com MX
dig -x 8.8.8.8 # reverse DNS lookup
```

#### curl
The curl command is used to transfer data to or from a server, supporting various protocols like HTTP, HTTPS, FTP, etc. Here are some use cases:
Some of the examples below may not work because we are using an example domain. Nonetheless, run them to see the output.

```
curl https://example.com
```

Save Output to a File:
Save the retrieved web page to a file:

```
curl -o index.html https://example.com
```

Follow Redirects:
Follow HTTP redirects and show the final URL:

```
curl -L -o redirected.html https://example.com
```

Send POST Data:
Send POST data to a server:

```
curl -X POST -d 'username=user&password=pass' https://example.com/login -f # -f is to fail on http error, useful for scripts or pipelines that use exit codes
```

Headers and Cookies:
Include headers or cookies in requests:

```
curl -H "Authorization: Bearer token" https://api.example.com/data
curl -b "cookie1=value1; cookie2=value2" https://example.com
```

### Listening Ports
It is important to know if your machine is listening for incoming connections. Remember, everything in Linux is a file.
Therefore, we can use the list open files (lsof) command to see what ports are open and to what hosts.
```
sudo lsof -i -P # sudo is likely needed
```

You should see ssh open to *:22, indicating that any host connecting on port 22 can connect to your machine. You may also notice the PID attached to this port. You can use that PID in the ps command as **ps -p <pid>** 

### Monitoring network traffic
Run the command below and then try to spam SSH into your machine without the key. If you have a webserver running, spam your webserver while using this command.
You will be able to monitor the network activity connecting to your machine.
```
netstat -c # c is for continuous
ss # this is similar, you can see how many established connections are on your machine and what protocol they are using (eg how many people are logged in via ssh or using your web server)
```

### Private IP and Subnet
A network interface is an active connection to a network where you have been assigned an IP address. You may have more than one network interface; typically, you will have at least one for your private network and one for your localhost network (loopback interface).

To see information on each of your network interfaces, you can run the following command on Unix-like operating systems:
```
ifconfig
```
- **inet**: This is the IP address assigned to the network interface. This can be a private IP address (in the case of IPv4) or a global address (in the case of IPv6).

- **netmask**: This indicates which portion of the IP address represents the network and which part represents the host. It is typically shown in the form of a subnet mask. For example:

1. A netmask of 255.0.0.0 (or /8 in CIDR notation) indicates that the first 8 bits of the IP address are the network part. If an IP address is 172.0.5.1 with a netmask of 255.0.0.0, then all IPs in that network must start with 172.x.x.x.  
2. A netmask of 255.255.255.0 (or /24 in CIDR notation) indicates that the first 24 bits of the IP address are the network part. If an IP address is 172.39.44.1 with a netmask of 255.255.255.0, then all IPs in that network must start with 172.39.44.x.  
3. With a netmask of 255.255.255.0, the network can have 256 addresses, ranging from 172.39.44.0 to 172.39.44.255. The first address (172.39.44.0) is the network address, and the last address (172.39.44.255) is the broadcast address, leaving 254 usable IP addresses for hosts.  

If you need more machines in your network, you can use a larger subnet (a smaller netmask), which allows more IP addresses. This is typically done using CIDR notation.

- **Broadcast**: This is the broadcast address for the network. It is used to send data to all devices on the network. For example, with a network address of 172.39.44.0/24, the broadcast address would be 172.39.44.255
 

# Summary
In this activity, we've explored essential Linux commands and techniques for effective system administration and network diagnostics. Let's recap what we've learned:  

#### Memory Management:
- Monitoring Memory Usage: Commands like cat /proc/meminfo and free --mega -h provide insights into total, free, and available memory.
- Process Management: Using ps to sort processes by memory (%mem) and CPU (%cpu) usage helps identify resource-intensive applications.

#### Inodes:
- Understanding Inodes: Files and directories on Linux are managed through inodes, which store metadata and data block pointers. The stat command reveals inode details.
- Checking Inode Usage: df -i displays inode usage statistics, crucial for managing filesystem limits.

#### Network Diagnostics:
- Ping: Uses ICMP to test network connectivity (ping <hostname_or_IP>).
- nslookup: Queries DNS for IP address mapping (nslookup <hostname_or_IP>).
- traceroute: Traces the path packets take to a destination (traceroute <hostname_or_IP>).
- dig: Provides detailed DNS information (dig <hostname>).
- Curl: HTTP/FTP Data Transfer: curl is versatile for retrieving and sending data over various protocols (curl https://example.com).
- Advanced Usage: Includes saving output to files (curl -o index.html), following redirects (curl -L), and sending POST data (curl -X POST -d 'data').
- Monitoring and Administration:
- Open Ports: lsof -i -P lists open ports and associated processes, crucial for network security.
- Monitoring Network Traffic: Commands like netstat -c and ss provide real-time network connection details.
- Private IP and Subnet: ifconfig displays network interface details including IP addresses, netmasks, and broadcast addresses.


# Excercise
1. Install stress:  
First, search for the stress package using dnf search and then install it.
```
dnf search stress
sudo dnf install stress
```

2. Capture free memory before starting the stress test:  
Use the free command to retrieve the amount of free memory in megabytes and save it to a file named free_mega_before_stress:
```
free --mega # make sure output aligns with awk
free --mega | awk 'NR==2 {print $4}' > free_mega_before_stress
# NR==2 is for row 2 and $4 is col 4
```

3. Perform the stress test:
Execute the stress command to stress the system with virtual memory for 300 seconds:

```
stress --vm 1 --vm-bytes 512M --vm-keep -t 300s &
# press enter
```

4. Capture free memory during the stress test:
While the stress test is running, again use the free command to get the amount of free memory in megabytes and save it to a file named free_mega_during_stress:

```
free --mega
free --mega | awk 'NR==2 {print $4}' > free_mega_during_stress
```

5. Capture the top 5 memory-consuming processes during the stress test:
Use the ps command to retrieve the PID, %mem, %cpu, and CMD of the 5 processes consuming the most memory

```
ps -eo pid,%mem,%cpu,cmd --sort=-%mem | head -n 6 
```

6. Use BC to calculate the difference between how much memory the stress test used.

```
bc <<< "$(cat free_mega_before_stress) - $(cat free_mega_during_stress)"
```




