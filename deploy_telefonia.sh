#!/bin/bash

tar -cvzf telefonia.tar.gz telefonia/static/* telefonia/templates/* telefonia/templatetags/* telefonia/*.py 
sshpass -p 'camara321' scp telefonia.tar.gz suporte@telefonia:/home/suporte