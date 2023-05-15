# Changelog

All notable changes to this project will be documented in this file. See
[Conventional Commits](https://conventionalcommits.org) for commit guidelines.

## [4.32.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.31.1...v4.32.0) (2023-05-15)


### Features

* create flag to enforce/ignore successful preparation steps ([4af06aa](https://github.com/emma-simbot/simbot-offline-inference/commit/4af06aad214e57367e8be390878811f35a3c5098))
* **script:** create script that prepares user area for running the offline inference ([951080a](https://github.com/emma-simbot/simbot-offline-inference/commit/951080a0d4b2deeda7630a1ccbe0105dedd04f75))


### Bug Fixes

* guard against `InterruptedByNewCommandBatch` ([6b8c239](https://github.com/emma-simbot/simbot-offline-inference/commit/6b8c2390304a38cfe597e42e98192a0a9259426a))
* **scripts:** automatically setup necessary symlinks ([b45cff7](https://github.com/emma-simbot/simbot-offline-inference/commit/b45cff7584c0ac4e285e2260dc6136b1f7074cd3))

## [4.31.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.31.0...v4.31.1) (2023-05-12)


### Bug Fixes

* raycast missed exception handling ([#40](https://github.com/emma-simbot/simbot-offline-inference/issues/40)) ([7a3d3c4](https://github.com/emma-simbot/simbot-offline-inference/commit/7a3d3c4abeecffb553d258873bcfaafbf5d2f025))

## [4.31.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.30.0...v4.31.0) (2023-04-28)


### Features

* add setting for fastmode ([b891a94](https://github.com/emma-simbot/simbot-offline-inference/commit/b891a94f431a86459a31ae92472899b7a7b3dc9f))
* added flag randomise start position ([#41](https://github.com/emma-simbot/simbot-offline-inference/issues/41)) ([741abc8](https://github.com/emma-simbot/simbot-offline-inference/commit/741abc8bae77aacfce0e891dd439166e75b8ae7f))


### Bug Fixes

* arena source cdfs ([be81cb8](https://github.com/emma-simbot/simbot-offline-inference/commit/be81cb89affc94d355ffaacc7765b04c3873c204))
* restore support for running the T1 trajectories ([75d545c](https://github.com/emma-simbot/simbot-offline-inference/commit/75d545c996c8acd4959b82ca6e3071a9719411b7))

## [4.30.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.9...v4.30.0) (2023-04-26)


### Features

* **T3:** add mission 1 ([455d023](https://github.com/emma-simbot/simbot-offline-inference/commit/455d023b07055ce23895e4768d647968f1e3b349))

## [4.29.9](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.8...v4.29.9) (2023-04-26)


### Bug Fixes

* operate microwave challenges ([59b8b44](https://github.com/emma-simbot/simbot-offline-inference/commit/59b8b441c73d447a2e9e43c7db2488053e785951))

## [4.29.8](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.7...v4.29.8) (2023-04-25)


### Bug Fixes

* **coffee unmaker:** improve plans, add pot to beans, and iterate layouts ([30a6a0d](https://github.com/emma-simbot/simbot-offline-inference/commit/30a6a0daff08057972ba940f7b776b6978831297))

## [4.29.7](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.6...v4.29.7) (2023-04-25)


### Bug Fixes

* ensure the microwave is empty ([a4c454a](https://github.com/emma-simbot/simbot-offline-inference/commit/a4c454aa86792d1213172b5aa6f6aa43c5e91791))
* remove the boss coffee mug from the colour changer missions ([eee16b4](https://github.com/emma-simbot/simbot-offline-inference/commit/eee16b45369978fc75668d64ce24d277efa0340b))

## [4.29.6](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.5...v4.29.6) (2023-04-25)


### Bug Fixes

* disabling color variants with microwave challenges ([0d8ad3a](https://github.com/emma-simbot/simbot-offline-inference/commit/0d8ad3aba632293be9f1cb637d42db5ac02d9b86))

## [4.29.5](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.4...v4.29.5) (2023-04-25)


### Bug Fixes

* prep condition for pickup objects from containers ([ab9a60c](https://github.com/emma-simbot/simbot-offline-inference/commit/ab9a60cc14f30c79d2354965c11470127d4dae4e))
* prep goal condition for place object in container challenge ([40769c4](https://github.com/emma-simbot/simbot-offline-inference/commit/40769c4c72f24e23880c70706fa192cba112aa49))

## [4.29.4](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.3...v4.29.4) (2023-04-25)


### Bug Fixes

* disable start colour variants for the colour changer challenges ([a1e39cb](https://github.com/emma-simbot/simbot-offline-inference/commit/a1e39cb79454a2f8c916d77c29319898fd416936))
* remove objects that cannot be color-changed ([66451f1](https://github.com/emma-simbot/simbot-offline-inference/commit/66451f13515900b59830cc674a20ea254dcf971f))
* update plans for the challenges ([b4269d1](https://github.com/emma-simbot/simbot-offline-inference/commit/b4269d1b9e9ab1e857a4434e9ecc1161f0bb9b00))

## [4.29.3](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.2...v4.29.3) (2023-04-25)


### Bug Fixes

* sink-related challenges ([e44408c](https://github.com/emma-simbot/simbot-offline-inference/commit/e44408c22707ffd5b522e673102a8bbc0f43469d))
* sink-related goal conditions and plans ([ed27162](https://github.com/emma-simbot/simbot-offline-inference/commit/ed271629859ca609e38270b18c66fb722fa47b70))

## [4.29.2](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.1...v4.29.2) (2023-04-23)


### Bug Fixes

* target object was not flagged as ambiguous in key ([5579cda](https://github.com/emma-simbot/simbot-offline-inference/commit/5579cda66407a435ba9200b5e4aeb0d382951507))

## [4.29.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.29.0...v4.29.1) (2023-04-23)


### Bug Fixes

* high level keys and plans ([b1dfde9](https://github.com/emma-simbot/simbot-offline-inference/commit/b1dfde9b82f6a64eff7a720f59a350e816c4ead8))
* include from_receptacle in breaking challenges ([0f236ba](https://github.com/emma-simbot/simbot-offline-inference/commit/0f236ba228ae8265cc13564b07077281e0d27545))
* remove the from receptacle from high level key in break challenges ([8db7588](https://github.com/emma-simbot/simbot-offline-inference/commit/8db75880e298f3f39e59bc51ceadb006b238ce05))

## [4.29.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.28.0...v4.29.0) (2023-04-23)


### Features

* break objects on random desks ([#39](https://github.com/emma-simbot/simbot-offline-inference/issues/39)) ([4e2afe9](https://github.com/emma-simbot/simbot-offline-inference/commit/4e2afe9858d346f811b4eec709cdcf119904f3cf))


### Bug Fixes

* desks should not be unique ([9f3f1f2](https://github.com/emma-simbot/simbot-offline-inference/commit/9f3f1f24ccafe77ae26012dcc2cd7f9884d30abb))
* do not use the colour changer to make the object the same color ([80d9a90](https://github.com/emma-simbot/simbot-offline-inference/commit/80d9a9076e39af74005d4341ed1d4ee1937a6e8e))

## [4.28.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.27.0...v4.28.0) (2023-04-23)


### Features

* place bowl on plate on gravity pad ([#38](https://github.com/emma-simbot/simbot-offline-inference/issues/38)) ([e058d15](https://github.com/emma-simbot/simbot-offline-inference/commit/e058d152c8d26945e0680f3328807218398725c5))


### Bug Fixes

* check that the gravity pad contains the plate during prep subgoal ([6ec8b31](https://github.com/emma-simbot/simbot-offline-inference/commit/6ec8b31532f5c9ae3e0c3662fd9d1edaa08a20e6))
* disable color variants for fridge/freezer challenges ([1778d72](https://github.com/emma-simbot/simbot-offline-inference/commit/1778d720632ecf629fd7d8c947679df09d530ca8))
* update room/colour was failing because there was no 0th index ([a57bb0c](https://github.com/emma-simbot/simbot-offline-inference/commit/a57bb0ccfe9946ab025c5fd27097d3afdf0a906e))

## [4.27.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.26.0...v4.27.0) (2023-04-23)


### Features

* added color variants flag ([#37](https://github.com/emma-simbot/simbot-offline-inference/issues/37)) ([6823c47](https://github.com/emma-simbot/simbot-offline-inference/commit/6823c478271c80634731d8df0e6a266a56d28c82))

## [4.26.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.25.0...v4.26.0) (2023-04-23)


### Features

* breaking things with the hammer ([#36](https://github.com/emma-simbot/simbot-offline-inference/issues/36)) ([0bed877](https://github.com/emma-simbot/simbot-offline-inference/commit/0bed87733900834c3cbbc8612cdebebb434319a3))

## [4.25.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.24.1...v4.25.0) (2023-04-23)


### Features

* pickup object from printer ([#35](https://github.com/emma-simbot/simbot-offline-inference/issues/35)) ([b5f1cb3](https://github.com/emma-simbot/simbot-offline-inference/commit/b5f1cb35c660149e46910fda9342dc8e0740bb1e))


### Bug Fixes

* add breakroom table to required objects list ([4e6d8b6](https://github.com/emma-simbot/simbot-offline-inference/commit/4e6d8b6daae52c837d1a0eda757239aa6acdd073))
* dont make the spawned object into a required one ([987a287](https://github.com/emma-simbot/simbot-offline-inference/commit/987a287e8819b0b8374b72815fedc11e04a29322))
* replace the spawned object with the printer cartridge ([172fb7a](https://github.com/emma-simbot/simbot-offline-inference/commit/172fb7a757dea6d1a4062623f64d4ad68434c246))

## [4.24.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.24.0...v4.24.1) (2023-04-22)


### Bug Fixes

* expliticly ensure at least the first subgoal has been completed ([f61f810](https://github.com/emma-simbot/simbot-offline-inference/commit/f61f810b94c3b569b533475fd79a24ab4edc0981))
* return after logging the failed trajectory ([940d400](https://github.com/emma-simbot/simbot-offline-inference/commit/940d40085493805275afa6072fd3eaab2dfaaa40))

## [4.24.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.23.0...v4.24.0) (2023-04-22)


### Features

* pickup target among distractors ([#34](https://github.com/emma-simbot/simbot-offline-inference/issues/34)) ([8264204](https://github.com/emma-simbot/simbot-offline-inference/commit/826420490dfb667b4cf8030d1d1a7e209b133662))

## [4.23.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.22.0...v4.23.0) (2023-04-22)


### Features

* add goal for prep steps ([f3db7ec](https://github.com/emma-simbot/simbot-offline-inference/commit/f3db7ecdb5b1fc7b9e264b9d8ae72fecc50ccd2d))

## [4.22.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.21.0...v4.22.0) (2023-04-22)


### Features

* add goal for prep steps ([7742128](https://github.com/emma-simbot/simbot-offline-inference/commit/7742128de7952519e6042e3183c561e97d932e1d))
* add goals to ensure the "objects in containers" missions are setup correctly ([606a4c3](https://github.com/emma-simbot/simbot-offline-inference/commit/606a4c3dcccac07e960310999a32aa276b932546))
* mark the run as failed if the preparation steps did not succeed ([4830023](https://github.com/emma-simbot/simbot-offline-inference/commit/48300234304ef524fe4fb85f9c3142b3a5d03eeb))
* mark the run as failed if the subgoal success is 0 ([f3659b3](https://github.com/emma-simbot/simbot-offline-inference/commit/f3659b35abaa77f0cb63ac4de619339e9f681c1a))


### Bug Fixes

* disable color variants usage for pickup and place missions separately ([b941892](https://github.com/emma-simbot/simbot-offline-inference/commit/b941892e05640fac81775394776ed349bf8e3c87))

## [4.21.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.20.0...v4.21.0) (2023-04-22)


### Features

* add the `target-object-is-ambiguous` high-level key ([f534502](https://github.com/emma-simbot/simbot-offline-inference/commit/f534502965f217fb8e87f667f3e0d95012de9417))


### Bug Fixes

* update high-level key config within wandb tracker ([3bbc069](https://github.com/emma-simbot/simbot-offline-inference/commit/3bbc0697d9730224062a4615458862353a144399))

## [4.20.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.19.1...v4.20.0) (2023-04-21)


### Features

* place object onto plate in container ([#33](https://github.com/emma-simbot/simbot-offline-inference/issues/33)) ([ae16713](https://github.com/emma-simbot/simbot-offline-inference/commit/ae16713e85483736fce93529a7b301f21d6048bc))

## [4.19.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.19.0...v4.19.1) (2023-04-21)


### Bug Fixes

* wrong receptacle for target object ([c45a898](https://github.com/emma-simbot/simbot-offline-inference/commit/c45a8982b2fc7a84f0158d1689b853c90e3c28e2))

## [4.19.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.18.0...v4.19.0) (2023-04-21)


### Features

* make it easier to generate trajectories in a different folder ([4215037](https://github.com/emma-simbot/simbot-offline-inference/commit/4215037258cf58945db50bfdf6e86b5ed8701c87))


### Bug Fixes

* make the output dir for generated trajectories ([fcedc65](https://github.com/emma-simbot/simbot-offline-inference/commit/fcedc65825904e3dbcda5cba3c9c67eb470b17c0))

## [4.18.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.17.0...v4.18.0) (2023-04-21)


### Features

* enable carrot machine challenges ([321d7a6](https://github.com/emma-simbot/simbot-offline-inference/commit/321d7a60edb6e5c1450dac0ab195e769a1a146ed))


### Bug Fixes

* kill the unity instance before trying to restart it ([1274ae2](https://github.com/emma-simbot/simbot-offline-inference/commit/1274ae218082d77c280bb96a203416fb4b4f6b39))

## [4.17.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.16.1...v4.17.0) (2023-04-21)


### Features

* stack food plate ([#32](https://github.com/emma-simbot/simbot-offline-inference/issues/32)) ([2ef14db](https://github.com/emma-simbot/simbot-offline-inference/commit/2ef14db383bb8f253b52b36291b20c978004d488))

## [4.16.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.16.0...v4.16.1) (2023-04-21)


### Bug Fixes

* always remove objects from microwave ([ea0dbcd](https://github.com/emma-simbot/simbot-offline-inference/commit/ea0dbcdedb72fd18c84e5446cdbc5a56c0582890))

## [4.16.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.15.1...v4.16.0) (2023-04-21)


### Features

* include stacked objects in the high level key ([3f937e7](https://github.com/emma-simbot/simbot-offline-inference/commit/3f937e76af5b7cbc1ba8c1afbf14d4c5cb654702))


### Bug Fixes

* remove the `change_color` instruction action ([d53cbaa](https://github.com/emma-simbot/simbot-offline-inference/commit/d53cbaa0e62698cde5343254be8bbdc3b77a203c))

## [4.15.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.15.0...v4.15.1) (2023-04-21)


### Bug Fixes

* color changer preparation step ([cc548ec](https://github.com/emma-simbot/simbot-offline-inference/commit/cc548ec415a371431d68e45e328d1697db65a080))

## [4.15.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.14.2...v4.15.0) (2023-04-21)


### Features

* Add container challenges for the warehouse sink ([#30](https://github.com/emma-simbot/simbot-offline-inference/issues/30)) ([460dbe1](https://github.com/emma-simbot/simbot-offline-inference/commit/460dbe1900af203d0a5d6dad24a1eb6a4fb7d614))


### Bug Fixes

* use color variants for both boss mug and normal mug ([a7b5371](https://github.com/emma-simbot/simbot-offline-inference/commit/a7b537191fd4729f4edef905470d1e15b8055307))

## [4.14.2](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.14.1...v4.14.2) (2023-04-21)


### Bug Fixes

* incorrect function call ([af355fd](https://github.com/emma-simbot/simbot-offline-inference/commit/af355fd9b5bd7a2f89baf1d18078b05d0861b0ec))

## [4.14.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.14.0...v4.14.1) (2023-04-20)


### Bug Fixes

* attempt to handle the 408 connection error ([467f5c7](https://github.com/emma-simbot/simbot-offline-inference/commit/467f5c7fc2c58a876b249c934e9e602758af1535))

## [4.14.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.13.3...v4.14.0) (2023-04-20)


### Features

* include unity logs with each run ([bdea65e](https://github.com/emma-simbot/simbot-offline-inference/commit/bdea65e4e677028028b1cc991fb70d1087029810))


### Bug Fixes

* preparation steps for operate microwave missions ([e23eb24](https://github.com/emma-simbot/simbot-offline-inference/commit/e23eb249b4624f2edf772726f3da0d3963bdffc2))
* Remove final pick ups ([#29](https://github.com/emma-simbot/simbot-offline-inference/issues/29)) ([fa71470](https://github.com/emma-simbot/simbot-offline-inference/commit/fa71470b50bcd5a6316f1965a95a02da40c7035a))

## [4.13.3](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.13.2...v4.13.3) (2023-04-20)


### Bug Fixes

* Color changer interaction object in High Level Key ([#28](https://github.com/emma-simbot/simbot-offline-inference/issues/28)) ([c0468d9](https://github.com/emma-simbot/simbot-offline-inference/commit/c0468d9a4e4c039abba7d4e23685f6879a01ec4a))

## [4.13.2](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.13.1...v4.13.2) (2023-04-20)


### Bug Fixes

* goal conditions for the operate printer challenges ([151647c](https://github.com/emma-simbot/simbot-offline-inference/commit/151647cfd91f35e28884d8d6e70b1e310432a4ea))

## [4.13.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.13.0...v4.13.1) (2023-04-19)


### Bug Fixes

* disable the carrot machine challenges ([4badcef](https://github.com/emma-simbot/simbot-offline-inference/commit/4badcef705a815b36d0d87dcb4e510ac28e1dc50))

## [4.13.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.12.1...v4.13.0) (2023-04-19)


### Features

* add more helper methods to structures ([893f0b6](https://github.com/emma-simbot/simbot-offline-inference/commit/893f0b6ac690f4fcb77973ce0ca9948423833408))


### Bug Fixes

* change starting room to robotics lab ([518425a](https://github.com/emma-simbot/simbot-offline-inference/commit/518425afe0df928959e9ee91819cd0114bdf568b))
* let object instance ID's end in a * ([f3d7713](https://github.com/emma-simbot/simbot-offline-inference/commit/f3d7713bd6b98b84fe031c4f243e8cf61c17b879))
* make the argument name be more descriptive to what is needed ([93e1760](https://github.com/emma-simbot/simbot-offline-inference/commit/93e1760f230d7782c0383418834523e6d675a457))
* operate printer challenges ([82ce622](https://github.com/emma-simbot/simbot-offline-inference/commit/82ce6222f12862ae7d987d8dc66cba56b70c3587))
* **operate printer:** make sure robotic arm is out the way ([1dca91b](https://github.com/emma-simbot/simbot-offline-inference/commit/1dca91b45747039a54e3e62dd3b73fa863c122e2))
* operate time machine with carrots ([1f85703](https://github.com/emma-simbot/simbot-offline-inference/commit/1f8570371a577218810a2c59ffa60ba6fd3616e0))
* printer cartridge name in the preparation plan ([b8250fa](https://github.com/emma-simbot/simbot-offline-inference/commit/b8250fa6d61260a6ebe73d023e637c150993166f))
* typo ([0355636](https://github.com/emma-simbot/simbot-offline-inference/commit/0355636fe90418f94c73ad994d4fc2de5bd10fd2))
* validator condition for object instance id suffix ([d8fb10f](https://github.com/emma-simbot/simbot-offline-inference/commit/d8fb10f3cccf97334a7f542da141039f50abee7c))

## [4.12.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.12.0...v4.12.1) (2023-04-19)


### Bug Fixes

* Initial room for carrot maker challenge ([#27](https://github.com/emma-simbot/simbot-offline-inference/issues/27)) ([7221c32](https://github.com/emma-simbot/simbot-offline-inference/commit/7221c3278ebeb42e1427f3034b4406fe5f8393ea))

## [4.12.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.11.0...v4.12.0) (2023-04-19)


### Features

* add printer challenges ([#26](https://github.com/emma-simbot/simbot-offline-inference/issues/26)) ([f895cd4](https://github.com/emma-simbot/simbot-offline-inference/commit/f895cd43da9d001ba003a9a902498bfa7896be55))

## [4.11.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.10.0...v4.11.0) (2023-04-19)


### Features

* Add carrot machine challenges ([#23](https://github.com/emma-simbot/simbot-offline-inference/issues/23)) ([dabbc47](https://github.com/emma-simbot/simbot-offline-inference/commit/dabbc474163ec653860a0757aa647b41fb54e3ff))

## [4.10.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.9.0...v4.10.0) (2023-04-19)


### Features

* Add time machine on carrots ([#25](https://github.com/emma-simbot/simbot-offline-inference/issues/25)) ([7d91e43](https://github.com/emma-simbot/simbot-offline-inference/commit/7d91e430ce1a22a816dc440f0d0f7b38a8f015c1))

## [4.9.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.8.0...v4.9.0) (2023-04-19)


### Features

* coffee unmaker with additional objects ([#22](https://github.com/emma-simbot/simbot-offline-inference/issues/22)) ([7f284f9](https://github.com/emma-simbot/simbot-offline-inference/commit/7f284f937ef572deb4cd9acc318d29a6006f80fd))

## [4.8.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.7.0...v4.8.0) (2023-04-19)


### Features

* Add microwave challenge ([#21](https://github.com/emma-simbot/simbot-offline-inference/issues/21)) ([f62b996](https://github.com/emma-simbot/simbot-offline-inference/commit/f62b99650c73603e23b592e981718e3450f4fc91))
* object transformations ([#19](https://github.com/emma-simbot/simbot-offline-inference/issues/19)) ([f76c4c2](https://github.com/emma-simbot/simbot-offline-inference/commit/f76c4c29bbf1e9f6926f37dbf9ca7515beb5c8bf))

## [4.7.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.6.0...v4.7.0) (2023-04-19)


### Features

* support setting wandb group name from run command ([9b72cc8](https://github.com/emma-simbot/simbot-offline-inference/commit/9b72cc898e36474b00c691f9330b659bb767bf8a))


### Bug Fixes

* kill command for the experience hub ([9852ce8](https://github.com/emma-simbot/simbot-offline-inference/commit/9852ce852600549e071a9469d65b560231d4b7a5))
* use the preparation plan to toggle the sink ([4d3c266](https://github.com/emma-simbot/simbot-offline-inference/commit/4d3c26666702eb682c8ffc9e3848db157a0b7b09))

## [4.6.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.5.0...v4.6.0) (2023-04-18)


### Features

* Add more pickable objects for fridge/freezer ([#18](https://github.com/emma-simbot/simbot-offline-inference/issues/18)) ([baf6850](https://github.com/emma-simbot/simbot-offline-inference/commit/baf68504e39212ad16e9bab3fce08f4bfbca8a11))
* save the mission trajectory file and the output file to wandb ([211bd8c](https://github.com/emma-simbot/simbot-offline-inference/commit/211bd8c47034806128fbfe6cbd3ab25c4513e019))

## [4.5.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.4.1...v4.5.0) (2023-04-18)


### Features

* log the experience hub version with the wandb run ([45c17fb](https://github.com/emma-simbot/simbot-offline-inference/commit/45c17fb4bbb12605f9f2b4b3c5b7b9ea2464f58d))

## [4.4.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.4.0...v4.4.1) (2023-04-17)


### Bug Fixes

* command that starts the experience hub ([f187fef](https://github.com/emma-simbot/simbot-offline-inference/commit/f187fef18711f47cbe7c7584abbc6316eac11bde))
* command used to kill the experience hub ([5e8bd3d](https://github.com/emma-simbot/simbot-offline-inference/commit/5e8bd3d5f588b29a5bba9e4c003acdc23cd0d961))
* if failed to go to a random viewpoint, just go to the first one in the room ([bb3d652](https://github.com/emma-simbot/simbot-offline-inference/commit/bb3d6523e6acf9e8725dc1c8318b1efcdf65730e))
* use 2 workers to hopefully stop the experience hub from crashing ([daa17a0](https://github.com/emma-simbot/simbot-offline-inference/commit/daa17a0ab4f76dd120b1d264ac1f330954a44f44))

## [4.4.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.3.0...v4.4.0) (2023-04-17)


### Features

* also send subgoal completion success rate to wandb per session ([3a789f0](https://github.com/emma-simbot/simbot-offline-inference/commit/3a789f0ece7443058b1fad536bcb92248983e44d))
* set the session id as the run name ([1960040](https://github.com/emma-simbot/simbot-offline-inference/commit/196004061d6f08939967b3926f298b195df6a5a4))

## [4.3.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.2.0...v4.3.0) (2023-04-17)


### Features

* use subprocess to run the experience hub because its easier to consistently kill ([bfaeea2](https://github.com/emma-simbot/simbot-offline-inference/commit/bfaeea2499fb69178f8d40a53af380176f6b1f62))


### Bug Fixes

* disable fast mode ([d894ef2](https://github.com/emma-simbot/simbot-offline-inference/commit/d894ef2bde809591e97530b8ae9ce4075df70593))
* disable look actions in random walk ([6060c33](https://github.com/emma-simbot/simbot-offline-inference/commit/6060c33601238e679aaf18d22a6f1803f7eeb486))
* increase number of healthcheck attempts for experience hub ([a6737a2](https://github.com/emma-simbot/simbot-offline-inference/commit/a6737a27173dabafe373266022657f2fc3148067))
* plan for placing objects in container ([f522c26](https://github.com/emma-simbot/simbot-offline-inference/commit/f522c2665c8060add37a63b691c48800fedce4b3))
* remove initial contained items from various containers ([d53b7a0](https://github.com/emma-simbot/simbot-offline-inference/commit/d53b7a06b92f9f642979a50f2601eb317d4941b2))

## [4.2.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.1.0...v4.2.0) (2023-04-16)


### Features

* track progress of generated trajectories on wandb ([cb5c1ab](https://github.com/emma-simbot/simbot-offline-inference/commit/cb5c1ab0622bb64c9401652d9aaac3aa5166cf5c))


### Bug Fixes

* set experience hub timeout to be stupidly high ([9302cca](https://github.com/emma-simbot/simbot-offline-inference/commit/9302ccacfb40b07673bf488692f0403fc8ffa72f))

## [4.1.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.0.1...v4.1.0) (2023-04-16)


### Features

* store any remaining utterances that have not been sent to the action outputs ([2bf68b7](https://github.com/emma-simbot/simbot-offline-inference/commit/2bf68b7302bf05866aee510168300228c4feb785))


### Bug Fixes

* break out the loop if all the goals are complete ([5b8a18f](https://github.com/emma-simbot/simbot-offline-inference/commit/5b8a18fbc5108b7156c661fb24193f75c7d01122))
* break out the loop if the goals have been completed ([5abe3b1](https://github.com/emma-simbot/simbot-offline-inference/commit/5abe3b15bdb2a44983d3cb79a5a2b7736c9227d1))

## [4.0.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v4.0.0...v4.0.1) (2023-04-16)


### Bug Fixes

* make sure the breakroom table exists, and has space for the preparation items ([34a10cd](https://github.com/emma-simbot/simbot-offline-inference/commit/34a10cd68c5be24c35c7b89b7467dec2aa87b480))
* preparation plan for fill object in sink challenge ([86a96b0](https://github.com/emma-simbot/simbot-offline-inference/commit/86a96b0a0833377b277f6571e2d9cb1c9d77379f))

## [4.0.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v3.2.0...v4.0.0) (2023-04-16)


### ⚠ BREAKING CHANGES

* migrate challenges to using state conditions

### Features

* migrate challenges to using state conditions ([615b37c](https://github.com/emma-simbot/simbot-offline-inference/commit/615b37cbf7b4b80ee2ab0285ed6ad7d1cfcae24d))
* turn on fastmode in the arena ([3325143](https://github.com/emma-simbot/simbot-offline-inference/commit/3325143c7bfc98a4d87dd46eb9ac581880fd071d))


### Bug Fixes

* "and" is no longer allowed ([1ca4655](https://github.com/emma-simbot/simbot-offline-inference/commit/1ca4655251035f6be205b59d4a0341d1c2798514))
* ensure the reimported CDF is same as the original CDF ([df7a6b8](https://github.com/emma-simbot/simbot-offline-inference/commit/df7a6b8971332553376e8d933c8c90065a5299a4))
* go to a random viewpoint that actually exists in the current scene ([f4a21cb](https://github.com/emma-simbot/simbot-offline-inference/commit/f4a21cb48608d07c209f7799709630a53b166743))
* high level key action for "fill object in sink" ([af4829b](https://github.com/emma-simbot/simbot-offline-inference/commit/af4829b9b087cb3f9b26b06749bf31022c8af098))
* remove the duplicated running of preparation steps ([4db9b7e](https://github.com/emma-simbot/simbot-offline-inference/commit/4db9b7e7b2b873c2a91f2a806d3875558780cc90))
* use join and close when killing the experience hub process ([3c18b58](https://github.com/emma-simbot/simbot-offline-inference/commit/3c18b58c1293213320411f23b78cb0e5ba8f2f0c))

## [3.2.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v3.1.2...v3.2.0) (2023-04-14)


### Features

* do not send utterances to the arena if all the goals are complete ([b8cc13c](https://github.com/emma-simbot/simbot-offline-inference/commit/b8cc13c125338e4965b03edf7f244e88aa46c46f))
* make it easier to kill the experience hub when something goes wrong ([7e375fe](https://github.com/emma-simbot/simbot-offline-inference/commit/7e375fec74eb0c7d20038fc8e02011201e1dd9ec))


### Bug Fixes

* fill the object challenge goals ([8543bb2](https://github.com/emma-simbot/simbot-offline-inference/commit/8543bb2a7d8f238a6330761fed959bae9d945d67))
* include a preparation plan to be able to pickup objects ([#16](https://github.com/emma-simbot/simbot-offline-inference/issues/16)) ([d86301a](https://github.com/emma-simbot/simbot-offline-inference/commit/d86301ad96dd407c6c768847e5b494cac1dbc825))

## [3.1.2](https://github.com/emma-simbot/simbot-offline-inference/compare/v3.1.1...v3.1.2) (2023-04-13)


### Bug Fixes

* remove the trajectory batching ([a467340](https://github.com/emma-simbot/simbot-offline-inference/commit/a467340cca8825bbcaa475155e584dccb41d5c6d))

## [3.1.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v3.1.0...v3.1.1) (2023-04-12)


### Bug Fixes

* do not randomise trajectory run order by default ([3e16279](https://github.com/emma-simbot/simbot-offline-inference/commit/3e16279bda25192d488792a0c5a297fc95252ba0))
* get rid of the progress bar ([133b049](https://github.com/emma-simbot/simbot-offline-inference/commit/133b04938b89eff8e864fd17fa35b6702b424e21))
* remove old "kill arena" command ([23e4cda](https://github.com/emma-simbot/simbot-offline-inference/commit/23e4cda97cac949b775835b2e17cc63206c0d6d9))

## [3.1.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v3.0.0...v3.1.0) (2023-04-12)


### Features

* restart the arena after every 10 sessions ([0f9fcdd](https://github.com/emma-simbot/simbot-offline-inference/commit/0f9fcdd800e30cc0e94a047dd37ec9a43dffdc42))


### Bug Fixes

* improve the styling of the progress bar ([3191a34](https://github.com/emma-simbot/simbot-offline-inference/commit/3191a3492b4a2765f5bcaeefc43d91a6b536aa8c))
* update the progress bar after sending the utterance ([5d698c3](https://github.com/emma-simbot/simbot-offline-inference/commit/5d698c36e0223bc46ed0d6cd12bbed32714ccbda))
* update the progress bar more ([4ecce70](https://github.com/emma-simbot/simbot-offline-inference/commit/4ecce701c75075be3859101114b320f80f777a1d))

## [3.0.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.13.0...v3.0.0) (2023-04-12)


### ⚠ BREAKING CHANGES

* use a new structure for the high-level keys

### Features

* do not re-run missions that have already been run ([1720664](https://github.com/emma-simbot/simbot-offline-inference/commit/1720664590646b82efd4de7f24d376b8f735c59c))
* use a new structure for the high-level keys ([2116539](https://github.com/emma-simbot/simbot-offline-inference/commit/211653951de884c7b953111bbdd61c4fb696abd6))


### Bug Fixes

* add more state names to the arena constants ([79365b2](https://github.com/emma-simbot/simbot-offline-inference/commit/79365b289adbcd1a912f9762e3034506f63a2af4))
* use kebab-case when converting high-level key to string ([2e2d3e8](https://github.com/emma-simbot/simbot-offline-inference/commit/2e2d3e8d271a7fb1447ddcdc1ee906fa2af4a1d9))

## [2.13.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.12.0...v2.13.0) (2023-04-12)


### Features

* print a table of num challenges per high level key ([4364dbd](https://github.com/emma-simbot/simbot-offline-inference/commit/4364dbd766c18e37c8952724203209cd287ed6b5))

## [2.12.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.11.0...v2.12.0) (2023-04-12)


### Features

* separate the trajectory generation from the trajectory running ([4b9cd0d](https://github.com/emma-simbot/simbot-offline-inference/commit/4b9cd0d4b78c59373351a3c79d30d426c023e3f0))

## [2.11.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.10.0...v2.11.0) (2023-04-12)


### Features

* **challenge:** convert coffee into beans using the coffee unmaker ([#15](https://github.com/emma-simbot/simbot-offline-inference/issues/15)) ([8e36065](https://github.com/emma-simbot/simbot-offline-inference/commit/8e36065c350a84400d92b61c1e5cb54c9c89e88e))

## [2.10.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.9.1...v2.10.0) (2023-04-12)


### Features

* ensure each object-related key is a 'readable name' (in the `HighLevelKey` ([0cb022e](https://github.com/emma-simbot/simbot-offline-inference/commit/0cb022ef2fefad9825095d9bdb083fc003bb586c))

## [2.9.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.9.0...v2.9.1) (2023-04-12)


### Bug Fixes

* explicitly forbid unsupported keys from the `HighLevelKey` ([aca0079](https://github.com/emma-simbot/simbot-offline-inference/commit/aca0079b905460b24e90a12dbfb99bd7136f5831))

## [2.9.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.8.0...v2.9.0) (2023-04-11)


### Features

* fill trajectories ([#13](https://github.com/emma-simbot/simbot-offline-inference/issues/13)) ([420313c](https://github.com/emma-simbot/simbot-offline-inference/commit/420313ce28cb490a45cf3f0d14ef171a5d5ce035))

## [2.8.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.7.0...v2.8.0) (2023-04-11)


### Features

* add challenge to clean a plate in sink ([392518a](https://github.com/emma-simbot/simbot-offline-inference/commit/392518afc26cc3741d8b47f8b296a35b435cf249))


### Bug Fixes

* object instance ids for the sink and plate ([9354196](https://github.com/emma-simbot/simbot-offline-inference/commit/9354196947139ee57ad5eddcaf4e7006fdda99c6))
* use deepcopy on the sink and create a trajectory for every layout ([0b004a5](https://github.com/emma-simbot/simbot-offline-inference/commit/0b004a588c04083afdf4f74491b508585c4bf9a4))

## [2.7.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.6.1...v2.7.0) (2023-04-11)


### Features

* lowercase the session ids (except for the prefix) ([eac8202](https://github.com/emma-simbot/simbot-offline-inference/commit/eac82027909d3d6ac14d666d4c94a7ec2f6e3dad))
* separate the readable name from the object key when building challenges ([35fbde2](https://github.com/emma-simbot/simbot-offline-inference/commit/35fbde272867788cb44e864ce4eedd1567c125fb))
* use readable names for the keys ([9c30b00](https://github.com/emma-simbot/simbot-offline-inference/commit/9c30b00fc30ce62d46b274c35d0db18fd20826c3))

## [2.6.1](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.6.0...v2.6.1) (2023-04-11)


### Bug Fixes

* add more error types to ignore when randomising start position ([f866cdb](https://github.com/emma-simbot/simbot-offline-inference/commit/f866cdb1168f891da9df29a734c4e2bb65025962))
* go back to using `str` for `str`-based structures ([8a62425](https://github.com/emma-simbot/simbot-offline-inference/commit/8a62425bd55156606165b42650ebb153633b3aed))

## [2.6.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.5.0...v2.6.0) (2023-04-11)


### Features

* add challenges for broken bowls and coloured bowls ([43cb76c](https://github.com/emma-simbot/simbot-offline-inference/commit/43cb76c9893ac908703e4c4a4b51577c111d994f))
* improve the progress bar for the challenge validator ([9e9e2d2](https://github.com/emma-simbot/simbot-offline-inference/commit/9e9e2d2607895e310ef349c3d3bc96e736581e36))
* only use the colour changer colors ([4775e46](https://github.com/emma-simbot/simbot-offline-inference/commit/4775e46b0bcac1e0a4cf444af8754b2581a3d289))
* shuffle the order trajectories are generated in ([33ea2fa](https://github.com/emma-simbot/simbot-offline-inference/commit/33ea2faa102a8511cfdaae77ea55263c905c3d0e))
* support using RNG for the CDF scenes (with `floor_plan`) ([b7e1b4d](https://github.com/emma-simbot/simbot-offline-inference/commit/b7e1b4d589c6350eed2a29411dd4e155e7686324))
* validate cdfs from generated missions ([062178c](https://github.com/emma-simbot/simbot-offline-inference/commit/062178c9c866533198fc3f1f3b2a7a9a68dab91f))


### Bug Fixes

* `required_objects` key within the `CDFScene` ([fe3bcd1](https://github.com/emma-simbot/simbot-offline-inference/commit/fe3bcd1148108a80c1879b6726574bd1636ab7eb))
* add `__str__` methods for the `ObjectId` and `ObjectInstanceId` ([9b764be](https://github.com/emma-simbot/simbot-offline-inference/commit/9b764bea87fcb33727086553b90db8bf619e8e22))
* change CDF `floor_plan` validation to allow for `"-1"` ([d12bfe2](https://github.com/emma-simbot/simbot-offline-inference/commit/d12bfe274da5de0f3e7c9ca03b71a0409e1d2b3d))
* object ids for broken cords and computer monitors ([33aaffa](https://github.com/emma-simbot/simbot-offline-inference/commit/33aaffabe498dd49313b436185cf3413cae96aae))
* remove the duplicated object state ([3d92f22](https://github.com/emma-simbot/simbot-offline-inference/commit/3d92f22cad37acabba14a437aacc806b644144a3))
* send actions to randomise start position one-by-one ([8b31f76](https://github.com/emma-simbot/simbot-offline-inference/commit/8b31f76017ad9b80054e96df8576ebdb79ac3737))

## [2.5.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.4.0...v2.5.0) (2023-04-10)


### Features

* generate all the pickup from fridge/freezer missions ([e263c93](https://github.com/emma-simbot/simbot-offline-inference/commit/e263c934e764ec0fd6c414c8bb46964fa0f606a8))

## [2.4.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.3.0...v2.4.0) (2023-04-10)


### Features

* add `insert` and `vendingmachine` actions to the high-level key structure ([a6486a2](https://github.com/emma-simbot/simbot-offline-inference/commit/a6486a2fc031c9c19a2c5ab36b15b1b640cec645))
* add command to print the high-levels keys that we have challenges for ([051043e](https://github.com/emma-simbot/simbot-offline-inference/commit/051043eac59053c09039dd16099fa5eaeb807c91))

## [2.3.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.2.0...v2.3.0) (2023-04-09)


### Features

* randomise start position before challenge begins ([f78a9fb](https://github.com/emma-simbot/simbot-offline-inference/commit/f78a9fb1e6e67bc2c9d1c07403e2db9e9d6f74f6))

## [2.2.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.1.0...v2.2.0) (2023-04-09)


### Features

* add 'pickup apple from fridge' mission, with coloured variants ([f431757](https://github.com/emma-simbot/simbot-offline-inference/commit/f43175720f914af22487e1c934b9b24ecf1b9b0e))
* register challenge to pick up (coloured) apples from an open fridge ([43fd6ed](https://github.com/emma-simbot/simbot-offline-inference/commit/43fd6ed2004167896404c595504c0063e5fe9399))
* support generating challenges from other challenges with minor modifications ([1ffbc1e](https://github.com/emma-simbot/simbot-offline-inference/commit/1ffbc1ecd79d63ee2c50f9348c52d56eca6474c9))


### Bug Fixes

* make sure the `isColorChanged` key doesn't exist already to prevent duplicates ([9555241](https://github.com/emma-simbot/simbot-offline-inference/commit/955524136a19148abd1bd53d3c46d4b2b2bfec2e))
* replace property setters with explicit functions ([2d4038f](https://github.com/emma-simbot/simbot-offline-inference/commit/2d4038fff20e611199e79b9dcf3ade9fff80a9af))
* using `*-is-container` when parsing high-level keys from string ([6c78d32](https://github.com/emma-simbot/simbot-offline-inference/commit/6c78d323cd3bf701b41ee83490d757078ee0a480))

## [2.1.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v2.0.0...v2.1.0) (2023-04-09)


### Features

* improve generalisability of challenge builders for less boilerplate ([fe24100](https://github.com/emma-simbot/simbot-offline-inference/commit/fe24100fc68860fd17f1730c3b634bdf7b9f205b))


### Bug Fixes

* add tests and make sure the generation process works ([1a6f6ac](https://github.com/emma-simbot/simbot-offline-inference/commit/1a6f6acf8368f260824b595fe25c68dd77d8f3a2))

## [2.0.0](https://github.com/emma-simbot/simbot-offline-inference/compare/v1.5.0...v2.0.0) (2023-04-08)


### ⚠ BREAKING CHANGES

* be able to generate missions from high-level keys

### Features

* add more missions for other layouts ([1c5615d](https://github.com/emma-simbot/simbot-offline-inference/commit/1c5615d1ce506db26868491bc9ef475bd97e765d))
* add option to send dummy actions when validating cdfs ([0de8f4b](https://github.com/emma-simbot/simbot-offline-inference/commit/0de8f4bc6fe1da3edfb79b727504bb2ef99359ef))
* be able to generate missions from high-level keys ([1772f92](https://github.com/emma-simbot/simbot-offline-inference/commit/1772f92f03db32379a03d0db388acac78cca2878))
* include progress to more clearly know the overall progress ([e135740](https://github.com/emma-simbot/simbot-offline-inference/commit/e1357400681ecfc31e674ac3ab23149f73805b63))
* optionally add randomness to the session id name ([c0c43e2](https://github.com/emma-simbot/simbot-offline-inference/commit/c0c43e281bbf4a2a0fbf20290f96a692e4bec4e7))
* upload trajectory results to s3 ([77d1532](https://github.com/emma-simbot/simbot-offline-inference/commit/77d153263128e7ea056c6655c641167eacad16bc))
* use cloudpathlib to upload all the metrics to S3 ([986b1ce](https://github.com/emma-simbot/simbot-offline-inference/commit/986b1ce9116a85b1a5a76d0c0fa53413c2461f8d))


### Bug Fixes

* create all parents for the metric output file ([41d9372](https://github.com/emma-simbot/simbot-offline-inference/commit/41d9372d27119b9f33abb4ccc4113c2db673957f))
* created session id needs to not have slashes ([644268b](https://github.com/emma-simbot/simbot-offline-inference/commit/644268bd3becaa28be1c0c7ee49a6965441be0eb))
* created session id to be in the form `T.DATE/KEY-UUID` ([e94d2ff](https://github.com/emma-simbot/simbot-offline-inference/commit/e94d2ff170f244da1e49364ad8670a807a10d392))
* env var key to enable the offline evaluation mode ([5380a4b](https://github.com/emma-simbot/simbot-offline-inference/commit/5380a4bf252e511d9ff7c9d1a11e1c5ecd3d299a))
* generated session id that is valid as a path and uri ([c2a033d](https://github.com/emma-simbot/simbot-offline-inference/commit/c2a033d174e3f10e51588b342af54b7547a07cf8))
* lint issues ([ad3527d](https://github.com/emma-simbot/simbot-offline-inference/commit/ad3527d1cfdd281354bf1500d8b85a93abf7f09a))
* set a long timeout for experience hub, which gets overridden by the settings client timeout ([30b45c1](https://github.com/emma-simbot/simbot-offline-inference/commit/30b45c1badac746085ea240278fec9ac4a5b7e04))
* simplify the provided session id prefix ([70c5971](https://github.com/emma-simbot/simbot-offline-inference/commit/70c5971b0b06a761efe66852ad69234a207e7ce2))

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
