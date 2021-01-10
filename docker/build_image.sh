###
 # @Author: shangyameng
 # @Email: shangyameng@aliyun.com
 # @Date: 2020-05-10 21:24:13
 # @LastEditTime: 2020-05-11 14:03:38
 # @FilePath: /crawler_web/build_image.sh
 ###

time=$(date "+%Y%m%d%H%M%S")
printf "\n================ Start build crawler:release_${time} image ================\n\n"
docker_app="docker_app"
mkdir ./${docker_app}
#cp ./requirements.txt ./${docker_app}/requirements.txt
cp ./default ./${docker_app}/default
cp ./init_database.sh ./${docker_app}/init_databases.sh
cp -R ../crawler/ ./${docker_app}/
cd ./${docker_app} && rm -f ./logs/* && cd ..
docker build -t crawler:"release_${time}" .

rm -rf ./${docker_app}

printf "\n================ crawler:release_${time} image build Successful ================\n\n"
