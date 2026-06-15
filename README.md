# Devbox for ready to use AiiDA

The idea is to have a ready to use environment, with initial hooks and cmdline tools to automatically setup AiiDA stuff, like computer and codes, profiles, connect to the right postgres, rabbitmq. In this way, the user just needs to provide information (minimal) about the computer and codes, via yaml files.
The only additional thing to understand is if we can use jupyter notebook kernels of the devbox environment. If so, I think everything is in place.

## AiiDA quick installation

Just run:

```shell
devbox run install-requirements
```

## Quickly setting up and AiiDA profile with full functionalities

You can create a profile with all functionalities (postgres, rabbitmq), by running:

```shell
devbox services up -b # to start postgres, rabbitmq
verdi presto --use-postgres 
```

or, alternatively:

```shell
devbox run create-aiida-profile # script to run both the above commands.
```

It is important that the services stay up when you use AiiDA (the can be turned off by running devbox services down). So, when you use AiiDA, be sure to manually run `devbox services up -b` (or without the `-b` if you want to check them).