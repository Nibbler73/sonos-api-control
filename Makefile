build: clean package_sonos
        cd package_sonos && zip -r9 ../function.zip .
        zip -g function.zip *.py

deploy:
        aws lambda update-function-code --function-name SonosCreateGroup --zip-file fileb://function.zip

package_sonos:
        mkdir -p ./package_sonos
        pip3 install --target ./package_sonos --system requests

clean:
        rm -f function.zip
