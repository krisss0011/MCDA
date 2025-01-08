# MCDA CALCULATOR

## Introduction
Multiple-criteria decision analysis calculator.

## Used methods
`https://github.com/Valdecy/pyDecision`

### Commands For Windows
1. **Create and Activate Virtual Environment:** 
```diff
- RUN POWERSHELL AS ADMINISTRATOR
```
```bash
cd mcda-calculator
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
.\venv\Scripts\activate
```
2. **Install Python Dependencies:**
```bash
cd mcda-calculator
pip install -r requirements.txt
python manage.py migrate
```
3. **Start app:** 
```bash
python manage.py runserver
```

## AutoStart the app:
first add permission to the script
```bash
chmod +x app_start.sh
```

```bash
./app_start.sh
```

### Urls
#### Web
`http://localhost:8000/`

#### Api
`http://localhost:8000/api/`

#### Default Calculation all methods
`http://localhost:8000/api/calculation/`

#### Custom Calculation ahp method
`http://127.0.0.1:8000/api/calculation/?method=ahp&weights=0.4,0.2,0.2,0.1,0.05,0.05`

#### Custom Calculation topsis method
`http://127.0.0.1:8000/api/calculation/?method=topsis&weights=0.4,0.2,0.2,0.1,0.05,0.05`

#### Custom Calculation fuzzy-topsis method - not completed
`http://127.0.0.1:8000/api/calculation/?method=fuzzy_topsis&weights=0.4,0.2,0.2,0.1,0.05,0.05`

#### Custom Calculation Waspas method
`http://127.0.0.1:8000/api/calculation/?method=waspas&weights=0.4,0.2,0.2,0.1,0.05,0.05`

### Used methods
#### AHP
`https://colab.research.google.com/drive/1qwFQs5xkTZ8K-Ul_wWcCtPjLH0QooU9g?usp=sharing`

#### TOPSIS
`https://colab.research.google.com/drive/1s87DC5_oa9GvgVe98oAP1UIhduac09CB?usp=sharing#scrollTo=cyCyvCXTDt9Z`

#### FUZZY TOPSIS - not completed
`https://colab.research.google.com/drive/1eKx7AOYrnG-kZcsBt28rMEtCrUO-j3J-?usp=sharing#scrollTo=FOS3wfnR47_x`

#### WASPAS
`https://colab.research.google.com/drive/1HbLwXI4HkrmI-lsNzDtBOlCiwxfJltHi?usp=sharing#scrollTo=RQkYBJM4nrGB`