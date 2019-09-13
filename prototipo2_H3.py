import openstack
from openstack.config import loader
import sys

config = loader.OpenStackConfig()

def _get_resource_value(resource_key, default):
    return config.get_extra_config('example').get(resource_key, default)


SERVER_NAME = 'prototipo2'
IMAGE_NAME = 'bionic'
FLAVOR_NAME = 'm1.small'
NETWORK_NAME = 'internal'
KEYPAIR_NAME = 'mykey'




def create_connection(auth_url, region, project_name, username, password):

    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
        region_name=region,
        app_name='examples',
        app_version='1.0',
    )

def list_flavors(conn):
    print("List Flavors:")

    for flavor in conn.compute.flavors():
        print(flavor)


def create_server(conn):
    print("Create Server:")

    image = conn.compute.find_image(IMAGE_NAME)
    flavor = conn.compute.find_flavor(FLAVOR_NAME)
    network = conn.network.find_network(NETWORK_NAME)
    keypair = conn.compute.find_keypair(KEYPAIR_NAME)

    server = conn.compute.create_server(
        name=SERVER_NAME, image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)

    server = conn.compute.wait_for_server(server)


def delete_server(conn):
    print("Delete Server:")

    server = conn.compute.find_server(SERVER_NAME)

    print(server)

    conn.compute.delete_server(server)


conn = create_connection("http://192.168.0.26:5000/v3", "RegionOne", "admin", "admin", "uSh1eexei2waich7")
print(conn)

list_flavors(conn)
create_server(conn)
delete_server(conn)
