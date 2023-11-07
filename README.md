# p-recs

A course search/recommendation system for the Claremont Colleges. Created by [ASPC Software Development Group](https://pomonastudents.org/sdg) and [p-ai](https://www.p-ai.org/).

Live site: [p-recs.com](https://p-recs.com)


### Getting Up and Running
_Note: keys required for contribution_

1. Clone this repo
```sh
git clone https://github.com/aspc/p-recs
```
2. Install required dependencies
```sh
conda create --name p-recs --file requirements.txt
```
3. Activate the environment
```sh
conda activate p-recs
```
4. Run `FLASK_APP=app.py flask run` from inside the cloned directory
5. Navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000)

