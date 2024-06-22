To host a Python project using NGINX and run `app.py` on a specific port, you need to follow several steps. Here's a detailed guide:

1. **Setup the Python environment**:
    - Ensure you have Python and the necessary packages installed.
    - Use a virtual environment to manage dependencies.

2. **Create the Python application (`app.py`)**:
    - Ensure your Python application is configured to run on a specific port.

3. **Install and configure NGINX**:
    - Install NGINX on your server.
    - Configure NGINX to proxy requests to your Python application.

### Step 1: Setup the Python environment

First, ensure Python is installed on your server. You can use a virtual environment to manage your dependencies.

```sh
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
```

Create a virtual environment and activate it:

```sh
python3 -m venv myenv
source myenv/bin/activate
```

Install necessary Python packages (e.g., Flask for a simple web application):

```sh
pip install flask
```

### Step 2: Create the Python application (`app.py`)

Create a simple Flask application as an example. Save the following code in `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Specify the port you want the app to run on
```

### Step 3: Install and configure NGINX

Install NGINX:

```sh
sudo apt install nginx -y
```

Configure NGINX to proxy requests to your Python application. Open the NGINX configuration file:

```sh
sudo nano /etc/nginx/sites-available/myapp
```

Add the following configuration to proxy requests to the Flask app running on port 5000:

```nginx
server {
    listen 80;

    server_name your_domain_or_IP;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the configuration by creating a symbolic link to the `sites-enabled` directory:

```sh
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
```

Test the NGINX configuration:

```sh
sudo nginx -t
```

If the test is successful, restart NGINX to apply the changes:

```sh
sudo systemctl restart nginx
```

### Step 4: Run the Python application

Ensure your virtual environment is activated and run the Flask app:

```sh
source myenv/bin/activate
python app.py
```

Now, your Python application should be accessible through NGINX at `http://your_domain_or_IP`.

### Optional: Using a Process Manager

For production environments, it's recommended to use a process manager like `gunicorn` or `supervisor` to manage the application process.

#### Using Gunicorn:

Install Gunicorn:

```sh
pip install gunicorn
```

Run your application with Gunicorn:

```sh
gunicorn --bind 0.0.0.0:5000 app:app
```

You can configure NGINX to proxy to Gunicorn as well. The NGINX configuration remains the same.

#### Using Supervisor:

Install Supervisor:

```sh
sudo apt install supervisor -y
```

Create a Supervisor configuration file for your app:

```sh
sudo nano /etc/supervisor/conf.d/myapp.conf
```

Add the following configuration:

```ini
[program:myapp]
command=/path/to/myenv/bin/gunicorn --bind 127.0.0.1:5000 app:app
directory=/path/to/your/app
user=your_user
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/myapp.log
stderr_logfile=/var/log/supervisor/myapp_error.log
```

Update Supervisor and start the application:

```sh
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start myapp
```

This setup ensures your Python application is running on the specified port and accessible through NGINX.


# IF not using a venv follow below 

Given that you are not using a virtual environment, you can still create a `systemd` service to manage your Flask application with Gunicorn. Here is how you can do it:

1. **Install Gunicorn**:
    ```bash
    pip install gunicorn
    ```

2. **Create a `systemd` Service File**: Create a new service file for your application. This file will instruct `systemd` on how to manage your Flask app.

    Create a new file `/etc/systemd/system/myflaskapp.service` (you'll need root privileges for this):
    ```bash
    sudo nano /etc/systemd/system/myflaskapp.service
    ```

    Add the following content to the file:
    ```ini
    [Unit]
    Description=Gunicorn instance to serve myflaskapp
    After=network.target

    [Service]
    User=youruser
    Group=www-data
    WorkingDirectory=/path/to/your/app
    ExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:6000 app:app

    [Install]
    WantedBy=multi-user.target
    ```

    Replace the placeholders:
    - `youruser` with your username.
    - `/path/to/your/app` with the path to your Flask application's directory.
    - `/usr/local/bin/gunicorn` with the path to your Gunicorn executable. You can find this path using `which gunicorn`.

3. **Reload `systemd` to Apply the New Service**:
    ```bash
    sudo systemctl daemon-reload
    ```

4. **Start the New Service**:
    ```bash
    sudo systemctl start myflaskapp
    ```

5. **Enable the Service to Start on Boot**:
    ```bash
    sudo systemctl enable myflaskapp
    ```

6. **Check the Status of Your Service**:
    ```bash
    sudo systemctl status myflaskapp
    ```

If everything is set up correctly, your Flask application should now be running under `systemd` with Gunicorn. The service will automatically start on boot and can be managed using the `systemctl` command.

**Example Commands for Managing Your Service**:
- **Start the service**:
    ```bash
    sudo systemctl start myflaskapp
    ```
- **Stop the service**:
    ```bash
    sudo systemctl stop myflaskapp
    ```
- **Restart the service**:
    ```bash
    sudo systemctl restart myflaskapp
    ```
- **Check the status of the service**:
    ```bash
    sudo systemctl status myflaskapp
    ```

This setup ensures your Flask app is managed efficiently by `systemd`, making it more robust and easier to manage.
