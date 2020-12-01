build: clean
        cd package_sonos && zip -r9 ../function.zip .
        zip -g function.zip *.py

deploy:
        aws lambda update-function-code --function-name SonosCreateGroup --zip-file fileb://function.zip

install:
        mkdir -p ./package_sonos
        pip3 install --target ./package_sonos --system requests

clean:
        rm -f function.zip
