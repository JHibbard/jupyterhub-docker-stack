FROM jupyterhub/jupyterhub:0.8.1

RUN pip install jupyter \
                jupyterlab \
                jupyterhub-ldapauthenticator \
                dockerspawner