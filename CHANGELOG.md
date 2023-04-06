# Changelog

All notable changes to this project will be documented in this file. See
[Conventional Commits](https://conventionalcommits.org) for commit guidelines.

## [1.5.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v1.4.0...v1.5.0) (2023-04-06)


### Features

* add command to validate cdfs within a dir ([8b65c55](https://github.com/emma-simbot/simbot-offline-inference/commit/8b65c55fbcd4330b33e2ce2d95d9c306815cd5fe))
* add flag to enable offline evaluation mode in experience hub ([4514467](https://github.com/emma-simbot/simbot-offline-inference/commit/4514467b75407d0fe5f999f99143b42f1338190d))
* add missions for picking up from freezer ([8108cf1](https://github.com/emma-simbot/simbot-offline-inference/commit/8108cf1ed1b93b9077be3bbe160b4dc0f454a527))
* clone the experience hub into the storage dir ([22b91a7](https://github.com/emma-simbot/simbot-offline-inference/commit/22b91a71272f8cd22a127bf21b3042fae31af31d))
* create new structures for the challenges and trajectories ([1e12c0b](https://github.com/emma-simbot/simbot-offline-inference/commit/1e12c0b445107020f3c0c4f869498af2650616c2))
* improve how generating trajectories are to be run ([d3b8979](https://github.com/emma-simbot/simbot-offline-inference/commit/d3b897970a148e5b7b43abff40bc5351d3cfd777))


### Bug Fixes

* improve the first attempt to make the CDFs ([c19be24](https://github.com/emma-simbot/simbot-offline-inference/commit/c19be24925f8da21c3116bda2ccfdcf0ed739ed9))
* just use a single high level key for each mission ([788ea34](https://github.com/emma-simbot/simbot-offline-inference/commit/788ea3411c0737d2ae0d0b2314b3bcb0d16437ed))
* kill command for the arena ([605863b](https://github.com/emma-simbot/simbot-offline-inference/commit/605863bcc7922daca752c1b4f9f661761a40e780))
* missions for pickup from fridge ([b74601c](https://github.com/emma-simbot/simbot-offline-inference/commit/b74601c7fb30e451bfee24c2ef0ce4ccc378ffdc))
* settings need to exist before being able to run things ([951aa38](https://github.com/emma-simbot/simbot-offline-inference/commit/951aa382e2673a7cbf0c6214f352374cfe41813e))
* the service registry path ([eb8c5c5](https://github.com/emma-simbot/simbot-offline-inference/commit/eb8c5c59ccc14fb383b5034cdbbb1f1012302bcd))

## [1.4.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v1.3.1...v1.4.0) (2023-04-05)


### Features

* be able to validate cdfs ([faa6722](https://github.com/emma-simbot/simbot-offline-inference/commit/faa6722aa5a73671e6a1dcedc6c0234ccf0767f9))


### Bug Fixes

* if the arena/experience hub are running, do not try and start it again ([cde1077](https://github.com/emma-simbot/simbot-offline-inference/commit/cde1077b0b030c7fa3c706c72e89e0b854fc47ae))
* make sure the experience hub dies ([5094187](https://github.com/emma-simbot/simbot-offline-inference/commit/50941874941b76df641ae79220d4b56788c5e941))
* run command with the new experience hub version ([6ad167b](https://github.com/emma-simbot/simbot-offline-inference/commit/6ad167bbf94c643210fd23ccad50d710affc6340))

## [1.3.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v1.3.0...v1.3.1) (2023-04-04)


### Bug Fixes

* context managers for the controllers/orchestrators ([fc27d12](https://github.com/emma-simbot/simbot-offline-inference/commit/fc27d126948705ce3683f7aabbd8253ca8c52f55))

## [1.3.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v1.2.0...v1.3.0) (2023-04-02)


### Features

* simplify run commands and add in the backend for the web tool ([4b4ee95](https://github.com/emma-simbot/simbot-offline-inference/commit/4b4ee95a2825058ba35c879b1b2b59af50873eec))

## [1.2.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v1.1.0...v1.2.0) (2023-04-01)


### Features

* add options to run for subset ([2391594](https://github.com/emma-simbot/simbot-offline-inference/commit/23915945e1f80cb5157554fbd37232cfc7e8c8b9))
* create separate module/script to run the background services ([ec19cd8](https://github.com/emma-simbot/simbot-offline-inference/commit/ec19cd8efc04afd6869b4f6ac50d94e0a27aa83e))
* dump all metrics so they can be stitched together again ([d8366ce](https://github.com/emma-simbot/simbot-offline-inference/commit/d8366ce36649a79e05fa1c48a357c97b64598b6d))
* improve metrics calculating ([1bfa793](https://github.com/emma-simbot/simbot-offline-inference/commit/1bfa79315252a66724fc7ce81f9ebe67a41d0b90))
* include CDFs ([d22fe14](https://github.com/emma-simbot/simbot-offline-inference/commit/d22fe1403b546c866b949992402cd2c2654b5b9d))
* just everything from running the eval before report submission ([07b000e](https://github.com/emma-simbot/simbot-offline-inference/commit/07b000e1afb17b54ac46f5451490ad500c522626))
* only evaluate missions that have not been evaluated yet ([453ceb9](https://github.com/emma-simbot/simbot-offline-inference/commit/453ceb9298dbe3cb3c199bfa84cb3f72621d7b49))
* run eval on single gpu ([bf16694](https://github.com/emma-simbot/simbot-offline-inference/commit/bf166941fe5530972d4f78c909443b99ef9bbe2c))
* set instance range in settings and send to s3 when done ([b126ffc](https://github.com/emma-simbot/simbot-offline-inference/commit/b126ffcb90d4c39f959e96c60b8006fdedcac026))


### Bug Fixes

* improve logs and healthchecks and responses ([849ba61](https://github.com/emma-simbot/simbot-offline-inference/commit/849ba61062f9cb5ef745bc1bd70a183623d9fc4d))
* just make loads of changes to make it actually work properly ([041d40c](https://github.com/emma-simbot/simbot-offline-inference/commit/041d40c75c34a7e672ddc34bdd2df5ebcddc7b13))
* just make loads of changes to make it actually work properly ([2a88df5](https://github.com/emma-simbot/simbot-offline-inference/commit/2a88df5716e1a7d14bcf96249feb5d31a2cab5cc))
* make sure we do all instances and dont miss any ([f4901b5](https://github.com/emma-simbot/simbot-offline-inference/commit/f4901b58127eac81e4cb55c6d8d849c9d60feb07))
* use the new arena executable ([c8a287d](https://github.com/emma-simbot/simbot-offline-inference/commit/c8a287dc3557339c2e63d6f0025ac9dc250d0a60))

## [1.1.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v1.0.1...v1.1.0) (2023-03-19)


### Features

* handle lightweight dialogs within the context of the actions ([8647fe7](https://github.com/emma-simbot/simbot-offline-inference/commit/8647fe7da42983dac5d2aa0a66b4efd44ce79182))

## [1.0.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v1.0.0...v1.0.1) (2023-01-24)


### Bug Fixes

* only download and prepare T2 validation data ([54f716e](https://github.com/emma-simbot/simbot-offline-inference/commit/54f716e97ad07053313fb89997fbcc9b7225d947))

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
