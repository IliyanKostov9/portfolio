.PHONY: sandbox-create
sandbox-create:
	npx ampx sandbox  --profile amplify-alien --identifier feature1sandbox

.PHONY: sandbox-delete
sandbox-delete:
	npx ampx sandbox delete --name feature1sandbox

.PHONY: add-cognito
add-cognito:
	export EMAIL="john.doe@mail"
	export USER_POOL_ID="blablabla"
	aws cognito-idp admin-create-user --user-pool-id $USER_POOL_ID --username $EMAIL
	aws cognito-idp admin-add-user-to-group --user-pool-id $USER_POOL_ID --username $EMAIL --group-name Admin

.PHONY: setup-form
add-cognito:
	export STACK_NAME="amplify-retailstore-feature1sandbox-sandbox-ba7774de28"
	cd src
	npx ampx generate forms --stack $STACK_NAME --models Category
	npx ampx generate forms --stack $STACK_NAME --models Product
	npx ampx generate graphql-client-code --stack $STACK_NAME --out graphql

.PHONY: local-run
local-run:
	npm run dev
