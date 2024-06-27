# Define variables
FUNCTION_NAME=get-discussions
ZIP_FILE=$(FUNCTION_NAME).zip
PACKAGE_DIR=package
DEPLOYMENT_PACKAGE=build/$(FUNCTION_NAME)-deployment-package.zip
DEV_FUNCTION_NAME=get-discussions-dev

# Define targets
.PHONY: build deploy clean

install: 
 	# Install dependencies to package directory
	pip3 install --upgrade -t $(PACKAGE_DIR) -r requirements.txt

build:
    # Copy function code to package directory
	cp -a src/. $(PACKAGE_DIR)
	rm -r build
	mkdir build
    # Create deployment package and install in build/ directory
	cd $(PACKAGE_DIR) && zip -r ../$(DEPLOYMENT_PACKAGE) .

deploy:
    # Upload deployment package to Lambda
	aws lambda update-function-code --function-name $(FUNCTION_NAME) --zip-file fileb://$(DEPLOYMENT_PACKAGE)

test:
	# Upload deployment package to Lambda dev
	# NOTE: Be sure to comment out or change the s3 writes when running here otherwise they will overwrite prod
	aws lambda update-function-code --function-name $(DEV_FUNCTION_NAME) --zip-file fileb://$(DEPLOYMENT_PACKAGE)

clean:
    # Remove deployment package and package directory
	rm -rf $(DEPLOYMENT_PACKAGE) $(PACKAGE_DIR)
