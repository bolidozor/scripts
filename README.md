# scripts
 Scripts useful to station administration


## bzremote
The ./bzremote sshpass -p odroid ssh % df -h should not be used anymore. The stations should be accessed using a private key (shared for selected users at space.astro.cz). Then the bzremote script can be run without sshpass, e.g. ./bzremote ssh % df -h