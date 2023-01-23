# Changelog

All notable changes to this project will be documented in this file. See
[Conventional Commits](https://conventionalcommits.org) for commit guidelines.

## 1.0.0 (2023-01-23)


### Features

* add arena wrapper from ml toolbox ([9837f96](https://github.com/emma-simbot/simbot-offline-inference/commit/9837f9688371930388b6465ec2a86ff20cfe6691))
* add code to orchestrate the test ([bc17922](https://github.com/emma-simbot/simbot-offline-inference/commit/bc17922989175672545b212c18a235fa6a7f90a8))
* add experience hub dir to settings ([d292d1b](https://github.com/emma-simbot/simbot-offline-inference/commit/d292d1bea89ccf56e71363a18f8af33ca262979d))
* add log points ([bac27af](https://github.com/emma-simbot/simbot-offline-inference/commit/bac27af447e875ba12a9bafd80229ab52b232019))
* add metric logging for the evaluation ([c0f8ee7](https://github.com/emma-simbot/simbot-offline-inference/commit/c0f8ee7da7a06609d953702502a034d7c698a02c))
* add run command ([0830cc5](https://github.com/emma-simbot/simbot-offline-inference/commit/0830cc5ea6f113b26dbb04137379023444165cf1))
* add script to launch xserver ([21389ce](https://github.com/emma-simbot/simbot-offline-inference/commit/21389ce89931a7b8576508dd06b7dfc67baa2f64))
* add scripts to download the mission data ([ef568c6](https://github.com/emma-simbot/simbot-offline-inference/commit/ef568c667236bb7064a3b1e76a88ec87609ee6ab))
* add terraform config for creating the instance ([4ab0e6c](https://github.com/emma-simbot/simbot-offline-inference/commit/4ab0e6c0fdf553e61c873d127c0b7a50125d9422))
* automatically prepare the file system for the evaluation ([397018b](https://github.com/emma-simbot/simbot-offline-inference/commit/397018b5d1eaaa3dc03ae0bca2920e747b63f2d5))
* automatically update permissions and start xserver ([37a39fe](https://github.com/emma-simbot/simbot-offline-inference/commit/37a39fe302167f2b459311f1b3b0791b8aed2b27))
* create the settings file ([1b45fcd](https://github.com/emma-simbot/simbot-offline-inference/commit/1b45fcdaed97654bb85f3df53412970139eb5802))
* disable client timeouts on experience hub ([ed5551d](https://github.com/emma-simbot/simbot-offline-inference/commit/ed5551d37527d5595ae26e9f127270b83fe6b367))
* install multiprocessing logging ([b767f43](https://github.com/emma-simbot/simbot-offline-inference/commit/b767f436115ac90522ee746cd55fe1983029085c))
* set ssh key to the ec2 key ([e4a98bd](https://github.com/emma-simbot/simbot-offline-inference/commit/e4a98bd352cd43ad62d1a48acc86b126f5c4cec8))
* setup repo ([39949b5](https://github.com/emma-simbot/simbot-offline-inference/commit/39949b597f71f64715b9aa3cf9cd5b54d10476e0))
* setup venv and prepare trajectory data in user-data script ([4ccf28d](https://github.com/emma-simbot/simbot-offline-inference/commit/4ccf28dd82bbe18a685f805285659a8cf7b25949))
* stop docker containers on exit too ([a369b42](https://github.com/emma-simbot/simbot-offline-inference/commit/a369b428f0213a5f3634a166f615d3c7e710d1e7))
* use experience hub for access to the storage/docker configs ([9249bbe](https://github.com/emma-simbot/simbot-offline-inference/commit/9249bbef93291aeeaad8b896a0d3338807575192))
* use loguru for logging in arena_orchestrator ([c9fc3ba](https://github.com/emma-simbot/simbot-offline-inference/commit/c9fc3ba6e2cfaeda4028b4ddf8617b7e78a2f9c9))
* use rich logging ([557b006](https://github.com/emma-simbot/simbot-offline-inference/commit/557b006fb8ac523124f1fbcfa546d56c141b77ba))


### Bug Fixes

* add catch for timeout on healthcheck ([0bbab99](https://github.com/emma-simbot/simbot-offline-inference/commit/0bbab99e3bb6604535fb96453a120436b805bb29))
* allow pickle when loading data ([7ac9ec0](https://github.com/emma-simbot/simbot-offline-inference/commit/7ac9ec0383df033c749dea215c8be72ca2f89ecf))
* change port for the experience hub to run on ([f211885](https://github.com/emma-simbot/simbot-offline-inference/commit/f211885e8a1c5cbc3c3196ea0e69a40e5d9b681a))
* copy the arena deps as ubuntu ([91f8c90](https://github.com/emma-simbot/simbot-offline-inference/commit/91f8c9083adb5c4970b2f224b260f7517a86a118))
* create session id directory for auxiliary metadata ([214ccb6](https://github.com/emma-simbot/simbot-offline-inference/commit/214ccb6204bd285de6715b6fd685e139c70ca7e9))
* creating the storage dir for cloning the experience hub ([8cc6dbf](https://github.com/emma-simbot/simbot-offline-inference/commit/8cc6dbf0637ab98ed9dcb187c88d0d203b1fa8e0))
* disable multiprocess logging ([f8cdc4a](https://github.com/emma-simbot/simbot-offline-inference/commit/f8cdc4a6fec3135c0462e1c39bafb699db96b154))
* do not create a symlink ([70cb36f](https://github.com/emma-simbot/simbot-offline-inference/commit/70cb36f7fa5aef5776cc98c85951352c6da8d44f))
* do not force download the models if they exist ([5b8949e](https://github.com/emma-simbot/simbot-offline-inference/commit/5b8949ecd4ba39906ab8d45a5a8af903b0105dce))
* do not run process as a daemon ([7ec2f2c](https://github.com/emma-simbot/simbot-offline-inference/commit/7ec2f2cad2172024f9abd99aff7f8a2f245ea59e))
* do not start xserver within the user-data ([700f440](https://github.com/emma-simbot/simbot-offline-inference/commit/700f4406783d2d6cc543477090ce75c518f68680))
* do not try to setup the python env on launch - it wont play nice ([9380128](https://github.com/emma-simbot/simbot-offline-inference/commit/9380128950cf6db6c706e0d97aa164769043a283))
* explicitly define the args to run the controller api ([a97ddb4](https://github.com/emma-simbot/simbot-offline-inference/commit/a97ddb493041cb0905357358ade7d4bdcc75a6de))
* explicitly disable observability and production ([79b43cd](https://github.com/emma-simbot/simbot-offline-inference/commit/79b43cdb55bf5b7c49141e0c58d856706cf5a910))
* formatting ([b21c550](https://github.com/emma-simbot/simbot-offline-inference/commit/b21c5500a69eecb92660f67cca63ca8c3ff4e705))
* improve orchestrators start order ([defb686](https://github.com/emma-simbot/simbot-offline-inference/commit/defb6864d22ade3f77be28ebb39cbf8646333330))
* lint errors ([ada1332](https://github.com/emma-simbot/simbot-offline-inference/commit/ada13320224a04ef302046baa08cb4ca5261adae))
* method order in class ([4a49a24](https://github.com/emma-simbot/simbot-offline-inference/commit/4a49a24c15c1908590963f26504a2b361ef962e7))
* model storage dir ([ced8940](https://github.com/emma-simbot/simbot-offline-inference/commit/ced89404a770e9646736e2219655d34e6d1de456))
* only need about 10 retries before it should be running ([61f6e20](https://github.com/emma-simbot/simbot-offline-inference/commit/61f6e2066d1468bb56e255704b98215a98f5f8ed))
* order of setting orchestrators up ([f4949ef](https://github.com/emma-simbot/simbot-offline-inference/commit/f4949ef170528e3ad80475a48fe29f5cbf692dec))
* re-able running as a daemon ([eceb2f4](https://github.com/emma-simbot/simbot-offline-inference/commit/eceb2f4a962748eed3804d8ec3899b86f0e2da70))
* remove dialog actions from the experience hub response actions ([e7f1d50](https://github.com/emma-simbot/simbot-offline-inference/commit/e7f1d50870ae729c346186e784d00270482ebd13))
* remove the xserver module - its not needed ([f1836b4](https://github.com/emma-simbot/simbot-offline-inference/commit/f1836b42d8d0e01f74ea9f20133fa28dc3ecffe8))
* send dummy actions when loading the game ([c152998](https://github.com/emma-simbot/simbot-offline-inference/commit/c152998e7fdbbf5bf87f36d1fd8292a02dded327))
* set arena env vars within the run ([5edb809](https://github.com/emma-simbot/simbot-offline-inference/commit/5edb809c6a4ea408ab0de988e5fb0e588ef33b73))
* set the appconfig to a dataclass so that it hopefully loads the env vars ([31624c9](https://github.com/emma-simbot/simbot-offline-inference/commit/31624c99feed5706d06f1dcbe10eae7faf50e152))
* set the envvars outside the function ([4192e36](https://github.com/emma-simbot/simbot-offline-inference/commit/4192e3683b468b54b5446bbab194ae9e5172e713))
* type error because im pickling so we dont care ([5f0c3a3](https://github.com/emma-simbot/simbot-offline-inference/commit/5f0c3a3d03d6e3f494ebe6904d52a99d6af997e8))
* types for paths in case they dont exist already because we create them ([05d565d](https://github.com/emma-simbot/simbot-offline-inference/commit/05d565de891567d953f261f9e6313b9a1f31ea7e))
* unzip path for cdf data ([a035e7c](https://github.com/emma-simbot/simbot-offline-inference/commit/a035e7c50a15faa8df136bd16d51524c911c61e6))
* use the httpx client when making the request ([5897d15](https://github.com/emma-simbot/simbot-offline-inference/commit/5897d15e5048576f37beebdbf5de67a9777aa000))
* use the settings to hopefully run the thing ([db07a39](https://github.com/emma-simbot/simbot-offline-inference/commit/db07a39d4dd9be16a0670bff44a4a539a6b2a6f5))
