# Linkedin people scraper

In this project, we start scraping LinkedIn based on the topic received and save the users who were active in the topic received in our database.

For example, we want to get the number of 100 users from LinkedIn. Users who are active in "**Forex**" topic.

Well, first of all, let's setup the project and run it... 🏁

## Setup project

The **project is Dockerized**, so it is not too difficult to implement.
It only needs a few steps:

- First, Docker must be installed and active on the operating system.
- Second, an **HTTP Proxy to install pip packages** inside the Docker container.
- Third, an **active LinkedIn account** (**optional**)

### Create .env

After cloning or downloading the project from Git, you must create an `.env` file in the main root of the project and put these values in it:

```plaintext
VERSION=0.1.0
PORT=9001

SECRET_KEY = 'cAjAKy_fUY4KVu3KLO3H4-ZXtouFjxXd5iTJfiknEmq3lFUaeEsoYKqlTqPaOntLai2ui1HqSXgW9YaNm1DBRw'

LINKEDIN_BASE_URL=https://www.linkedin.com/
LINKEDIN_USERNAME='xapaj45124@nasmis.com'
LINKEDIN_PASSWORD='vUTT!PE2t5mgKWS'

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=scraper
POSTGRES_USER=amin
POSTGRES_PASSWORD=123456@

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

HTTP_PROXY= # Link of your HTTP Proxy

```

### Build in docker 🛠

Now type the `docker compose build` command into your terminal. 🛠

We wait until the Docker build operation is finished. (**Depending on internet speed, it may take up to 15 minutes**)

### Up containers

After the project is successfully built, enter the `docker compose up -d` command in the terminal.

After the containers are up, the five containers should be run in the following order:

⠿ Container redis
⠿ Container postgres
⠿ Container fastapi
⠿ Container celery_worker
⠿ Container worker_monitor


## Use project

Congratulations, the project has been successfully set up. 🎉

Now let's use it :)
To use project endpoints (APIs), you can refer to project Swagger Doc.

Enter the following address in your browser:

```plaintext
localhost:9001/docs
```

In this address, you can use the APIs of the application.

### Register an account

You must register first. To do this, click on `/sign-up` Endpoint and enter the required information.

Now you can by clicking the Authorize 🔒 button at the top right of the page. Enter your username and password to be able to use other endpoints.

### Scrap a topic ✏️

Now you can click on `/v1/scrapers/linkedin` Endpoint and **enter your topic**.
You can also **specify the maximum number of people** that will be scraped for you. By default, the value is 20. It means that only 20 people will be scraped, but you can scrap up to 999 people from LinkedIn.

After you enter your topic and number of people. **A UUID will be returned to you**. This ID is actually the Task ID that has been activated for you and is scraping people based on the entered subject.

Now you can enter the received ID in `/v1/scrapers/result/{task_id}` Endpoint and find out about the status of your ongoing task.

- If the scrap task is finished, the saved user results will be displayed for you. 🟢
- If the task is still running, it will give you a running message. 🟡
- It will also show you a 404 message if the task failed or did not find any results. 🔴



### Monitor you celery task

In this project, we also have a Celery task monitor, through which you can find out about the status of all the Celery tasks that are running.

```plaintext
localhost:5555/tasks/
```
