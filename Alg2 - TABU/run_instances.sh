# for i in r102 rc107 c204 r107 r206 r210 c207 c106 rc105 c109 r106 rc108 rc204 r101 c107 rc207 r207 rc102 r203 pr10 c102 c201 pr01 rc208 r201 r109 r103 pr07 pr04 c103 r110 c205 rc201 rc103
#
# do
#     python grasp.py <../Instances/$i.txt > ./Instances/$i_output.txt
# done
for i in r102.txt rc107.txt c204.txt r107.txt r206.txt r210.txt c207.txt c106.txt rc105.txt c109.txt r106.txt rc108.txt rc204.txt r101.txt c107.txt rc207.txt r207.txt rc102.txt r203.txt pr10.txt c102.txt c201.txt pr01.txt rc208.txt r201.txt r109.txt r103.txt pr07.txt pr04.txt c103.txt r110.txt c205.txt rc201.txt rc103.txt
do
     python tabu.py < ../Instances/$i > ./Instances/$i
done
