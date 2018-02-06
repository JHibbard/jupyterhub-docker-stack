import os
import json

c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = os.environ['JUPYTERHUB_LDAP']
c.Authenticator.admin_users = {os.environ['JUPYTERHUB_ADMIN']}

# Setup Docker Spawner
from dockerspawner import DockerSpawner


docker_images = json.loads(os.environ['JUPYTERHUB_DOCKER_IMAGES'])
docker_images = ['<option value="{image}">{label}</option>'.format(image=image, label=label) for label,image in docker_images.items()]

class DemoFormSpawner(DockerSpawner):
    def _options_form_default(self):
        default_stack = "jupyter/minimal-notebook"
        return (
            '<label for="stack">Select your desired stack</label>' +\
            '<select name="stack" size="1">' +\
            ''.join(docker_images) +\
            '</select>'
        )

    def options_from_form(self, formdata):
        options = {}
        options['stack'] = formdata['stack']
        container_image = ''.join(formdata['stack'])
        print("SPAWN: " + container_image + " IMAGE" )
        self.container_image = container_image
        return options

c.JupyterHub.spawner_class = DemoFormSpawner

# Persistence
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# Add containers to this network
c.DemoFormSpawner.network_name = os.environ['JUPYTERHUB_NETWORK']
c.DemoFormSpawner.remove_containers = True

# ADDED FOR JUPYTER LAB
c.DemoFormSpawner.default_url = '/lab'
c.DemoFormSpawner.cmd = ['jupyter-labhub']

# need to be accessible from proxy + container
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = os.environ['JUPYTERHUB_CONNECT_IP']
c.JupyterHub.hub_port = 8080
