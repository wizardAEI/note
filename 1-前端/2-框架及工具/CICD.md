### ci.yml

```yaml
Global:
  version: 2.0

Default:
  profile: [app]

Profiles:
  - profile:
    name: app
    mode: AGENT
    environment:
      image: DECK_CENTOS7U5_K3
      tools:
        - nodejs: 18.3.0
    check:
      - reuse: TASK
        enable: true
    build:
      command: sh scripts/build.sh
    cache:
      enable: true
      paths:
        - node_modules
    artifacts:
      release: true
```

### scripts/build.sh

```sh
#!/usr/bin/env bash

set -e

export PATH=$NODEJS_14_15_4_BIN:$PATH

echo "node $(node -v)"
echo "npm $(npm -v)"

rm -rf dist output

NODE_ENV=development npm install
NODE_ENV=production npm run build

mkdir output
mkdir output/chatall

cd dist

cp -r ./ ../output/chatall

cd ..

echo "build success"
```

