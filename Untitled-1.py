name: Inline Shell Script Example

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Run a one-line script
        run: echo Hello, GitHub Actions!
      - name: Run a multi-line script
        run: |
          mkdir my-directory
          ls -a    #!/bin/bash
    echo "Running script from file!"
    touch new_file.txt
    
    name: External Shell Script Example

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Make script executable
        run: chmod +x my_script.sh
      - name: Run script from file
        run: ./my_script.sh