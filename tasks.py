#!/usr/bin/env python
import os

from invoke import task

__ROOT_DIR__ = os.path.dirname(os.path.abspath(__file__))


@task
def install_dependencies(c):
    """
    install required packages on the host
    """
    c.run('sudo apt-get update')
    c.run('sudo apt-get install openssh-server')
    c.run('sudo apt-get install python3-venv')


@task
def set_config_params(c):
    """
    reads configuration parameters from invoke.yaml
    """
    os.environ['TZ'] = c.config['TZ']
    os.environ['STORAGE_DIR'] = c.config['STORAGE_DIR']
    os.environ['PUID'] = str(c.config['PUID'])
    os.environ['PGID'] = str(c.config['PGID'])
    c.config['COMPOSE_FILE'] = os.path.join(
        c.cwd, 'docker', 'compose-mediamachinery.yml')
    os.environ['COMPOSE_FILE'] = c.config['COMPOSE_FILE']
    os.environ['COMPOSE_PROJECT_NAME'] = "mediamachinery"


@task(set_config_params)
def create_storage_dir(c):
    """
    creating and setting up the storage dir
    """
    c.run('mkdir -p {}'.format(c.config['STORAGE_DIR']))


@task(set_config_params)
def create_media_dirs(c):
    """
    creating the media library dirs
    """
    c.run('mkdir -p {}'.format(os.path.join(c.config['STORAGE_DIR'], 'tv')))
    c.run('mkdir -p {}'.format(os.path.join(c.config['STORAGE_DIR'], 'movies')))


@task
def create_docker_dirs(c):
    """
    creating the docker dirs for all containers
    """
    # portainer
    c.run('mkdir -p {}'.format(os.path.join(
        c.config['STORAGE_DIR'], 'docker', 'portainer', 'data')))

    # jackett
    jackett_dir = os.path.join(c.config['STORAGE_DIR'], 'docker', 'jackett')
    dirs = [os.path.join(jackett_dir, 'config'),
            os.path.join(jackett_dir, 'blackhole')]
    for directory in dirs:
        c.run('mkdir -p {}'.format(directory))

    # radarr
    c.run('mkdir -p {}'.format(os.path.join(
        c.config['STORAGE_DIR'], 'docker', 'radarr', 'config')))

    # sonarr
    c.run('mkdir -p {}'.format(os.path.join(
        c.config['STORAGE_DIR'], 'docker', 'sonarr', 'config')))

    # bazarr
    c.run('mkdir -p {}'.format(os.path.join(
        c.config['STORAGE_DIR'], 'docker', 'bazarr', 'config')))

    # emby
    c.run('mkdir -p {}'.format(os.path.join(
        c.config['STORAGE_DIR'], 'docker', 'emby', 'config')))

    # transmission
    transmission_dir = os.path.join(
        c.config['STORAGE_DIR'], 'docker', 'transmission')
    dirs = [os.path.join(transmission_dir, 'config'),
            os.path.join(transmission_dir, 'scripts'),
            os.path.join(transmission_dir, 'downloads'),
            os.path.join(transmission_dir, 'torrents')]
    for directory in dirs:
        c.run('mkdir -p {}'.format(directory))


@task(create_docker_dirs)
def copy_docker_configs(c):
    """
    copy the configuration files for docker containers
    """
    c.run('cp -r {transmission_stuff} {docker_dir}'.format(
        transmission_stuff=os.path.join(
            __ROOT_DIR__, 'docker', 'transmission', '*'),
        docker_dir=os.path.join(
            c.config['STORAGE_DIR'], 'docker', 'transmission')))

    # TODO: handle backup configurations


@task
def install_media_machinery(c):
    """
    creates all directories needed and copy mandatory docker configuration files
    """
    create_storage_dir(c)
    create_media_dirs(c)
    create_docker_dirs(c)
    copy_docker_configs(c)
    # TODO: Setup Kodi to start automatically on boot


@task
def uninstall_media_machinery(c):
    """
    removes the docker configuration but keeps the media content
    """
    if input("This will remove all content from ({docker})\n"
             "are you sure? (y/n)".format(
            docker=os.path.join(c.config['STORAGE_DIR'], 'docker'))) != "y":
        print('User aborted.')
        exit()
    print('Removing all contents...')

    c.run('sudo rm -r {}'.format(os.path.join(c.config['STORAGE_DIR'], 'docker')))


@task(set_config_params)
def start_media_machinery(c, logs=False):
    """
    starts all the media machinery containers
    """
    c.run('docker-compose up --force-recreate -d --remove-orphans')
    if logs:
        log_media_machinery(c, follow=True)


@task(set_config_params)
def stop_media_machinery(c):
    """
    stop all the Media Machinery containers
    """
    c.run('docker-compose down --remove-orphans')


@task(set_config_params)
def update_media_machinery(c):
    """
    fetches the latest images for all containers
    """
    c.run('docker-compose pull')


@task(set_config_params)
def log_media_machinery(c, follow=False):
    """
    prints the output from the media machinery's containers
    """
    c.run('docker-compose logs {follow}'.format(follow="-f" if follow else ""))


@task
def generate_portainer_password(c, password):
    """
    generate a htpasswd that is used as admin password for portainer
    """
    gen_pwd = str(c.run(
        'docker run --rm httpd:2.4-alpine htpasswd -nbB admin {password} '
        '| cut -d ":" -f 2'.format(
            password=password)).stdout.strip())
    compose_pwd = gen_pwd.replace('$', '$$')
    print("htpasswd:      '{}'".format(gen_pwd))
    print("composepasswd: '{}'".format(compose_pwd))
