#!/bin/bash
if [ $CONDITION == "CREATE" ]
then
  echo "CONSTRUYENDO PROYECTO"
  ./docker/commands/run_installation_config.sh
else
  echo "INICIANDO PROYECTO"
  ./docker/commands/run_local_container.sh
fi