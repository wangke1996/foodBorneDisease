# foodBorneDisease

This is a guide for developers.

## Backend Setup
* Python >=3.6
- Install packages in [requirements.txt](requirements.txt)

- Create Neo4j nodes ( Only the first time )

    change self.g in  backend\lib\QASystemOnMedicalKG\build_buggraph.py ;answer_search.py ;decision_tree.py  to your Neo4j port ,username and password.

    Uncomment these lines in build_buggraph.py

    ```
        # handler.create_graphnodes()
        # handler.create_graphrels()
    ```

    Then, run

    ```
    python build_buggraph.py
    ```

- Download [Pre-trained BERT Model](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip)
- Start the BERT service

    ```
    bert-serving-start -model_dir \chinese_L-12_H-768_A-1
    ```

- Run

        python run.py --port=xxx --debug

    to check if any error occurred. __"xxx"__ is a server port you can use, such as 5000. (__Make sure this port is opened in your firewall rules__)

## Frontend Setup
- Change value of variable ___serverURL___ in [frontend/src/api.js](frontend/src/api.js) to 
  
        http://your.ip.address:xxx
    In which __"xxx"__ is the server port mentioned above.
* You need [nodejs](https://nodejs.org/en/) installed
- cd to the frontend directory, then run:
        
        npm install
* To check if you set the environment properly, try:

        npm start
    If everything goes fine, you should see:
    
        Compiled successfully!
        You can now view frontend in the browser.
            http://localhost:3000/
    Here, localhost means your IP address. For example, if your IP is 101.6.70.15, then open http://101.6.70.15:3000 in browser, you should see the page, that means everything is fine.

