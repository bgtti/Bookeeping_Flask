# Bookeeping_Flask

Bookeeping_BE is the Flask backend of the Expenses React project

creating a virtual environment (windows)
python -m venv env
.\env\Scripts\activate

in .env include:
SECRET_KEY = "..."
JWT_SECRET_KEY = "..."

## Installation

<details>
   <summary>1. Clone this repository</summary>

> \
> More information on how to clone this repository available at https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
> Use the main branch, which is intended for local (production). The code from the deployment branch was changed to suit the deployment environment. More information bellow.
> <br/><br/>

</details>

<details>
   <summary>2. Create a virtual environment</summary>

> \
>
> ```pwsh
> py -m venv env
> ```
>
> Then activate the environment with the following command:
>
> ```pwsh
> .\env\Scripts\activate
> ```

If you are using windows: you may encounter an error that "running scripts is disabled on this system". In this case, you can run the following:

```pwsh
Set-ExecutionPolicy Unrestricted -Scope Process
```

Then try to activate the environment again.

More information on how to set up a virtual envinronment on Windows and MacOS here: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#:~:text=To%20create%20a%20virtual%20environment,virtualenv%20in%20the%20below%20commands.&text=The%20second%20argument%20is%20the,project%20and%20call%20it%20env%20.

> <br/><br/>

</details>

<details>
   <summary>3. Install dependencies</summary>

> \
>
> ```pwsh
> pip install -r requirements.txt
> ```
>
> If you make changes to the project, you can always update the requirements with
>
> ```pwsh
> pip freeze > requirements.txt
> ```
>
> <br/><br/>

</details>

<details>
   <summary>4. Run the app</summary>

> \
>
> ```pwsh
> python manage.py run
> ```
>
> <br/><br/>

</details>
