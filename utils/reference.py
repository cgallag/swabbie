class Reference(object):

    class Shell:
        RUN_IMAGE = 'docker run -it {} /bin/bash'
        RUN_CONTAINER = 'docker exec -it {} bash'