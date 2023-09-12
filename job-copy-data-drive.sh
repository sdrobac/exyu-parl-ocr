#!/bin/bash
#SBATCH -J drive
#SBATCH -o log-%j
#SBATCH -e log-%j
#SBATCH --account=Project_2002776
#SBATCH --mem=2G
#SBATCH -p small
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH -t 3-00:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=senka.drobac@gmail.com


module load rclone

# for year in 1921 1922 1931 1932
for year in 1933 1934 1935 1936 1937 1938 1939
do
# year=1919 # <- change year
dir=/scratch/project_2004614/senka-slo/data-images/$year
rclone copy gdrive:$year $dir --ignore-existing

done
