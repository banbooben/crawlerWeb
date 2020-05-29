###
 # @Author: shangyameng
 # @Email: shangyameng@aliyun.com
 # @Date: 2020-05-10 21:24:13
 # @LastEditTime: 2020-05-11 14:03:38
 # @FilePath: /crawler_web/build_image.sh
 ###

printf "\n================ Start build crawler-web:latest image ================\n\n"
docker_app="docker_app"
mkdir ./${docker_app}
cp ./requirements.txt ./${docker_app}/requirements.txt
cp ./default ./${docker_app}/default
#cp ./uwsgi.ini ./${docker_app}/uwsgi.ini
cp -R ./crawler_web/ ./${docker_app}/
cd ./${docker_app} && rm -f ./logs/* && cd ..
docker build -t crawler-web:latest .

rm -rf ./${docker_app}

printf "\n================ crawler-web:latest image build Successful ================\n\n"