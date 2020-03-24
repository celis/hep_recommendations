# HEP recommender

This project contains the code for the [hep-recommender](https://www.hep-recommender.com) web application.
See [here](https://celis.github.io/personal/recommender/gensim/python/aws/flask/2020/02/20/hep-recommender.html) for more details about the project.

The embeddings used are downloaded from AWS S3, the training of
such embeddings is done with [this](https://github.com/celis/hep-recommender) repository.

# Usage

The project is currently deployed in Heroku and the necessary Procfile is provided.    
Configuration values for local testing can be set on the config files, and for deployment must be set in Heroku.