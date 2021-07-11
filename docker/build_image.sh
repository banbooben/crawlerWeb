###
# @Author: shangyameng
# @Email: shangyameng@aliyun.com
# @Date: 2020-05-10 21:24:13
# @LastEditTime: 2021-04-12 10:33:17
# @FilePath: /flask/docker/build_image.sh
###

time=$(date "+%Y%m%d%H%M%S")
printf "\n================ Start build flaskr:release_${time} image ================\n\n"
docker_app="flaskr"
mkdir ./${docker_app}
cp -R ../app ./${docker_app}
cp -R ../deploy ./${docker_app}
#cp ./requirements.txt ./${docker_app}/requirements.txt
#cp ./default ./${docker_app}/default
#cp ./init_database.sh ./${docker_app}/init_databases.sh
#cp -R ../crawler/ ./${docker_app}/
# cd ./${docker_app}/flaskr && rm -f ./logs/* && cd ..
echo "build"
docker build -f Dockerfile -t flaskr:"release_${time}" .

rm -rf ./${docker_app}

printf "\n================ flaskr:release_${time} image build Successful ================\n\n"
