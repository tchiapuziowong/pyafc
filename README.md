# pyafc

This python binding is written for Aruba Fabric Composer v6.3 or later

See the [Release Notes](RELEASE-NOTES.md) for more information.


## Structure
* REST API call functions are found in the modules in /pyafc.
* REST API call functions are combined into other functions that emulate low-level processes. These low-level process functions are also placed in files in /pyafc.
* Functions from the /pyafc files (API functions and low-level functions) are combined to emulate larger network configuration processes (workflows). These workflow scripts stored in the /workflows folder.


## How to contribute

Please see the accompanying [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this repository.

## Git Workflow

This repo adheres to the 'shared repo' git workflow:
1. Clone the repo to a local machine:

    ```git clone <repo_URL>```
2. Checkout a local working branch:

    ```git checkout -b <local_working_branch_name>```
3. Add and amend files in the local working branch:

    ```git add <file_name>```
4. Commit regularly. Each commit should encompass a single logical change to the repo (e.g. adding a new function in /pyaoscx is one commit; writing docstrings for all functions in a module is another commit). Include an explanatory message with each commit:

    ```git commit -m "<Clear_explanation_of_commit_here>"```
5. Push commits to github.hpe.com:

    ```git push origin <local_working_branch_name>```
6. Merge changes using a Pull Request on github.hpe.com. Ensure the PR has a relevant title and additional comments if necessary. PRs should be raised regularly once code is tested and the user satisfied that it is ready for submission. Do not put off creaing a PR until a whole project is complete. The larger the PR, the difficult it is to successfully merge.

## Troubleshooting Issues
1. If you encounter module import errors, make sure that the package has been installed correctly.

Additionally, please read the RELEASE-NOTES.md file for the current release information and known issues.
