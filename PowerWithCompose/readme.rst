Docker Compose
===============

Powerful, lightweight, server-side, container management tool. Create, start, stop, restart, kill, rm, ps, pull, build, push, save, and load containers

Features
--------
Features of docker-compose are:
    

1. Start your docker-compose file

.. code-block:: bash

    docker-compose up -d

2. View your dokcer containers

.. code-block:: bash

    docker-compose ps

3. Stop your docker-compose file

.. code-block:: bash

    docker-compose stop

4. Restart your docker-compose file

.. code-block:: bash

    docker-compose restart

5. Remove your docker-compose file

.. code-block:: bash
    
    docker-compose rm

    Example:
    --------
    docker-compose rm -f

6. Build your docker-compose file

.. code-block:: bash

    docker-compose build

    Example:
    --------
    docker-compose build --no-cache

7. Push your docker-compose file

.. code-block:: bash

    docker-compose push


8. Pull your docker-compose file

.. code-block:: bash
    
    docker-compose pull


9. Save your docker-compose file

.. code-block:: bash
    
    docker-compose save

    Example:
    --------
    docker-compose save > docker-compose.yml

10. Load your docker-compose file

.. code-block:: bash
        
    docker-compose load

    Example:
    --------

        docker-compose -f docker-compose.yml up -d

11. Create your docker-compose file

.. code-block:: bash
        
    docker-compose create

    Example:
    --------

        docker-compose create --file docker-compose.yml