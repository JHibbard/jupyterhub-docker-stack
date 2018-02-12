# jupyterhub-docker-stack: An Example JupyterHub deployment using Docker stacks.

## LDAP Setup

To deploy your JupyterHub environment, you will have to provide the address of your LDAP server in the 
docker-compose.yml file provided.  Under the "hub" service, there is an environment variable "JUPYTERHUB_LDAP",
change the value mapping to a reachable LDAP server's address.  If no LDAP server is available, you can 
instead use an alternative [JupyterHub auth plugin](https://github.com/jupyterhub/jupyterhub/wiki/Authenticators).

Once your LDAP authenticator is configured, anyone with a valid LDAP account can access your JupyterHub (and Hail!).

## Config Creation

Under the configuration directory, there is a config file that Jupyter uses to set common values.  To make this 
available within your containerized deployment, you will need to make a "docker config".  You can accomplish this
with the following command:

    docker config create jupyterhub-config jupyterhub-config ./configurations/jupyterhub_config.py

Your config file will now be "attachable" to any docker services you plan on running.

## Running the Stack

Running the hub stack is simple.  On a linux machine with Docker (version 17.12.0 or later) installed, execute the
following command in the save directory as teh docker-compose.yml:

    docker-machine init
    docker stack deploy -c docker-compose.yml hub

You should now have a running JupyterHub serving a Spark/Hail environment.
