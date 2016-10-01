# A tutorial for using 21 and AWS for deep learning 

See the tutorial at [https://21.co/learn/deep-learning-aws](https://21.co/learn/deep-learning-aws/)

## Quick deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/21dotco/two1-deep-learning/tree/master)

**Important:** You will not be able to quick-deploy without setting up an AWS
account and the needed security profiles, etc. See the tutorial at
[https://21.co/learn/deep-learning-aws](https://21.co/learn/deep-learning-aws/)
for an in-depth description. Here is a short list of the parameters you will
need

 - `AWS_ACCESS_KEY_ID`
 - `AWS_SECRET_ACCESS_KEY`
 - `AWS_DEFAULT_REGION`
 - `EC2_SSH_KEYPAIR_ID`
 - `EC2_IAM_INSTANCE_PROFILE_ARN`
 - `EC2_SECURITY_GROUP_NAME`
 - `S3_BUCKET_NAME`
 - `IMGUR_CLIENT_ID`
 - `IMGUR_CLIENT_SECRET`
 - `TWO1_USERNAME`
 - `TWO1_WALLET_MNEMONIC`

You can get imgur API keys [here](https://api.imgur.com/oauth2/addclient).

Finally, if you are going to use GPU instances, you should request a instance
limit increase from AWS. Currently they only allow for 2 simultaneously running
GPU instances. We have the environment variable `EC2_MAX_NUM_INSTANCES` to
gracefully fail when the limit is reached, and it's set to 1 by default.

If you clone this repository directly (and don't use one of the tagged
releases) note that `ALLOWED_HOSTS` is set to a wildcard to enable the
quick-deploy button above. For security purposes you should change this to your
specific domain, and note that it's only enforced when DEBUG mode is off.
