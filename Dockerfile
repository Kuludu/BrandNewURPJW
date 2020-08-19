FROM	python
MAINTAINER	Kuludu "i@kuludu.net"

RUN	apt-get update \
	&& apt-get install libgl1-mesa-glx -y \
	&& git clone https://github.com/Kuludu/BrandNewURPJW.git \
	&& pip install -r /BrandNewURPJW/requirements.txt -i https://pypi.doubanio.com/simple \
	&& chmod +x /BrandNewURPJW/start.sh

EXPOSE	8000

ENTRYPOINT /BrandNewURPJW/start.sh
