echo Edge Counting Script
for pathname in /home/ubuntu/comp596/edges/*.csv; do
    wc -l $pathname
done